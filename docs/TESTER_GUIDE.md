# دليل المختبر / Tester guide

## العربية (Arabic)

### التثبيت
- شغل المثبت (الأسهل) واللعبة مغلقة.
- يدويا: ضع ملفات pak في مجلد `~mods`.

### الإزالة
- `REMOVE_AR.bat`: التعريب كله - `REMOVE_IMAGES.bat`: الصور فقط. واللعبة مغلقة.

### ماذا تختبر
- الأماكن التي في `technical\BUILD7_CHECKLIST.md`, `BUILD6_CHECKLIST.md`, `IMAGES_MASS_CHECKLIST.md`.
- أول مشهد سينمائي في كل عالم.
- قتال - سفينة Gummi - الألعاب المصغرة - Re Mind - دفتر اليوميات - المتاجر - الشروح - نهاية اللعبة.

### كيف تبلغ عن مشكلة (سطر واحد)
`رقم السطر أو الكلمات التي رأيتها | المكان | نوع المشكلة`

| type | المشكلة | ماذا تكتب |
|---|---|---|
| cut | النص مقطوع | اكتب رقم السطر ومكان القطع |
| reversed | ترتيب معكوس | اكتب الكلمات كما ظهرت |
| english | بقي بالإنجليزية | اكتب الكلمة الإنجليزية الباقية |
| meaning | معنى خاطئ | اكتب الكلمات والمعنى الصحيح الذي تقترحه |
| boxes | مربعات أو حروف غريبة | اكتب مكان المربعات |
| crash | انهيار | اكتب ما كنت تفعله قبل الانهيار |

- لقطة شاشة: Win+Shift+S ثم احفظها وأرسلها مع السطر في نفس المحادثة.
- ابحث عن كلمة: `python tools\find_text.py <كلمة>` (اربية أو إنجليزية; `--ids`, `--around 3`).
- القالب: `state\FEEDBACK_TEMPLATE.tsv` -> `state\FEEDBACK.tsv`, ثم `python tools\apply_feedback.py`.

## English

### Install
Run the installer (easiest) with the game closed. Manual: copy the pak files into the game's `~mods` folder.

### Remove
`REMOVE_AR.bat` removes the whole translation; `REMOVE_IMAGES.bat` removes only the optional images pack. Game closed.

### What to test
- The places in `technical\BUILD7_CHECKLIST.md`, `BUILD6_CHECKLIST.md` and `IMAGES_MASS_CHECKLIST.md`.
- Each world's first cutscene, a battle, the Gummi ship, mini-games, Re Mind, the journal, shops, tutorials, game over.

### Report a problem in ONE line
`id or the Arabic words you saw | where | type`

| type | meaning | what to write |
|---|---|---|
| cut | text cut off | the row id or words, and where it is cut |
| reversed | reversed order | the words as shown |
| english | English left | the English word still showing |
| meaning | wrong meaning | the words and the meaning you expect |
| boxes | boxes / broken letters | where the boxes appear |
| crash | game crash | what you were doing before it |

### Screenshot
Win+Shift+S, save the picture, send it in the same chat as your one-line report.

### Tools
- `python tools\find_text.py <word>`: finds the row by Arabic (also copied from a screenshot) or English; `--ids` ids only; `--around N` N neighbours.
- Fill `state\FEEDBACK.tsv` (columns of `state\FEEDBACK_TEMPLATE.tsv`), run `python tools\apply_feedback.py` -> `review\FEEDBACK_REPORT.md`.
