# Interim Payment Certificate module
#
# Calculation flow (JCT / FIDIC style):
#   Gross valuation of works done to date
# +  Materials on site
# +  Variations approved this period
# -  Retention (sliding: full % up to cap, then frozen)
# -  Previous certificates (cumulative paid to date)
# =  Amount due this certificate (net of VAT)
# +/- VAT and statutory levies
# =  Amount payable

mod_ipc_ui <- function(id) {
  ns <- NS(id)
  tagList(
    bslib::layout_columns(
      col_widths = c(8, 4),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("file-earmark-medical"),
                           " Certificate header"),
        bslib::layout_columns(
          col_widths = c(4, 4, 4),
          textInput(ns("project_name"), "Project",
                    value = "Proposed 3-Bedroom Bungalow at East Legon"),
          textInput(ns("employer"),     "Employer", value = ""),
          textInput(ns("contractor"),   "Contractor", value = "")
        ),
        bslib::layout_columns(
          col_widths = c(3, 3, 3, 3),
          numericInput(ns("cert_no"), "Certificate no.", value = 1, min = 1, step = 1),
          dateInput(ns("valuation_date"), "Valuation date", value = Sys.Date()),
          dateInput(ns("issue_date"),     "Date of issue",  value = Sys.Date()),
          dateInput(ns("due_date"),       "Due date",
                    value = Sys.Date() + 14)
        )
      ),
      bslib::value_box(
        title    = "Amount payable this certificate",
        value    = textOutput(ns("payable")),
        showcase = bsicons::bs_icon("currency-exchange"),
        theme    = "success"
      )
    ),
    bslib::layout_columns(
      col_widths = c(7, 5),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("clipboard-data"),
                           " Work done to date - by trade / element"),
        helpText("Enter the % completion or value of work done for each trade. ",
                 "You can pull live totals from the BOQ tab using the button below."),
        actionButton(ns("pull_boq"), "Pull trades from current BOQ",
                     icon = icon("download"), class = "btn-outline-primary mb-2"),
        DT::DTOutput(ns("wd_table")),
        bslib::layout_columns(
          col_widths = c(6, 6),
          actionButton(ns("add_wd"), "Add row", class = "btn-success btn-sm",
                       icon = icon("plus")),
          actionButton(ns("del_wd"), "Delete selected",
                       class = "btn-outline-danger btn-sm", icon = icon("trash"))
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("sliders2"),
                           " Contract & deductions"),
        currency_input(ns("contract_sum"),       "Contract sum (net of VAT)",
                       value = 0, settings = DEFAULT_SETTINGS),
        currency_input(ns("materials_on_site"),  "Materials on site this period",
                       value = 0, settings = DEFAULT_SETTINGS),
        currency_input(ns("variations"),         "Variations approved this period",
                       value = 0, settings = DEFAULT_SETTINGS),
        currency_input(ns("previous_paid"),      "Previous certificates paid",
                       value = 0, settings = DEFAULT_SETTINGS),
        currency_input(ns("advance_repaid"),     "Advance payment recouped this period",
                       value = 0, settings = DEFAULT_SETTINGS),
        bslib::layout_columns(
          col_widths = c(6, 6),
          numericInput(ns("retention_pct"), "Retention %",
                       value = 10, min = 0, max = 25, step = 0.5),
          numericInput(ns("retention_cap"), "Cap (% of contract sum)",
                       value = 5,  min = 0, max = 25, step = 0.5)
        ),
        bslib::layout_columns(
          col_widths = c(6, 6),
          numericInput(ns("vat_pct"), "VAT %", value = 12.5, min = 0, max = 30),
          numericInput(ns("levies_pct"), "NHIL/GETFund %", value = 6, min = 0, max = 30)
        )
      )
    ),
    bslib::card(
      bslib::card_header(bsicons::bs_icon("file-text"),
                         " Payment certificate summary"),
      DT::DTOutput(ns("cert_summary")),
      downloadButton(ns("export_xlsx"),
                     "Export certificate (Excel)",
                     class = "btn-primary mt-3"),
      downloadButton(ns("export_csv"),
                     "Export work-done breakdown (CSV)",
                     class = "btn-outline-secondary mt-2")
    )
  )
}

