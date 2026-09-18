# Commercial Department — Outstanding Projects & Deliverables

Management status deck for the commercial deliverables register as at **18 September 2026**,
prepared for presentation by the Commercial Manager.

## Deliverable

`Commercial_Department_Deliverables_Sep2026.pptx` — 9 slides, speaker notes on every slide.

| # | Slide | Visual |
|---|-------|--------|
| 1 | Title | Headline KPI tiles |
| 2 | Executive summary | Stat tiles + three ranked takeaways |
| 3 | Where the 22 deliverables stand | Doughnut + progress-against-plan bars |
| 4 | Where the portfolio is behind | Planned vs actual bar chart (3 projects with variance) |
| 5 | 18 deliverables signed off | 4×3 project cards |
| 6 | 4 outstanding deliverables | Per-row progress bars with planned markers |
| 7 | The next three weeks | Deadline runway timeline |
| 8 | Blockers and decisions required | Three escalation cards |
| 9 | Workload across the team | Stacked bar, delivered vs outstanding |

## Headline numbers

| Measure | Value |
|---|---|
| Deliverables tracked | 22 |
| Active projects | 13 |
| Delivered | 18 (82%) |
| Outstanding | 4 (3 in progress, 1 not started) |
| Actual progress | 86.4% |
| Planned progress | 93.2% |
| Variance | −6.8 points, one and a half deliverables |

## Rebuilding

```
npm install pptxgenjs
node build/deck.js
```

`build/analyze.py` recomputes the rollups from the source workbook (needs `openpyxl`).

## Revision history

- **18 Sep 2026, rev 2** — Ecole International School "BoQ and Budget" actual raised from
  50% to 100% in the register, which is the only cell that changed. Every dependent figure,
  chart, card and speaker note was recalculated. Ecole moved from the watch list to the
  completed grid, the 18 September milestone became a bare "today" anchor on the timeline,
  and Tracy and Eunice are now fully closed out.
- The closing "Next Steps" slide was removed from the reviewed copy. Its code is retained
  in `build/deck.js` behind `INCLUDE_NEXT_STEPS`; set that flag to `true` to restore it,
  and it will build with the current figures.

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
