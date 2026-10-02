# Kaneshie Block N - worked pipeline (project-specific)

These scripts produced the four workbooks in the repo root. They hard-code page numbers, gridline
dimensions, file names (`docs/Documents.pdf`, `arch/…`) and project data - copy and adapt, do not run as-is.

| Stage | Scripts | Output |
|---|---|---|
| BBS OCR + parse + visual check | `ocrall.py`, `parse.py`, `overlay.py`, `fixes.py`, `data.py` | parsed bar rows |
| Column schedule | `colparse.py` | `cols_final.json`, `colheights.json` |
| Reinforcement workbook | `build.py`, `build2.py` | `Kaneshie_Block_N_Reinforcement_Takeoff.xlsx` |
| Grid calibration, slab areas | `grid.py`, `slabarea.py` | slab areas / masks |
| Beam lengths | `beams.py`, `beams2.py` | beam runs per width |
| Arch walls | `arcs.py` (scale), `walls.py`, `wallrun.py` | `walls.json` |
| Rooms / finishes | `rooms2.py`, `rooms3.py`, `runfin.py` | `finishes.json` |
| Quantity engine (per floor terms) | `qty.py` | `Q[sheet][key]` formula terms, door/window allocation |
| Verified lump BOQ | `vboq.py` | `KANESHIE_BLOCK_N_BOQ_rev1_VERIFIED.xlsx` |
| Priced floor-by-floor BOQ | `pboq.py` | `BOQ_KANESHIE_BLOCK_N_PRICED_FLOOR_BY_FLOOR.xlsx` |
| Labelled TAKEOFF into client's book | `lab.py` (labels from qty.py), `tk.py` (rows), `tkxml.py` (XML) | `BOQ_KANESHIE_BLOCK_N_WITH_TAKEOFF.xlsx` |

Generic versions: `../../scripts/takeoff_sheet.py`, `recalc_check.py`, `inject_cached_values.py`.
