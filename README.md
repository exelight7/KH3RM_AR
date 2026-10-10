# KH3RM_AR — تعريب Kingdom Hearts III + Re Mind

<div dir="rtl">

## بالعربية

**ترجمة عربية غير رسمية (من المعجبين) للعبة Kingdom Hearts III + Re Mind على الكمبيوتر (Steam).** مجانية، وغير تابعة لشركتي Square Enix أو Disney.

**الحالة: نسخة تجريبية (pre-release) لم تُختبر بالكامل.**

| المقياس | النسبة |
|---|---|
| مترجم | 95.3% |
| مراجَع لغويا | 95.3% |
| مثبّت في ملف اللعبة | 95.3% |
| تم التحقق منه بلقطات شاشة داخل اللعبة | 0.6% |

(الأرقام من `state/STATS.md`، المجموع 17222 نصا.)

### التنزيل
**[نزّل الإصدار 0.8.2 (نسخة تجريبية)](https://github.com/exelight7/KH3RM_AR/releases/tag/0.8.2)**: شغّل `KH3RM_AR_Setup_v0.8.2.exe`، وسيجد المثبّت مجلد اللعبة (Steam أو Epic) وينسخ الملف ويتحقق منه. إن ظهرت نافذة SmartScreen (البرنامج غير موقّع): «مزيد من المعلومات» ثم «تشغيل على أي حال».

![واجهة المثبّت](docs/img/ui_ar.png)

### التثبيت اليدوي
1. نزّل `pakchunk99-arabic_P.pak` من صفحة [Releases](../../releases) (أو شغّل `INSTALL_AR.bat` وسيفعل الخطوات تلقائيا).
2. انسخه إلى مجلد `Content\Paks\~mods` داخل مجلد اللعبة، مثلا:
   `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods`
   (أنشئ المجلد `~mods` إن لم يكن موجودا).
3. أبقِ ملف pak واحدا فقط من هذا التعريب في المجلد.

### الإزالة
احذف `pakchunk99-arabic_P.pak` من `~mods` (أو شغّل `REMOVE_AR.bat`). لا نغيّر أي ملف أصلي من اللعبة.

### المتطلبات والمشاكل المعروفة
- النسخة الإنجليزية من اللعبة على Steam (Windows)؛ التعريب يستبدل النصوص الإنجليزية.
- لم يُتحقق من كل الشاشات: قد تظهر نصوص مقصوصة أو طويلة في بعض القوائم وصناديق المساعدة.
- الصور والفيديوهات التي فيها كلمات إنجليزية (نحو 315 ملفا) لم تُترجم بعد.
- أي تحديث للعبة قد يكسر الملف؛ احذفه ثم أعد التثبيت.

### خارطة الطريق
- **0.8.x**: تصحيحات النصوص (ترجمة ومراجعة وأسطر مقصوصة) حسب لقطات الشاشة.
- **0.9.0**: الصور والنصوص المرسومة داخل الصور (القوائم، الشروحات، أسماء الأماكن)؛ الشعارات تبقى كما هي.
- **1.0.0**: بعد اختبار كامل داخل اللعبة بلقطات الشاشة.

### الإبلاغ عن مشكلة
افتح [Issue](../../issues) وأرفق لقطة شاشة وموضع المشكلة في اللعبة (القائمة، المشهد، اسم الشخصية).

### كيف يعمل (٦ أسطر)
1. اللعبة (Unreal Engine 4.17) تقرأ نصوصها من ملفات locres؛ نضع ملف locres عربيا في pak إضافي (`~mods`).
2. واجهة اللعبة (Scaleform) لا تشكّل الحروف العربية ولا تعكس الاتجاه.
3. لذلك نشكّل النص مسبقا (أشكال العرض: ابتدائية ووسطية ونهائية) ونخزّنه بترتيب العرض البصري.
4. نضيف خطا (حروف Segoe UI العربية) في ملف الخط TresFont داخل الـ pak.
5. نكسر الأسطر حسب عرض كل حقل نص في الواجهة (`technical/FIELD_WIDTHS.tsv`).
6. كل شيء يُبنى بسكربتات في `tools/` ويُتحقق منه بـ SHA256 لكل ملف.

### المساهمة والشكر
الشكر: _(قائمة المساهمين لاحقا)_

### ملاحظة قانونية
هذا المستودع لا يحتوي على أي ملف من اللعبة ولا على النص الإنجليزي الأصلي؛ ملفات الترجمة فيه عربية فقط (معرّف الصف ومفتاحه وبصمة المصدر). لبناء الـ pak من المصدر تحتاج نسختك الخاصة من اللعبة ومفتاح AES الذي نشره المجتمع، وهذا المستودع لا يوزّعه. الترخيص لم يُحسم بعد (انظر `LICENSE_TODO.md`).

الخط: يحتوي الـ pak على رسوم حروف محوّلة من خط Segoe UI من مايكروسوفت، ويُستخدم على مسؤولية صاحب المشروع.

</div>

## English

**Unofficial fan Arabic localization of Kingdom Hearts III + Re Mind (PC / Steam).** Free. Not affiliated with Square Enix or Disney.

**Status: pre-release, not fully tested.**

| Metric | Share |
|---|---|
| Translated | 95.3% |
| Reviewed | 95.3% |
| Installed in the game pak | 95.3% |
| Verified by in-game screenshot | 0.6% |

(From `state/STATS.md`, 17222 strings in total.)

### Download
**[Get 0.8.2 (pre-release)](https://github.com/exelight7/KH3RM_AR/releases/tag/0.8.2)**: run `KH3RM_AR_Setup_v0.8.2.exe`; it finds the game folder (Steam or Epic), copies the pak and verifies it. If Windows SmartScreen appears (the app is unsigned): More info > Run anyway.

![Installer](docs/img/ui_ar.png)

### Manual install
1. Download `pakchunk99-arabic_P.pak` from [Releases](../../releases) (or run `INSTALL_AR.bat`, which does the steps below).
2. Copy it into the game's `Content\Paks\~mods` folder, e.g.
   `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods`
   (create `~mods` if it does not exist).
3. Keep only one pak of this localization in the folder.

### Remove
Delete `pakchunk99-arabic_P.pak` from `~mods` (or run `REMOVE_AR.bat`). No original game file is modified.

### Requirements and known issues
- The Steam (Windows) game; the mod replaces the English strings.
- Not every screen has been checked: text may be clipped or too long in some menus and help boxes.
- Images and videos containing English words (about 315 assets) are not translated yet.
- A game update may break the pak; delete it and reinstall.

### Roadmap
- **0.8.x**: text fixes (translation, review, clipped lines) from screenshots.
- **0.9.0**: images, i.e. English text drawn inside textures (menus, tutorials, place names); logos stay as they are.
- **1.0.0**: after full in-game testing with screenshots.

### Reporting problems
Open an [issue](../../issues) with a screenshot and where it happens (menu, cutscene, character).

### How it works (6 lines)
1. The game (Unreal Engine 4.17) reads its text from locres files; we ship an Arabic locres in an extra pak (`~mods`).
2. The UI (Scaleform) does no Arabic letter shaping and no bidi.
3. So the text is pre-shaped (presentation forms) and stored in visual order.
4. A font (Segoe UI Arabic glyphs) is added to the TresFont asset inside the pak.
5. Lines are broken to the width of each UI text field (`technical/FIELD_WIDTHS.tsv`).
6. Everything is built by the scripts in `tools/` and checked with per-file SHA256.

### Credits
_(contributors list to be added)_

### Legal
This repository contains no game files and no English source text; the translation files hold Arabic only (row id, key, source hash). To build the pak from source you need your own copy of the game and the community-published AES key, which this repository does not distribute. The license is still undecided (see `LICENSE_TODO.md`).

Font: the pak contains glyph outlines converted from Microsoft's Segoe UI, used at the author's own responsibility.