mod_ipc_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    wd <- reactiveVal(
      tibble::tibble(
        trade = c("Preliminaries", "Substructure", "Superstructure",
                  "Finishes", "Services"),
        boq_value      = c(45000, 380000, 620000, 240000, 310000),
        prev_pct_done  = c(80, 70, 30, 0, 0),
        this_pct_done  = c(95, 85, 55, 15, 10)
      )
    )

    # Reflect settings defaults
    observe({
      updateNumericInput(session, "retention_pct", value = settings$retention_pct)
      updateNumericInput(session, "retention_cap", value = settings$retention_cap)
      updateNumericInput(session, "vat_pct",       value = settings$vat_pct)
      updateNumericInput(session, "levies_pct",    value = settings$nhil_getfl_pct)
    })

    observeEvent(input$pull_boq, {
      boq <- app_state$boq
      if (is.null(boq) || !nrow(boq)) {
        showNotification("No BOQ data in memory. Build a BOQ first.",
                         type = "warning"); return()
      }
      summary <- boq_summary_by_trade(boq) %>%
        dplyr::transmute(trade = .data$trade,
                         boq_value     = .data$total,
                         prev_pct_done = 0,
                         this_pct_done = 0)
      wd(summary)
      showNotification("Pulled trade totals from BOQ.", type = "message")
    })

    observeEvent(input$add_wd, {
      wd(dplyr::bind_rows(wd(), tibble::tibble(
        trade = "New trade", boq_value = 0,
        prev_pct_done = 0, this_pct_done = 0
      )))
    })

    observeEvent(input$del_wd, {
      sel <- input$wd_table_rows_selected
      if (length(sel)) wd(wd()[-sel, , drop = FALSE])
    })

    wd_calc <- reactive({
      df <- wd() %>%
        dplyr::mutate(
          boq_value      = as_num(.data$boq_value),
          prev_pct_done  = as_num(.data$prev_pct_done),
          this_pct_done  = as_num(.data$this_pct_done),
          prev_value     = round(.data$boq_value * .data$prev_pct_done / 100, 2),
          gross_value    = round(.data$boq_value * .data$this_pct_done / 100, 2),
          this_period    = round(.data$gross_value - .data$prev_value, 2)
        )
      df
    })

    output$wd_table <- DT::renderDT({
      df <- wd_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = c(4, 5, 6))), # computed cols
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Trade", "BOQ value", "Prev % done", "This % done",
                     "Prev value", "Gross value", "This period")
      ) %>%
        DT::formatCurrency(c("boq_value", "prev_value", "gross_value", "this_period"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$wd_table_cell_edit, {
      info <- input$wd_table_cell_edit
      df <- wd()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("boq_value", "prev_pct_done", "this_pct_done"))
        df[info$row, col_name] <- as_num(info$value)
      else
        df[info$row, col_name] <- info$value
      wd(df)
    })

    # Certificate calculation ---------------------------------------------
    cert <- reactive({
      df <- wd_calc()
      gross_wd     <- sum(df$gross_value, na.rm = TRUE)
      mos          <- as_num(input$materials_on_site)
      var          <- as_num(input$variations)
      gross_total  <- gross_wd + mos + var

      # Retention: applied to gross_wd + variations, capped at % of contract sum
      contract_sum <- as_num(input$contract_sum)
      ret_pct      <- as_num(input$retention_pct) / 100
      ret_cap_val  <- contract_sum * as_num(input$retention_cap) / 100
      retention    <- min(gross_total * ret_pct, ret_cap_val)

      net_valuation <- gross_total - retention
      prev_paid     <- as_num(input$previous_paid)
      advance       <- as_num(input$advance_repaid)

      due_net <- net_valuation - prev_paid - advance

      vat_amt <- due_net * as_num(input$vat_pct) / 100
      lev_amt <- due_net * as_num(input$levies_pct) / 100
      payable <- due_net + vat_amt + lev_amt

      tibble::tibble(
        Item   = c("Gross value of work done to date",
                   "Materials on site",
                   "Variations approved this period",
                   "Gross total",
                   sprintf("Less retention (%.1f%%, capped at %.1f%% of contract sum)",
                           as_num(input$retention_pct), as_num(input$retention_cap)),
                   "Net valuation",
                   "Less previous certificates paid",
                   "Less advance payment recouped",
                   "Amount due (net of taxes)",
                   sprintf("Add VAT @ %.1f%%", as_num(input$vat_pct)),
                   sprintf("Add NHIL + GETFund @ %.1f%%", as_num(input$levies_pct)),
                   "AMOUNT PAYABLE THIS CERTIFICATE"),
        Amount = c(gross_wd, mos, var, gross_total,
                   -retention, net_valuation,
                   -prev_paid, -advance, due_net,
                   vat_amt, lev_amt, payable)
      )
    })

    output$cert_summary <- DT::renderDT({
      DT::datatable(cert(), rownames = FALSE,
                    options = list(dom = "t", pageLength = 15)) %>%
        DT::formatCurrency("Amount",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$payable <- renderText({
      df <- cert()
      fmt_money(df$Amount[nrow(df)], settings$currency_symbol)
    })

    output$export_xlsx <- downloadHandler(
      filename = function()
        sprintf("IPC_%s_no%s_%s.xlsx",
                gsub("[^A-Za-z0-9]+", "_", input$project_name %||% "project"),
                input$cert_no %||% "1",
                format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "Certificate")

        money_style <- openxlsx::createStyle(numFmt =
          paste0('"', settings$currency_symbol, ' "#,##0.00'))
        bold        <- openxlsx::createStyle(textDecoration = "bold")
        hdr         <- openxlsx::createStyle(textDecoration = "bold",
                                             fgFill = "#1f4e79", fontColour = "white")

        header_lines <- c(
          settings$practice_name,
          settings$practice_addr,
          paste0(settings$qs_name, " | ", settings$qs_credentials),
          "",
          "INTERIM PAYMENT CERTIFICATE",
          paste("Project:    ", input$project_name),
          paste("Employer:   ", input$employer),
          paste("Contractor: ", input$contractor),
          paste("Certificate no:", input$cert_no),
          paste("Valuation date:", format(input$valuation_date, "%d %B %Y")),
          paste("Issue date:    ", format(input$issue_date,     "%d %B %Y")),
          paste("Due date:      ", format(input$due_date,       "%d %B %Y")),
          ""
        )
        for (i in seq_along(header_lines))
          openxlsx::writeData(wb, "Certificate", header_lines[i], startRow = i, startCol = 1)
        openxlsx::addStyle(wb, "Certificate", hdr, rows = 5, cols = 1)

        start_row <- length(header_lines) + 1
        openxlsx::writeData(wb, "Certificate", wd_calc(),
                            startRow = start_row, startCol = 1)
        openxlsx::addStyle(wb, "Certificate", hdr,
                           rows = start_row, cols = 1:7, gridExpand = TRUE)

        sum_row <- start_row + nrow(wd_calc()) + 3
        openxlsx::writeData(wb, "Certificate", cert(),
                            startRow = sum_row, startCol = 1)
        openxlsx::addStyle(wb, "Certificate", hdr,
                           rows = sum_row, cols = 1:2)
        openxlsx::addStyle(wb, "Certificate", money_style,
                           rows = (sum_row + 1):(sum_row + nrow(cert())),
                           cols = 2, gridExpand = TRUE, stack = TRUE)
        openxlsx::addStyle(wb, "Certificate", bold,
                           rows = sum_row + nrow(cert()),
                           cols = 1:2, gridExpand = TRUE, stack = TRUE)
        openxlsx::setColWidths(wb, "Certificate", cols = 1, widths = 55)
        openxlsx::setColWidths(wb, "Certificate", cols = 2:7, widths = 18)

        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    output$export_csv <- downloadHandler(
      filename = function() sprintf("IPC_breakdown_%s.csv",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) readr::write_csv(wd_calc(), file)
    )
  })
}
