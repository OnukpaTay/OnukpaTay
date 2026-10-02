# Reinforcement take-off from bar bending schedules

## Extracting the BBS
- Tables drawn as vector strokes have no text layer. Render each sheet in overlapping tiles
  (230 dpi, 1500 px tiles, 200 px overlap) and OCR with RapidOCR (`rapidocr_onnxruntime`); de-duplicate tokens
  within ~15 px. One tile file **per job** if OCR runs in parallel (shared tile names corrupt results);
  save per page (`ocrp_<page>.json`) so long runs are resumable.
- Parse rows by bar mark pattern (`(10|12|16|20|25|32)\d{2}`, optional `Y` prefix), then the numbers to its right
  on the same baseline: members, bars per member, cut length. Normalise OCR confusions
  (O->0, S->5, l/I->1, B->8, Z->2).
- **Overlay check**: draw the parsed values back onto the rendered sheet (`overlay.py`) and inspect at
  readable zoom (small targeted crops - large contact sheets hit image size limits). Record every
  correction in a fixes table (`fixes.py`) with the sheet and mark.
- Column schedules: parse separately (`colparse.py`) and cross-check counts/heights against the plans
  (a "Column Check" sheet). Unknown storey labels -> resolve before allocating (e.g. '??' -> EIGHT).

## Calculation per line (all as Excel formulas)
| Col | Content |
|---|---|
| Members | number of identical members (floors x elements) |
| Bars/member | from BBS |
| Total bars | = members x bars |
| Cut length (m) | from BBS (includes laps/bends as scheduled) |
| Total length | = total bars x cut length |
| kg/m | = d^2/162  (Y10 0.617, Y12 0.888, Y16 1.580, Y20 2.469, Y25 3.858, Y32 6.321) |
| kg | = length x kg/m |
| t | = kg/1000 |

## Workbook layout
- Notes & Assumptions (method, levels, allocation rule, typical-floor repetition, exclusions)
- Summary (floors x elements, t) and Element x Size by Floor (bar-size matrix per floor + all floors)
- One sheet per level F00 Substructure ... top; each ends with **totals by element and by bar size**
- Column Check, BBS Register (sheet, mark, dia, nos, length, source)
- Typical floors: measure the typical schedule on each floor it applies to (state which floors).
  Stair BBS are usually per storey; count storeys per stair (main and emergency separately).

## Checks
- t/m3 of concrete per element in a sensible range (slabs ~0.08-0.12, columns 0.15-0.35, raft ~0.1).
- Sum of floor sheets = summary = size matrix total.
