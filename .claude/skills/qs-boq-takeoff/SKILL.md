---
name: qs-boq-takeoff
description: Professional Quantity Surveyor workflow for building projects from PDF drawings to a priced Excel BOQ. Use when given structural/architectural drawings (PDF or zip) and asked for a reinforcement take-off (bar bending schedules -> tonnes, floor by floor, totals by bar size), concrete/formwork/blockwork/finishes/doors/windows quantities, verifying or correcting an existing (lump) BOQ, re-presenting quantities floor by floor in a client's BOQ template, pricing it (e.g. Ghana cedis) with linked rates, adding a take-off/dimension sheet linked to the BOQ quantity column, or reporting gross floor area. Triggers - "reinforcement take-off", "BBS", "bar schedule", "verify the BOQ", "floor by floor BOQ", "price the BOQ", "link the rates", "take-off sheet", "dimension sheet", "total floor area", "GFA", "SMM7".
---

# QS take-off -> verified, priced, floor-by-floor BOQ

Built from the Kaneshie Block N job (12-storey RC frame, Accra): 108 structural sheets + architectural set ->
reinforcement take-off (1,306 t), verified lump BOQ, priced floor-by-floor BOQ in the client's format (GHS),
and a TAKEOFF dimension sheet linked into the client's own edited workbook.
Worked scripts for every stage are in `examples/kaneshie/` - adapt them, do not run them blind.

## Golden rules (apply to every stage)

1. **Every quantity is a formula, never a typed number.** The QTY cell (or the take-off line it reads) must
   show the arithmetic (`=22.05*3.05*0.25+25.57*3.05*0.25`), so a checker can audit it.
2. **Show your source.** Each line says where it came from: drawing number, bar mark, gridline, floor, element.
3. **Floor allocation rule:** columns/walls/stair flights between level X and the level above are measured
   under level X; starters from raft to ground under Substructure. State the rule in the notes sheet.
4. **Units are not all m / m2 / m3 / t** (SMM7R): doors/windows/ironmongery `nr`, hinges `pr`,
   provisional sums `item`, edges/strips not exceeding 250 mm wide in `m`, steel in `t`.
5. **Never alter a client template's format.** If the client sends a workbook, edit it at XML level
   (`scripts/takeoff_sheet.py` shows how) - openpyxl round-trips drop images, duotone effects,
   web-extensions and calcChain. Change only the cells you were asked to change.
6. **Verify by recalculation, not by eye.** `scripts/recalc_check.py` recalculates the whole book with zero
   errors required; reconcile totals against the previous version (same grand total unless quantities changed).
7. **Ambiguities go to an RFI list,** not silent assumptions: record the assumption, measure it, and flag it
   in the notes / remarks column (e.g. fill 2,700 vs 1,700 on two drawings).

## Workflow

Do the stages the user asks for; each later stage reuses the earlier outputs.

### 1. Read the drawing set
- Unzip, list sheets: title-block text with PyMuPDF (`page.get_text()`); private-use fonts decode with
  `chr(ord(c)-0xF000)`. Build a register (sheet no, title, level) before measuring anything.
- Scale from gridlines: find two gridline bubbles a known distance apart (dimension strings) and
  calibrate mm/pt per page in x and y separately.

### 2. Reinforcement take-off (see `references/reinforcement.md`)
- BBS numbers are often vector strokes, not text: render tiles at ~230 dpi and OCR (RapidOCR), parse rows
  (mark, dia, no. of members, bars per member, cut length), then **overlay the parsed values on the image
  and check visually**; keep a fixes table for OCR errors.
- Tonnes = members x bars x cut length x d^2/162 / 1000 - write that as Excel formulas per line.
- Workbook: Notes & Assumptions, Summary, Element x Size by Floor, one sheet per floor (F00 Substructure ...),
  checks (e.g. column schedule cross-check), BBS register. Every floor sheet ends with totals by element
  **and by bar size**, plus an all-floors size matrix.

