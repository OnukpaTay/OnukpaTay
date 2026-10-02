# The prompt

For when you just want the deck and don't want to install anything. Paste this
into Claude and attach your register spreadsheet.

---

I'm attaching our project deliverables register. Build me a PowerPoint deck that
the department manager can present to senior management.

**The data.** Each row is a deliverable with a project, a description, an
expected finish date, a planned and an actual completion figure (0 to 1), an
owner, and sometimes a remark. Before you compute anything:

- Project, owner and remark columns use **merged cells**. Fill a value down only
  inside its real merged range, never blindly down the column, or you will
  attribute remarks and owners to rows they don't belong to.
- The date column mixes real dates with text dates and mixes day-first with
  month-first formats. Work out the convention from the entries where the day is
  above 12, and read the whole column that way. If a date lands more than a year
  from today on a row marked complete, treat it as a typo, use the sensible
  reading, and tell me.
- If I give you a previous week's register too: these are **live snapshots**, so
  closed rows get deleted. Never compare the overall percentages between weeks.
  Compare individual deliverables and say on the slide why the totals can't be
  compared.

**What to work out.** How many delivered, in progress and not started. Actual
progress against planned, as a percentage and as a number of whole deliverables.
Which few items hold the entire gap. What the remarks column says when you group
it — a flag repeating across several rows is usually the real story. Workload per
owner, split between finished and open, counting shared items once per named
person and footnoting that.

**The deck.** Around nine slides, 16:9. Lead with what changed and what decision
you need, not with a description of the spreadsheet. Build from these, dropping
any the data no longer supports: a title slide with headline numbers; an
executive summary with four stat tiles and three ranked takeaways; a status
breakdown with a doughnut and progress-against-plan bars; week-on-week movement
if I gave you a prior register; the completed work as project cards; whatever the
repeated remark flag turns out to be, as its own slide; the still-open items as
rows with progress bars showing a marker for where each was planned to be today;
blockers where every card ends in a decision someone can make in the room; and
workload by owner.

Two rules. Don't chart rows that are all identical — ten projects at 100% planned
and 100% actual is twenty redundant bars that bury the three that matter; chart
the variance and summarise the rest in a stat panel. And write speaker notes on
every slide in the manager's voice, as spoken sentences.

**Look.** Navy `1B2A41` for dark slides and headings, white content slides,
rounded cards with a soft shadow and a small coloured circular badge as the
repeating motif. Cambria for titles and big numbers, Calibri for body. Charts use
blue `2A78D6` for actual or current and orange `EB6834` for planned or prior.
Status colours stay reserved: green `0CA30C`, amber `FAB219`, red `D03B3B`, and
always with a text label beside them, never colour alone. No accent stripes, no
lines under titles.

**Before you tell me it's done:** render every slide to an image and actually
look at them. Text overflowing a card, a long project name colliding with its
badge, and a right-hand column running into the next one are the defects that
always show up and that no automated check catches. Then grep the deck's text for
any figure that should have changed but didn't — one number moving in the source
ripples through counts, percentages, charts, cards, footnotes and speaker notes.

Tell me any assumption you had to make about my data.
