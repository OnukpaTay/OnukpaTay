# Measurement rules and raster techniques

## Calibration
- Use two gridlines with a known overall dimension (e.g. grid 1-12 = 36,500 mm, A1-Q = 34,350 mm);
  scale x and y separately (sheets are often not exactly isotropic).

## Structural
| Item | Rule (unit) |
|---|---|
| Suspended slab | measured slab area x thickness (m3); soffit formwork = area (m2); edge formwork = perimeter (m, edge <= 250 mm) |
| Slab area | raster: render at 4x, grey-fill mask, morphological open/close, keep components > 20,000 px, crop to grid box + 3.5 m |
| Beams | downstand only: length x width x (depth below slab) (m3); formwork length x (2 x depth + width) (m2). Length from dashed-line pairs at beam-width spacing |
| Columns | nr x a x b x (storey ht - slab thk) (m3); formwork nr x 2(a+b) x ht (m2) |
| Walls (shear/lift/core) | run x (storey ht - 0.25) x 0.25 (m3); formwork 2 faces |
| Stairs | per storey: flights pro-rata storey height + landings (m3); soffits, landings and risers formwork (m2) |
| Lintels | nr x (opening width + 2 x 150 bearing) x 0.15 x 0.225 (m3); formwork girth 0.60 |
| Raft / earthworks | raft L x W x thk; excavation footprint incl. working space; backfill = footprint less raft; disposal = excavation - backfill |

## Architectural
| Item | Rule |
|---|---|
| Blockwork | wall-band skeleton length x (storey ht - slab), classified by band thickness (<=210 mm band -> 150 wall, 210-245 -> 200 wall, >245 -> RC); add walling over openings (nr x w x (3.05 - opening ht)) |
| Internal render/paint | 2 faces of block runs + RC faces - shaft inner faces - external face - washroom walls - openings (doors both faces) |
| Washrooms | nr approx = wet area / 3.8 m2; walls 8.0 m girth x ht less doors 0.75 x 2.2; tiles to 2.4 m |
| External render/paint | perimeter x storey ht - windows |
| Floor finishes | room segmentation (wall mask + 79 px door bridging, structural slab mask as footprint, eroded 25 px), class by room label keywords (WC/BATH -> wet tiles, LOBBY -> 60x120, CORRIDOR/TERRACE -> non-slip, BEDROOM/LIVING -> semi-polished, PARKING/RAMP -> PU); unlabelled rooms by hatch colour |
| Doors/windows | nr from schedule; per floor by largest-remainder allocation; frames/stops nr x (2h + w) m; hinges 1.5 pr per leaf (pr) |

Mask out non-wall black objects (tank plinths, cars) and blank text only inside the clip region
(negative slice indices blank whole strips).

## Floor areas
- **GFA (gross)** = ground floor + all suspended slab areas (gross outline incl. balconies/terraces,
  excluding voids/atria); roof slabs and lift-core roofs excluded. Kaneshie: suspended 13,187.5 m2.
- Ground floor basis must be stated: building/raft footprint (41 x 36 = 1,476 m2 -> GFA 14,663.5 m2)
  vs measured finished floor (750.4 -> 13,937.9 m2). For cost/m2 use the gross (footprint) figure.
- **Net finished area** = sum of floor-finish areas (Kaneshie ~10,209 m2).
