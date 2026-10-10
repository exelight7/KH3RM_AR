using System.Diagnostics;
using System.IO;

namespace Kh3rmAr;

/// <summary>KH3RM_AR_Setup.exe --selftest out.txt : runs on temp folders only, never on a real game.</summary>
public static class SelfTest
{
    static string J(params string[] p) => Path.Combine(p);

    public static int Run(string outFile)
    {
        var log = new List<string>(); int fail = 0;
        void Check(string name, bool ok) { log.Add($"{(ok ? "PASS" : "FAIL")} {name}"); if (!ok) fail++; }
        var root = J(Path.GetTempPath(), "kh3rm_selftest_" + Guid.NewGuid().ToString("N")[..8]);
        try
        {
            Check("embedded pak sha == BUILD-5", Core.EmbeddedSha() == Core.ExpectedSha);

            // fake Steam: library 2 holds the game under a custom installdir, listed in libraryfolders.vdf
            var steam = J(root, "Steam"); var lib2 = J(root, "Games", "SteamLib");
            Directory.CreateDirectory(J(steam, "steamapps"));
            var gameRoot = J(lib2, "steamapps", "common", "KH3X");
            var paks = J(gameRoot, "KINGDOM HEARTS III", "Content", "Paks");
            Directory.CreateDirectory(paks);
            File.WriteAllText(J(steam, "steamapps", "libraryfolders.vdf"),
                "\"libraryfolders\"\n{\n\t\"0\"\n\t{\n\t\t\"path\"\t\t\"" + steam.Replace("\\", "\\\\") + "\"\n\t}\n\t\"1\"\n\t{\n\t\t\"path\"\t\t\"" + lib2.Replace("\\", "\\\\") + "\"\n\t}\n}\n");
            File.WriteAllText(J(lib2, "steamapps", "appmanifest_2552450.acf"), "\"AppState\"\n{\n\t\"appid\"\t\t\"2552450\"\n\t\"installdir\"\t\t\"KH3X\"\n}\n");
            var found = Core.FindSteam(new[] { steam }).ToList();
            Check("steam: library from vdf + installdir from acf", found.Count == 1 && found[0] == paks);
            Check("steam: no manifest, no game -> nothing", !Core.FindSteam(new[] { J(root, "nothing") }).Any());

            // fake Epic
            var epicGame = J(root, "Epic", "KINGDOM HEARTS III");
            var epicPaks = J(epicGame, "KINGDOM HEARTS III", "Content", "Paks");
            Directory.CreateDirectory(epicPaks);
            var dat = J(root, "LauncherInstalled.dat");
            File.WriteAllText(dat, "{\"InstallationList\":[{\"InstallLocation\":\"" + J(root, "Epic", "Other").Replace("\\", "\\\\") +
                "\",\"AppName\":\"x\"},{\"InstallLocation\":\"" + epicGame.Replace("\\", "\\\\") + "\",\"AppName\":\"y\"}]}");
            Check("epic: LauncherInstalled.dat", Core.FindEpic(dat).SequenceEqual(new[] { epicPaks }));

            // Browse validation
            Check("browse: game root", Core.ResolvePaks(gameRoot) == paks);
            Check("browse: inner KINGDOM HEARTS III folder", Core.ResolvePaks(J(gameRoot, "KINGDOM HEARTS III")) == paks);
            Check("browse: Paks itself", Core.ResolvePaks(paks) == paks);
            Check("browse: wrong folder rejected", Core.ResolvePaks(root) == null && Core.ResolvePaks("") == null && Core.ResolvePaks(null) == null);

            // process check
            var self = Process.GetCurrentProcess().ProcessName;
            Check("running check: true for a live process name", Core.IsGameRunning(self));
            Check("running check: false for an unknown name", !Core.IsGameRunning("zz_no_such_process_" + Guid.NewGuid().ToString("N")));

            // install / remove
            var mods = Core.ModsDir(paks); var ours = J(mods, Core.PakName);
            Check("status: not installed", Core.GetStatus(paks) == new Core.Status(Core.State.NotInstalled, 0));
            Check("install refused while running", Core.Install(paks, () => true) == Core.Result.GameRunning && !Directory.Exists(mods));
            Check("install ok", Core.Install(paks, () => false) == Core.Result.Ok && Core.ShaFile(ours) == Core.ExpectedSha);
            Check("status: current", Core.GetStatus(paks).State == Core.State.Current);
            File.WriteAllText(J(mods, "other_mod_P.pak"), "x");
            File.WriteAllText(J(mods, "readme.txt"), "keep");
            Check("status: other mods counted", Core.GetStatus(paks).OtherPaks == 1);
            File.WriteAllText(ours, "old build");
            Check("status: other version", Core.GetStatus(paks).State == Core.State.OtherVersion);
            Check("reinstall overwrites", Core.Install(paks, () => false) == Core.Result.Ok && Core.GetStatus(paks).State == Core.State.Current);
            Check("remove refused while running", Core.Remove(paks, () => true) == Core.Result.GameRunning && File.Exists(ours));
            Check("remove touches only our pak", Core.Remove(paks, () => false) == Core.Result.Ok && !File.Exists(ours)
                  && File.Exists(J(mods, "other_mod_P.pak")) && File.Exists(J(mods, "readme.txt")) && Directory.Exists(mods));
            File.Delete(J(mods, "other_mod_P.pak")); File.Delete(J(mods, "readme.txt"));
            Core.Install(paks, () => false);
            Check("remove deletes empty ~mods", Core.Remove(paks, () => false) == Core.Result.Ok && !Directory.Exists(mods));
            Check("install on missing Paks -> NoPaks", Core.Install(J(root, "nope"), () => false) == Core.Result.NoPaks);
        }
        catch (Exception e) { log.Add("FAIL exception " + e); fail++; }
        finally { try { Directory.Delete(root, true); } catch (Exception) { } }
        log.Add(fail == 0 ? "selftest: ALL PASS" : $"selftest: {fail} FAIL");
        File.WriteAllLines(outFile, log);
        return fail == 0 ? 0 : 1;
    }
}
