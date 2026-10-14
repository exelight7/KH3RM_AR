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
    public const string Version = "0.9.1";
    public const string PakName = "pakchunk99-arabic_P.pak";
    public const string ExpectedSha = "89e00ead0a83e5d1cb07d257d98530541da447a5849c42f84ba9759dd4c7beea"; // BUILD-10
    public const string ImagesPakName = "pakchunk98-arabic-images_P.pak";
    public const string ImagesSha = "e8ebf70acab5612339cdbe20cb130f197199bc0d9b1776c96232f28bc541a403"; // IMAGES-MASS4
    public const string SteamAppId = "2552450";
    public const string ProcPrefix = "KINGDOM HEARTS III";

    /// <summary>One embedded pak: file name in ~mods, manifest resource name, expected SHA256.</summary>
    public sealed record Pak(string Name, string Resource, string Sha);
    public static readonly Pak Text = new(PakName, "pak", ExpectedSha);
    public static readonly Pak Images = new(ImagesPakName, "pak.images", ImagesSha);
    public static readonly Pak[] All = { Text, Images };

    public static Stream OpenPak(Pak? pak = null) =>
        Assembly.GetExecutingAssembly().GetManifestResourceStream((pak ?? Text).Resource) ?? throw new InvalidOperationException("pak resource missing");

    public static string Sha(Stream s) => Convert.ToHexString(SHA256.HashData(s)).ToLowerInvariant();
    public static string ShaFile(string p) { using var f = File.OpenRead(p); return Sha(f); }
    public static string EmbeddedSha(Pak? pak = null) { using var s = OpenPak(pak); return Sha(s); }

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
        var seen = new HashSet<string>(OperatingSystem.IsWindows() ? StringComparer.OrdinalIgnoreCase : StringComparer.Ordinal);
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
        if (!OperatingSystem.IsWindows())
        {
            var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            found.AddRange(new[] {
                Path.Combine(home, ".steam", "steam"), Path.Combine(home, ".steam", "root"),
                Path.Combine(home, ".local", "share", "Steam"),
                Path.Combine(home, ".var", "app", "com.valvesoftware.Steam", ".local", "share", "Steam"),
                Path.Combine(home, ".var", "app", "com.valvesoftware.Steam", "data", "Steam")
            });
            var data = Environment.GetEnvironmentVariable("XDG_DATA_HOME");
            if (!string.IsNullOrEmpty(data)) found.Add(Path.Combine(data, "Steam"));
            return found.Where(Directory.Exists).Distinct(StringComparer.Ordinal).ToList();
        }
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
        FindSteam(SystemSteamRoots()).Concat(OperatingSystem.IsWindows() ? FindEpic(EpicDat()) : Array.Empty<string>())
            .Distinct(OperatingSystem.IsWindows() ? StringComparer.OrdinalIgnoreCase : StringComparer.Ordinal).ToList();

    // ---- state / install / remove --------------------------------------------------------------------------
    public enum State { NotInstalled, Current, OtherVersion }

    public record Status(State State, int OtherPaks);

    public static string ModsDir(string paks) => Path.Combine(paks, "~mods");

    /// <summary>State of one of our paks (default: the text pak); OtherPaks = .pak files in ~mods that are not ours.</summary>
    public static Status GetStatus(string paks, Pak? pak = null)
    {
        pak ??= Text;
        var mods = ModsDir(paks);
        var ours = Path.Combine(mods, pak.Name);
        int others = Directory.Exists(mods)
            ? Directory.EnumerateFiles(mods).Count(f => f.EndsWith(".pak", StringComparison.OrdinalIgnoreCase)
                                                       && !All.Any(p => string.Equals(Path.GetFileName(f), p.Name, StringComparison.OrdinalIgnoreCase)))
            : 0;
        if (!File.Exists(ours)) return new(State.NotInstalled, others);
        return new(ShaFile(ours) == pak.Sha ? State.Current : State.OtherVersion, others);
    }

    public static bool IsGameRunning(string prefix = ProcPrefix)
    {
        foreach (var p in Process.GetProcesses())
        {
            try
            {
                if (p.ProcessName.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)) return true;
                // Proton/Wine process names can be truncated; inspect executable arguments locally.
                if (OperatingSystem.IsLinux() && prefix == ProcPrefix)
                {
                    var args = File.ReadAllText($"/proc/{p.Id}/cmdline").Split('\0');
                    if (args.Any(arg => Path.GetFileName(arg.Replace('\\', '/'))
                        .StartsWith(ProcPrefix, StringComparison.OrdinalIgnoreCase))) return true;
                }
            }
            catch (Exception) { }
            finally { p.Dispose(); }
        }
        return false;
    }

    public enum Result { Ok, GameRunning, NoPaks, Denied, HashMismatch, Error }

    /// <summary>Writes the text pak, and the images pak only when withImages. An installed images pak is never
    /// removed by Install. Each pak is staged, its SHA256 verified, then moved into ~mods; the first failure stops.</summary>
    public static Result Install(string paks, bool withImages = false, Func<bool>? running = null)
    {
        foreach (var pak in withImages ? All : new[] { Text })
        {
            var r = InstallOne(paks, pak, running);
            if (r != Result.Ok) return r;
        }
        return Result.Ok;
    }

    public static Result Install(string paks, Func<bool>? running) => Install(paks, false, running);

    /// <summary>Creates ~mods, writes only this pak, verifies the SHA256 of the written file.</summary>
    public static Result InstallOne(string paks, Pak pak, Func<bool>? running = null)
    {
        if ((running ?? (() => IsGameRunning()))()) return Result.GameRunning;
        if (!Directory.Exists(paks)) return Result.NoPaks;
        var dst = Path.Combine(ModsDir(paks), pak.Name);
        var temporary = dst + "." + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            Directory.CreateDirectory(ModsDir(paks));
            using (var src = OpenPak(pak))
            using (var f = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None))
                src.CopyTo(f);
            if (ShaFile(temporary) != pak.Sha) return Result.HashMismatch;
            if ((running ?? (() => IsGameRunning()))()) return Result.GameRunning;
            File.Move(temporary, dst, true);
            return Result.Ok;
        }
        catch (UnauthorizedAccessException) { return Result.Denied; }
        catch (Exception) { return Result.Error; }
        finally
        {
            // Never remove an installed pak when staging or verification fails.
            try { if (File.Exists(temporary)) File.Delete(temporary); }
            catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }
    }

    /// <summary>Deletes only the chosen paks of ours (default: the text pak); removes ~mods only when it is then empty.</summary>
    public static Result Remove(string paks, Func<bool>? running = null, params Pak[] which)
    {
        if ((running ?? (() => IsGameRunning()))()) return Result.GameRunning;
        var mods = ModsDir(paks);
        try
        {
            foreach (var pak in which.Length == 0 ? new[] { Text } : which)
            {
                var ours = Path.Combine(mods, pak.Name);
                if (File.Exists(ours)) File.Delete(ours);
            }
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
