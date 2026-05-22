# Interim Payment Certificate module
#
# Two variants matching real-world templates:
#  1. Main Contractor IPC  - Barry Callebaut / SPEKTRA style with "I/We certify"
#     block, monthly valuation (PREV / CURRENT / CUM columns), materials on
#     site, materials in transit, retention, VAT, NHIL/GETFund levies.
#  2. Subcontractor IPC    - Thoroughbred / Results Plumbing style with
#     advance payment (e.g. 70 percent) recovery and A-G letter-coded
#     certificate body.
#
# Both produce a styled Excel workbook for issue to client/contractor.

mod_ipc_ui <- function(id) {
  ns <- NS(id)
  bslib::navset_card_tab(
    id = ns("ipc_tabs"),

    # ------------------------------------------------------------------
    bslib::nav_panel(
      "Main Contractor IPC",
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("file-earmark-medical"),
                             " Certificate header"),
          bslib::layout_columns(
            col_widths = c(6, 6),
            textInput(ns("mc_project"),    "Project / works known as",
                      value = "Proposed Security Post, Drive and Walkway"),
            textInput(ns("mc_location"),   "Situated at",
                      value = "Tema Free Zones"),
            textInput(ns("mc_employer"),   "Employer",
                      value = "Barry Callebaut"),
            textInput(ns("mc_contractor"), "Main Contractor",
                      value = "SPEKTRA GLOBAL LIMITED"),
            textInput(ns("mc_contractor_addr"), "Contractor address",
                      value = "Tema, Ghana"),
            textInput(ns("mc_architect"),  "Architect / consultant",
                      value = "")
          ),
          bslib::layout_columns(
            col_widths = c(3, 3, 3, 3),
            numericInput(ns("mc_cert_no"), "Certificate no.", value = 1,
                         min = 1, step = 1),
            textInput(ns("mc_serial"),   "Serial / ref",
                      value = "SG/PROJ/IPC/01"),
            dateInput(ns("mc_val_date"), "Valuation date",
                      value = Sys.Date()),
            dateInput(ns("mc_due_date"), "Due date",
                      value = Sys.Date() + 14)
          )
        ),
        bslib::value_box(
          title    = "Amount payable this certificate",
          value    = textOutput(ns("mc_payable")),
          showcase = bsicons::bs_icon("currency-exchange"),
          theme    = "success"
        )
      ),

      bslib::card(
        bslib::card_header(bsicons::bs_icon("table"),
                           " Monthly valuation - work done by item"),
        helpText("Columns mirror the Barry Callebaut general summary: ",
                 "BOQ amount, cumulative previous work done, work done this ",
                 "period, total to date. Use the button to pull live trade ",
                 "totals from the BOQ tab as a starting point."),
        bslib::layout_columns(
          col_widths = c(3, 3, 3, 3),
          actionButton(ns("mc_pull_boq"), "Pull from BOQ",
                       class = "btn-outline-primary", icon = icon("download")),
          actionButton(ns("mc_pull_vo"),  "Pull approved VOs",
                       class = "btn-outline-primary", icon = icon("plus-circle")),
          actionButton(ns("mc_add"),      "Add row",
                       class = "btn-success", icon = icon("plus")),
          actionButton(ns("mc_del"),      "Delete selected",
                       class = "btn-outline-danger", icon = icon("trash"))
        ),
        DT::DTOutput(ns("mc_val_tbl"))
      ),

      bslib::layout_columns(
        col_widths = c(6, 6),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("boxes"),
                             " Materials on site"),
          bslib::layout_columns(
            col_widths = c(6, 6),
            actionButton(ns("mc_add_mos"), "Add material",
                         class = "btn-success btn-sm", icon = icon("plus")),
            actionButton(ns("mc_del_mos"), "Delete selected",
                         class = "btn-outline-danger btn-sm", icon = icon("trash"))
          ),
          DT::DTOutput(ns("mc_mos_tbl"))
        ),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("sliders2"),
                             " Contract & deductions"),
          currency_input(ns("mc_contract_sum"), "Total contract sum (incl. VAT & contingency)",
                         value = 1165965.69),
          currency_input(ns("mc_prev_certified"),
                         "Total amount previously certified",
                         value = 779548.37),
          currency_input(ns("mc_advance_outstanding"),
                         "Outstanding advance payment to recoup",
                         value = 0),
          bslib::layout_columns(
            col_widths = c(6, 6),
            numericInput(ns("mc_retention_pct"), "Retention %",
                         value = 10, min = 0, max = 25, step = 0.5),
            numericInput(ns("mc_retention_cap"), "Cap (% of contract sum)",
                         value = 5, min = 0, max = 25, step = 0.5)
          ),
          bslib::layout_columns(
            col_widths = c(4, 4, 4),
            numericInput(ns("mc_vat_pct"),     "VAT %",
                         value = 12.5, min = 0, max = 30, step = 0.5),
            numericInput(ns("mc_levies_pct"),  "NHIL+GETFund+Covid %",
                         value = 6, min = 0, max = 30, step = 0.5),
            numericInput(ns("mc_wht_pct"),     "Withholding tax %",
                         value = 5, min = 0, max = 30, step = 0.5)
          ),
          checkboxInput(ns("mc_apply_wht"),
                        "Apply withholding tax (5 percent on construction)",
                        value = TRUE)
        )
      ),

      bslib::card(
        bslib::card_header(bsicons::bs_icon("file-text"),
                           " Certificate body (A through G)"),
        DT::DTOutput(ns("mc_cert_body")),
        bslib::layout_columns(
          col_widths = c(6, 6),
          downloadButton(ns("mc_export_xlsx"),
                         "Export IPC (Excel - styled like Barry Callebaut template)",
                         class = "btn-primary mt-3"),
          downloadButton(ns("mc_export_breakdown"),
                         "Export valuation breakdown (CSV)",
                         class = "btn-outline-secondary mt-3")
        )
      )
    ),

    # ------------------------------------------------------------------
    bslib::nav_panel(
      "Subcontractor IPC",
      helpText("Subcontractor IPC structure matching the Thoroughbred / ",
               "Results Plumbing format. Use this for package contracts with ",
               "an advance mobilisation payment (typically 70 percent) ",
               "recovered against work done."),
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("file-earmark-medical"),
                             " Subcontract IPC header"),
          bslib::layout_columns(
            col_widths = c(6, 6),
            textInput(ns("sc_project"), "Project",
                      value = "Thoroughbred Place"),
            textInput(ns("sc_scope"),   "Detailed scope",
                      value = "Substructure plumbing works"),
            textInput(ns("sc_subcontractor"),
                      "Subcontractor name & contact",
                      value = "Results Plumbing and Civil Engineering - 055 778 1321"),
            textInput(ns("sc_serial"),   "Certificate ref",
                      value = "SG/TBRED/SUBPLUM/IPC02")
          ),
          bslib::layout_columns(
            col_widths = c(4, 4, 4),
            numericInput(ns("sc_cert_no"), "Certificate no.", value = 2,
                         min = 1, step = 1),
            dateInput(ns("sc_date"), "Certificate date", value = Sys.Date()),
            textInput(ns("sc_prepared_by"), "Prepared by",
                      value = "Sedem Kwabla Tay")
          )
        ),
        bslib::value_box(
          title    = "Amount now due subcontractor",
          value    = textOutput(ns("sc_due")),
          showcase = bsicons::bs_icon("cash-coin"),
          theme    = "success"
        )
      ),

      bslib::layout_columns(
        col_widths = c(7, 5),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("list-task"),
                             " Subcontract valuation breakdown"),
          helpText("Match the Thoroughbred valuation table - itemised work ",
                   "with previous, current and cumulative quantities/amounts."),
          bslib::layout_columns(
            col_widths = c(6, 6),
            actionButton(ns("sc_add"), "Add item",
                         class = "btn-success", icon = icon("plus")),
            actionButton(ns("sc_del"), "Delete selected",
                         class = "btn-outline-danger", icon = icon("trash"))
          ),
          DT::DTOutput(ns("sc_val_tbl"))
        ),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("sliders2"),
                             " Contract terms"),
          currency_input(ns("sc_contract_sum"), "Contract sum (provisional)",
                         value = 34355),
          numericInput(ns("sc_retention_pct"),  "Retention %",
                       value = 5, min = 0, max = 25, step = 0.5),
          numericInput(ns("sc_advance_pct"),    "Advance payment %",
                       value = 70, min = 0, max = 100, step = 1),
          currency_input(ns("sc_advance_paid"),
                         "Advance payment already paid",
                         value = 26855),
          currency_input(ns("sc_advance_repaid_to_date"),
                         "Advance recouped previously",
                         value = 26855),
          currency_input(ns("sc_prev_certified"),
                         "Total previously certified",
                         value = 26855)
        )
      ),

      bslib::card(
        bslib::card_header(bsicons::bs_icon("file-text"),
                           " Subcontract certificate (A through G)"),
        DT::DTOutput(ns("sc_cert_body")),
        bslib::layout_columns(
          col_widths = c(6, 6),
          downloadButton(ns("sc_export_xlsx"),
                         "Export subcontract IPC (Excel - Thoroughbred style)",
                         class = "btn-primary mt-3"),
          downloadButton(ns("sc_export_breakdown"),
                         "Export valuation (CSV)",
                         class = "btn-outline-secondary mt-3")
        )
      )
    )
  )
}


