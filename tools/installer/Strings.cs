namespace Kh3rmAr;

/// <summary>UI texts: Arabic (default) and English.</summary>
public static class Loc
{
    public static string Lang = "ar";

    static readonly Dictionary<string, (string ar, string en)> T = new()
    {
        ["title"] = ("تعريب كينغدوم هارتس III + Re Mind", "Arabic localization of Kingdom Hearts III + Re Mind"),
        ["sub"] = ("ترجمة عربية غير رسمية من المعجبين · نسخة تجريبية", "Unofficial fan translation · pre-release"),
        ["folder"] = ("مجلد اللعبة", "Game folder"),
        ["browse"] = ("تصفح...", "Browse..."),
        ["notfound"] = ("لم أجد اللعبة. اضغط «تصفح» واختر مجلدها.", "Game not found. Click Browse and pick its folder."),
        ["state"] = ("الحالة", "Status"),
        ["st_none"] = ("غير مثبّت", "Not installed"),
        ["st_cur"] = ("مثبّت · الإصدار {0}", "Installed · version {0}"),
        ["st_old"] = ("مثبّت (إصدار مختلف) · اضغط «تثبيت» للتحديث", "Installed (different version) · press Install to update"),
        ["st_nogame"] = ("اختر مجلد اللعبة أولا", "Choose the game folder first"),
        ["st_other"] = (" · تعديلات أخرى في ~mods: {0}", " · other mods in ~mods: {0}"),
        ["install"] = ("تثبيت التعريب", "Install"),
        ["remove"] = ("إزالة التعريب", "Remove"),
        ["savelog"] = ("حفظ سجل بجانب البرنامج", "Save a log next to this program"),
        ["lang"] = ("English", "العربية"),
        ["ok_inst"] = ("تم التثبيت بنجاح وتم التحقق من الملف. شغّل اللعبة.", "Installed and verified. Start the game."),
        ["ok_rem"] = ("تمت إزالة التعريب.", "Arabic removed."),
        ["running"] = ("اللعبة تعمل الآن. أغلقها ثم حاول مجددا.", "The game is running. Close it and try again."),
        ["badfolder"] = ("هذا ليس مجلد اللعبة (لم أجد Content\\Paks).", "This is not the game folder (Content\\Paks not found)."),
        ["denied"] = ("لا توجد صلاحية للكتابة. أعد التشغيل كمسؤول؟", "No permission to write. Restart as administrator?"),
        ["badhash"] = ("فشل التحقق من الملف (SHA256). لم يُترك أي ملف.", "File check (SHA256) failed. Nothing was left behind."),
        ["error"] = ("حدث خطأ غير متوقع.", "Unexpected error."),
        ["foot"] = ("غير رسمي · غير تابع لشركتي Square Enix وDisney · لا يغيّر أي ملف أصلي من اللعبة", "Unofficial · not affiliated with Square Enix or Disney · changes no original game file"),
        ["ver"] = ("الإصدار {0}", "Version {0}"),
    };

    public static string Get(string k) => Lang == "ar" ? T[k].ar : T[k].en;
    public static string Get(string k, params object[] a) => string.Format(Get(k), a);
}
