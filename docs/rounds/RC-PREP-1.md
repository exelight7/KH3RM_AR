# RC-PREP-1 — 2026-10-31

طلب المالك: خطة الوصول إلى 1.0.0 (المراحل 0 إلى 5). نُفّذ منها ما يمكن تنفيذه من **المستودع العام فقط**. فُرمت جهاز المالك قبل نحو أسبوعين، فلا يوجد المشروع الخاص (`C:\filessss\mewo\kh3fm-arabic`) في C أو D أو E أو Windows.old، ولا Python ولا git ولا gh. هذا المجلد تنزيل جديد من المستودع العام، فهو الآن النسخة الوحيدة من الأدوات والوثائق. الحزمتان الحقيقيتان أُخذتا من إصدار 0.9.9 على GitHub. لا بناء لحزمة نص أو صور جديدة، ولا تثبيت في اللعبة، ولا إصدار، ولا تغيير في الترجمة.

## المرحلة 0.1: المثبّت إلى .NET 10

- `tools/installer/Installer.csproj`: `TargetFramework` من `net8.0` إلى `net10.0`. لم يتغير غير ذلك (Avalonia 11.3.22، SelfContained، بلا SingleFile ولا ضغط، بلا رموز تصحيح).
- **SDK:** `dotnet-sdk-10.0.403-win-x64.zip` من `builds.dotnet.microsoft.com`، 300,745,255 بايت، وSHA512 مطابق للقيمة الرسمية في `releases.json` للقناة 10.0 (آخر إصدار 10.0.14، LTS، دعمه حتى 2028-11-14). فُكّ في مجلد مؤقت ولم يُثبَّت على النظام، وكل ما يكتبه dotnet (حزم NuGet ومجلد المستخدم) بقي هناك.
- **البناء** في نسخة عمل خارج المستودع (فلا `bin` ولا `obj` في المستودع)، على جولتين. الأولى بحزمتين تجريبيتين وبصمتين معدّلتين في النسخة وحدها (37/37). **الثانية، المعتمدة أدناه**، بالحزمتين الحقيقيتين `pakchunk99-arabic_P.pak` (5,103,489 بايت) و`pakchunk98-arabic-images_P.pak` (41,493,315 بايت) من إصدار 0.9.9 على GitHub: SHA256 لكل منهما محسوب محليا ويطابق `Core.cs` (`dde67ce6…e527` و`7b37f84b…c964`)، و`Core.cs` دون أي تعديل.

| الفحص | النتيجة |
|---|---|
| `dotnet publish -r win-x64 --self-contained` | نجح، بلا تحذيرات |
| `dotnet publish -r linux-x64 --self-contained` | نجح |
| .NET المضمن | Microsoft.NETCore.App 10.0.14 |
| ملفات المجلد المنشور | win-x64 218، linux-x64 217 |
| رموز التصحيح (pdb) | 0 |
| SingleFile / ضغط | لا؛ EXE حجمه 222,208 بايت |
| `--selftest` على المجلد المبني (الحزمتان الحقيقيتان) | 37 من 37، بما فيها فحصا هوية الحزمتين |
| `--selftest` بعد ضغط المجلد وفكّه في مجلد جديد | 37 من 37 |
| حجم المجلد وملفاته | 144.8 MB، 218 ملفا؛ ZIP تجريبي 92,063,231 بايت |
| `KH3RM_AR_Setup.exe` (win-x64) | 222,208 بايت، SHA256 `d0efae0b…ee66` (بناء تجريبي وليس للنشر) |

## ما لا يثبته هذا الفحص

قبول Windows بالحزمتين الحقيقيتين تحقق. الباقي من شروط الخطة:

1. Linux بُني فقط ولم يُشغَّل (لا WSL ولا جهاز Linux). الفحص الذاتي 37/37 على linux-x64 مطلوب على جهاز Linux حقيقي، ومعه تثبيت وإزالة وكشف Steam.
2. لم يُنتج ZIP نهائي ولا SHA256SUMS ولا ملفات الإصدار، ولا فحص VirusTotal للحزمة الجديدة (يلزم أن يكون للحزمة المنشورة نفسها).
3. الفحص الذاتي يعمل على مجلدات مؤقتة فقط؛ لم يُجرَّب التثبيت على مجلد اللعبة الحقيقي.

## المرحلة 1: قائمة الفحص

- ملف جديد `technical/RC_CHECKLIST.md`: 64 مكانا بصيغة نعم/لا (العناوين والقوائم 10، الخطوط 9، HUD القتال 6، أول مشهد في 9 عوالم، أسطر تجاوز العرض الـ11، الصور 11، Gummi وRe Mind والقائمة المميزة وهاتف الغامي والمتاجر 8).
- كل معرّف فيها فُحص وجوده في ملفات الترجمة العامة (17,222 صفا)، والنصوص المقتبسة أخذت من الترجمة الحالية. معرّفات أول مشهد هي أول صف في ملف مشاهد كل عالم، وهي «متوقعة» لا مؤكدة.
- **نسختان من القائمة:** كانت الجلسة السحابية قد دفعت قبل ذلك إلى فرعها (`claude/stoic-bell-4bd73b`، الـcommit `39921e0`، غير مدموج في main) نسخة من الملف نفسه بـ62 مكانا في جداول ✓/✗. دُمج الفرع في main، واعتُمدت القائمة ذات الـ64 أساسا لأنها تتبع تصنيفات خطتك وتذكر المعرّفات المتوقعة، وأضيف إليها القسم الاختياري ح (17 مكانا) من الأماكن التي لا تغطيها. نسخة السحابة تبقى كاملة في تاريخ git.
- فُسّرت كلمة «اليوميات» في الخطة بأنها قائمة هاتف الغامي (القصة والتقارير السرية وسجلات اللعبة)، لأن كلمة اليوميات في المسرد لا تظهر إلا في أسطر المشاهد. يمكن تعديل البند G6 إن قُصد غير ذلك.

