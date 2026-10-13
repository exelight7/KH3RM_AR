# مثبت KH3RM_AR — Windows وLinux

الإصدار **0.8.3**، بنفس حزمة BUILD-7 المنشورة (4,889,918 بايت). التغييرات تخص البرنامج؛ تصحيحات مراجعة الدفعات الأربع لم تدخل في حزمة اللعبة بعد.

## التشغيل

- Windows x64: شغل `KH3RM_AR_Setup_v0.8.3_windows-x64.exe`.
- Linux x64، ومنها Steam Deck: فك `KH3RM_AR_Setup_v0.8.3_linux-x64.tar.gz` وشغل `KH3RM_AR_Setup` من المجلد. اللعبة نفسها تعمل عبر Steam/Proton؛ هذا مثبت التعريب وليس منفذا للعبة.
- .NET مضمن. Linux يحتاج جلسة رسومية X11 أو XWayland، ومكتبات النظام المعتادة: libX11، libICE، libSM، libfontconfig. لا تشغل المثبت كـroot؛ اختر مكتبة Steam التي يملكها مستخدمك.
- يدعم اكتشاف مكتبات Steam من libraryfolders.vdf وappmanifest، ومنها Steam Flatpak. Epic يكتشف تلقائيا على Windows؛ Linux يمكن اختيار مجلد تثبيت اللعبة يدويا.
- أغلق اللعبة، اختر مجلدها ثم ثبت التعريب. الإزالة تحذف ملف التعريب الذي يملكه البرنامج فقط.
- يتعرف على التثبيت من SHA256 لا رقم الواجهة؛ حزمة اللعبة لم تتغير عن الإصدار السابق.

## البناء

```powershell
dotnet publish tools/installer/Installer.csproj -c Release -r win-x64 --self-contained true -o out/release/v0.8.3-crossplatform/windows
dotnet publish tools/installer/Installer.csproj -c Release -r linux-x64 --self-contained true -o out/release/v0.8.3-crossplatform/linux
```

يفترض البناء وجود BUILD-7 تحت out/builds. يمكن تمرير `-p:PakPath=...`؛ يجب أن تطابق حزمة المصدر Core.ExpectedSha. في بيئة SDK Windows التي يفشل فيها workload resolver: مرر `-p:MSBuildEnableWorkloadResolver=false`.

الواجهة العربية افتراضية، والتبديل إلى الإنجليزية داخل التطبيق. `--demo` معاينة لا تسمح بالتثبيت أو الإزالة ولا تفحص اللعبة. `--render ar output.png` أو `--render en output.png` يلتقط الواجهة التجريبية ثم يغلق البرنامج. الملفات القديمة MainWindow.xaml وApp.xaml وEmblem محفوظة للتاريخ لكنها مستبعدة من Compile. بقي وضع --selftest الموجود سابقا، ولم تشغل اختبارات الوحدة ضمن هذه الجولة.

## ما تغير

- Avalonia 11.3.22 / .NET 8 لواجهة واحدة على Windows وLinux.
- صورة Sora المختارة، واجهة ليلية ولمسات ذهبية ونص عربي واضح.
- متصفح مجلدات أصلي، حالات التثبيت، تبديل اللغة، مؤشر عمل وسجل اختياري.
- تجهيز ملف مؤقت والتحقق من بصمته قبل استبدال الحزمة الموجودة؛ فشل التحضير لا يحذف النسخة المثبتة.
- فحص عمليات Proton/Wine محليا على Linux، ومنع الإغلاق أثناء عملية كتابة.
- الحقوق في [CREDITS.md](CREDITS.md) فقط، وليست ضمن الواجهة.

نجح بناء Windows وLinux، ومعاينة الواجهة على Windows. لم يتوفر نظام Linux لتشغيل النسخة فعليا؛ يحتاج التحقق على جهاز Linux قبل وصفها بأنها مجربة هناك. لم تشغل اللعبة ولم تثبت حزمة على جهاز المستخدم.
