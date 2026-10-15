# مثبت KH3RM_AR — Windows وLinux

الإصدار **0.9.8**. يضم ملف واحد حزمتين:
- حزمة النص BUILD-18 (`pakchunk99-arabic_P.pak`، 5,103,489 بايت) وفيها تصحيحات المراجعة اللغوية الكاملة؛ تثبت دائما.
- حزمة الصور IMAGES-MASS11 (`pakchunk98-arabic-images_P.pak`، 41,493,315 بايت)، اختيارية: تنسخ فقط عند تفعيل خانة «تثبيت حزمة الصور أيضًا». الخانة غير مفعلة افتراضيا، وتظهر مفعلة إذا كانت حزمة الصور مثبتة من قبل في المجلد المختار.

## التشغيل

- Windows x64: شغل `KH3RM_AR_Setup_v0.9.8_windows-x64.exe`.
- Linux x64، ومنها Steam Deck: فك `KH3RM_AR_Setup_v0.9.8_linux-x64.tar.gz` وشغل `KH3RM_AR_Setup` من المجلد. اللعبة نفسها تعمل عبر Steam/Proton؛ هذا مثبت التعريب وليس منفذا للعبة.
- .NET مضمن. Linux يحتاج جلسة رسومية X11 أو XWayland، ومكتبات النظام المعتادة: libX11، libICE، libSM، libfontconfig. لا تشغل المثبت كـroot؛ اختر مكتبة Steam التي يملكها مستخدمك.
- يدعم اكتشاف مكتبات Steam من libraryfolders.vdf وappmanifest، ومنها Steam Flatpak وXDG_DATA_HOME. Epic يكتشف تلقائيا على Windows؛ Linux يمكن اختيار مجلد تثبيت اللعبة يدويا.
- أغلق اللعبة، اختر مجلدها، فعّل خانة الصور إن أردتها، ثم ثبت التعريب. يرفض البرنامج العمل واللعبة تعمل، ويفحص عمليات Proton/Wine على Linux.
- «إزالة التعريب» تحذف حزمة النص، ومعها حزمة الصور إذا كانت الخانة مفعلة. زر «إزالة حزمة الصور فقط» يظهر عندما تكون حزمة الصور مثبتة، ويبقي النص.
- كل حزمة تكتب في ملف مؤقت ويفحص SHA256 الخاص بها قبل وضعها في `~mods`؛ فشل حزمة لا يحذف أي حزمة مثبتة.

## البناء

```powershell
dotnet publish tools/installer/Installer.csproj -c Release -r win-x64 --self-contained true -o out/release/v0.9.8/windows
dotnet publish tools/installer/Installer.csproj -c Release -r linux-x64 --self-contained true -o out/release/v0.9.8/linux
```

يفترض البناء وجود BUILD-18 وIMAGES-MASS11 تحت out/builds، ويتوقف إذا غابت إحداهما. يمكن تمرير `-p:PakPath=...` و`-p:ImagesPakPath=...`؛ يجب أن تطابق الحزمتان Core.ExpectedSha وCore.ImagesSha. في بيئة SDK Windows التي يفشل فيها workload resolver: مرر `-p:MSBuildEnableWorkloadResolver=false`.

الواجهة العربية افتراضية، والتبديل إلى الإنجليزية داخل التطبيق. `--demo` معاينة لا تسمح بالتثبيت أو الإزالة ولا تفحص اللعبة. `--render ar output.png` أو `--render en output.png` يلتقط الواجهة التجريبية ثم يغلق البرنامج. `--selftest out.txt` يشغل 37 فحصا على مجلدات مؤقتة فقط. الملفات القديمة MainWindow.xaml وApp.xaml وEmblem محفوظة للتاريخ لكنها مستبعدة من Compile.

## ما تغير في 0.9.8

- حزمة النص BUILD-18 بدل BUILD-12: تصحيحات المراجعة اللغوية الكاملة، وخط IBM Plex Sans Arabic للقوائم والترجمة مع Segoe UI Bold للعناوين، وكلمات شريط المعركة مرسومة بدقة مضاعفة.
- حزمة الصور IMAGES-MASS11 بدل IMAGES-MASS5: الكتابة الصغيرة في الصور أوضح وأكثر حدة.

## ما تغير في 0.9.2

- حزمة النص BUILD-12 بدل BUILD-10.
- حزمة الصور IMAGES-MASS5 بدل IMAGES-MASS4.

## ما تغير في 0.9.1

- حزمة النص BUILD-10 بدل BUILD-8.
- حزمة الصور IMAGES-MASS4 بدل IMAGES-MASS3.

## ما تغير في 0.9.0

- خانة اختيارية لحزمة الصور، مع حالة كل حزمة وزر لإزالة الصور وحدها.
- حزمتان مضمنتان، لكل منهما بصمة SHA256 وتثبيت وإزالة مستقلان.
- حزمة النص BUILD-8 بدل BUILD-7.
- الحقوق في [CREDITS.md](CREDITS.md) فقط، وليست ضمن الواجهة.

نجح بناء Windows وLinux، ونجحت فحوص `--selftest` الـ37 على Windows، وعوينت الواجهة على Windows. لم يتوفر نظام Linux لتشغيل النسخة فعليا؛ يحتاج التحقق على جهاز Linux قبل وصفها بأنها مجربة هناك. لم يجرب التثبيت أو الإزالة على مجلد اللعبة الحقيقي.
