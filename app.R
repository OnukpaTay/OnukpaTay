# OnukpaTay - Quantity Surveyor Assistant
# Main Shiny app entry point. Run with shiny::runApp() or in RStudio.

source("global.R")

# ---- UI --------------------------------------------------------------------

ui <- bslib::page_navbar(
  title = tagList(
    tags$span(class = "brand-title", APP_NAME),
    tags$span(class = "brand-tagline", APP_TAGLINE)
  ),
  id = "main_nav",
  fillable = FALSE,
  theme = bslib::bs_theme(
    version = 5,
    primary = "#1f4e79",
    secondary = "#6c757d",
    success = "#198754",
    info = "#0dcaf0",
    warning = "#ffc107",
    danger = "#dc3545",
    base_font = bslib::font_google("Inter"),
    heading_font = bslib::font_google("Inter")
  ),
  header = tags$head(
    includeCSS("www/styles.css"),
    tags$link(rel = "icon", type = "image/svg+xml",
              href = "data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%231f4e79'/%3E%3Ctext x='32' y='42' text-anchor='middle' font-family='Inter,Arial' font-size='32' font-weight='700' fill='white'%3EOT%3C/text%3E%3C/svg%3E")
  ),

  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("speedometer2"), " Dashboard"),
    bslib::layout_columns(
      col_widths = c(12),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("hand-thumbs-up"),
                           " Welcome to OnukpaTay"),
        tags$p(tags$strong("OnukpaTay"),
               " is your professional GhIS / RICS Quantity Surveyor assistant. ",
               "It supports the full pre- to post-contract workflow:"),
        tags$ul(
          tags$li(tags$strong("BOQ -"), " Build, price and export a fully-formatted Bill of Quantities."),
          tags$li(tags$strong("IPC -"), " Generate Interim Payment Certificates with retention, levies and VAT."),
          tags$li(tags$strong("Valuations & Variations -"),
                  " Track VOs, omissions, additions and daywork sheets."),
          tags$li(tags$strong("Claims -"),
                  " EOT register with concurrent-delay handling and prolongation cost build-up."),
          tags$li(tags$strong("Budgeting -"),
                  " NRM1 elemental cost plans and S-curve cash flow forecasts.")
        ),
        tags$p("Configure your firm, the measurement standard ",
               "(NRM2 / SMM7 / GhIS), contract form (JCT / FIDIC / GhIS), and ",
               "default rates in the ",
               tags$strong("Settings"), " tab. Defaults use Ghana cedi (GH₵), ",
               "12.5% VAT and 6% NHIL/GETFund/Covid levies.")
      )
    ),
    bslib::layout_columns(
      col_widths = c(3, 3, 3, 3),
      bslib::value_box(
        title = "Measurement standard",
        value = textOutput("dash_std"),
        showcase = bsicons::bs_icon("rulers"),
        theme = "primary"
      ),
      bslib::value_box(
        title = "Contract form",
        value = textOutput("dash_contract"),
        showcase = bsicons::bs_icon("file-earmark-ruled"),
        theme = "secondary"
      ),
      bslib::value_box(
        title = "Currency",
        value = textOutput("dash_currency"),
        showcase = bsicons::bs_icon("coin"),
        theme = "success"
      ),
      bslib::value_box(
        title = "Practice",
        value = textOutput("dash_practice"),
        showcase = bsicons::bs_icon("building"),
        theme = "info"
      )
    )
  ),

  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("file-spreadsheet"), " BOQ"),
    mod_boq_ui("boq")
  ),
  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("receipt"), " IPC"),
    mod_ipc_ui("ipc")
  ),
  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("clipboard-check"), " Valuations & VOs"),
    mod_valuations_ui("val")
  ),
  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("exclamation-triangle"), " Claims"),
    mod_claims_ui("clm")
  ),
  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("piggy-bank"), " Budgeting"),
    mod_budgeting_ui("bud")
  ),
  bslib::nav_spacer(),
  bslib::nav_panel(
    title = tagList(bsicons::bs_icon("gear"), " Settings"),
    mod_settings_ui("settings")
  ),
  bslib::nav_item(
    tags$span(class = "version-badge", paste("v", APP_VERSION))
  )
)

# ---- Server ----------------------------------------------------------------

server <- function(input, output, session) {

  # Settings live as a reactiveValues so changes flow to every module.
  settings <- do.call(reactiveValues, DEFAULT_SETTINGS)

  # Shared state for cross-module data passing (e.g. BOQ -> IPC).
  app_state <- reactiveValues(boq = NULL)

  mod_settings_server("settings", settings)
  mod_boq_server("boq",       settings, app_state)
  mod_ipc_server("ipc",       settings, app_state)
  mod_valuations_server("val", settings, app_state)
  mod_claims_server("clm",    settings, app_state)
  mod_budgeting_server("bud", settings, app_state)

  output$dash_std       <- renderText({ settings$measurement_std })
  output$dash_contract  <- renderText({ settings$contract_form })
  output$dash_currency  <- renderText({
    paste0(settings$currency_code, " (", settings$currency_symbol, ")")
  })
  output$dash_practice  <- renderText({ settings$practice_name })
}

shinyApp(ui, server)
