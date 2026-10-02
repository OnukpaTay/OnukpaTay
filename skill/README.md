# Share this with a friend

Two ways to get the same deck. Both take a project deliverables register
spreadsheet and produce a management PowerPoint presentation.

## Option 1 — the prompt (nothing to install)

Open [`PROMPT.md`](PROMPT.md), copy the whole thing, paste it into Claude and
attach the register. Works in the Claude app, on claude.ai and in Claude Code.

Good when it's a one-off, or when your friend just wants to see what comes out.

## Option 2 — the skill (better, reusable)

[`commercial-status-deck.skill`](commercial-status-deck.skill) is an installable
Claude skill. Send them the file. In the Claude app or on claude.ai they open it
and press **Save skill**; in Claude Code they unzip it into `~/.claude/skills/`.

After that they never paste anything. They just say "turn this register into a
deck for management" and attach the spreadsheet, and Claude picks the skill up on
its own.

The skill carries more than the prompt does:

| | Prompt | Skill |
|---|---|---|
| Design system and layout rules | summarised | full reference |
| Spreadsheet parsing traps | described | a tested script that handles them |
| Week-on-week comparison | described | built into the script |
| Slide geometry | left to Claude | specified per slide |
| Reusable chart and card helpers | no | yes |
| A complete worked example deck | no | yes |

## What's inside the skill

```
commercial-status-deck/
├── SKILL.md                      the method: read, find the story, build, check
├── references/
│   ├── design-system.md          palette, type, layout, pptxgenjs traps
│   └── slide-patterns.md         geometry for each slide archetype
├── scripts/
│   ├── read_register.py          parses the register, prints every rollup
│   └── deck_kit.js               tokens + header/card/dot/progress/chip helpers
└── assets/
    └── example_deck.js           a complete nine-slide deck built on the kit
```

`read_register.py` needs `openpyxl`. The deck generator needs `pptxgenjs`
(`npm install pptxgenjs`). Both get installed automatically when Claude runs them.

## Trying the script on its own

```bash
python3 scripts/read_register.py register.xlsx
python3 scripts/read_register.py this_week.xlsx --compare last_week.xlsx
```

It prints delivery counts, progress against plan, the outstanding items ordered
by exposure, workload per owner, grouped remark flags, and warns when a date
looks like a typo or when the register has shrunk enough that week-on-week
percentages stop being comparable.
