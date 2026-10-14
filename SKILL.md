---
name: blog-council
description: Source-first method and an independent-reviewer "council" for blog articles whose facts must be provably right - history, mythology, religion, science, health, law, places, people, definitions, and "what is X / who was X / why is X" explainers. Use when the user asks to fact-check, verify, score or review an article against its sources, to "run the council", to write an explainer with every claim traced to a source, or to make an article citable by search engines and AI assistants. Works with any site and CMS. Not for opinion pieces, personal stories, product announcements or quick drafts without sources.
---

# Blog Council

A method for writing articles that are **right first**, and a council of independent reviewers that proves it.

It exists because drafts that read well are often wrong in small ways: a detail the source never says, a quote slightly changed, a "first" or "only" nobody can back, a claim credited to the wrong chapter. Those errors survive self-review because the writer checks what they meant, not what the source says. The council fixes that by separating the writer from the people who check, and by making every check open the source.

## When to use it

- Articles whose facts live in sources: history, mythology, religion, science, health, law, places, people, "how it works", definitions, comparisons.
- Any article that will carry your name, a client's name, or claims an AI assistant might quote.
- Rewriting an old article: treat the old text as a **list of claims to check**, not as text to polish.

Not a fit on its own for opinion pieces, personal stories or product announcements. Posts built on fresh data need the optional data step (`references/sop.md`, step 2b).

## Before anything

1. **Load the site profile.** Look for `blog-council.profile.md` in the project, or ask the user for the facts in `templates/site-profile.md` (audience, byline, call to action, banned words, sensitive topics, quality bar). Never invent a site's rules.
2. **Never publish.** The skill ends at a reviewed draft and a fact-check log. Publishing, and anything that changes a live site, needs the user's explicit go-ahead each time.

## The order of work

| # | Step | Detail |
|---|---|---|
| 1 | Pick the search | The phrase people actually type, and its close variants. Title leads with it |
| 2 | Read the originals | The chapter, verse, statute, paper, dataset or interview itself, not blogs about it. (2b: collect data, for data-led posts) |
| 3 | Build the claims ledger | Create a working folder `blog-council/<slug>/` in the project and copy `templates/claims-ledger.csv`, `templates/article-outline.md` and `templates/fact-check-log.md` into it. Never edit the skill's own `templates/`. One ledger row per fact: source, exact location, the exact supporting quote, and the date you checked it. Before writing a word. A filled example is in `examples/claims-ledger-example.csv` |
| 4 | Write in the template | `templates/article-outline.md`: quick answer, key facts with sources, question headings with a bold answer first, FAQ, sources |
| 5 | Machine checks | `python <skill-dir>/scripts/check_quotes.py blog-council/<slug>/claims-ledger.csv --article blog-council/<slug>/draft.md`: every ledger quote is word for word on its raw source page, and every quotation in the draft has a ledger row |
| 6 | Self-check | Remove every word the sources do not have (the mistake catalogue in `references/sop.md`) |
| 7 | **Convene the council** | `references/council.md`: independent reviewers verify, try to disprove, and score. Fix, re-verify each fix, repeat with fresh reviewers |
| 8 | Gate | Pass only when the hard gates hold and two rounds in a row are clean at or above the profile's bar |
| 9 | Hand over | A draft for the user's CMS and the fact-check log. After publishing: `scripts/verify_live.py <url> --draft draft.md` (also proves the CMS kept the reviewed text) and an indexing request |

Full method with the reasons: `references/sop.md`. The council in detail: `references/council.md`. Scoring: `references/rubric.md`.

## The ten rules that stop most errors

1. **Retell only what the source states.** No scene-setting word (gate, alive, young, royal, first, famous) the source does not contain.
2. **Quotation marks mean word for word.** Copy from the source, never from memory. Your own paraphrase gets no quotation marks.
3. **The source named beside a fact must contain that fact**, in the place you name.
4. **No "first", "oldest", "only", "best known", "most", "usually", "often", "always"** unless a source says exactly that. "First" and "not in X" claims get their own search, and are written as "the oldest mention we found".
5. **Never write a fact from memory**, and never from one uncited line in an encyclopedia. Re-read every number in the source on the day.
6. **When sources disagree, or there is only one, say so in the text.** A company website is not an official record; a publisher's blurb is not a scholar; a commentary is not the text it comments on.
7. **Every section opens with one bold sentence that answers its heading on its own**, with the subject named. FAQ answers and key-fact rows read correctly when lifted out, and carry the same caveats as the body.
8. **Explain every specialist or foreign term the first time.** Plain language a 15-year-old can follow.
9. **Describe the site's own product in the site's own words**, read fresh each time. Claim no link you cannot show.
10. **Every fix is checked against the source too.** Fixes, including a reviewer's suggested wording, introduce new errors.

## The council in one paragraph

Each round, the chair (you) convenes **fresh** reviewers who have not seen earlier rounds (in Claude Code, one subagent per role): a **Source Auditor** that checks every ledger row against its source and returns a verdict per claim; a **Skeptic** that searches outside the listed sources to disprove the most surprising claims; an **Editor** that scores search fit, citability, readability and structure; and a **Profile Checker** for the site's own rules. The chair verifies every reported defect against the source before fixing it, rejects false alarms with a reason, logs everything, and convenes a new council. Any claim CONTRADICTED, NOT FOUND or unsourced, and any misquote, fails the article whatever its score; a hard-gate finding can be overruled only by quoting the source's own line, and every overrule is shown to the user. Details, prompts and the adjudication rules: `references/council.md`.

## Files

| Path | What |
|---|---|
| `references/sop.md` | The full method, the mistake catalogue, the data step, images, after-publishing |
| `references/council.md` | Roles, independence rules, the claims ledger, adjudication, gates, stop rule, cost control |
| `references/rubric.md` | The 10-point rubric with hard gates |
| `references/prompts/` | Ready prompts for each council role |
| `templates/` | Site profile, claims ledger (headers only), article outline, fact-check log |
| `scripts/check_quotes.py` | Checks each ledger quote word for word against the raw source page |
| `scripts/verify_live.py` | Checks a published page: status, title, description, canonical, headings, links, images, structured data, sitemap |
| `examples/` | `worked-example.md` (errors the council caught, with public sources) and a filled `claims-ledger-example.csv` |
