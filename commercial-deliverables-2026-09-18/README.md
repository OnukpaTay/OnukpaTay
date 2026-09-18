# Commercial Department — Outstanding Projects & Deliverables

Management status deck for the commercial deliverables register as at **18 September 2026**,
prepared for presentation by the Commercial Manager.

## Deliverable

`Commercial_Department_Deliverables_Sep2026.pptx` — 10 slides, speaker notes on every slide.

| # | Slide | Visual |
|---|-------|--------|
| 1 | Title | Headline KPI tiles |
| 2 | Executive summary | Stat tiles + three ranked takeaways |
| 3 | Where the 22 deliverables stand | Doughnut + progress-against-plan bars |
| 4 | Where the portfolio is behind | Planned vs actual bar chart (4 projects with variance) |
| 5 | 17 deliverables signed off | 3×3 project cards |
| 6 | 5 outstanding deliverables | Per-row progress bars with planned markers |
| 7 | The next three weeks | Deadline runway timeline |
| 8 | Blockers and decisions required | Three escalation cards |
| 9 | Workload across the team | Stacked bar, delivered vs outstanding |
| 10 | Closing the nine-point gap | Numbered actions with owners and dates |

## Headline numbers

| Measure | Value |
|---|---|
| Deliverables tracked | 22 |
| Active projects | 13 |
| Delivered | 17 (77%) |
| Outstanding | 5 (4 in progress, 1 not started) |
| Actual progress | 84.1% |
| Planned progress | 93.2% |
| Variance | −9.1 points, about two deliverables |

## Rebuilding

```
npm install pptxgenjs
node build/deck.js
```

`build/analyze.py` recomputes the rollups from the source workbook (needs `openpyxl`).

## Notes on the source data

- The register mixes stored date values with text dates, and mixes `dd/mm/yyyy` with
  `mm-dd-yy` cell formats. Dates are read throughout as day/month/year, which is the
  convention the text entries use.
- Three completed items (Vanguard Assurance ×2, Barry Callebaut) are stored as
  9 November 2026 but were entered as 11/09 and are read as 11 September 2026.
  No due date shown in the deck depends on this.
- Deliverable names were lightly corrected for spelling.
- Shared deliverables count once for each named owner, so the workload totals (28)
  exceed the 22 items on the register.
