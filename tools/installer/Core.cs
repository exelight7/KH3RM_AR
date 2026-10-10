using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace Kh3rmAr;

/// <summary>Everything that touches the disk. No UI, so SelfTest can run it on fake folder trees.</summary>
public static class Core
{
    public const string Version = "0.8.2";
    public const string PakName = "pakchunk99-arabic_P.pak";
    public const string ExpectedSha = "f9e23f373ce52a5e9c6690d264b7228d43d0e28aa55d9d76386514db511e82d7"; // BUILD-7
    public const string SteamAppId = "2552450";
    public const string ProcPrefix = "KINGDOM HEARTS III";

    public static Stream OpenPak() =>
        Assembly.GetExecutingAssembly().GetManifestResourceStream("pak") ?? throw new InvalidOperationException("pak resource missing");

    public static string Sha(Stream s) => Convert.ToHexString(SHA256.HashData(s)).ToLowerInvariant();
    public static string ShaFile(string p) { using var f = File.OpenRead(p); return Sha(f); }
    public static string EmbeddedSha() { using var s = OpenPak(); return Sha(s); }

    // ---- locating the game -------------------------------------------------------------------------------
    /// <summary>Returns the ...\Content\Paks folder if dir is (or contains) a KH3 install, else null.</summary>
    public static string? ResolvePaks(string? dir)
    {
        if (string.IsNullOrWhiteSpace(dir)) return null;
        try
        {
            dir = dir.Trim().Trim('"').TrimEnd('\\', '/');
            var leaf = Path.GetFileName(dir);
            if (string.Equals(leaf, "Paks", StringComparison.OrdinalIgnoreCase) && Directory.Exists(dir)) return dir;
            if (string.Equals(leaf, "~mods", StringComparison.OrdinalIgnoreCase)) return ResolvePaks(Path.GetDirectoryName(dir));
            foreach (var c in new[] { Path.Combine(dir, "Content", "Paks"),
                                      Path.Combine(dir, "KINGDOM HEARTS III", "Content", "Paks") })
                if (Directory.Exists(c)) return c;
        }
        catch (Exception) { }
        return null;
    }

    static IEnumerable<string> SteamLibraries(string steamRoot)
    {
        yield return steamRoot;
        var vdf = Path.Combine(steamRoot, "steamapps", "libraryfolders.vdf");
        if (!File.Exists(vdf)) yield break;
        foreach (Match m in Regex.Matches(File.ReadAllText(vdf), "\"path\"\\s+\"([^\"]+)\""))
            yield return m.Groups[1].Value.Replace("\\\\", "\\");
    }

