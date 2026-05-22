# Contract Claims module
#
# Two calculators:
#  - EOT (Extension of Time) register: events, days impact, concurrent delay
#  - Loss & Expense / Prolongation cost build-up

mod_claims_ui <- function(id) {
  ns <- NS(id)
  bslib::navset_card_tab(
    id = ns("ctabs"),
    bslib::nav_panel(
      "EOT Register",
      bslib::layout_columns(
        col_widths = c(9, 3),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("hourglass-split"),
                             " Extension of Time events"),
          helpText("Log delay events, who bears the risk (Employer/Contractor/Neutral), ",
                   "the gross days impact, and any concurrent delay deduction. ",
                   "Net days drives the contract completion adjustment."),
          bslib::layout_columns(
            col_widths = c(6, 6),
            actionButton(ns("add_event"), "Add event",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("del_event"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash"))
          ),
          DT::DTOutput(ns("eot_table"))
        ),
        bslib::value_box(
          title    = "Total EOT claimed (days)",
          value    = textOutput(ns("eot_days")),
          showcase = bsicons::bs_icon("calendar-week"),
          theme    = "warning"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("file-earmark-bar-graph"),
                           " EOT summary by risk allocation"),
        DT::DTOutput(ns("eot_summary")),
        downloadButton(ns("export_eot"), "Export EOT register (Excel)",
                       class = "btn-primary mt-3")
      )
    ),

    bslib::nav_panel(
      "Loss & Expense",
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("calculator-fill"),
                             " Prolongation cost build-up"),
          helpText("Daily rate method: total each cost head per day, ",
                   "multiply by the prolongation period. Use the EOT register's ",
                   "Employer-risk days as the period."),
          numericInput(ns("prolong_days"), "Prolongation period (days)",
                       value = 30, min = 0, step = 1),
          DT::DTOutput(ns("loss_table")),
          bslib::layout_columns(
            col_widths = c(6, 6),
            actionButton(ns("add_loss"), "Add cost head",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("del_loss"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash"))
          )
        ),
        bslib::value_box(
          title    = "Total loss & expense claim",
          value    = textOutput(ns("loss_total")),
          showcase = bsicons::bs_icon("cash-coin"),
          theme    = "danger"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("ui-checks"),
                           " Head of claim summary"),
        DT::DTOutput(ns("loss_summary")),
        downloadButton(ns("export_loss"), "Export loss & expense build-up (Excel)",
                       class = "btn-primary mt-3")
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("info-circle"),
                           " Reference - typical heads of claim"),
        tags$ul(
          tags$li(tags$strong("Site preliminaries -"),
                  " staff salaries, site office, security, welfare, utilities."),
          tags$li(tags$strong("Off-site overheads -"),
                  " formula methods e.g. Hudson, Emden, Eichleay."),
          tags$li(tags$strong("Plant and equipment -"),
                  " idle plant, retained hire, mobilisation re-runs."),
          tags$li(tags$strong("Loss of productivity -"),
                  " measured mile or industry studies (MCAA, NECA)."),
          tags$li(tags$strong("Financing costs -"),
                  " interest on retained working capital."),
          tags$li(tags$strong("Inflation / escalation -"),
                  " labour, materials, fuel price indices.")
        )
      )
    )
  )
}

