# Blog Council

**A Claude skill for writing articles that are right first, and a council of independent reviewers that proves it.**

Drafts that read well are often wrong in small ways: a detail the source never says, a quote slightly changed, a "first" nobody can back, a fact credited to the wrong chapter. Those errors survive self-review, because the writer checks what they meant and not what the source says. They then get repeated by search engines and AI assistants.

Blog Council separates the writer from the people who check, and makes every check open the source.

## What it does

1. **Source-first writing.** Read the original (the chapter, statute, paper, interview), build a claims ledger with the exact supporting quote for every fact, then write in a template built to be quoted: a 60-word answer, a key facts table with sources, question headings that each open with a stand-alone answer, a FAQ and a source list.
2. **Machine checks.** A script downloads every source page, checks each ledger quote word for word, and flags any quotation in the draft that has no ledger row. Misquotes are caught before a reviewer spends time on them.
3. **The council.** Each round, fresh reviewers who have not seen earlier rounds:
   - a **Source Auditor** checks every ledger row against its cited source and gives a verdict (confirmed, partly, not found, contradicted, disputed, unsourced);
   - a **Skeptic** searches outside the article's sources to disprove the five most surprising claims, and hunts for an older source behind every "first";
   - an **Editor** scores search fit, citability, information gain, readability and structure;
   - a **Profile Checker** applies your site's own rules.
4. **Adjudication.** The chair verifies every reported defect, and every suggested fix, against the source before changing a word. False alarms are rejected with a reason; a hard-gate finding can only be overruled by quoting the source, and every overrule is shown to the user.
5. **A gate.** Any contradicted, unfound or unsourced claim, and any misquote, fails the article whatever its score. It passes after two consecutive clean rounds at or above your bar (default 9.0 of 10), with a round ceiling so it does not run forever or chase a number.
6. **After publishing.** A script checks the live page: status, title, description, canonical, H1, noindex, links, images, structured data, sitemap, and that your CMS kept every sentence of the reviewed draft.

It works with any site and any CMS. Your site's rules (byline, call to action, banned claims, sensitive topics, quality bar) go in one profile file.

## Install

Copy the folder into your Claude skills directory and name it `blog-council`.

macOS or Linux:

```bash
git clone https://github.com/ram15126/claude-blog-council.git ~/.claude/skills/blog-council
```

Windows (PowerShell):

```powershell
git clone https://github.com/ram15126/claude-blog-council.git "$env:USERPROFILE\.claude\skills\blog-council"
```

Or, for one project only, put it at `.claude/skills/blog-council/` inside the project. The scripts need Python 3.9 or later (`python --version`) and nothing else.

## Use

Ask Claude in plain words:

- "Write a blog post on why Diwali is celebrated, using the blog council."
- "Run the council on this article and score it."
- "Fact-check this draft against its sources."

Before the first article, fill in `templates/site-profile.md` and save it as `blog-council.profile.md` in your project.

Run the scripts yourself any time:

```bash
python scripts/check_quotes.py claims-ledger.csv
python scripts/verify_live.py https://example.com/blog/my-article --sitemap https://example.com/sitemap.xml
```

## Files

| Path | What |
|---|---|
| `SKILL.md` | The skill: when to use it, the order of work, the ten rules |
| `references/sop.md` | The full method and the mistake catalogue |
| `references/council.md` | Council roles, independence rules, claims ledger, adjudication, gates, stop rule, cost control |
| `references/rubric.md` | The 10-point rubric with hard gates |
| `references/prompts/` | Prompts for the Source Auditor, Skeptic, Editor, Profile Checker, and a combined reviewer for short pieces |
| `templates/` | Site profile, claims ledger, article outline, fact-check log |
| `scripts/` | `check_quotes.py`, `verify_live.py` |
| `examples/` | `worked-example.md` (real errors the council caught, each with its public source) and a filled `claims-ledger-example.csv` |

## Good to know

- **Best fit:** articles whose facts live in sources: history, mythology, religion, science, health, law, places, people, explainers. Posts built on fresh data use the optional data step in `references/sop.md`.
- **Cost:** a council round is several reviewer runs. Scripts do the deterministic checks for free, an early round can use a smaller model, and the stop rule and round ceiling end the loop. The rounds that count use the strongest model you have: in the documented run, a smaller model passed two errors the stronger one caught.
- **Independence matters.** In Claude Code each reviewer runs as its own subagent. In a chat app, run each reviewer in a new conversation. A round reviewed by the writer does not count.
- **It never publishes.** It ends at a reviewed draft and a fact-check log. Publishing is your call.
- **It does not make a weak source strong.** It makes the article say how strong its sources are.

## Licence

MIT. See `LICENSE`.
