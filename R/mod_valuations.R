# Valuations & Variations module
#
# Two sub-tabs:
#  - Variation Register: log Architect's Instructions / Variation Orders
#    with omission and addition values, status, and running totals.
#  - Dayworks Sheet: labour / plant / materials at agreed rates + on-costs.

mod_valuations_ui <- function(id) {
  ns <- NS(id)
  bslib::navset_card_tab(
    id = ns("vtabs"),

    # ------------------------------------------------------------------
    bslib::nav_panel(
      "Variation Register",
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("journal-text"),
                             " Variations / Architect's Instructions"),
          helpText("Use omission (-) and addition (+) values per the contract ",
                   "valuation rules. Net effect totals the contract sum impact."),
          bslib::layout_columns(
            col_widths = c(6, 6),
            actionButton(ns("add_vo"), "Add variation",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("del_vo"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash"))
          ),
          DT::DTOutput(ns("vo_table"))
        ),
        bslib::value_box(
          title    = "Net effect on contract sum",
          value    = textOutput(ns("net_effect")),
          showcase = bsicons::bs_icon("plus-slash-minus"),
          theme    = "warning"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("bar-chart-line"),
                           " Variations summary"),
        DT::DTOutput(ns("vo_summary")),
        downloadButton(ns("export_vo"), "Export variation register (Excel)",
                       class = "btn-primary mt-3")
      )
    ),
    bslib::nav_panel(
      "Dayworks Sheet",
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("clock-history"),
                             " Daywork entries"),
          helpText("Record agreed daywork resources. The on-cost % adds ",
                   "overheads, profit and supervision per the contract schedule."),
          bslib::layout_columns(
            col_widths = c(4, 4, 4),
            actionButton(ns("add_dw"), "Add row",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("del_dw"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash")),
            numericInput(ns("dw_oncost"), "On-cost %",
                         value = 25, min = 0, max = 100, step = 1)
          ),
          DT::DTOutput(ns("dw_table"))
        ),
        bslib::value_box(
          title    = "Daywork sheet total (incl. on-cost)",
          value    = textOutput(ns("dw_total")),
          showcase = bsicons::bs_icon("hammer"),
          theme    = "info"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("table"), " Daywork summary"),
        DT::DTOutput(ns("dw_summary")),
        downloadButton(ns("export_dw"), "Export dayworks (Excel)",
                       class = "btn-primary mt-3")
      )
    ),

    # ------------------------------------------------------------------
    bslib::nav_panel(
      "Materials on Site",
      helpText("Materials delivered to site and accepted, but not yet ",
               "incorporated into the works. These typically attract their ",
               "own valuation (subject to vesting/insurance terms) and feed ",
               "into the IPC 'Materials on Site' line."),
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("box-seam"),
                             " Material entries"),
          bslib::layout_columns(
            col_widths = c(4, 4, 4),
            actionButton(ns("add_mos"), "Add material",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("del_mos"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash")),
            dateInput(ns("mos_as_at"), "As at date", value = Sys.Date())
          ),
          DT::DTOutput(ns("mos_table"))
        ),
        bslib::value_box(
          title    = "Total materials on site",
          value    = textOutput(ns("mos_total")),
          showcase = bsicons::bs_icon("boxes"),
          theme    = "info"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("table"),
                           " Materials summary by category"),
        DT::DTOutput(ns("mos_summary")),
        downloadButton(ns("export_mos"),
                       "Export materials on site (Excel)",
                       class = "btn-primary mt-3")
      )
    ),

    # ------------------------------------------------------------------
    bslib::nav_panel(
      "Final Account",
      helpText("Final account summary mirrors the Spektra / Barry Callebaut ",
               "format - original contract sum less contingency, plus net ",
               "variations (including additional preliminaries), less ",
               "withholding tax and total payments received."),
      bslib::layout_columns(
        col_widths = c(4, 8),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("sliders2"),
                             " Inputs"),
          textInput(ns("fa_project"), "Project",
                    value = "Proposed Security Post, Drive and Walkway"),
          textInput(ns("fa_location"), "Location",
                    value = "Tema Free Zones"),
          currency_input(ns("fa_contract_sum"),
                         "Original contract sum (incl. contingency)",
                         value = 820577.22),
          numericInput(ns("fa_contingency_pct"),
                       "Contingency % originally included",
                       value = 10, min = 0, max = 30, step = 0.5),
          numericInput(ns("fa_prelims_pct"),
                       "Preliminaries % on net variations",
                       value = 7, min = 0, max = 30, step = 0.5),
          numericInput(ns("fa_wht_pct"),
                       "Withholding tax %",
                       value = 5, min = 0, max = 30, step = 0.5),
          currency_input(ns("fa_total_paid"),
                         "Total payment received to date",
                         value = 779548.37),
          actionButton(ns("fa_pull_vo"),
                       "Pull net variations from VO register",
                       class = "btn-outline-primary",
                       icon = icon("plus-circle")),
          currency_input(ns("fa_net_variations"),
                         "Net variations (omissions + additions)",
                         value = 392510.65)
        ),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("file-earmark-spreadsheet"),
                             " Final account statement"),
          DT::DTOutput(ns("fa_statement")),
          downloadButton(ns("export_fa"),
                         "Export final account (Excel)",
                         class = "btn-primary mt-3")
        )
      )
    )
  )
}