mod_claims_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    # --- EOT register -----------------------------------------------------
    eot <- reactiveVal(
      tibble::tibble(
        event_no    = c("EOT-001", "EOT-002", "EOT-003"),
        event_date  = as.Date(c("2026-01-15", "2026-02-08", "2026-03-12")),
        description = c("Late issue of structural drawings - 21 days",
                        "Unforeseen ground conditions at column line 7",
                        "Exceptionally adverse weather - 5 days rain"),
        cause       = c("Employer", "Employer", "Neutral"),
        gross_days  = c(21, 14, 5),
        concurrent_days = c(0, 4, 0),
        notice_ref  = c("L-014", "L-019", "L-027"),
        status      = c("Granted", "Under review", "Granted")
      )
    )

    observeEvent(input$add_event, {
      eot(dplyr::bind_rows(eot(), tibble::tibble(
        event_no = sprintf("EOT-%03d", nrow(eot()) + 1),
        event_date = Sys.Date(),
        description = "New delay event",
        cause = "Employer", gross_days = 0, concurrent_days = 0,
        notice_ref = "", status = "Notified"
      )))
    })

    observeEvent(input$del_event, {
      sel <- input$eot_table_rows_selected
      if (length(sel)) eot(eot()[-sel, , drop = FALSE])
    })

    eot_calc <- reactive({
      eot() %>%
        dplyr::mutate(
          gross_days = as_num(.data$gross_days),
          concurrent_days = as_num(.data$concurrent_days),
          net_days = pmax(0, .data$gross_days - .data$concurrent_days)
        )
    })

    output$eot_table <- DT::renderDT({
      df <- eot_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "net_days") - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Event no", "Event date", "Description",
                     "Cause / risk party", "Gross days",
                     "Concurrent (deduct)", "Notice ref", "Status",
                     "Net days claimed")
      )
    }, server = FALSE)

    observeEvent(input$eot_table_cell_edit, {
      info <- input$eot_table_cell_edit
      df <- eot()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("gross_days", "concurrent_days")) {
        df[info$row, col_name] <- as_num(info$value)
      } else if (col_name == "event_date") {
        df[info$row, col_name] <- suppressWarnings(as.Date(info$value))
      } else {
        df[info$row, col_name] <- info$value
      }
      eot(df)
    })

    output$eot_summary <- DT::renderDT({
      df <- eot_calc() %>%
        dplyr::group_by(.data$cause, .data$status) %>%
        dplyr::summarise(events = dplyr::n(),
                         gross_days = sum(.data$gross_days),
                         concurrent_days = sum(.data$concurrent_days),
                         net_days = sum(.data$net_days),
                         .groups = "drop")
      DT::datatable(df, rownames = FALSE, options = list(dom = "t"))
    })

    output$eot_days <- renderText({
      sprintf("%d days", sum(eot_calc()$net_days))
    })

    # Push employer-risk net days to the loss & expense default
    observe({
      df <- eot_calc()
      employer_days <- sum(df$net_days[df$cause == "Employer"], na.rm = TRUE)
      if (employer_days > 0)
        updateNumericInput(session, "prolong_days", value = employer_days)
    })

    output$export_eot <- downloadHandler(
      filename = function() sprintf("EOT_Register_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "EOT")
        openxlsx::writeData(wb, "EOT", eot_calc())
        openxlsx::setColWidths(wb, "EOT", cols = 1:9,
                               widths = c(10, 12, 50, 18, 12, 15, 12, 14, 14))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    # --- Loss & Expense ---------------------------------------------------
    loss <- reactiveVal(
      tibble::tibble(
        head     = c("Site preliminaries",
                     "Site preliminaries",
                     "Site preliminaries",
                     "Off-site overheads (Hudson)",
                     "Plant and equipment",
                     "Loss of productivity",
                     "Financing costs"),
        item     = c("Project manager - daily cost",
                     "Site office and welfare - daily cost",
                     "Security and utilities - daily cost",
                     "Head office contribution - daily allocation",
                     "Idle tower crane - daily standing charge",
                     "Reduced output of finishes trades - daily loss",
                     "Interest on working capital - daily"),
        daily_rate = c(450, 320, 180, 850, 1200, 600, 220),
        applies   = c(TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE)
      )
    )

    observeEvent(input$add_loss, {
      loss(dplyr::bind_rows(loss(), tibble::tibble(
        head = "Site preliminaries",
        item = "New cost head", daily_rate = 0, applies = TRUE
      )))
    })

    observeEvent(input$del_loss, {
      sel <- input$loss_table_rows_selected
      if (length(sel)) loss(loss()[-sel, , drop = FALSE])
    })

    loss_calc <- reactive({
      days <- as_num(input$prolong_days)
      loss() %>%
        dplyr::mutate(
          daily_rate = as_num(.data$daily_rate),
          days = days,
          amount = ifelse(.data$applies,
                          round(.data$daily_rate * days, 2),
                          0)
        )
    })

    output$loss_table <- DT::renderDT({
      df <- loss_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) %in%
                                       c("days", "amount")) - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Head of claim", "Item", "Daily rate",
                     "Applies?", "Days", "Amount")
      ) %>%
        DT::formatCurrency(c("daily_rate", "amount"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$loss_table_cell_edit, {
      info <- input$loss_table_cell_edit
      df <- loss()
      col_name <- names(df)[info$col + 1]
      if (col_name == "daily_rate") {
        df[info$row, col_name] <- as_num(info$value)
      } else if (col_name == "applies") {
        df[info$row, col_name] <- isTRUE(as.logical(info$value)) ||
                                   tolower(info$value) %in% c("true", "yes", "y", "1")
      } else {
        df[info$row, col_name] <- info$value
      }
      loss(df)
    })

    output$loss_summary <- DT::renderDT({
      df <- loss_calc() %>%
        dplyr::group_by(.data$head) %>%
        dplyr::summarise(items = dplyr::n(),
                         daily = sum(.data$daily_rate[.data$applies]),
                         total = sum(.data$amount),
                         .groups = "drop")
      DT::datatable(df, rownames = FALSE, options = list(dom = "t")) %>%
        DT::formatCurrency(c("daily", "total"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$loss_total <- renderText({
      fmt_money(sum(loss_calc()$amount, na.rm = TRUE), settings$currency_symbol)
    })

    output$export_loss <- downloadHandler(
      filename = function() sprintf("Loss_and_Expense_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "Loss_Expense")
        openxlsx::writeData(wb, "Loss_Expense", loss_calc())
        openxlsx::setColWidths(wb, "Loss_Expense", cols = 1:6,
                               widths = c(30, 50, 14, 10, 8, 14))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )
  })
}