### 3. Measure concrete, formwork, masonry and finishes (see `references/measurement.md`)
- Slabs: raster area of the slab fill (grey-pixel mask, open/close, components > threshold) calibrated on
  gridlines; edges = perimeter. Beams: pair dashed (hidden) lines with parallel lines at beam-width spacing.
- Columns/walls: schedule x storey height less slab (h - 0.25); SWC L-shapes as (a*t + b*t).
- Architecture: wall bands -> skeleton length, classify by band thickness (150 / 200 / RC);
  rooms by segmentation with door bridging, finishes by room label keywords with hatch-colour fallback.
- Doors/windows: schedules give totals - if plans are not tagged, allocate per floor by largest remainder
  pro-rata to habitable/wet area, and say so. Totals must equal the schedules.

### 4. Verify a client BOQ (lump or otherwise)
- Insert a **Verified Qty** column next to Qty (and a Verified Unit column), keep the original Qty for
  comparison, recompute Amount from the verified qty, add a Remarks column.
- Corrected descriptions go into the description cell (prefix "VERIFIED:"/keep original wording otherwise).
- Missing items are added as new yellow rows; put every calc on a "Verification Take-off" sheet with
  formulas, and a "Verification Notes" sheet summarising the big variances and RFIs.

### 5. Floor-by-floor priced BOQ in the client's format
- Load the client template, keep its styles (font, column layout, bill-summary per element, collections),
  write one bill per floor from Substructure to the top floor, using the client's/verified descriptions.
- **RATES sheet**: one row per distinct rate; every rate cell in every bill is `=RATES!$D$n`, so like rates
  change everywhere at once; GEN SUMMARY links to each bill total; levies as `=subtotal*rate`.
- Fix template bugs you find (e.g. SUM ranges that skip floors), strip stale defined names / external links.
- Recalculate, then inject cached values (`scripts/inject_cached_values.py`) so previews show numbers.

### 6. Take-off (dimension) sheet linked to the QTY column
```
python scripts/takeoff_sheet.py CLIENT.xlsx OUT.xlsx [--labels labels.json] [--sheets "A,B"]
```
- Splits each QTY formula into Times | Dim1 | Dim2 | Dim3 rows (`=PRODUCT`), distributes collections,
  Ddt lines negative, "Total carried to BOQ" per item; bill QTY cells become `=TAKEOFF!$H$n`.
- Aborts if any take-off total differs from the original quantity. Existing sheets stay byte-identical
  except the QTY formulas; calcChain removed and fullCalcOnLoad set.
- Give it `labels.json` for meaningful dimension descriptions (floor, element, bar mark, door type) -
  see `examples/kaneshie/lab.py` + `tk.py` for generating labels from the measurement engine.

### 7. Floor areas
- GFA = ground floor + every suspended floor slab area (gross, incl. balconies/terraces, excl. voids);
  roofs and lift-core roof excluded. State the basis of the ground floor (raft/building footprint vs
  measured finished floor) - they can differ a lot. Net finished area = sum of finish areas.
  See `references/measurement.md`.

## Deliverables checklist
- [ ] Every quantity traceable to a formula and a drawing reference
- [ ] Recalc: 0 formula errors; grand total reconciled with the previous issue
- [ ] Units per SMM7R (nr / pr / item / m for <=250 mm)
- [ ] Notes & assumptions + RFI list
- [ ] Files committed and pushed; tell the user what changed, the totals, and open assumptions

## Files
- `scripts/takeoff_sheet.py` - generic TAKEOFF sheet builder + XML-level linking (tested on a 15-bill, 982-item BOQ)
- `scripts/recalc_check.py` - recalc any xlsx with the `formulas` library, report errors / cell values
- `scripts/inject_cached_values.py` - write recalculated values into openpyxl-built files
- `references/reinforcement.md` - BBS extraction, unit masses, workbook layout, checks
- `references/measurement.md` - concrete/formwork/masonry/finishes rules, raster measuring, GFA
- `references/boq-and-pricing.md` - verify-BOQ layout, client template, RATES linking, lessons learned
- `examples/kaneshie/` - the full project pipeline (see its README)
