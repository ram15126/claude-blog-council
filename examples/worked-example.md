# Worked example: what the council catches

Real errors from drafts about well-known stories, each caught by a reviewer who opened the source. Every case links the public source and the place in it, so you can check it yourself. None of these drafts looked wrong on a careful read. All of them were wrong against the source. Sources were read in October 2026.

The pattern names refer to the mistake catalogue in `references/sop.md`, section 6.

---

## 1. The detail the source does not have (pattern A)

**Draft:** "Krishna carried the conch to the city of Yama and blew it at the gate. Yama gave the boy back alive, and Krishna kept the conch."

**Source:** *Bhagavata Purana* 10.45 ([vedabase.io](https://vedabase.io/en/library/sb/10/45/)): he "loudly blew His conchshell" on arriving, and Yama "brought forth the guru's son". No gate, no "alive", nothing about keeping it.

**Fixed:** "He and Balarama carried it to Samyamani, the city of Yama, and Krishna blew it loudly when they arrived. Yama brought the boy out."

**Caught by:** Source Auditor.

## 2. The popular version passed off as the text (pattern A)

**Draft:** "In the later version, Satyabhama strikes the killing blow."

**Source:** the summary the draft cited, [Wikipedia: Narakasura](https://en.wikipedia.org/wiki/Narakasura) (section on his death): Satyabhama "attacked Narakasura and Krishna killed him with his Sudarshana Chakra".

**Fixed:** "Satyabhama attacks in anger, and Naraka is killed. The final blow is still Krishna's disc."

## 3. The swapped noun (pattern A)

**Draft:** "One arm is cut off, with the mace it held."

**Source:** *Yuddha Kanda* 67, verse 158 ([valmikiramayan.net](https://www.valmikiramayan.net/utf8/yuddha/sarga67/yuddhasans67.htm)): "chopped off Kumbhakarna's arm along with the hammer".

**Fixed:** "One arm is cut off, with the hammer it held."

**Caught by:** the second reviewer, after a first reviewer on a smaller model passed it.

## 4. The misquote (pattern B)

**Draft:** the name is said to mean "he who makes the worlds cry out".

**Source:** *Uttara Kanda*, chapter 16, Hari Prasad Shastri's translation ([wisdomlib.org](https://www.wisdomlib.org/hinduism/book/the-ramayana-of-valmiki/d/doc424777.html)): "He who causes the worlds to cry out".

**Lesson:** quotation marks mean copied, not remembered. `scripts/check_quotes.py` now catches this before any reviewer sees it.

## 5. The "first" that was not first (pattern C)

**Draft (from an older article):** "The squirrel who helps build the bridge first appears in a Telugu retelling of around 1200."

**Source:** a Tamil devotional poem, *Tirumalai* verse 27 ([koyil.org](https://divyaprabandham.koyil.org/index.php/2016/10/thirumalai-27/)), already has squirrels helping close the sea. Its poet is placed in the 8th century ([Wikipedia: Thondaradippodi Alvar](https://en.wikipedia.org/wiki/Thondaradippodi_Alvar)); the Telugu retelling is dated to the 13th century ([Wikipedia: Ranganatha Ramayanamu](https://en.wikipedia.org/wiki/Ranganatha_Ramayanamu)).

**Fixed:** "The oldest mention we found is in Tamil." The headline claim of the older article was wrong, and many websites repeat it.

**Caught by:** a search for an older source, which the Skeptic role now does on every "first" claim.

## 6. A true sentence that misleads this year (pattern F)

**Draft (bold opener):** "Yes: Tamil Nadu celebrates a day before the north."

**Source:** the [Drik Panchang 2026 calendar](https://www.drikpanchang.com/diwali/diwali-puja-calendar.html?year=2026) lists Naraka Chaturdashi, Tamil Deepavali and Lakshmi Puja on the same date, and [officeholidays.com](https://www.officeholidays.com/holidays/india/tamil-nadu/diwali) gives the same date (checked 13 October 2026).

**Fixed:** "One lunar day before, but not always one calendar date before. In 2026 both fall on Sunday 8 November."

## 7. The reviewer's own wrong fix (adjudication)

**Draft:** "when Rama first sees the giant on the battlefield" (wrong: he is seen in the city).

**Reviewer's suggested fix:** "striding through Lanka". The text has no "striding".

**Chair's fix:** "when Rama sees the giant in Lanka and asks who he is", which is what *Yuddha Kanda* 61, verse 5 says ([valmikiramayan.net](https://www.valmikiramayan.net/utf8/yuddha/sarga61/yuddhasans61.htm)): the giant "is seen in Lanka".

**Lesson:** every fix, including a reviewer's, is checked against the source.

---

## What a council run looked like

One run, for illustration: a 1,500-word explainer written with this method from the start.

| Round | Reviewer | Score | Findings |
|---:|---|---:|---|
| 1 | Smaller model | 9.5 | No wrong fact reported |
| 2 | Strongest model | 9.0 | Two wrong details (the hammer; a joined step) |
| 3 | Strongest model | 9.0 | Two wordings past the text (PARTLY) |
| 4 | Strongest model | 9.0 | No wrong fact, quote, number or verse reference |

That run stopped at round 4. Under the stricter clean-round rule now in `references/council.md` (no PARTLY allowed), round 3 does not count as clean, so the same article would need one more clean round before hand-over. The smaller model in round 1 missed the two errors that round 2 found.
