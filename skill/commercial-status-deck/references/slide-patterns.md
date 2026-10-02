# Slide patterns

Geometry for each archetype, in inches on the 13.333 × 7.5 canvas. `M` is the
0.62 margin, `CW` the 12.093 content width, `y0` the value returned by `header()`.
All of these assume the helpers in `scripts/deck_kit.js`.

## Title (dark)

Navy background. Three translucent circles as a motif, placed clear of the
content — a disc crossing a card looks like a mistake, not a design. Eyebrow at
y 1.52, two-line title at 1.95 in 46pt Cambria, subtitle at 3.92, a date chip at
4.52, then four KPI tiles at y 5.42, each 2.72 wide and 1.10 tall with a 0.30
gap, filled white at 90% transparency with a hairline white border.

## Executive summary

Four stat tiles across the full width, `(CW - 3×0.28) / 4` wide and 1.52 tall:
a 40pt number, a 12.5pt bold label, a 9.5pt muted sub-label, and a small status
dot in the top right.

Below them, three full-width takeaway cards, 0.94 tall with a 0.12 gap. Each
carries a numbered circular badge 0.46 across at the left, a 13pt bold headline
and a 10.5pt body. Colour the badge by severity, and order the takeaways by what
you want remembered, not by the register's row order.

## Where the N deliverables stand

Doughnut on the left at x `M`, 5.30 wide and 4.50 tall, `holeSize: 62`, legend
and value labels off. Put the total in the hole as a 40pt number with an 11pt
caption beneath.

Right column from x 6.30. Three legend rows, 0.80 tall, each a flat panel card
with a colour dot, a bold label, a muted description, a 24pt count and a
right-aligned percentage. These rows are the legend, which is why the chart
needs none.

Below them a "progress against plan" card 1.66 tall holding two drawn bars
(planned in orange, actual in blue) and a one-line verdict in status colour.
Drawn bars beat a second chart here: they are smaller, align to the card, and
carry no axis furniture.

## What changed since <last period>

Horizontal grouped bars, two series: the prior period in orange, the current in
blue. One row per deliverable carried over from the previous register, ordered
with the biggest movement at the top. Remember `data[0]` plots at the **bottom**,
so reverse the array.

Chart 8.35 wide; two stat panels stacked on the right, each 2.08 tall. Put the
caveat about live snapshots directly under the chart as a footnote, since this
is the slide where someone will try to compare the two periods' totals.

## Where the portfolio is behind

Same grouped-bar form, one row per project with variance, planned versus actual.
Only include projects that actually differ. Pair it with stat panels giving the
count fully delivered and the count behind, so the whole portfolio is still
accounted for without charting the identical rows.

## Delivered this period

A grid of project cards. Three columns when you have up to six projects, four
when more; height `(6.58 - y0 - gaps) / rows`. Each card: project name top-left,
a green circular badge with the deliverable count top-right, a bulleted list,
an optional status chip, and the owner in muted bold at the bottom.

Keep the title text box about 1.0in clear of the badge, or a long project name
runs into it. Let titles wrap to two lines and anchor them `valign: 'top'` so
every card's title starts on the same line.

## The bottleneck

One row per stuck item, ordered oldest first. Row card with a status dot, the
project and deliverable, then micro-labelled columns for owner, the relevant
date, and the waiting time, and finally a horizontal bar scaled against the
oldest item. The bar is what makes the backlog legible at a glance — a column
of numbers does not.

## Still open / watch list

Row cards, taller when there are only a few items. Each holds a status dot, the
project and deliverable, a progress bar with a dark tick marking where the item
was planned to be today, the due date, the owner and a status chip. The planned
marker is what turns "40%" into "40% against a 50% plan" without extra text.

With four or fewer rows, centre the content vertically inside the taller row and
add a full-width note card beneath explaining the cause and the ask.

## Blockers and decisions

Two or three cards across, 3.3–3.4 tall. Badge and title on the first line, the
affected projects on their own line beneath (never beside the title — a
two-line title collides with it), the explanation, then a tinted box at the
bottom headed DECISION REQUIRED holding one sentence someone can act on.

Close with a full-width navy band: "What we need from this meeting", and the
asks in one line. It is the slide the meeting should end on.

## Workload

Stacked horizontal bars, delivered in status green and open in status amber, one
row per owner, ordered by total ascending so the busiest sits at the top. Labels
centred in navy, zeros hidden. Three note cards on the right carrying the
interpretation, because a workload chart without it invites the wrong conclusion
about whoever has the fewest completed items.

Footnote that shared deliverables count once per named owner.
