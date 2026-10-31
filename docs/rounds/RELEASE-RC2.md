# RELEASE-RC2 — 2026-10-31

طلب المالك: «نعم، جهّزها»، أي مرشح الإصدار `1.0.0-rc.2` للمثبّت وحده، بالحزمتين نفسهما (BUILD-18 وIMAGES-MASS11) والمثبّت على .NET 10، قبل 2026-11-10. **جُهّز محليا ولم يُنشر**: لا push ولا وسم ولا إصدار على GitHub، ولا تثبيت في اللعبة.

## ما تغيّر في المصدر

- `tools/installer/Core.cs` و`tools/installer/Installer.csproj`: الإصدار `1.0.0-rc.2` (`ExpectedSha` و`ImagesSha` و`PakPath` كما هي، لأن الحزمتين لم تتغيرا).
- `tools/make_public.py`: `RELEASE = '1.0.0-rc.2'` و`SETUP = 'KH3RM_AR_Setup_v1.0.0-rc.2_windows-x64-folder.zip'` و`BUILD` ما زال `BUILD-18`.
- `README.md`: القيم التي كان سيولّدها `make_public.py` (رقم الإصدار وروابط التنزيل). **لا تدفعه إلى main قبل أن يكون الإصدار موجودا**، وإلا انكسرت روابط التنزيل.
- `tools/installer/README.md`: قسم «ما تغير في 1.0.0-rc.2» وأسماء الملفات.

## الحزم

مجلد الإصدار على الجهاز: `C:\1\release_1.0.0-rc.2\` (خارج المستودع عمدا).

| الملف | الحجم (بايت) | SHA256 |
|---|---|---|
| `KH3RM_AR_Setup_v1.0.0-rc.2_windows-x64-folder.zip` | 93,561,841 | `405773c0ac2a061f2e6dc8393245ab8d61a33b8b2cf63a0ecfbf44ff0019e7a8` |
| `KH3RM_AR_Setup_v1.0.0-rc.2_linux-x64.tar.gz` | 91,300,871 | `abcca3ffebb307f2a9f252f6f6c5030ee7683c44b6e912798080b1974e7af392` |
| `pakchunk99-arabic_P.pak` (BUILD-18) | 5,103,489 | `dde67ce67b7d93bf95835a0126e317e003e3a2a51370321da51ce48035afe527` |
| `pakchunk98-arabic-images_P.pak` (IMAGES-MASS11) | 41,493,315 | `7b37f84b390db3d62fe837892a99bbe3fe4ae7cccf9bc67a119decb3d643c964` |
| `OFL-IBM-Plex-Sans-Arabic.txt` | 4,360 | `91c25c350d3cac39da2736d74f7ba37ef648f5237a4e330a240615bc8d8c4360` |
| `SHA256SUMS.txt` (5 أسطر، CRLF) | 513 | — |
| `RELEASE_NOTES.md` (نص الإصدار بالعربي) | 1,716 | — |

- الحزمتان والرخصة هي نفسها ملفات إصدار 0.9.9 (تحققت من بصمتيهما قبل البناء، والرخصة مستخرجة من أرشيف 0.9.9).
- بنيت بـ.NET SDK 10.0.403 (SHA512 للتنزيل محقق)، والمضمن runtime 10.0.14. الأرشيفان مسطّحان كما في 0.9.9: ملفات المثبّت و`OFL-IBM-Plex-Sans-Arabic.txt` و`README_AR.md`. Windows 220 ملفا، وLinux 219.
- tar.gz: الملف `KH3RM_AR_Setup` وحده بصلاحية 0755 والباقي 0644، ولا مسارات بشرطة مائلة.

## التحقق

| الفحص | النتيجة |
|---|---|
| `--selftest` على مجلد win-x64 المنشور (قبل التغليف) | 37 من 37 |
| فك ZIP في مجلد جديد: كل الملفات مطابقة بـSHA256 للأصل | 220 من 220 |
| `--selftest` على المجلد المفكوك من ZIP | 37 من 37 |
| فك tar.gz في مجلد جديد: كل الملفات مطابقة | 219 من 219 |
| إعادة حساب كل أسطر `SHA256SUMS.txt` من مجلد الإصدار | 5 من 5 |
| الإصدار داخل `KH3RM_AR_Setup.dll` | 1.0.0-rc.2 |
| `KH3RM_AR_Setup.exe` داخل ZIP | SHA256 `c3f90fcd420da44673025113deb304de1e0e70d4049ea8a14f4fcad5762cf5b8` |

## ما لم يتحقق

1. **Linux:** الأرشيف سليم لكنه لم يُشغَّل على Linux (لا جهاز ولا WSL). مكتوب هذا في نص الإصدار.
2. **VirusTotal:** لم تُفحص هذه الحزمة. الفحص السابق (0/70) لا ينطبق عليها. ارفع ملف ZIP هذا نفسه قبل النشر إن أردت رقما صادقا.
3. التثبيت والإزالة على مجلد اللعبة الحقيقي، وكشف Steam وEpic على تثبيتات حقيقية.
4. المثبّت غير موقع (تنبيه SmartScreen متوقع).

## النشر (لم يُنفَّذ، ينتظر أمر المالك)

بعد أن يكون عندك git وgh (`winget install Git.Git GitHub.cli` ثم `gh auth login`)، ومن نسخة git للمستودع العام:

```powershell
# 1) انسخ إلى النسخة ملفات المصدر المعدلة (README.md وCHANGELOG.md وPROJECT_MAP.md وstate/PROGRESS.md وtechnical/RC_CHECKLIST.md
#    وtools/installer/* وtools/make_public.py وdocs/rounds/RC-PREP-1.md وdocs/rounds/RELEASE-RC2.md) ثم:
git add -A; git commit -m "RELEASE-RC2: installer on .NET 10, version 1.0.0-rc.2"; git push origin main

# 2) أنشئ الإصدار (وسم بلا v، مرشح إصدار) بالملفات الستة ونص الإصدار
cd C:\1\release_1.0.0-rc.2
gh release create 1.0.0-rc.2 --prerelease --title "1.0.0-rc.2 (release candidate)" --notes-file RELEASE_NOTES.md `
  KH3RM_AR_Setup_v1.0.0-rc.2_windows-x64-folder.zip KH3RM_AR_Setup_v1.0.0-rc.2_linux-x64.tar.gz `
  pakchunk99-arabic_P.pak pakchunk98-arabic-images_P.pak SHA256SUMS.txt OFL-IBM-Plex-Sans-Arabic.txt

# 3) تحقق: أحجام الأصول وبصماتها على GitHub = الملفات المحلية
gh release view 1.0.0-rc.2 --json assets,isPrerelease
```

الأفضل أن يُنشأ الإصدار أولا كمسودة (`--draft`) ثم يُدفع main ثم يُنشر، حتى لا يشير README إلى روابط غير موجودة. بديل بلا gh: صفحة Releases على GitHub، `Draft a new release`، الوسم `1.0.0-rc.2`، علامة `Set as a pre-release`، وإرفاق الملفات الستة ولصق `RELEASE_NOTES.md`.