mod_valuations_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    # --- Variations -------------------------------------------------------
    vo <- reactiveVal(
      tibble::tibble(
        vo_no = c("VO-001", "VO-002"),
        date  = as.Date(c("2026-02-15", "2026-03-20")),
        description = c("Upgrade external wall finish from paint to stone cladding",
                        "Omit timber doors, substitute with steel doors"),
        omission = c(0, 28500),
        addition = c(78400, 41200),
        status   = c("Approved", "Pending"),
        instruction_ref = c("AI-007", "AI-011")
      )
    )

    observeEvent(input$add_vo, {
      vo(dplyr::bind_rows(vo(), tibble::tibble(
        vo_no = sprintf("VO-%03d", nrow(vo()) + 1),
        date = Sys.Date(),
        description = "New variation",
        omission = 0, addition = 0,
        status = "Pending", instruction_ref = ""
      )))
    })

    observeEvent(input$del_vo, {
      sel <- input$vo_table_rows_selected
      if (length(sel)) vo(vo()[-sel, , drop = FALSE])
    })

    vo_calc <- reactive({
      vo() %>%
        dplyr::mutate(
          omission = as_num(.data$omission),
          addition = as_num(.data$addition),
          net_effect = round(.data$addition - .data$omission, 2)
        )
    })

    # Share VO register with other modules (IPC pulls approved VOs)
    observe({ app_state$vo <- vo_calc() })

    output$vo_table <- DT::renderDT({
      df <- vo_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "net_effect") - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("VO no", "Date", "Description", "Omission", "Addition",
                     "Status", "Instruction ref", "Net effect")
      ) %>%
        DT::formatCurrency(c("omission", "addition", "net_effect"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$vo_table_cell_edit, {
      info <- input$vo_table_cell_edit
      df <- vo()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("omission", "addition")) {
        df[info$row, col_name] <- as_num(info$value)
      } else if (col_name == "date") {
        df[info$row, col_name] <- suppressWarnings(as.Date(info$value))
      } else {
        df[info$row, col_name] <- info$value
      }
      vo(df)
    })

    output$vo_summary <- DT::renderDT({
      df <- vo_calc() %>%
        dplyr::group_by(.data$status) %>%
        dplyr::summarise(count = dplyr::n(),
                         omission = sum(.data$omission),
                         addition = sum(.data$addition),
                         net      = sum(.data$net_effect),
                         .groups = "drop")
      DT::datatable(df, rownames = FALSE,
                    options = list(dom = "t")) %>%
        DT::formatCurrency(c("omission", "addition", "net"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$net_effect <- renderText({
      total <- sum(vo_calc()$net_effect, na.rm = TRUE)
      fmt_money(total, settings$currency_symbol)
    })

    output$export_vo <- downloadHandler(
      filename = function() sprintf("Variation_Register_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "Variations")
        openxlsx::writeData(wb, "Variations", vo_calc())
        openxlsx::setColWidths(wb, "Variations", cols = 1:8,
                               widths = c(10, 12, 60, 15, 15, 12, 15, 15))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    # --- Dayworks ---------------------------------------------------------
    dw <- reactiveVal(
      tibble::tibble(
        date     = as.Date("2026-04-10") + 0:2,
        category = c("Labour", "Labour", "Plant"),
        description = c("Skilled mason - additional concrete chasing",
                        "Unskilled labourer - assisting mason",
                        "Petrol breaker hire incl operator"),
        unit     = c("hr", "hr", "hr"),
        quantity = c(16, 24, 8),
        rate     = c(45, 22, 95)
      )
    )

    observeEvent(input$add_dw, {
      dw(dplyr::bind_rows(dw(), tibble::tibble(
        date = Sys.Date(), category = "Labour",
        description = "New daywork entry", unit = "hr",
        quantity = 0, rate = 0
      )))
    })

    observeEvent(input$del_dw, {
      sel <- input$dw_table_rows_selected
      if (length(sel)) dw(dw()[-sel, , drop = FALSE])
    })

    dw_calc <- reactive({
      oncost <- as_num(input$dw_oncost) / 100
      dw() %>%
        dplyr::mutate(
          quantity = as_num(.data$quantity),
          rate     = as_num(.data$rate),
          net      = round(.data$quantity * .data$rate, 2),
          oncost_amt = round(.data$net * oncost, 2),
          total    = round(.data$net + .data$oncost_amt, 2)
        )
    })

    output$dw_table <- DT::renderDT({
      df <- dw_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) %in%
                                       c("net", "oncost_amt", "total")) - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Date", "Category", "Description", "Unit", "Qty", "Rate",
                     "Net", "On-cost", "Total")
      ) %>%
        DT::formatCurrency(c("rate", "net", "oncost_amt", "total"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$dw_table_cell_edit, {
      info <- input$dw_table_cell_edit
      df <- dw()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("quantity", "rate")) {
        df[info$row, col_name] <- as_num(info$value)
      } else if (col_name == "date") {
        df[info$row, col_name] <- suppressWarnings(as.Date(info$value))
      } else {
        df[info$row, col_name] <- info$value
      }
      dw(df)
    })

    output$dw_summary <- DT::renderDT({
      df <- dw_calc() %>%
        dplyr::group_by(.data$category) %>%
        dplyr::summarise(entries = dplyr::n(),
                         net = sum(.data$net),
                         oncost = sum(.data$oncost_amt),
                         total = sum(.data$total),
                         .groups = "drop")
      DT::datatable(df, rownames = FALSE,
                    options = list(dom = "t")) %>%
        DT::formatCurrency(c("net", "oncost", "total"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$dw_total <- renderText({
      fmt_money(sum(dw_calc()$total, na.rm = TRUE), settings$currency_symbol)
    })

    output$export_dw <- downloadHandler(
      filename = function() sprintf("Dayworks_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "Dayworks")
        openxlsx::writeData(wb, "Dayworks", dw_calc())
        openxlsx::setColWidths(wb, "Dayworks", cols = 1:9,
                               widths = c(12, 12, 50, 8, 10, 12, 14, 14, 14))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    # ---- Materials on Site ----------------------------------------------
    mos <- reactiveVal(
      tibble::tibble(
        category = c("Aggregates", "Finishes", "External works",
                     "External works"),
        description = c("Black soil",
                        "Wall tiles",
                        "Street light poles",
                        "Street lights"),
        quantity = c(1, 3, 2, 2),
        unit     = c("trip", "boxes", "nr", "nr"),
        rate     = c(2500, 200, 2000, 4000),
        delivery_note = c("DN-001", "DN-014", "DN-027", "DN-028")
      )
    )

    observeEvent(input$add_mos, {
      mos(dplyr::bind_rows(mos(), tibble::tibble(
        category = "Materials", description = "New material",
        quantity = 0, unit = "nr", rate = 0, delivery_note = ""
      )))
    })

    observeEvent(input$del_mos, {
      sel <- input$mos_table_rows_selected
      if (length(sel)) mos(mos()[-sel, , drop = FALSE])
    })

    mos_calc <- reactive({
      mos() %>%
        dplyr::mutate(
          quantity = as_num(.data$quantity),
          rate     = as_num(.data$rate),
          amount   = round(.data$quantity * .data$rate, 2)
        )
    })

    output$mos_table <- DT::renderDT({
      df <- mos_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "amount") - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Category", "Description", "Qty", "Unit", "Rate",
                     "Delivery note", "Amount")
      ) %>%
        DT::formatCurrency(c("rate", "amount"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$mos_table_cell_edit, {
      info <- input$mos_table_cell_edit
      df <- mos()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("quantity", "rate")) {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      mos(df)
    })

    output$mos_summary <- DT::renderDT({
      df <- mos_calc() %>%
        dplyr::group_by(.data$category) %>%
        dplyr::summarise(items = dplyr::n(),
                         total = sum(.data$amount), .groups = "drop")
      DT::datatable(df, rownames = FALSE,
                    options = list(dom = "t")) %>%
        DT::formatCurrency("total",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$mos_total <- renderText({
      fmt_money(sum(mos_calc()$amount, na.rm = TRUE), settings$currency_symbol)
    })

    output$export_mos <- downloadHandler(
      filename = function() sprintf("Materials_on_Site_%s.xlsx",
                                    format(input$mos_as_at, "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "MaterialsOnSite")
        openxlsx::writeData(wb, "MaterialsOnSite",
                            sprintf("MATERIALS ON SITE AS AT %s",
                                    format(input$mos_as_at, "%d %B %Y")),
                            startRow = 1, startCol = 1)
        openxlsx::writeData(wb, "MaterialsOnSite", mos_calc(),
                            startRow = 3, startCol = 1)
        openxlsx::setColWidths(wb, "MaterialsOnSite", cols = 1:7,
                               widths = c(18, 40, 10, 10, 14, 16, 16))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    # Expose materials on site to other modules (IPC can pull)
    observe({ app_state$mos <- mos_calc() })

    # ---- Final Account ---------------------------------------------------
    observeEvent(input$fa_pull_vo, {
      net <- sum(vo_calc()$net_effect, na.rm = TRUE)
      updateNumericInput(session, "fa_net_variations", value = net)
      showNotification(sprintf("Pulled net variations: %s",
                              fmt_money(net, settings$currency_symbol)),
                       type = "message")
    })

    fa_calc <- reactive({
      contract_sum <- as_num(input$fa_contract_sum)
      cont_pct     <- as_num(input$fa_contingency_pct) / 100
      prelims_pct  <- as_num(input$fa_prelims_pct) / 100
      wht_pct      <- as_num(input$fa_wht_pct) / 100
      net_var      <- as_num(input$fa_net_variations)
      total_paid   <- as_num(input$fa_total_paid)

      contingency_amt <- contract_sum * cont_pct / (1 + cont_pct)
      # ^ if contract sum includes contingency, contingency = sum * c/(1+c)
      # Better: ask the user instead. For now treat contingency_pct as % of
      # contract sum.
      contingency_amt <- contract_sum * cont_pct
      subtotal_1      <- contract_sum - contingency_amt
      prelims_on_var  <- net_var * prelims_pct
      net_var_total   <- net_var + prelims_on_var
      revised_sum     <- subtotal_1 + net_var_total
      wht_amt         <- revised_sum * wht_pct
      revised_net_wht <- revised_sum - wht_amt
      outstanding     <- revised_net_wht - total_paid

      tibble::tibble(
        code   = c("A", "B", "", "C", "C", "", "", "D", ""),
        Item   = c("Original Contract sum (including contingency)",
                   sprintf("Less Contingency @ %.1f%%",
                           as_num(input$fa_contingency_pct)),
                   "Sub-total 1",
                   sprintf("Add net variations (omission + addition)"),
                   sprintf("Add Preliminaries @ %.1f%% on variations",
                           as_num(input$fa_prelims_pct)),
                   "Revised Contract Sum (Final)",
                   sprintf("Less Withholding Tax @ %.1f%%",
                           as_num(input$fa_wht_pct)),
                   "Less Total Payments Received",
                   "OUTSTANDING PAYMENT DUE TO CONTRACTOR"),
        Amount = c(contract_sum, -contingency_amt, subtotal_1,
                   net_var, prelims_on_var, revised_sum,
                   -wht_amt, -total_paid, outstanding)
      )
    })

    output$fa_statement <- DT::renderDT({
      DT::datatable(fa_calc(), rownames = FALSE,
                    options = list(dom = "t", pageLength = 12),
                    colnames = c("Code", "Item", "Amount")) %>%
        DT::formatCurrency("Amount",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$export_fa <- downloadHandler(
      filename = function() sprintf("Final_Account_%s_%s.xlsx",
                                    gsub("[^A-Za-z0-9]+", "_",
                                         input$fa_project %||% "project"),
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "FinalAccount")
        sym <- settings$currency_symbol
        title_s <- openxlsx::createStyle(textDecoration = "bold", fontSize = 14)
        label_s <- openxlsx::createStyle(textDecoration = "bold")
        money_s <- openxlsx::createStyle(numFmt =
          paste0('"', sym, ' "#,##0.00'))

        openxlsx::writeData(wb, "FinalAccount",
                            sprintf("FINAL ACCOUNT SUMMARY - %s",
                                    input$fa_project),
                            startRow = 1, startCol = 1)
        openxlsx::addStyle(wb, "FinalAccount", title_s, rows = 1, cols = 1)
        openxlsx::writeData(wb, "FinalAccount",
                            sprintf("Location: %s",
                                    input$fa_location),
                            startRow = 2, startCol = 1)
        openxlsx::writeData(wb, "FinalAccount",
                            sprintf("Date: %s",
                                    format(Sys.Date(), "%d %B %Y")),
                            startRow = 3, startCol = 1)

        df <- fa_calc()
        openxlsx::writeData(wb, "FinalAccount", df,
                            startRow = 5, startCol = 1)
        n <- nrow(df)
        openxlsx::addStyle(wb, "FinalAccount", label_s, rows = 5, cols = 1:3,
                           gridExpand = TRUE)
        openxlsx::addStyle(wb, "FinalAccount", money_s, rows = 6:(5 + n),
                           cols = 3, gridExpand = TRUE, stack = TRUE)
        openxlsx::setColWidths(wb, "FinalAccount", cols = 1:3,
                               widths = c(8, 55, 18))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )
  })
}
