# The method

The full standard operating procedure behind the `blog-council` skill. Read it once in full; after that, `SKILL.md` is enough to work from.

---

## 1. Pick the search

- Start from a real query: the words people type, not the words you would use. Free signals are enough: autocomplete, "People also ask", the search tool's own keyword planner, forum titles.
- Note the main phrase, its close variants, and the questions people attach to it ("who", "why", "how old", "is it real").
- **The title leads with the searched phrase**, then a plain tail that says what the page really holds. No hype, no promise the page does not keep. Aim for 60 characters or fewer.
- Each question that matters gets its own heading later. A supporting phrase with real demand gets a heading, not a buried sentence.

## 2. Read the originals

The single biggest gain in accuracy. Summaries, encyclopedias and other blogs copy each other's errors; the original does not.

| Topic | Read |
|---|---|
| Religious and classical texts | A full translation, by chapter and verse. Note the translator. A commentary is not the text |
| History | Primary documents, then peer-reviewed or well-sourced secondary work |
| Science and health | The paper or the official guidance, not the press release |
| Law and policy | The statute, regulation or official notice |
| A company, product or place | Its own official page, read on the day |
| People | Interviews in their own words, official records |

Rules:
- **Read the raw page when a tool summarises it for you.** Reader tools return a model's reading of a page, not the page. Before writing "the source does not say X", ask again with a narrower question or download the page and search it.
- **Record where each fact is**: chapter, verse, page, paragraph, table.
- A page you could not open supports nothing.

### 2b. Collect data (data-led posts only)

If the article's value is a finding ("we checked 1,000 sites and found..."), collect the data before writing: define the sample, record how and when it was collected, keep the raw file and the script, and state the counts exactly. Every number in the article must be reproducible from the file. Do not collect data against a site's terms.

## 3. Build the claims ledger

Before writing, list every fact the article will state in `templates/claims-ledger.csv`:

| Column | What goes in it |
|---|---|
| `id` | C1, C2, ... |
| `claim` | The fact in one plain sentence |
| `source_url` | The page that supports it (the text page, not a frame or index) |
| `location` | Chapter, verse, section, paragraph |
| `quote` | The exact words on the page that support it. Copy and paste |
| `type` | story, number, date, quote, attribution, definition, comparison, superlative |
| `checked_on` | The date you read the source (YYYY-MM-DD). Re-check anything older than 30 days before publishing |
| `status` | Set by the Chair after each round: CONFIRMED, PARTLY, NOT FOUND, CONTRADICTED, DISPUTED, UNSOURCED (see `council.md`, section 4) |
| `note` | Who gave the verdict, and the source line that settles it |

A fact without a quote from a source does not go in the article. A quote under 6 words does not count as support unless the claim is the quote itself: short phrases match almost any page. The ledger is also what the council checks against, and what `scripts/check_quotes.py` reads.

## 4. Write in the template

The shape is in `templates/article-outline.md`. It is built for two readers at once: a person scanning on a phone, and a search engine or AI assistant lifting one passage as an answer.

1. **Quick answer** (60 words or fewer): answers the title, names the subject.
2. **Key facts table**: fact, detail, source. Each row reads correctly on its own.
3. **Sections**: 6 to 11, each heading a real question, each opening with **one bold sentence that answers it on its own**.
4. **Common questions**: 8 to 12, each answer self-contained, each carrying the same caveats as the body.
5. **The site's call to action**, described in the site's own words (from the profile).
6. **Sources**: title, publisher, link, and what each source supports.

Writing rules:
- Plain language. Short sentences. One idea per paragraph.
- Explain every specialist or foreign term the first time it appears.
- Say once what a paragraph says. Do not repeat a point in three places.
- Label your own reading: "That reading is ours, but both halves are in the text."
- No em dashes, no filler ("in today's world", "delve", "tapestry", "it is important to note").

## 5. Machine checks

Run `python <skill-dir>/scripts/check_quotes.py blog-council/<slug>/claims-ledger.csv --article blog-council/<slug>/draft.md`. It downloads each source page, strips the markup, checks that each ledger `quote` appears word for word, flags short quotes and stale `checked_on` dates, and reports any quotation in the draft that has no ledger row. Fix the article to match the source, never the other way round.

PDFs and pages built by JavaScript may return no usable text: save the text yourself and point `source_url` at it with a `file://` URL, or check those rows by hand.

Not scripted yet: that every number in the text matches the ledger, and that every internal link answers 200. The Source Auditor and Profile Checker check these.

## 6. Self-check: the mistake catalogue

Read the draft once more against this list. Every pattern here is a real error that got past a careful writer.

### A. Saying more than the source says

| Pattern | Example of the error | Rule |
|---|---|---|
| Scene-setting words | "He blew the conch **at the gate**"; "returned the boy **alive**" when the text says neither | Retell only what is stated |
| Tidied endings | "He **set the captives free**" when the text says he sent them away and married them | Do not tidy a story into the ending people expect |
| The popular version | "Satyabhama **strikes the blow**" when the text has the hero's weapon kill him | Say which version is the text's and which is later |
| Joined steps | "Drank the wine **before setting out for battle**" when he first went to his brother's palace | Do not merge two steps into one |
| The dramatic cause | "Cursed **after he attacked** the god" when the god struck first and the complaint was something else | State the cause the text states |
| Swapped nouns | "**Mace**" where the translation says "hammer" | Use the translation's own noun for objects |
| Widened scope | "**The south** celebrates a day earlier" when the source says one state | Do not widen a region, period or group |
| Turned "sometimes" into a rule | "**Usually** a day apart" when recent years fall on the same date | Frequency words need evidence |
| Superlatives | "**The oldest** telling", "**the best known**", "**the first** mention" | Need a source making the same superlative |
| Numbers from memory | "**Ten** lines" for a four-line verse; a count where sources say 140 or 143 | Re-read every number. If sources differ, say so or leave it out |