## المرحلة 2: لم تبدأ

`review/DECISIONS_1.0.md` يحتاج سياق المشاهد (`review/script/`) وملفات `review/codex_full_review/batch_N/unsure.tsv`، وهي خاصة. ومجلد `review/` غير منشور أصلا (`public_check.py` يمنع كل ملف فيه عدا `RULES.md`). وقد ضاع المشروع الخاص مع فرمتة الجهاز، فلا يمكن إعداد الملف قبل استعادة نسخة احتياطية منه، أو إعادة بناء مساحة العمل: تثبيت اللعبة، ومفتاح AES، وملفات `extracted\`، وسياق المشاهد. بدائل جزئية: المستودع الخاص `exelight7/KH3RM_AR_work` (مساحة عمل الجلسات السحابية بنصوص EN وAR)، وهو يحتاج دخولك إلى GitHub.

## ما بقي، بالترتيب

1. **المستودع العام هو المصدر الوحيد الآن.** `make_public.py` و`refresh.bat` و`publish.bat` تفترض المشروع الخاص ولا تعمل بدونه. تعديلات هذه الجولة (`Installer.csproj`، `tools/installer/README.md`، `technical/RC_CHECKLIST.md`، هذا التقرير، وأقسام الخريطة وCHANGELOG وPROGRESS) موجودة في هذا المجلد وتحتاج رفعها إلى GitHub (يلزم git و`gh auth login` على هذا الجهاز). إن وُجدت نسخة احتياطية من المشروع الخاص فادمج هذه التعديلات فيه بدل رفعها من هنا، حتى لا يطمسها النشر التالي.
2. إن استُعيد المشروع الخاص: `python -I tools\repair_docs.py` ثم `tools\refresh.bat`، ثم دمج فرع MAINT-1 (`claude/stoic-bell-4bd73b`) إن لم يُدمج بعد. يعيد هذا توليد القسم 5 من الخريطة. النسخة العامة نفسها سليمة (فحصتها).
3. المثبّت بالحزمتين الحقيقيتين: نجح على Windows (الجدول أعلاه). أوامر إعادة الفحص من أي مجلد (الحزمتان من إصدار 0.9.9، وتُفحص بصمتاهما قبل البناء):

```powershell
# تنزيل SDK مع تحقق SHA512 (القيمة من releases.json الرسمي؛ تحقق منها من جديد قبل الاستعمال)
$url  = 'https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.403/dotnet-sdk-10.0.403-win-x64.zip'
$want = '7a114c318fa7f1d9822991b534b2814d0e78386ceda816b371f5141acefe741d87ccb606ede06cadac8f9ac5070e32b708a67bbd1619ff5e5a7858a27874ef48'
Invoke-WebRequest $url -OutFile sdk10.zip
if ((Get-FileHash -Algorithm SHA512 sdk10.zip).Hash.ToLower() -ne $want) { throw 'SHA512 mismatch' }
Expand-Archive sdk10.zip -DestinationPath sdk10
$env:DOTNET_ROOT = "$PWD\sdk10"; $env:PATH = "$PWD\sdk10;$env:PATH"; $env:DOTNET_MULTILEVEL_LOOKUP = '0'

# الحزمتان: حمّل pakchunk99-arabic_P.pak وpakchunk98-arabic-images_P.pak من
# https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.9 إلى مجلد paks، وتحقق أن SHA256 يطابق Core.cs
# من جذر المستودع العام:
dotnet publish tools/installer/Installer.csproj -c Release -r win-x64 --self-contained true -o out/release/rc/windows -p:PakPath=paks/pakchunk99-arabic_P.pak -p:ImagesPakPath=paks/pakchunk98-arabic-images_P.pak
dotnet publish tools/installer/Installer.csproj -c Release -r linux-x64 --self-contained true -o out/release/rc/linux -p:PakPath=paks/pakchunk99-arabic_P.pak -p:ImagesPakPath=paks/pakchunk98-arabic-images_P.pak
# المثبّت WinExe: PowerShell لا ينتظره بلا Start-Process -Wait
Start-Process -Wait -FilePath out\release\rc\windows\KH3RM_AR_Setup.exe -ArgumentList '--selftest','out\release\rc\selftest_win.txt'
Get-Content out\release\rc\selftest_win.txt | Select-Object -Last 1   # المتوقع: selftest: ALL PASS
```

4. **قرار للمالك:** حزمة نص جديدة (BUILD-19) أو صور (IMAGES-MASS12) تحتاج اللعبة ومفتاح AES وملفات `extracted\`، أي استعادة المشروع الخاص. لذلك تُصنع الآن نسخة rc.2 من المثبّت وحده بالحزمتين نفسهما (BUILD-18 وIMAGES-MASS11)، وتصحيحات الترجمة اللاحقة تنزل في rc.3 بعد استعادة المشروع، أو يُنتظر استعادته. ثم المراحل 1 و4 و5 كما في الخطة، والمرحلة 2 بعد الاستعادة.