mod_ipc_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    # =================================================================
    # MAIN CONTRACTOR IPC
    # =================================================================

    mc_val <- reactiveVal(
      tibble::tibble(
        item        = c("1", "2", "3", "4", "5"),
        description = c("Security Post",
                        "Drive and walkway",
                        "Variation Order 1",
                        "Variation Order 2",
                        "Variation Order 3"),
        boq_amount      = c(406635.91, 290541, 56013.50, 289132.15, 47365),
        cum_prev_amount = c(251635.91, 3000, 133506, 346017, 0),
        current_amount  = c(0, 0, 147507.50, 32016.15, 176005)
      )
    )

    mc_mos <- reactiveVal(
      tibble::tibble(
        description = c("Black soil", "Wall tiles",
                        "Street light poles", "Street lights"),
        quantity = c(1, 3, 2, 2),
        unit     = c("trip", "boxes", "nr", "nr"),
        rate     = c(2500, 200, 2000, 4000)
      )
    )

    observeEvent(input$mc_pull_boq, {
      boq <- app_state$boq
      if (is.null(boq) || !nrow(boq)) {
        showNotification("No BOQ in memory. Load or build a BOQ first.",
                         type = "warning"); return()
      }
      df <- boq_summary_by_trade(boq) %>%
        dplyr::transmute(item = as.character(dplyr::row_number()),
                         description = .data$trade,
                         boq_amount  = .data$total,
                         cum_prev_amount = 0,
                         current_amount  = 0)
      mc_val(df)
      showNotification("Pulled trade totals from BOQ.", type = "message")
    })

    observeEvent(input$mc_pull_vo, {
      vo <- app_state$vo
      if (is.null(vo) || !nrow(vo)) {
        showNotification("No variations to pull. Add some in the Valuations tab.",
                         type = "warning"); return()
      }
      approved <- vo %>% dplyr::filter(.data$status == "Approved")
      if (!nrow(approved)) {
        showNotification("No approved variations.", type = "warning"); return()
      }
      add <- approved %>%
        dplyr::transmute(
          item = sprintf("VO-%s", .data$vo_no),
          description = paste("Variation:", .data$description),
          boq_amount  = as_num(.data$addition) - as_num(.data$omission),
          cum_prev_amount = 0,
          current_amount = 0
        )
      mc_val(dplyr::bind_rows(mc_val(), add))
      showNotification(sprintf("Added %d approved VO(s).", nrow(add)),
                       type = "message")
    })

    observeEvent(input$mc_add, {
      mc_val(dplyr::bind_rows(mc_val(), tibble::tibble(
        item = as.character(nrow(mc_val()) + 1),
        description = "New item", boq_amount = 0,
        cum_prev_amount = 0, current_amount = 0
      )))
    })

    observeEvent(input$mc_del, {
      sel <- input$mc_val_tbl_rows_selected
      if (length(sel)) mc_val(mc_val()[-sel, , drop = FALSE])
    })

    mc_val_calc <- reactive({
      mc_val() %>%
        dplyr::mutate(
          boq_amount      = as_num(.data$boq_amount),
          cum_prev_amount = as_num(.data$cum_prev_amount),
          current_amount  = as_num(.data$current_amount),
          cum_total = round(.data$cum_prev_amount + .data$current_amount, 2)
        )
    })

    output$mc_val_tbl <- DT::renderDT({
      df <- mc_val_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "cum_total") - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(15),
        colnames = c("Item", "Description", "BOQ amount",
                     "Cum. previous", "This period",
                     "Cum. total")
      ) %>%
        DT::formatCurrency(c("boq_amount", "cum_prev_amount",
                             "current_amount", "cum_total"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$mc_val_tbl_cell_edit, {
      info <- input$mc_val_tbl_cell_edit
      df <- mc_val()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("boq_amount", "cum_prev_amount", "current_amount")) {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      mc_val(df)
    })

    # Materials on site
    observeEvent(input$mc_add_mos, {
      mc_mos(dplyr::bind_rows(mc_mos(), tibble::tibble(
        description = "New material", quantity = 0, unit = "nr", rate = 0
      )))
    })
    observeEvent(input$mc_del_mos, {
      sel <- input$mc_mos_tbl_rows_selected
      if (length(sel)) mc_mos(mc_mos()[-sel, , drop = FALSE])
    })

    mc_mos_calc <- reactive({
      mc_mos() %>%
        dplyr::mutate(quantity = as_num(.data$quantity),
                      rate     = as_num(.data$rate),
                      amount   = round(.data$quantity * .data$rate, 2))
    })

    output$mc_mos_tbl <- DT::renderDT({
      df <- mc_mos_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "amount") - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(8),
        colnames = c("Description", "Quantity", "Unit", "Rate", "Amount")
      ) %>%
        DT::formatCurrency(c("rate", "amount"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$mc_mos_tbl_cell_edit, {
      info <- input$mc_mos_tbl_cell_edit
      df <- mc_mos()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("quantity", "rate")) {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      mc_mos(df)
    })

    # Main Contractor certificate calculation
    mc_cert <- reactive({
      val <- mc_val_calc()
      mos <- mc_mos_calc()

      cum_prev    <- sum(val$cum_prev_amount, na.rm = TRUE)
      this_period <- sum(val$current_amount, na.rm = TRUE)
      cum_total   <- cum_prev + this_period

      mos_total <- sum(mos$amount, na.rm = TRUE)

      gross_value <- cum_total + mos_total

      contract_sum <- as_num(input$mc_contract_sum)
      ret_pct      <- as_num(input$mc_retention_pct) / 100
      ret_cap      <- contract_sum * as_num(input$mc_retention_cap) / 100
      retention    <- min(cum_total * ret_pct, ret_cap)

      net_after_retention <- gross_value - retention

      vat_amt <- net_after_retention * as_num(input$mc_vat_pct) / 100
      lev_amt <- net_after_retention * as_num(input$mc_levies_pct) / 100

      gross_payable <- net_after_retention + vat_amt + lev_amt

      wht <- if (isTRUE(input$mc_apply_wht))
        gross_payable * as_num(input$mc_wht_pct) / 100 else 0

      prev_cert  <- as_num(input$mc_prev_certified)
      adv_recoup <- as_num(input$mc_advance_outstanding)

      amount_now_due <- gross_payable - wht - prev_cert - adv_recoup

      tibble::tibble(
        code = c("",
                 "A", "B", "C",
                 "",
                 "D", "E",
                 "",
                 "F", "G",
                 "",
                 "H", "I",
                 "",
                 "J", "K"),
        Item = c("VALUATION OF WORK DONE",
                 "Total value of work executed previously",
                 "Total value of work done this month",
                 sprintf("Total value of work executed as at %s",
                         format(input$mc_val_date %||% Sys.Date(), "%d %B %Y")),
                 "MATERIALS",
                 "Materials on site",
                 "GROSS VALUE OF WORK DONE",
                 "RETENTION",
                 sprintf("Less retention (%.1f%%, capped at %.1f%% of contract sum)",
                         as_num(input$mc_retention_pct),
                         as_num(input$mc_retention_cap)),
                 "AMOUNT NOW CERTIFIED (net of retention)",
                 "TAXES & LEVIES",
                 sprintf("Add NHIL + GETFund + Covid levies @ %.1f%%",
                         as_num(input$mc_levies_pct)),
                 sprintf("Add VAT @ %.1f%%", as_num(input$mc_vat_pct)),
                 "DEDUCTIONS",
                 sprintf("Less withholding tax @ %.1f%% (if applicable)",
                         as_num(input$mc_wht_pct)),
                 "AMOUNT NOW DUE TO CONTRACTOR"),
        Amount = c(NA,
                   cum_prev, this_period, cum_total,
                   NA,
                   mos_total, gross_value,
                   NA,
                   -retention, net_after_retention,
                   NA,
                   lev_amt, vat_amt,
                   NA,
                   -wht, amount_now_due)
      )
    })

    output$mc_cert_body <- DT::renderDT({
      DT::datatable(mc_cert(), rownames = FALSE,
                    options = list(dom = "t", pageLength = 20),
                    colnames = c("Code", "Item", "Amount")) %>%
        DT::formatCurrency("Amount",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$mc_payable <- renderText({
      df <- mc_cert()
      fmt_money(df$Amount[nrow(df)], settings$currency_symbol)
    })

    output$mc_export_xlsx <- downloadHandler(
      filename = function()
        sprintf("IPC_MainContractor_%s_no%s_%s.xlsx",
                gsub("[^A-Za-z0-9]+", "_", input$mc_project %||% "project"),
                input$mc_cert_no %||% "1",
                format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        write_main_contractor_ipc(
          file, settings,
          project = input$mc_project, location = input$mc_location,
          employer = input$mc_employer, contractor = input$mc_contractor,
          contractor_addr = input$mc_contractor_addr,
          architect = input$mc_architect,
          cert_no  = input$mc_cert_no, serial = input$mc_serial,
          val_date = input$mc_val_date, due_date = input$mc_due_date,
          val_table = mc_val_calc(), mos_table = mc_mos_calc(),
          cert_body = mc_cert(),
          contract_sum = as_num(input$mc_contract_sum)
        )
      }
    )

    output$mc_export_breakdown <- downloadHandler(
      filename = function() sprintf("IPC_breakdown_%s.csv",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) readr::write_csv(mc_val_calc(), file)
    )

    # =================================================================
    # SUBCONTRACTOR IPC
    # =================================================================

    sc_val <- reactiveVal(
      tibble::tibble(
        item = c("1", "2"),
        description = c("Total Material cost", "Total Labour cost"),
        unit = c("item", "item"),
        budget_amount = c(26855, 7500),
        prev_pct = c(100, 100),
        current_pct = c(0, 0)
      )
    )

    observeEvent(input$sc_add, {
      sc_val(dplyr::bind_rows(sc_val(), tibble::tibble(
        item = as.character(nrow(sc_val()) + 1),
        description = "New item", unit = "item",
        budget_amount = 0, prev_pct = 0, current_pct = 0
      )))
    })
    observeEvent(input$sc_del, {
      sel <- input$sc_val_tbl_rows_selected
      if (length(sel)) sc_val(sc_val()[-sel, , drop = FALSE])
    })

    sc_val_calc <- reactive({
      sc_val() %>%
        dplyr::mutate(
          budget_amount = as_num(.data$budget_amount),
          prev_pct      = as_num(.data$prev_pct),
          current_pct   = as_num(.data$current_pct),
          cum_pct       = pmin(100, .data$prev_pct + .data$current_pct),
          prev_amount   = round(.data$budget_amount * .data$prev_pct / 100, 2),
          current_amount= round(.data$budget_amount * .data$current_pct / 100, 2),
          cum_amount    = round(.data$prev_amount + .data$current_amount, 2)
        )
    })

    output$sc_val_tbl <- DT::renderDT({
      df <- sc_val_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) %in%
                          c("cum_pct", "prev_amount", "current_amount",
                            "cum_amount")) - 1)),
        selection = "multiple", rownames = FALSE,
        options = dt_editable_opts(12),
        colnames = c("Item", "Description", "Unit", "Budget",
                     "Prev %", "Current %", "Cum %",
                     "Prev amt", "Current amt", "Cum amt")
      ) %>%
        DT::formatCurrency(c("budget_amount", "prev_amount",
                             "current_amount", "cum_amount"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$sc_val_tbl_cell_edit, {
      info <- input$sc_val_tbl_cell_edit
      df <- sc_val()
      col_name <- names(df)[info$col + 1]
      if (col_name %in% c("budget_amount", "prev_pct", "current_pct")) {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      sc_val(df)
    })

    # Subcontractor certificate calculation (A through G)
    sc_cert <- reactive({
      val <- sc_val_calc()
      contract_sum <- as_num(input$sc_contract_sum)
      ret_pct      <- as_num(input$sc_retention_pct) / 100
      adv_pct      <- as_num(input$sc_advance_pct)  / 100

      # A: Value of work done this period (cumulative)
      A_value_wd  <- sum(val$cum_amount, na.rm = TRUE)

      # B: Retention on value of work done
      B_retention <- A_value_wd * ret_pct

      # C: Sub-Total 1 = A - B
      C_subtotal  <- A_value_wd - B_retention

      # D: Advance paid earlier
      D_advance_paid     <- as_num(input$sc_advance_paid)
      D_advance_recouped <- as_num(input$sc_advance_repaid_to_date)
      D_advance_outstanding <- max(0, D_advance_paid - D_advance_recouped)

      # E: Amount now certified = C  (Advance recovery is shown separately)
      E_certified <- C_subtotal

      # F: Less previously certified
      F_prev_cert <- as_num(input$sc_prev_certified)

      # G: Amount now due
      G_due <- E_certified - F_prev_cert

      tibble::tibble(
        code = c("A", "B", "C", "D", "D", "E", "F", "G"),
        Item = c("Value of Work Done (cumulative)",
                 sprintf("Less: Retention (%.1f%%)",
                         as_num(input$sc_retention_pct)),
                 "Sub-Total 1 (A minus B)",
                 sprintf("ADD: Advance Payment (%.0f%%) already paid",
                         as_num(input$sc_advance_pct)),
                 "LESS: Advance payment outstanding to be recouped",
                 "AMOUNT NOW CERTIFIED",
                 "LESS: Amount previously certified",
                 "AMOUNT NOW DUE TO SUBCONTRACTOR"),
        Amount = c(A_value_wd, -B_retention, C_subtotal,
                   D_advance_paid, -D_advance_outstanding,
                   E_certified, -F_prev_cert, G_due)
      )
    })

    output$sc_cert_body <- DT::renderDT({
      DT::datatable(sc_cert(), rownames = FALSE,
                    options = list(dom = "t", pageLength = 10),
                    colnames = c("Code", "Item", "Amount")) %>%
        DT::formatCurrency("Amount",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$sc_due <- renderText({
      df <- sc_cert()
      fmt_money(df$Amount[nrow(df)], settings$currency_symbol)
    })

    output$sc_export_xlsx <- downloadHandler(
      filename = function()
        sprintf("IPC_Subcontractor_%s_no%s_%s.xlsx",
                gsub("[^A-Za-z0-9]+", "_", input$sc_project %||% "project"),
                input$sc_cert_no %||% "1",
                format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        write_subcontractor_ipc(
          file, settings,
          project = input$sc_project, scope = input$sc_scope,
          subcontractor = input$sc_subcontractor, serial = input$sc_serial,
          cert_no = input$sc_cert_no, date = input$sc_date,
          prepared_by = input$sc_prepared_by,
          val_table = sc_val_calc(), cert_body = sc_cert(),
          contract_sum = as_num(input$sc_contract_sum),
          advance_pct = as_num(input$sc_advance_pct)
        )
      }
    )

    output$sc_export_breakdown <- downloadHandler(
      filename = function() sprintf("SubIPC_breakdown_%s.csv",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) readr::write_csv(sc_val_calc(), file)
    )
  })
}
