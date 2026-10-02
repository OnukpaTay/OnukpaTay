# Verifying, re-formatting and pricing a BOQ

## Verifying a lump BOQ
- Columns after edit: Item | Description | Original Qty | **Verified Qty** | Unit | **Verified Unit** | Rate |
  Amount (= Rate x Verified Qty) | Remarks. Remap every summary/collection reference to the new Amount column.
- Verified quantities reference a "Verification Take-off" sheet where each line is a formula with source.
- Corrected units in red (m2 -> m for edges <= 250 mm, nr -> pr for hinges, -> item for provisional sums).
- Added items (beams missing, etc.) in yellow rows with a remark. A "Verification Notes" sheet lists major
  variances (Kaneshie: columns overstated x5, walls 667 vs 306 m3, lintels 360 -> 56 m3, beams missing
  210.7 m3 / 111 t, DW2 qty 1 not 2) and RFIs.

## Client template, floor by floor
- One bill per floor (Substructure, Ground ... top floor, plus Lifts & PS / provisional sums), each with
  a bill summary by element, page collections, and "To Bill General Summary".
- Descriptions: client / previous BOQ wording, including verified corrections.
- Quantities: dimension formulas per floor, generated from one quantity engine
  (`examples/kaneshie/qty.py` -> `Q[sheet][key] = [terms]`) so floor bills always add up to the verified BOQ.

## Pricing and linked rates
- RATES sheet: code | description | unit | rate (GHS) | basis/notes. Every bill rate cell `=RATES!$D$n`;
  identical items share one rate row. Composite rates (e.g. windows) = w x h x rate per m2.
- Preliminaries: lump sums linked to RATES; page collections `=SUM`.
- GEN SUMMARY: each bill total linked; Sub-total `=SUM(...)` over **all** bills (check templates for ranges
  that skip floors); levies/taxes `=Subtotal x %`; total.
- The client may later convert rates to `=base*factor` (e.g. `=230*F5`) - keep that structure when updating.

## Excel engineering notes
- No Excel/LibreOffice Calc in the container: recalc with `formulas` (scripts/recalc_check.py), then
  inject cached values for openpyxl-built books. Remove external links/defined names like `[31]!Name` first
  (`wb._external_links=[]`, delete defined names) or the evaluator fails.
- For the client's own saved workbook use XML edits only (see takeoff_sheet.py): read/write parts with
  `newline=''` (keeps CRLF), append styles (never renumber), add the sheet part + rel + content-type, remove
  calcChain, set `<calcPr fullCalcOnLoad="1"/>`. Confirm existing sheet XML is identical apart from `<f>`.

## Lessons learned (Kaneshie)
- Stair storey counts: count main and emergency stairs separately (23, not 22).
- Hinge pairs: round up per floor in every file so totals match (452 pr).
- Architectural levels may differ from structural (+300 mm) - use structural SSL for heights, flag RFI.
- Atrium voids leak room segmentation - use the structural slab mask as the footprint.
- Keep one engine for quantities; every workbook (verified, priced, take-off) reads from it, so they reconcile.
