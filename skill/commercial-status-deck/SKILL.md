---
name: commercial-status-deck
description: >-
  Turn a project deliverables register or status tracker spreadsheet into a
  presentable management PowerPoint deck with charts, progress bars and speaker
  notes. Use this whenever someone has a tracker of work items with planned
  versus actual progress, owners and due dates, and wants a deck, slides, a
  status report, a weekly update or a management presentation out of it — in
  construction, quantity surveying, consulting, PMO, agency or any project
  environment. Trigger it even when they only say "make this presentable",
  "turn this into slides for management", "prepare my weekly update" or attach
  a register and ask for a presentation, and also when they want to refresh an
  existing deck of this kind with a newer week of data.
---

# Commercial status deck

Turn a deliverables register into a deck a manager can actually stand up and
present. The spreadsheet is the input; a narrative with evidence is the output.

The trap with tracker data is producing a data dump: one slide per column,
every row charted, no point of view. Management does not need the register read
aloud. They need to know what moved, what is at risk, and what decision is
being asked of them. Everything below serves that.

## Workflow

1. **Read the register** (`scripts/read_register.py`). Do not eyeball the
   spreadsheet — the parsing traps in it are real and cost you correctness.
2. **Find the story** before opening a design tool. Write the three sentences
   you would say if you had thirty seconds.
3. **Build the deck** with `pptxgenjs`, starting from `scripts/deck_kit.js`.
4. **Validate and look at every slide.** Non-negotiable; see QA.

## Step 1 — Read the register

```bash
python3 scripts/read_register.py <register.xlsx>                  # one week
python3 scripts/read_register.py <new.xlsx> --compare <old.xlsx>  # week on week
```

It prints the rollups, the outstanding items, owner workload, remark flags and,
with `--compare`, the per-deliverable movement. It handles the four traps that
bite anyone parsing these files by hand:

**Merged cells.** Registers merge the project, owner and remarks columns across
a project's rows. Forward-filling blindly down a column is wrong — it carries a
value into rows the merge never covered, which silently inflates counts. Fill
only inside real merged ranges.

**Mixed date formats.** The same column routinely holds real dates and text
dates, under both `dd/mm/yyyy` and `mm-dd-yy` cell formats, because entries with
a day above 12 stay text while others get parsed in US locale. Work out the
convention from the unambiguous text entries and read everything that way.

**Impossible dates.** A finish date a year out on a row marked 100% complete is
a typo, not a plan. Read it the sensible way, say so in a footnote, and tell the
person so they can fix the source.

**Live snapshots versus cumulative registers.** Many teams delete closed rows
each week. When the row count drops sharply, the register is a live snapshot:
portfolio percentages are then **not comparable** between weeks, because the
denominator changed. Compare individual deliverables instead and say on the
slide why. Reporting "86% last week, 80% this week" as a decline when fourteen
finished items were simply removed is the worst error this skill can make.

## Step 2 — Find the story

Compute these, then decide what leads:

| Measure | How |
|---|---|
| Delivered / in progress / not started | count of actual = 1, 0 < actual < 1, actual = 0 |
| Actual progress | sum(actual) / count |
| Planned progress | sum(planned) / count |
| Variance | the gap in points, and in whole deliverables |
| Concentration | which few items hold the entire gap |
| Blockers | the remarks column, grouped |
| Workload | items per named owner, split delivered vs open |

The lead is whichever is true this period:

- **Something landed.** Items flagged critical last period completed. Lead with
  it; managers rarely hear good news from a tracker.
- **The gap is concentrated.** "Nine points behind" means little. "All of it in
  three items, two of them tenders closing Thursday" is actionable.
- **The bottleneck moved.** Work finishing but not being signed off is a
  different problem from work not being done, and needs a different decision.
- **Nothing moved.** An item unchanged across two periods is a finding in its
  own right, especially when it is blocked on someone outside the department.

Shared deliverables count once per named owner, so owner totals exceed the item
count. Say so in a footnote rather than quietly double-counting.

## Step 3 — Build the deck

Use `pptxgenjs` (`npm install pptxgenjs`). Copy `scripts/deck_kit.js` as your
preamble — it carries the tokens and the `header`, `card`, `dot`, `progress`,
`chip` and `footer` helpers, so slides stay consistent without re-deriving
geometry. `assets/example_deck.js` is a complete working deck built on it;
read it when you want a concrete pattern rather than a description.

Pick slides from these archetypes and drop any the data no longer supports.
A nine-slide deck where every slide earns its place beats a fixed template.

| Slide | Use it when | Visual |
|---|---|---|
| Title | always | dark background, four KPI tiles |
| Executive summary | always | four stat tiles, three numbered takeaways |
| Where the N deliverables stand | always | doughnut plus progress-against-plan bars |
| What changed since <last period> | you have a prior register | grouped bars, per deliverable |
| Where the portfolio is behind | 2+ projects carry variance | grouped bars, only the projects with variance |
| Delivered this period | always | project cards with counts and status chips |
| The bottleneck | a remark flag repeats across items | queue rows with age bars |
| Still open / watch list | always | rows with progress bars and planned markers |
| Blockers and decisions | always | escalation cards, each ending in one decision |
| Workload | always | stacked bar, delivered vs open |

Two rules that do most of the work:

**Never chart rows that are all identical.** Nine projects at 100% planned and
100% actual is eighteen redundant bars that bury the four that matter. Chart
the variance; summarise the rest in a stat panel ("10 projects fully
delivered").

**Every escalation card ends in a decision, not a status.** "Awaiting review"
is a status. "Nominate a reviewer for each of the five and set a clearance date
for the two already overdue" is a decision someone can make in the room.

Write speaker notes on every slide, in the voice of the person presenting, as
spoken sentences. They are what makes the deck usable by someone who did not
build it.

Read `references/design-system.md` before writing slide code — it has the
palette, typography, geometry and the `pptxgenjs` traps. Read
`references/slide-patterns.md` for the layout of each archetype.

## Step 4 — QA

```bash
node deck.js
python3 <pptx-skill>/scripts/office/validate.py deck.pptx
soffice --headless --convert-to pdf deck.pptx && pdftoppm -jpeg -r 110 deck.pdf slide
```

Then **look at every rendered slide**. This is where the real defects are, and
they are always the same four: text overflowing its card, a long title colliding
with a badge, a right-hand column running into the next, and a label wrapping to
two lines into the text below. Static checks catch none of them.

Also sweep the extracted text for figures from a previous version that should
have changed:

```bash
markitdown deck.pptx | grep -nE "<old totals, old percentages, dropped project names>"
```

When a single input number changes, it moves through counts, percentages,
chart data, card lists, chip states, footnotes and speaker notes. Trace all of
them; a deck that says 18 on one slide and 17 on another destroys trust in the
rest of it.

## Updating an existing deck

When a newer register arrives, diff it against the previous one first — often
only one or two cells changed, and knowing which saves rebuilding blind. If the
person edited the deck you produced (deleted a slide, reworded a title), build
on their version and keep the edit rather than overwriting it. If you drop a
slide for that reason, keep its code behind a flag so it can be restored, and
tell them you did.

Archive each period beside the last rather than overwriting, so the history
survives.
