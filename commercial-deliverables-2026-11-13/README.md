# Commercial Department — Outstanding Projects & Deliverables

Weekly management status deck for the register as at **13 November 2026**.

Previous weeks: [`../commercial-deliverables-2026-11-06/`](../commercial-deliverables-2026-11-06/) ·
[`../commercial-deliverables-2026-09-25/`](../commercial-deliverables-2026-09-25/) ·
[`../commercial-deliverables-2026-09-18/`](../commercial-deliverables-2026-09-18/)

## Deliverable

`Commercial_Department_Deliverables_2026-11-13.pptx` — 9 slides, speaker notes throughout.

| # | Slide | Visual |
|---|-------|--------|
| 1 | Title | Headline KPI tiles |
| 2 | Executive summary | Stat tiles + three ranked takeaways |
| 3 | Where the 23 deliverables stand | Doughnut + progress-against-plan bars |
| 4 | What moved since 6 November | Week-on-week bars for every item open a week ago |
| 5 | 17 deliverables finished | 10 project cards, amber dot for awaiting review |
| 6 | 6 open deliverables, 5 due today | Progress bars with planned markers |
| 7 | Priority Insurance deep dive | Item bars + four-report blocker history |
| 8 | Blockers and decisions required | Three escalation cards |
| 9 | Workload across the team | Stacked bar, finished vs still open |

## Headline numbers

| Measure | Value |
|---|---|
| Deliverables | 23 (22 distinct, see below) |
| Active projects | 10 |
| Delivered | 17 (74%) |
| On plan but incomplete | 2 |
| Behind plan | 4 |
| Open and due today | 5 of 6 |
| Actual progress | 90.6% |
| Planned progress | 93.9% |
| Variance | −3.3 points, 0.75 of a deliverable |

Variance reconciles two ways: `21.6 − 20.85 = 0.75` from the column totals, and
`0.30 + 0.20 + 0.15 + 0.10 = 0.75` from the four behind-plan rows.

## What moved in the week

| Deliverable | 6 Nov | 13 Nov |
|---|---|---|
| Priority Insurance — preliminaries budget | 50% | 70% |
| Priority Insurance — Complete BoQ | 50% | 50% |
| Priority Insurance — Complete Budget | 10% | 10% |
| Barry Callebaut Factory — Valuation | 90% | 90% |

Four deliverables were open a week ago and one of them moved. Four new items came
onto the register and two closed off it.

## Priority Insurance, eight weeks on

| Report | Complete BoQ | Due | Remark |
|---|---|---|---|
| 18 Sep 2026 | 40% | 30 Sep | Awaiting floor finishes schedule and structural drawings |
| 25 Sep 2026 | 40% | 30 Sep | No movement in seven days |
| 6 Nov 2026 | 50% | 13 Nov | Deadline re-based; structural drawings still outstanding |
| 13 Nov 2026 | 50% | **today** | Re-based deadline reached, drawings still not received |

The take-off has read 90% complete at all four reports. The deck's ask has
changed accordingly: it now seeks approval to price the structural element
provisionally rather than another issue date.

## Rebuilding

```
python3 build/v.py source/*.xlsx        # extract + reconcile every figure
npm install pptxgenjs && node build/deck.js
```

## Notes on the source data

- **The workbook holds three sheets**, two of them hidden and dated 2 and 9
  October. Only `13-11-2026` was used. The skill's parser was fixed this week to
  prefer the visible sheet with the latest report date and to print which sheet it
  read, because taking sheet zero silently read the 2 October week.
- **Rows 21 and 22 are an exact duplicate**: RE Villa, Budgetary Report, same date,
  same planned and actual, same owner. Counts in the deck follow the register as
  issued (23 deliverables, 17 delivered); the distinct totals are 22 and 16. Worth
  deleting one row at source.
- The Priority Insurance remark is merged across rows 8 to 10. "Awaiting Review"
  applies to 2 deliverables, the same two as last week.
- Dates read as day/month/year. All items fall due 13 November except two RE Villa
  items due 16 November.
- Project and client names are reproduced as spelled in the register, including
  "Goldfied".

Built with the [`commercial-status-deck`](../skill/) skill.
