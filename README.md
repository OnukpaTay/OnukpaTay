# OnukpaTay

**Professional Quantity Surveyor Assistant - GhIS / RICS practice**

An R Shiny application that supports the full pre- to post-contract QS workflow:

| Module | What it does |
| --- | --- |
| **BOQ** | Build, price, import and export a fully-formatted Bill of Quantities (NRM2 / SMM7 / GhIS trade groupings). |
| **IPC** | Interim Payment Certificates - work done to date, materials on site, retention (with cap), advance recovery, VAT and NHIL/GETFund/Covid levies. |
| **Valuations & VOs** | Variation register (omissions / additions, status) plus a daywork sheet with on-cost build-up. |
| **Claims** | EOT register with concurrent-delay deduction, plus a loss & expense / prolongation cost build-up. |
| **Budgeting** | NRM1 elemental cost plan (£/m² GIFA) and an S-curve cash-flow forecast with peak demand and working-capital indicators. |

Defaults: Ghana cedi (GH₵), 12.5 % VAT, 6 % NHIL + GETFund + Covid, 10 % retention capped at 5 % of contract sum. All configurable in **Settings**.

---

## Quick start

```r
# 1. Install the dependencies (first run only)
install.packages(c(
  "shiny", "bslib", "bsicons", "DT", "dplyr", "tidyr",
  "readr", "purrr", "lubridate", "scales", "openxlsx",
  "rmarkdown", "htmltools", "shinyjs", "jsonlite", "ggplot2"
))

# 2. Launch the app
shiny::runApp(".")
```

Open the link Shiny prints (e.g. `http://127.0.0.1:7654`).

---

## Project layout

```
OnukpaTay/
├── app.R                  # main Shiny entry point
├── global.R               # package loading, constants, helpers
├── DESCRIPTION            # dependency manifest
├── R/
│   ├── helpers.R          # shared utilities (formatting, Excel export)
│   ├── mod_boq.R          # Bill of Quantities module
│   ├── mod_ipc.R          # Interim Payment Certificate module
│   ├── mod_valuations.R   # Variations & Daywork module
│   ├── mod_claims.R       # EOT & Loss-and-expense module
│   ├── mod_budgeting.R    # Cost plan & cash-flow module
│   └── mod_settings.R     # Practice, standards, tax settings
├── data/                  # reference CSVs (trades, units, sample rates)
├── www/styles.css         # theme overrides
├── reports/               # placeholder for RMarkdown report templates
└── templates_to_integrate/ # drop your existing Excel/Word templates here
```

---

## Bringing in your own templates

You mentioned you have existing templates - drop them into
`templates_to_integrate/` and the next iteration will:

1. Map the column structure of your BOQ template into the BOQ module's
   importer.
2. Replicate the layout of your IPC / valuation forms in the Excel export.
3. Pre-load your firm's letterhead and signatory block in `R/mod_settings.R`.

CSV format expected by the BOQ importer:

```
item_no,trade,description,unit,quantity,rate
A1,Preliminaries,Site establishment,item,1,45000
B1,Substructure,Excavation to reduce levels,m3,180,65
...
```

---

## Standards & conventions supported

- **Measurement** - RICS NRM2, SMM7, GhIS (switchable per project in Settings).
- **Cost planning** - RICS NRM1 elements (32-element breakdown).
- **Contract forms** - JCT SBC/IC, FIDIC Red / Yellow Book, GhIS Standard Form.
- **Tax & deductions** - Ghana VAT (12.5%), NHIL + GETFund + Covid (6%),
  retention (10% capped at 5% of contract sum). Override per certificate.

---

## Roadmap

- [ ] PDF rendering of BOQs and certificates via RMarkdown / pagedown
- [ ] Persistent project storage (SQLite)
- [ ] Multi-user / project switching
- [ ] Sub-contract package comparison module
- [ ] Final account reconciliation module
- [ ] Integration with user's existing letterheads & templates

---

## Contact

Sedem Onukpa-Tay - onukpatay@gmail.com
