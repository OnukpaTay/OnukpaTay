# Budgeting & Cost Planning module
#
# Two views:
#  - Elemental cost plan (NRM1 elements, GIFA based)
#  - Cash flow forecast: S-curve over the contract period

mod_budgeting_ui <- function(id) {
  ns <- NS(id)
  bslib::navset_card_tab(
    id = ns("btabs"),

    bslib::nav_panel(
      "Elemental Cost Plan",
      bslib::layout_columns(
        col_widths = c(8, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("buildings"),
                             " Project parameters"),
          bslib::layout_columns(
            col_widths = c(4, 4, 4),
            textInput(ns("project"), "Project",
                      value = "Mixed-use building, Accra"),
            numericInput(ns("gifa"), "Gross internal floor area (m²)",
                         value = 1800, min = 1),
            numericInput(ns("storeys"), "Number of storeys",
                         value = 3, min = 1)
          )
        ),
        bslib::value_box(
          title    = "Total construction cost",
          value    = textOutput(ns("ecp_total")),
          showcase = bsicons::bs_icon("graph-up-arrow"),
          theme    = "primary"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("list-columns-reverse"),
                           " Elemental cost plan (NRM1)"),
        helpText("Enter cost per m² GIFA or override the total. ",
                 "Elements default to the NRM1 standard breakdown."),
        bslib::layout_columns(
          col_widths = c(6, 6),
          actionButton(ns("reset_elements"), "Reset to NRM1 elements",
                       class = "btn-outline-secondary", icon = icon("rotate")),
          actionButton(ns("load_demo"), "Load demo costs",
                       class = "btn-outline-primary", icon = icon("file-import"))
        ),
        DT::DTOutput(ns("ecp_table")),
        downloadButton(ns("export_ecp"), "Export cost plan (Excel)",
                       class = "btn-primary mt-3")
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("pie-chart-fill"),
                           " Cost distribution by element group"),
        plotOutput(ns("ecp_plot"), height = "320px")
      )
    ),

    bslib::nav_panel(
      "Cash Flow Forecast",
      bslib::layout_columns(
        col_widths = c(4, 4, 4),
        bslib::card(
          bslib::card_header(bsicons::bs_icon("currency-exchange"),
                             " Inputs"),
          currency_input(ns("cf_contract_sum"), "Contract sum",
                         value = 2500000, settings = DEFAULT_SETTINGS),
          numericInput(ns("cf_months"), "Contract period (months)",
                       value = 12, min = 1, max = 60, step = 1),
          dateInput(ns("cf_start"), "Start date", value = Sys.Date()),
          selectInput(ns("cf_curve"), "S-curve type",
                      choices = c("Standard S-curve (1/4-1/2-1/4)" = "standard",
                                  "Front-loaded" = "front",
                                  "Back-loaded"  = "back",
                                  "Linear"       = "linear"),
                      selected = "standard"),
          numericInput(ns("cf_mob_pct"),
                       "Mobilisation / advance payment %",
                       value = 15, min = 0, max = 30, step = 1)
        ),
        bslib::value_box(
          title    = "Peak monthly cash demand",
          value    = textOutput(ns("cf_peak")),
          showcase = bsicons::bs_icon("graph-up"),
          theme    = "warning"
        ),
        bslib::value_box(
          title    = "Working capital requirement",
          value    = textOutput(ns("cf_wcr")),
          showcase = bsicons::bs_icon("bank2"),
          theme    = "info"
        )
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("activity"),
                           " Monthly cash flow & S-curve"),
        plotOutput(ns("cf_plot"), height = "380px"),
        DT::DTOutput(ns("cf_table")),
        downloadButton(ns("export_cf"), "Export cash flow (Excel)",
                       class = "btn-primary mt-3")
      )
    )
  )
}

