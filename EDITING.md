# Editing the Bible

Everything on the site comes from the Markdown files in `content/`. Edit a file, commit, and the site rebuilds about a minute later. The quickest way in is the **Edit this page** button at the bottom of any page.

## How pages are organised

```
content/
  _home.md                  home page
  0-start/                  one folder per Part (the tabs on the left)
    _part.md                the Part's tab, name and colour, plus its overview text
    01-how-to-use-this.md   one file per page
  1-system/ … 5-appendices/
```

- **Order** follows the file names, so the number at the front matters: `03-…` comes before `04-…`. Rename a file to move it.
- **A new page** is a new `.md` file in a Part's folder. It appears in that Part's list automatically.
- **Removing a page** means deleting its file. Links that pointed to it show up as warnings in the build log.
- **A new Part** is a new folder, such as `6-mock-oas/`, containing a `_part.md` (see [Parts](#parts) below).

## The top of every page

```markdown
---
numeral: Card 13
title: Segment Trees — range queries in log n
---
```

- **title** is the page name. Anything after ` — ` (a spaced em dash) becomes the grey subtitle.
- **numeral** is the page's identity, and it's also how references find it. Use these forms:

| numeral | used for | example link it makes work |
| --- | --- | --- |
| `§14` | a chapter | "see §14" or "§14.3" (its `14.3` section) |
| `Card 7` | a pattern card | "Card 7", "Cards 3 + 7" |
| `Appendix L` | an appendix | "Appendix L" |
| `Part V` | a Part overview (in `_part.md`) | "Part V" |

Optional lines:

- `id: card-3` fixes the page's web address. Existing pages have one, so bookmarks keep working. New pages get an address from the file name.
- `card: 13` makes "Card 13" in the text point to this page, even though it isn't a card. §12 Trees uses this.
- `tracker: true` turns the page's anchor tables into the interactive log (Appendix C).

## Writing

| You write | You get |
| --- | --- |
| `## Heading` and `### Smaller heading` | a section, listed in "On this page" |
| `## 14.3 Template D1 — 1D linear DP` | numbered and template headings get stable addresses, like `14-3` and `t-1a` |
| `**bold**`, `*italic*`, `` `code` `` | the usual |
| a paragraph wrapped in `*…*` | a note: indented, italic commentary (as under the templates) |
| `- item` or `1. item` | a list |
| `[ZERO]{.red}`, `[Probably]{.green}`, `[Coin flip]{.amber}` | a verdict colour |
| `[the stuck protocol](§9)` | a link to any numeral: `§7.3`, `Card 10`, `Appendix J`, `Part II` |
| `[LeetCode 307](https://leetcode.com/…)` | an outside link, which opens in a new tab |
| `<br>` inside a table cell | a line break |
| `\*`, `\|` | a literal `*`, or a `|` inside a table |

You don't need to link references by hand. Any "§7.2", "Card 11", "Appendix C", "Part III", "Shape A", "Template 6B", "G6" or "D3" in normal text becomes a link on its own, as long as the target exists.

## Callouts

```markdown
> [!NOTE]
> **Optional title in bold on the first line**
>
> Body text. Separate paragraphs with a line containing only >.
```

| Marker | Colour | Used in the Bible for |
| --- | --- | --- |
| `[!NOTE]` or `[!IMPORTANT]` | blue | guidance, "how to run a card" |
| `[!TIP]` | green | what to do, what to print |
| `[!WARNING]` or `[!CAUTION]` | red | warnings, deadlines |
| no marker, just `>` | grey | rules and boundaries |

## Code and special blocks

````markdown
```java
int lo = 0, hi = n;            // blurred in Cover mode until revealed
```

```java idiom
map.getOrDefault(k, 0)         // Java reference, never blurred
```

```python
def f(x): ...                  // any language works; add "cover" to blur it: ```python cover
```

```text Example log entry
[2026-09-05]  Triplet Sum to Zero  |  FAILED cold (18 min)
```
````

A `text` block is shown as-is in monospace. Anything after `text` becomes its caption.

These blocks turn into components:

| Block | Where it's used | Line format |
| --- | --- | --- |
| ` ```rules ` | Appendix K | `1. Short rule. Longer explanation.` (the first sentence is bolded) |
| ` ```decision-tree ` | Appendix E | a question ending in `?`, then branches like `  \|- cue ....... Pattern   (Card 2)` |
| ` ```log Caption ` | Appendix I | `KEY` followed by two or more spaces, then the value |
| ` ```talk-track ` | §10.3 | `"what you say"   [what you do]` |

## Tables with special behaviour

These are ordinary Markdown tables. The build recognises them by their column headings.

- **The first table on a page, with one row**, becomes the status strip under the title (Status, Your coverage, Current level, Target).
- **`# | Anchor | Why this one`** gets a **Log today** column. The anchor name must match a row in Appendix C.
- **In Appendix C** (`tracker: true`), tables with `#`, `Pattern` and `Anchor problem` columns become the log. To add an anchor, add a row with a new number. Numbers are how dates are stored, so don't renumber existing rows. A table with an `Activate when` column becomes the "later" group.
- **`Problem | Status | P | Note`** gets coloured chips and the filter bar (Appendix D). P values are `A`, `1`, `2`, `3` and `×`. Status values are `Revised`, `Solved` and `Not started`.
- **`Card | Pattern | Your state | Priority`** (Part II overview) links each pattern, and it feeds the home-page pattern board. Update `9/12 · L2` there and the tallies follow.
- **`§ | Topic | …`** (Part III overview) links each topic.

## The home page

`content/_home.md` works the same way:

- The front-matter `title` is split into two lines at `|`.
- The table under a heading becomes the "Where are you today?" rows. The last column holds the buttons, written as `[Label](§7.1)`.
- A list of links becomes the "Keep these three close" cards.
- `{{pattern-board}}` and `{{anchor-summary}}` place those two components. Move or delete those lines to rearrange the page.

## Parts

`_part.md` sets up a Part:

```markdown
---
key: V
tab: V
label: Mocks
title: Mock OAs
color: teal
numeral: Part V
---

Optional overview text. If there's text here, the Part gets an overview page.
```

`color` can be `slate`, `ochre`, `blue`, `green`, `brick`, `violet`, `teal` or `rose`. The folder's number prefix sets the tab order.

## If something looks wrong

Open the **Actions** tab on GitHub and click the latest run. The build lists a warning for every link or reference it couldn't resolve, along with the file it's in. A failed run leaves the previous version of the site online, so nothing breaks while you fix it.
