# مكان الصورة الاختيارية (art slot)

المثبّت يرسم خلفيته كاملة بنفسه (سماء ليلية ونجوم وقلب بمفتاح ذهبي) من ملفات XAML أصلية، ولا يستخدم أي صورة من الإنترنت.

إذا أردت استخدام عمل فني خاص بك، أو لفنان أعطاك إذنا صريحا بنشره:
1. ضع الصورة هنا باسم `background.png` (يفضّل 900×560 أو أكبر بنفس النسبة).
2. ضع في ملف `CREDIT.txt` سطر الشكر، مثلا: `الخلفية: اسم الفنان (رابط حسابه)`.
3. أعد بناء البرنامج (انظر قسم 6 في `PROJECT_MAP.md`): تُدمج الصورة داخل الـ EXE وتظهر خلف الواجهة بشفافية 55٪، ويظهر سطر الشكر أسفل الشعار.

لا تضع هنا صورا رسمية من Square Enix أو Disney أو أعمالا للمعجبين بلا إذن مكتوب من صاحبها. إذا لم يوجد الملف يُبنى البرنامج بالخلفية المرسومة.

# Optional art slot
If `art\background.png` exists at build time it is embedded as the window background, with the credit line from `art\CREDIT.txt` shown under the emblem. Only use art you own or have the artist's written permission to publish. Without the file the built-in XAML art is used.
