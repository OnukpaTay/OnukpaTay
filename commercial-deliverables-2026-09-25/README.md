# Commercial Department — Outstanding Projects & Deliverables

Weekly management status deck for the commercial deliverables register as at
**25 September 2026**, prepared for presentation by the Commercial Manager.

Previous week: [`../commercial-deliverables-2026-09-18/`](../commercial-deliverables-2026-09-18/)

## Deliverable

`Commercial_Department_Deliverables_2026-09-25.pptx` — 9 slides, speaker notes on every slide.

| # | Slide | Visual |
|---|-------|--------|
| 1 | Title | Headline KPI tiles |
| 2 | Executive summary | Stat tiles + three ranked takeaways |
| 3 | Where the 8 deliverables stand | Doughnut + progress-against-plan bars |
| 4 | What changed since 18 September | Week-on-week bar chart, per deliverable |
| 5 | 6 deliverables finished | Project cards with review-status chips |
| 6 | 5 deliverables waiting on review | Queue rows with age bars |
| 7 | 2 deliverables still open | Progress bars with planned markers |
| 8 | Blockers and decisions required | Two escalation cards |
| 9 | Workload across the team | Stacked bar, finished vs still open |

## Headline numbers

| Measure | Value |
|---|---|
| Live deliverables | 8 |
| Active projects | 6 |
| Delivered | 6 (75%) |
| Awaiting review | 5 |
| Still open | 2, both Priority Insurance |
| Actual progress | 80.0% |
| Planned progress | 81.3% |
| Variance | −1.3 points, 0.1 deliverables |

## Week on week

| Deliverable | 18 Sep | 25 Sep |
|---|---|---|
| Kinbu — Priced BoQ | 10% | 100% |
| Stanbic — tender submission | 50% | 100% |
| Priority Insurance — Complete BoQ | 40% | 40% |
| Priority Insurance — Complete Budget | 0% | 0% |

## Rebuilding

```
npm install pptxgenjs
node build/deck.js
```

`build/analyze.py` recomputes the rollups and the week-on-week comparison from both
weeks' workbooks (needs `openpyxl`).

## Notes on the source data

- **The register carries live work only.** It shrank from 22 rows to 8 because 17
  closed deliverables were removed. Portfolio percentages are therefore *not*
  comparable week to week; the week-on-week slide compares individual deliverables.
- **One date reads 2027.** The Stanbic "Relevant Experience and CV" expected finish
  date is recorded as 25 September 2027. It is read throughout as 2026, matching the
  Cost Proposal it was submitted with and its 100% complete status.
- **Remarks use merged cells.** The "Awaiting Review" flag applies to 5 deliverables.
  Thoroughbred Place carries no flag and is shown as complete rather than in review.
- Stanbic was recorded last week as one "Preliminary Estimate" and this week as two
  documents, "Cost Proposal" and "Relevant Experience and CV".
- Thoroughbred Place's deliverable changed from "Financial Report (internal)" last
  week to "Financial Report (external)" this week; they are treated as separate items.
- Dates are read as day/month/year. Deliverable names lightly corrected for spelling.
- The closing "Next Steps" slide removed from the 18 September deck has not been
  reinstated; its asks appear on slide 8.
