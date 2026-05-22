# OnukpaTay - Global setup
# Loaded once when the Shiny app starts.

suppressPackageStartupMessages({
  library(shiny)
  library(bslib)
  library(bsicons)
  library(DT)
  library(dplyr)
  library(tibble)
  library(tidyr)
  library(readr)
  library(purrr)
  library(lubridate)
  library(scales)
  library(openxlsx)
  library(htmltools)
  library(shinyjs)
  library(jsonlite)
  library(ggplot2)
})

# ---- App constants ---------------------------------------------------------

APP_NAME    <- "OnukpaTay"
APP_TAGLINE <- "Professional Quantity Surveyor Assistant"
APP_VERSION <- "0.1.0"

# Default settings (user can override in the Settings tab and they persist
# in app state for the session).
DEFAULT_SETTINGS <- list(
  practice_name   = "OnukpaTay Quantity Surveyors",
  practice_addr   = "Accra, Ghana",
  qs_name         = "Sedem Onukpa-Tay",
  qs_credentials  = "BSc QS, GhIS, MRICS (Probationer)",
  architect_name  = "",
  architect_addr  = "",
  approver_name   = "",
  approver_title  = "",
  accountant_name = "",
  currency_code   = "GHS",
  currency_symbol = "GH₵",
  measurement_std = "NRM2",       # NRM2 | SMM7 | GhIS
  contract_form   = "FIDIC-Red",  # JCT-SBC | JCT-IC | FIDIC-Red | FIDIC-Yellow | GhIS-Standard
  retention_pct   = 10,           # %
  retention_cap   = 5,            # % of contract sum
  vat_pct         = 12.5,         # Ghana VAT default
  nhil_getfl_pct  = 6,            # NHIL + GETFund + Covid (typical Ghana levies)
  withholding_tax_pct = 5,        # WHT on construction contracts
  overhead_pct    = 12,
  profit_pct      = 8,
  prelims_pct     = 7,            # Prelims as % of measured works
  contingency_pct = 5             # Contingency as % of measured + prelims
)

# Lookup tables (loaded from /data) ------------------------------------------

load_csv <- function(path) {
  if (!file.exists(path)) return(NULL)
  suppressWarnings(suppressMessages(readr::read_csv(path, show_col_types = FALSE)))
}

UNITS_DF         <- load_csv("data/units.csv")
TRADE_GROUPS_DF  <- load_csv("data/trade_groups.csv")
SAMPLE_RATES_DF  <- load_csv("data/sample_rates.csv")
SAMPLE_BOQ_DF    <- load_csv("data/sample_boq.csv")
SAMPLE_BILLS_DF  <- load_csv("data/sample_boq_bills.csv")
ELEMENTS_DF      <- load_csv("data/elements_nrm1.csv")

# ---- Helpers ---------------------------------------------------------------

#' Format a numeric value as money using the active currency symbol.
fmt_money <- function(x, symbol = "GH₵", digits = 2) {
  if (is.null(x) || length(x) == 0) return("")
  ifelse(is.na(x), "",
         paste0(symbol, " ",
                formatC(round(as.numeric(x), digits), format = "f",
                        big.mark = ",", digits = digits)))
}

#' Safe numeric coercion (NA -> 0)
as_num <- function(x) {
  v <- suppressWarnings(as.numeric(x))
  v[is.na(v)] <- 0
  v
}

#' Generate a sequential document reference, e.g. IPC-2026-001
make_ref <- function(prefix, n, year = lubridate::year(Sys.Date())) {
  sprintf("%s-%d-%03d", prefix, year, n)
}

#' Load source files in R/ on app start (R/ is auto-sourced by shiny but
#' we do it explicitly here so it works under runApp() as well).
source_R_dir <- function(dir = "R") {
  files <- list.files(dir, pattern = "\\.R$", full.names = TRUE, ignore.case = TRUE)
  invisible(lapply(files, source, local = FALSE))
}
source_R_dir("R")