mod_budgeting_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    # --- Elemental cost plan ---------------------------------------------
    default_ecp <- function() {
      if (is.null(ELEMENTS_DF) || !nrow(ELEMENTS_DF))
        return(tibble::tibble(element_group = character(),
                              element = character(),
                              cost_per_m2 = numeric()))
      ELEMENTS_DF %>%
        dplyr::transmute(.data$element_group, .data$element,
                         cost_per_m2 = 0)
    }

    ecp <- reactiveVal(default_ecp())

    observeEvent(input$reset_elements, { ecp(default_ecp()) })

    observeEvent(input$load_demo, {
      df <- default_ecp()
      # Indicative cost / m2 rates for a typical Ghanaian commercial build
      demo_rates <- c(
        "Substructure" = 380, "Frame" = 280, "Upper floors" = 220,
        "Roof" = 165, "Stairs and ramps" = 45, "External walls" = 240,
        "Windows and external doors" = 180, "Internal walls and partitions" = 120,
        "Internal doors" = 90, "Wall finishes" = 95, "Floor finishes" = 130,
        "Ceiling finishes" = 85, "Fittings furnishings and equipment" = 110,
        "Sanitary installations" = 60, "Disposal installations" = 70,
        "Water installations" = 90, "Space heating and air conditioning" = 280,
        "Ventilation" = 90, "Electrical installations" = 260,
        "Lift and conveyor installations" = 220,
        "Fire and lightning protection" = 80,
        "Communication security and control" = 100,
        "Builders work in connection" = 45,
        "Site preparation works" = 35, "Roads paths and pavings" = 65,
        "Soft landscaping planting" = 25, "Fencing railings and walls" = 30,
        "External drainage" = 40,
        "Main contractor preliminaries" = 240,
        "Main contractor overheads and profit" = 220,
        "Project / design team fees" = 320,
        "Risk allowance" = 120, "Inflation allowance" = 90
      )
      df$cost_per_m2 <- vapply(df$element,
                               function(e) unname(demo_rates[e]) %||% 0,
                               numeric(1))
      df$cost_per_m2[is.na(df$cost_per_m2)] <- 0
      ecp(df)
    })

    ecp_calc <- reactive({
      gifa <- as_num(input$gifa)
      ecp() %>%
        dplyr::mutate(
          cost_per_m2 = as_num(.data$cost_per_m2),
          total = round(.data$cost_per_m2 * gifa, 2)
        )
    })

    output$ecp_table <- DT::renderDT({
      df <- ecp_calc()
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "total") - 1)),
        rownames = FALSE,
        options = dt_editable_opts(40),
        colnames = c("Element group", "Element", "Cost / m²", "Total")
      ) %>%
        DT::formatCurrency(c("cost_per_m2", "total"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    }, server = FALSE)

    observeEvent(input$ecp_table_cell_edit, {
      info <- input$ecp_table_cell_edit
      df <- ecp()
      col_name <- names(df)[info$col + 1]
      if (col_name == "cost_per_m2") {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      ecp(df)
    })

    output$ecp_total <- renderText({
      fmt_money(sum(ecp_calc()$total, na.rm = TRUE), settings$currency_symbol)
    })

    output$ecp_plot <- renderPlot({
      df <- ecp_calc() %>%
        dplyr::group_by(.data$element_group) %>%
        dplyr::summarise(total = sum(.data$total, na.rm = TRUE), .groups = "drop") %>%
        dplyr::filter(.data$total > 0) %>%
        dplyr::arrange(dplyr::desc(.data$total))
      if (!nrow(df)) {
        plot.new(); title("No costs entered yet"); return()
      }
      ggplot2::ggplot(df,
                      ggplot2::aes(x = stats::reorder(element_group, .data$total),
                                   y = .data$total)) +
        ggplot2::geom_col(fill = "#1f4e79") +
        ggplot2::coord_flip() +
        ggplot2::scale_y_continuous(labels = scales::label_comma(
          prefix = paste0(settings$currency_symbol, " "))) +
        ggplot2::labs(x = NULL, y = "Total cost") +
        ggplot2::theme_minimal(base_size = 12)
    })

    output$export_ecp <- downloadHandler(
      filename = function() sprintf("Elemental_Cost_Plan_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "Cost_Plan")
        header <- c(sprintf("Project: %s", input$project),
                    sprintf("GIFA: %s m2", input$gifa),
                    sprintf("Storeys: %s", input$storeys),
                    sprintf("Total: %s",
                            fmt_money(sum(ecp_calc()$total),
                                      settings$currency_symbol)),
                    "")
        for (i in seq_along(header))
          openxlsx::writeData(wb, "Cost_Plan", header[i],
                              startRow = i, startCol = 1)
        openxlsx::writeData(wb, "Cost_Plan", ecp_calc(),
                            startRow = length(header) + 1)
        openxlsx::setColWidths(wb, "Cost_Plan", cols = 1:4,
                               widths = c(38, 50, 16, 18))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )

    # --- Cash flow forecast ----------------------------------------------
    cf_calc <- reactive({
      n <- max(1L, as.integer(input$cf_months))
      sum_ <- as_num(input$cf_contract_sum)
      mob_pct <- as_num(input$cf_mob_pct) / 100
      curve <- input$cf_curve

      # Build a base weighting vector that sums to 1
      x <- seq(0, 1, length.out = n)
      w <- switch(
        curve,
        "standard" = stats::dbeta(x, shape1 = 2, shape2 = 2),
        "front"    = stats::dbeta(x, shape1 = 1.4, shape2 = 3),
        "back"     = stats::dbeta(x, shape1 = 3, shape2 = 1.4),
        "linear"   = rep(1, n)
      )
      w <- w / sum(w)

      monthly_construction <- (sum_ * (1 - mob_pct)) * w
      mob_row <- c(sum_ * mob_pct, rep(0, n - 1))
      monthly_total <- monthly_construction + mob_row
      cumulative <- cumsum(monthly_total)

      start <- as.Date(input$cf_start)
      months <- seq(start, by = "month", length.out = n)

      tibble::tibble(
        month_no = seq_len(n),
        month    = format(months, "%b %Y"),
        mobilisation = round(mob_row, 2),
        construction = round(monthly_construction, 2),
        monthly_total = round(monthly_total, 2),
        cumulative   = round(cumulative, 2),
        pct_complete = round(cumulative / sum_ * 100, 1)
      )
    })

    output$cf_table <- DT::renderDT({
      DT::datatable(cf_calc(), rownames = FALSE,
                    options = list(pageLength = 12, dom = "tip")) %>%
        DT::formatCurrency(c("mobilisation", "construction",
                             "monthly_total", "cumulative"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$cf_plot <- renderPlot({
      df <- cf_calc()
      long <- df %>%
        dplyr::transmute(.data$month_no,
                         month = factor(.data$month, levels = .data$month),
                         Monthly = .data$monthly_total,
                         Cumulative = .data$cumulative)
      scale_factor <- max(long$Cumulative) / max(long$Monthly)
      if (!is.finite(scale_factor) || scale_factor <= 0) scale_factor <- 1
      ggplot2::ggplot(long, ggplot2::aes(x = .data$month)) +
        ggplot2::geom_col(ggplot2::aes(y = .data$Monthly), fill = "#1f77b4",
                          alpha = 0.7) +
        ggplot2::geom_line(ggplot2::aes(y = .data$Cumulative / scale_factor,
                                        group = 1),
                           colour = "#d62728", linewidth = 1.2) +
        ggplot2::geom_point(ggplot2::aes(y = .data$Cumulative / scale_factor),
                            colour = "#d62728", size = 2) +
        ggplot2::scale_y_continuous(
          name = "Monthly value",
          labels = scales::label_comma(
            prefix = paste0(settings$currency_symbol, " ")),
          sec.axis = ggplot2::sec_axis(
            ~ . * scale_factor, name = "Cumulative",
            labels = scales::label_comma(
              prefix = paste0(settings$currency_symbol, " ")))
        ) +
        ggplot2::labs(x = NULL, title = "S-curve cash flow forecast") +
        ggplot2::theme_minimal(base_size = 12) +
        ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, hjust = 1))
    })

    output$cf_peak <- renderText({
      fmt_money(max(cf_calc()$monthly_total), settings$currency_symbol)
    })

    output$cf_wcr <- renderText({
      # Rough WCR: largest monthly outflow x 1.5 months
      fmt_money(max(cf_calc()$monthly_total) * 1.5, settings$currency_symbol)
    })

    output$export_cf <- downloadHandler(
      filename = function() sprintf("Cash_Flow_Forecast_%s.xlsx",
                                    format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        wb <- openxlsx::createWorkbook()
        openxlsx::addWorksheet(wb, "CashFlow")
        openxlsx::writeData(wb, "CashFlow", cf_calc())
        openxlsx::setColWidths(wb, "CashFlow", cols = 1:7,
                               widths = c(8, 12, 16, 16, 16, 18, 14))
        openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
      }
    )
  })
}