    /// <summary>Steam: every library with appmanifest_2552450.acf (installdir) -> Paks. Fallback: common\KINGDOM HEARTS III.</summary>
    public static IEnumerable<string> FindSteam(IEnumerable<string> steamRoots)
    {
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var root in steamRoots.Where(r => !string.IsNullOrWhiteSpace(r)))
            foreach (var lib in SteamLibraries(root))
            {
                var apps = Path.Combine(lib, "steamapps");
                string? dir = null;
                var acf = Path.Combine(apps, $"appmanifest_{SteamAppId}.acf");
                if (File.Exists(acf))
                {
                    var m = Regex.Match(File.ReadAllText(acf), "\"installdir\"\\s+\"([^\"]+)\"");
                    if (m.Success) dir = Path.Combine(apps, "common", m.Groups[1].Value);
                }
                dir ??= Path.Combine(apps, "common", "KINGDOM HEARTS III");
                var paks = ResolvePaks(dir);
                if (paks != null && seen.Add(paks)) yield return paks;
            }
    }

    /// <summary>Epic: LauncherInstalled.dat (JSON, InstallationList[].InstallLocation).</summary>
    public static IEnumerable<string> FindEpic(string? datPath)
    {
        var locs = new List<string>();
        if (datPath != null && File.Exists(datPath))
        {
            try
            {
                using var doc = JsonDocument.Parse(File.ReadAllText(datPath));
                foreach (var e in doc.RootElement.GetProperty("InstallationList").EnumerateArray())
                    if (e.TryGetProperty("InstallLocation", out var l) && l.GetString() is string s &&
                        s.Contains("KINGDOM HEARTS III", StringComparison.OrdinalIgnoreCase)) locs.Add(s);
            }
            catch (Exception) { }
        }
        foreach (var l in locs) if (ResolvePaks(l) is string p) yield return p;
    }

    public static IEnumerable<string> SystemSteamRoots()
    {
        var found = new List<string>();
        foreach (var (hive, key, name) in new[] { (Microsoft.Win32.Registry.CurrentUser, @"Software\Valve\Steam", "SteamPath"),
                                                  (Microsoft.Win32.Registry.LocalMachine, @"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                                                  (Microsoft.Win32.Registry.LocalMachine, @"SOFTWARE\Valve\Steam", "InstallPath") })
        {
            try { if (hive.OpenSubKey(key)?.GetValue(name) is string v) found.Add(v.Replace('/', '\\')); } catch (Exception) { }
        }
        var pf = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);
        if (pf.Length > 0) found.Add(Path.Combine(pf, "Steam"));
        return found;
    }

    public static string EpicDat() =>
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData), "Epic", "UnrealEngineLauncher", "LauncherInstalled.dat");

    public static List<string> DetectAll() =>
        FindSteam(SystemSteamRoots()).Concat(FindEpic(EpicDat())).Distinct(StringComparer.OrdinalIgnoreCase).ToList();

    // ---- state / install / remove --------------------------------------------------------------------------
    public enum State { NotInstalled, Current, OtherVersion }

    public record Status(State State, int OtherPaks);

    public static string ModsDir(string paks) => Path.Combine(paks, "~mods");

    public static Status GetStatus(string paks)
    {
        var mods = ModsDir(paks);
        var ours = Path.Combine(mods, PakName);
        int others = Directory.Exists(mods)
            ? Directory.EnumerateFiles(mods).Count(f => f.EndsWith(".pak", StringComparison.OrdinalIgnoreCase)
                                                       && !string.Equals(Path.GetFileName(f), PakName, StringComparison.OrdinalIgnoreCase))
            : 0;
        if (!File.Exists(ours)) return new(State.NotInstalled, others);
        return new(ShaFile(ours) == EmbeddedSha() ? State.Current : State.OtherVersion, others);
    }

    public static bool IsGameRunning(string prefix = ProcPrefix)
    {
        foreach (var p in Process.GetProcesses())
        {
            try { if (p.ProcessName.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)) return true; }
            catch (Exception) { }
            finally { p.Dispose(); }
        }
        return false;
    }

    public enum Result { Ok, GameRunning, NoPaks, Denied, HashMismatch, Error }

    /// <summary>Creates ~mods, writes only our pak, verifies the SHA256 of the written file.</summary>
    public static Result Install(string paks, Func<bool>? running = null)
    {
        if ((running ?? (() => IsGameRunning()))()) return Result.GameRunning;
        if (!Directory.Exists(paks)) return Result.NoPaks;
        var dst = Path.Combine(ModsDir(paks), PakName);
        try
        {
            Directory.CreateDirectory(ModsDir(paks));
            using (var src = OpenPak())
            using (var f = new FileStream(dst, FileMode.Create, FileAccess.Write, FileShare.None)) src.CopyTo(f);
            if (ShaFile(dst) == EmbeddedSha()) return Result.Ok;
            File.Delete(dst);
            return Result.HashMismatch;
        }
        catch (UnauthorizedAccessException) { return Result.Denied; }
        catch (Exception) { return Result.Error; }
    }

    /// <summary>Deletes only our pak; removes ~mods only when it is then empty.</summary>
    public static Result Remove(string paks, Func<bool>? running = null)
    {
        if ((running ?? (() => IsGameRunning()))()) return Result.GameRunning;
        var mods = ModsDir(paks);
        try
        {
            var ours = Path.Combine(mods, PakName);
            if (File.Exists(ours)) File.Delete(ours);
            if (Directory.Exists(mods) && !Directory.EnumerateFileSystemEntries(mods).Any()) Directory.Delete(mods);
            return Result.Ok;
        }
        catch (UnauthorizedAccessException) { return Result.Denied; }
        catch (Exception) { return Result.Error; }
    }

    public static void Log(string line)
    {
        try { File.AppendAllText(Path.Combine(AppContext.BaseDirectory, "KH3RM_AR_Setup.log"), $"{DateTime.Now:yyyy-MM-dd HH:mm:ss}\t{line}\r\n"); }
        catch (Exception) { }
    }
}
