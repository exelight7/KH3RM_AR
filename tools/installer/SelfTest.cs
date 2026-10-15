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
            Check("embedded pak sha == BUILD-18", Core.EmbeddedSha() == Core.ExpectedSha);
            Check("embedded images pak sha == IMAGES-MASS11", Core.EmbeddedSha(Core.Images) == Core.ImagesSha);

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

            // images pack (0.9.0): optional second pak, installed / removed on its own
            var img = J(mods, Core.ImagesPakName);
            Check("install text only: images pak absent", Core.Install(paks, false, () => false) == Core.Result.Ok
                  && File.Exists(ours) && !File.Exists(img) && Core.GetStatus(paks, Core.Images).State == Core.State.NotInstalled);
            Check("install text + images: both present, both sha match", Core.Install(paks, true, () => false) == Core.Result.Ok
                  && Core.ShaFile(ours) == Core.ExpectedSha && Core.ShaFile(img) == Core.ImagesSha);
            Check("status: images current", Core.GetStatus(paks, Core.Images).State == Core.State.Current);
            var imgTime = File.GetLastWriteTimeUtc(img);
            Check("images unticked after an images install: images pak untouched", Core.Install(paks, false, () => false) == Core.Result.Ok
                  && File.Exists(img) && File.GetLastWriteTimeUtc(img) == imgTime && Core.ShaFile(img) == Core.ImagesSha);
            File.WriteAllText(J(mods, "other_mod_P.pak"), "x");
            Check("status: our images pak is not counted as another mod", Core.GetStatus(paks).OtherPaks == 1);
            File.WriteAllText(img, "modified");
            Check("status: images other version (modified file)", Core.GetStatus(paks, Core.Images).State == Core.State.OtherVersion);
            Check("reinstall with images repairs the images pak", Core.Install(paks, true, () => false) == Core.Result.Ok && Core.ShaFile(img) == Core.ImagesSha);
            Check("install with images refused while running: nothing changes", Core.Install(paks, true, () => true) == Core.Result.GameRunning
                  && Core.ShaFile(ours) == Core.ExpectedSha && Core.ShaFile(img) == Core.ImagesSha);
            Check("remove images refused while running", Core.Remove(paks, () => true, Core.Images) == Core.Result.GameRunning && File.Exists(img));
            Check("remove images only: text pak and ~mods stay", Core.Remove(paks, () => false, Core.Images) == Core.Result.Ok
                  && !File.Exists(img) && File.Exists(ours) && Directory.Exists(mods));
            Core.Install(paks, true, () => false);
            Check("remove text only: images pak stays", Core.Remove(paks, () => false) == Core.Result.Ok && !File.Exists(ours) && File.Exists(img));
            Check("other mods untouched by every case", File.ReadAllText(J(mods, "other_mod_P.pak")) == "x");
            File.Delete(J(mods, "other_mod_P.pak"));
            Core.Install(paks, true, () => false);
            Check("remove both: ~mods deleted when empty", Core.Remove(paks, () => false, Core.All) == Core.Result.Ok && !Directory.Exists(mods));
            Directory.CreateDirectory(img);   // a folder squatting on the images pak name: that write fails
            var failed = Core.Install(paks, true, () => false);
            Check("failed images write: reported (Denied/Error), text pak intact, no temp file left",
                  (failed == Core.Result.Error || failed == Core.Result.Denied)
                  && Core.ShaFile(ours) == Core.ExpectedSha && !Directory.EnumerateFiles(mods, "*.tmp").Any());
            Directory.Delete(img);
            Check("installer never wrote outside the temp tree", !Directory.Exists(J(root, "nope", "~mods")));
        }
        catch (Exception e) { log.Add("FAIL exception " + e); fail++; }
        finally { try { Directory.Delete(root, true); } catch (Exception) { } }
        log.Add(fail == 0 ? "selftest: ALL PASS" : $"selftest: {fail} FAIL");
        File.WriteAllLines(outFile, log);
        return fail == 0 ? 0 : 1;
    }
}
