# Commercial Department — Outstanding Projects & Deliverables

Weekly management status deck for the register as at **6 November 2026**,
prepared for presentation by the Commercial Manager.

Previous weeks: [`../commercial-deliverables-2026-09-25/`](../commercial-deliverables-2026-09-25/) ·
[`../commercial-deliverables-2026-09-18/`](../commercial-deliverables-2026-09-18/)

## Deliverable

`Commercial_Department_Deliverables_2026-11-06.pptx` — 8 slides, speaker notes on every slide.

| # | Slide | Visual |
|---|-------|--------|
| 1 | Title | Headline KPI tiles |
| 2 | Executive summary | Stat tiles + three ranked takeaways |
| 3 | Where the 20 deliverables stand | Doughnut + progress-against-plan bars |
| 4 | 16 deliverables finished | 11 project cards, amber dot for awaiting review |
| 5 | 4 deliverables still open | Progress bars with planned markers |
| 6 | Priority Insurance deep dive | Item bars + three-report blocker history |
| 7 | Blockers and decisions required | Three escalation cards |
| 8 | Workload across the team | Stacked bar, finished vs still open |

## Headline numbers

| Measure | Value |
|---|---|
| Deliverables | 20 |
| Active projects | 11 |
| Delivered | 16 (80%) |
| On plan but incomplete | 2 |
| Behind plan | 2 |
| Actual progress | 90.0% |
| Planned progress | 93.0% |
| Variance | −3.0 points, 0.6 of a deliverable |

Variance reconciles two ways: `18.6 − 18.0 = 0.6` from the column totals, and
`0.5 + 0.1 = 0.6` from the two behind-plan rows.

## The one open issue

Priority Insurance has been waiting on structural drawings since 18 September.

| Report | Complete BoQ | Due | Remark |
|---|---|---|---|
| 18 Sep 2026 | 40% | 30 Sep | Awaiting floor finishes schedule and structural drawings |
| 25 Sep 2026 | 40% | 30 Sep | No movement in seven days |
| 6 Nov 2026 | 50% | 13 Nov | Structural drawings still outstanding |

Ten points of progress in seven weeks, with the deadline moved out six. The item
reads as on plan only because the plan moved with it.

## Rebuilding

```
pdftotext -layout -bbox-layout source/*.pdf bbox.html
python3 build/extract.py bbox.html      # -> rows.json
python3 build/verify.py                 # reconciles every figure
npm install pptxgenjs && node build/deck.js
```

## Notes on the source data

- **The register arrived as a PDF this week**, not a spreadsheet. Merged cells
  carry no structure in a PDF, so `build/extract.py` reconstructs the merged spans
  from word coordinates: it recovers the boundaries that explain where each merged
  label is vertically centred, rather than filling values down the column. That
  matters here because the owner and remark columns are merged across project
  blocks. **Sending the .xlsx would remove this step and the risk with it.**
- The Priority Insurance remark is merged across three rows (Complete BOQ, Cash
  Flow, Complete Budget). "Awaiting Review" applies to 2 deliverables.
- Project and client names are reproduced exactly as spelled in the register,
  including "Goldfied", which was not corrected since changing a client name
  carries more risk than leaving it.
- Dates read as day/month/year. All items fall due 6 November except the three
  Priority Insurance items due 13 November.
- The register is a live snapshot: only two deliverables carried over from the
  25 September report, so portfolio percentages are not comparable between weeks.

Built with the [`commercial-status-deck`](../skill/) skill.