### B. Quotes and attributions

| Pattern | Rule |
|---|---|
| A translation retyped from memory ("makes the worlds cry" for "causes the worlds to cry out") | Copy, never retype. Keep the source's numerals and spelling inside quotes |
| A gloss put in quotation marks that no source gives in those words | Your own wording goes without quotation marks |
| A fact credited to a chapter that does not contain it (a mountain's name the chapter never gives) | The source named must contain the fact. Two sources for two halves: name both |
| The right fact, the wrong chapter | Give the place you actually read it |
| A quote nobody can find today | Out of the article |
| A finding in quotation marks from a document you never opened | Write it as reported, credited to who reports it |
| "Composed", "wrote", "founded", "invented" where the source says "sang", "used", "led" | Each of these verbs needs its own evidence |
| "Wrote in 1946" where the source says "released in 1946" | Keep the source's verb for dates |

### C. Simply wrong

| Pattern | Rule |
|---|---|
| A "first appears in X" claim copied from many websites, when an older source exists | "First", "earliest" and "not in X" claims get their own search. Write "the oldest mention we found" |
| A story detail from memory of a retelling | Never write a story fact from memory |
| One uncited encyclopedia line contradicted by several other sources | Find a second source or say whose claim it is |
| An error introduced while fixing another sentence | Re-check every fix against the source |

### D. Disagreement and thin sourcing

- Two sources disagree: say so in the text, name both.
- One source only: say whose claim it is ("According to ...").
- A source marked "citation needed" by its own editors: say so in the source note.
- A company or aggregator site is not an official record. Say what it is.
- Debated dates: give the scholarly and the traditional date, labelled.

### E. Product links and site rules

| Pattern | Rule |
|---|---|
| "Named after", "inspired by", "based on" when the product page says no such thing | Say only what the product page says. "Shares its name with" is safe |
| A heading that promises a link the body then denies | The heading states plainly what the section is |
| Words written in a real person's voice as a placeholder | Never, not even as a placeholder |
| Off-topic facts added to make a link feel deep | Cut any sentence that is about neither the topic nor the product |
| Links to pages that do not exist yet | Link only to pages that answer 200 today |

### F. Search and AI answers

| Pattern | Rule |
|---|---|
| Section openers like "No.", "Yes.", "There is no single reason." | The first sentence answers the heading alone, subject named |
| A bold answer that is true in general but wrong this year | Read each opener as if it were the whole answer, on the day it will be read |
| A "why" heading the sources cannot answer | Then it is not a "why" heading |
| Headings nobody searches; mixed contents under one heading | One real question per heading, and only answers to it beneath |
| FAQ answers that start "It..." or dangle ("After a fast..., the god granted") | Each answer names its subject and reads alone |
| FAQ firmer than the body | Same hedge in both |

## 7. Convene the council

See `references/council.md`. Do not score your own article. The council is the step that turns "reads well" into "checks out".

## 8. The gate

The article passes only when:
- every claim in the ledger is CONFIRMED, or DISPUTED and labelled as such in the text;
- no claim is CONTRADICTED;
- every quote passes `check_quotes.py`;
- two consecutive council rounds found no wrong fact and scored at or above the profile's bar (default 9.0).

## 9. Images

- **The cover is usually cropped to a wide banner by the site's theme.** A tall picture used as a cover will lose its top and bottom; the subject's face is often cut off. Look at the cover the way the site draws it before publishing. Set the crop point (focal point or hotspot) on the subject, or choose a wide picture.
- **A tall picture** can go inside the article as its own image, shown whole, with its caption and credit.
- Use your own images or openly licensed ones, and credit them as the licence asks. Do not use AI-generated images where the site promises otherwise.

## 10. Hand over, publish, verify

1. Put the draft in the site's CMS as a draft. Preview it on desktop and phone.
2. The site owner reads and publishes. Sensitive sections (religion, health, politics, named people) get read by someone who answers for the site.
3. After it is live, run `python <skill-dir>/scripts/verify_live.py <url> --sitemap <sitemap-url> --draft draft.md`: status and redirects, title, description, canonical, single H1, no noindex (tag or header), internal links, images, valid structured data, sitemap, and that the CMS kept every sentence of the reviewed draft. Read the quick answer and FAQ on the live page yourself.
4. Ask the search engine to index it (in Google, URL Inspection then Request indexing). The daily allowance is small and shared across a whole account: put new articles first.
5. Write the fact-check log (`templates/fact-check-log.md`): scores by round, errors caught, single-source claims, open questions for the owner.

## 11. Cost and models

- Script anything deterministic. Quotes and the live page are scripted; add your own checks for numbers and links if you need them.
- A smaller model is fine for an early review round. The rounds that count for the gate run on the strongest model available (see `council.md`, section 5).
- Reviewers that download the raw page and search it are more reliable than ones relying on a reader tool's summary. Say so in the prompt.
