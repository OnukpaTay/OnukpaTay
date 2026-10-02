# Design system

Canvas is `LAYOUT_WIDE`, 13.333 × 7.5 inches. Set `pres.layout` **before** adding
any slide — coordinates past the edge are written, not clamped, so a shape simply
vanishes.

## Palette

Hex values carry no `#` and no alpha. Both corrupt the file.

| Role | Hex | Used for |
|---|---|---|
| Navy | `1B2A41` | dark slide backgrounds, titles, big numbers |
| Ink | `0B0B0B` / `52514E` | body text, secondary text |
| Muted | `898781` | captions, axis labels, footnotes |
| Panel | `F2F5F8` | tinted cards |
| Track | `E3E9F0` | progress bar troughs |
| Hairline | `E1E0D9` | card borders, gridlines |
| Amber | `E08A3C` | accent on dark slides only |
| Ice | `AFC1D6` | secondary text on dark slides |

**Chart series** use one validated categorical pair: blue `2A78D6` and orange
`EB6834`. They clear colourblind separation and 3:1 contrast on white. Use blue
for the current or actual value and orange for the plan or prior value.

**Status colours are reserved** and never used as a series: good `0CA30C`,
warning `FAB219`, serious `EC835A`, critical `D03B3B`. Amber and serious are
below 3:1 on white by design, so they always ship with a visible label beside
them, never carrying meaning by colour alone. On an amber fill put navy text,
not white.

Do not invent extra series colours. If a chart needs more than two, it is
probably two charts.

## Typography

Cambria for titles, headline numbers and project names. Calibri for everything
else. Both ship with Office and render true-to-width in LibreOffice, so the
visual QA preview can be trusted on overflow. Avoid Aptos and Georgia: their
substitutes have different widths, so the preview lies about fit.

| Element | Size |
|---|---|
| Slide title | 31pt bold Cambria |
| Eyebrow above title | 10.5pt bold, blue, letterspaced |
| Headline number | 40–46pt bold Cambria |
| Card title | 11.5–15pt bold |
| Body | 10–11pt |
| Micro-label (OWNER, DUE) | 8pt bold, muted, letterspaced |
| Footnote | 8.5–9pt muted |

## Layout

Margin 0.62in each side, so content width is 12.093in. Content starts at y 1.54
without a subtitle, 1.86 with one, and stops at 6.58. The footer sits at 6.95.

Cards are rounded rectangles, radius 0.10, with a hairline border and a soft
shadow, or a flat `F2F5F8` fill with no border. Keep 0.2–0.3in between cards.
Repeat one motif across the deck — here, rounded cards with a small coloured
circular badge — rather than decorating each slide differently.

Avoid accent stripes, bars under titles and single-edge borders. They read as
filler. Use whitespace, a tint or a badge instead.

## pptxgenjs traps

These each cost a render cycle to find.

**`line: { width: 0 }` draws a visible line.** It emits `<a:ln w="12700">` with a
solid `333333` stroke, so every "borderless" shape gets a 1pt dark outline. Use
`line: { type: 'none' }`. This is the single most common cause of a deck looking
subtly dirty.

**Option objects are mutated in place.** pptxgenjs converts values to EMU on
first use, so a shared `shadow` or options object silently corrupts the second
shape that uses it. Build a fresh object per call — a small factory function is
the easy fix.

**Stacked bars reject `dataLabelPosition: 'outEnd'`** and corrupt the file. Use
`ctr`, `inEnd` or `inBase`.

**Zero labels clutter stacked bars.** Hide them with
`dataLabelFormatCode: '0;;;'` rather than passing nulls.

**`outEnd` labels clip at the axis maximum.** A series reaching 100 against
`valAxisMaxVal: 100` has nowhere to put its label. Set the max about 12% above
the data.

**Data labels on coloured fills should be navy**, not white. Navy clears 4:1 on
the status green and 7:1 on the amber; white fails on both.

**`rectRadius` only applies to `ROUNDED_RECTANGLE`.** On a plain rectangle it is
ignored.

**Shadow offsets must be ≥ 0.** A negative offset corrupts the file; to throw a
shadow upward use `angle: 270` with a positive offset.

**`charSpacing`, not `letterSpacing`.** The latter is silently ignored.

**Every `addText` needs `isTextBox: true`**, or screen readers announce the text
as a graphic. Set `margin: 0` whenever text must align with a shape at the same x.

**Gradients are unsupported.** Use a flat fill or a background image.

**Charts render bare by default.** Always set `chartColors`, label colours, font
faces, `valGridLine`, `catGridLine: { style: 'none' }` and turn off the legend
for a single series.

**Speaker notes go in `slide.addNotes()`**, never a text box on the slide.

## Chart defaults that read well

```js
showTitle: false,                        // the slide title already says it
showLegend: true, legendPos: 't',        // omit entirely for one series
showValue: true, dataLabelPosition: 'outEnd',
dataLabelFormatCode: '0"%"',
valGridLine: { color: 'E1E0D9', size: 1 },
catGridLine: { style: 'none' },
catAxisLabelFontFace: 'Calibri', valAxisLabelFontFace: 'Calibri',
dataLabelFontFace: 'Calibri', legendFontFace: 'Calibri'
```

For a doughnut, turn labels and legend off entirely and put the counts in a
high-contrast list beside it. Labels on thin coloured segments are unreadable at
any size, and a list doubles as the legend.
