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
  })
}
