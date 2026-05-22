# Settings module - practice details, standards, currency, default rates.

mod_settings_ui <- function(id) {
  ns <- NS(id)
  bslib::layout_columns(
    col_widths = c(6, 6),
    bslib::card(
      bslib::card_header(bsicons::bs_icon("building"), " Practice & signatories"),
      textInput(ns("practice_name"), "Practice / firm name",
                value = DEFAULT_SETTINGS$practice_name),
      textInput(ns("practice_addr"), "Address",
                value = DEFAULT_SETTINGS$practice_addr),
      textInput(ns("qs_name"), "Lead Quantity Surveyor",
                value = DEFAULT_SETTINGS$qs_name),
      textInput(ns("qs_credentials"), "Credentials / registration",
                value = DEFAULT_SETTINGS$qs_credentials),
      tags$hr(),
      textInput(ns("architect_name"), "Default architect / consultant", value = ""),
      textInput(ns("architect_addr"), "Architect address", value = ""),
      textInput(ns("approver_name"),  "Default approver name", value = ""),
      textInput(ns("approver_title"), "Default approver title",
                value = "Commercial Manager"),
      textInput(ns("accountant_name"), "Default accountant name", value = "")
    ),
    bslib::card(
      bslib::card_header(bsicons::bs_icon("sliders"), " Standards & contract"),
      selectInput(ns("measurement_std"), "Measurement standard",
                  choices = c("RICS NRM2" = "NRM2",
                              "SMM7"      = "SMM7",
                              "GhIS"      = "GhIS"),
                  selected = DEFAULT_SETTINGS$measurement_std),
      selectInput(ns("contract_form"), "Contract form",
                  choices = c("JCT Standard Building Contract" = "JCT-SBC",
                              "JCT Intermediate Building Contract" = "JCT-IC",
                              "FIDIC Red Book (employer-design)"  = "FIDIC-Red",
                              "FIDIC Yellow Book (design-build)"  = "FIDIC-Yellow",
                              "GhIS Standard Form"                = "GhIS-Standard"),
                  selected = DEFAULT_SETTINGS$contract_form),
      textInput(ns("currency_code"), "Currency code",
                value = DEFAULT_SETTINGS$currency_code),
      textInput(ns("currency_symbol"), "Currency symbol",
                value = DEFAULT_SETTINGS$currency_symbol),
      bslib::layout_columns(
        col_widths = c(6, 6),
        numericInput(ns("retention_pct"), "Retention %",
                     value = DEFAULT_SETTINGS$retention_pct, min = 0, max = 25, step = 0.5),
        numericInput(ns("retention_cap"), "Retention cap (% of contract sum)",
                     value = DEFAULT_SETTINGS$retention_cap, min = 0, max = 25, step = 0.5)
      ),
      bslib::layout_columns(
        col_widths = c(6, 6),
        numericInput(ns("vat_pct"), "VAT %", value = DEFAULT_SETTINGS$vat_pct,
                     min = 0, max = 30, step = 0.5),
        numericInput(ns("nhil_getfl_pct"), "NHIL + GETFund + Covid %",
                     value = DEFAULT_SETTINGS$nhil_getfl_pct,
                     min = 0, max = 30, step = 0.5)
      ),
      bslib::layout_columns(
        col_widths = c(6, 6),
        numericInput(ns("overhead_pct"), "Overhead % (cost build-up)",
                     value = DEFAULT_SETTINGS$overhead_pct,
                     min = 0, max = 50, step = 0.5),
        numericInput(ns("profit_pct"), "Profit % (cost build-up)",
                     value = DEFAULT_SETTINGS$profit_pct,
                     min = 0, max = 50, step = 0.5)
      ),
      bslib::layout_columns(
        col_widths = c(4, 4, 4),
        numericInput(ns("prelims_pct"),     "Preliminaries % (BOQ)",
                     value = DEFAULT_SETTINGS$prelims_pct,
                     min = 0, max = 30, step = 0.5),
        numericInput(ns("contingency_pct"), "Contingency % (BOQ)",
                     value = DEFAULT_SETTINGS$contingency_pct,
                     min = 0, max = 30, step = 0.5),
        numericInput(ns("withholding_tax_pct"),
                     "Withholding tax % (IPC)",
                     value = DEFAULT_SETTINGS$withholding_tax_pct,
                     min = 0, max = 30, step = 0.5)
      ),
      actionButton(ns("save"), "Save settings",
                   class = "btn-primary", icon = icon("save"))
    )
  )
}

mod_settings_server <- function(id, settings) {
  moduleServer(id, function(input, output, session) {
    observeEvent(input$save, {
      settings$practice_name   <- input$practice_name
      settings$practice_addr   <- input$practice_addr
      settings$qs_name         <- input$qs_name
      settings$qs_credentials  <- input$qs_credentials
      settings$architect_name  <- input$architect_name
      settings$architect_addr  <- input$architect_addr
      settings$approver_name   <- input$approver_name
      settings$approver_title  <- input$approver_title
      settings$accountant_name <- input$accountant_name
      settings$measurement_std <- input$measurement_std
      settings$contract_form   <- input$contract_form
      settings$currency_code   <- input$currency_code
      settings$currency_symbol <- input$currency_symbol
      settings$retention_pct   <- input$retention_pct
      settings$retention_cap   <- input$retention_cap
      settings$vat_pct         <- input$vat_pct
      settings$nhil_getfl_pct  <- input$nhil_getfl_pct
      settings$overhead_pct    <- input$overhead_pct
      settings$profit_pct      <- input$profit_pct
      settings$prelims_pct     <- input$prelims_pct
      settings$contingency_pct <- input$contingency_pct
      settings$withholding_tax_pct <- input$withholding_tax_pct
      showNotification("Settings saved for this session.",
                       type = "message", duration = 3)
    })
  })
}
