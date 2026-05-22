# Bill of Quantities module
#
# Workflow:
#   1. User sets project details
#   2. Adds / edits BOQ items (trade, description, unit, qty, rate)
#   3. Imports from Excel / CSV or starts from a sample BOQ
#   4. Reviews trade summaries and grand total
#   5. Exports a priced BOQ to Excel

mod_boq_ui <- function(id) {
  ns <- NS(id)
  tagList(
    bslib::layout_columns(
      col_widths = c(8, 4),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("file-earmark-text"), " Project details"),
        bslib::layout_columns(
          col_widths = c(6, 6),
          textInput(ns("project_name"),  "Project name",
                    value = "Proposed Multi-Storey Shop Complex"),
          textInput(ns("project_ref"),   "Project / job no",
                    value = make_ref("JOB", 1)),
          textInput(ns("employer"),      "Client / Employer", value = "Diana Williams"),
          textInput(ns("contractor"),    "Contractor (if priced)", value = ""),
          textInput(ns("location"),      "Location",
                    value = "Kwabenya - Greater Accra"),
          dateInput(ns("date"), "BOQ date", value = Sys.Date())
        ),
        bslib::layout_columns(
          col_widths = c(4, 4, 4),
          numericInput(ns("markup_pct"), "Tender markup % (0 = single column)",
                       value = 20, min = 0, max = 100, step = 1),
          numericInput(ns("prelims_pct"), "Preliminaries %",
                       value = 7, min = 0, max = 30, step = 0.5),
          numericInput(ns("contingency_pct"), "Contingency %",
                       value = 5, min = 0, max = 30, step = 0.5)
        )
      ),
      bslib::value_box(
        title    = "BOQ grand total (prime cost)",
        value    = textOutput(ns("grand_total")),
        showcase = bsicons::bs_icon("cash-stack"),
        theme    = "primary"
      )
    ),
    bslib::card(
      bslib::card_header(
        bsicons::bs_icon("list-task"),
        " BOQ items - click any cell to edit"
      ),
      bslib::layout_columns(
        col_widths = c(3, 3, 3, 3),
        actionButton(ns("add_row"), "Add item",
                     class = "btn-success", icon = icon("plus")),
        actionButton(ns("del_row"), "Delete selected",
                     class = "btn-outline-danger", icon = icon("trash")),
        fileInput(ns("import_csv"), NULL, accept = ".csv",
                  buttonLabel = "Import CSV", placeholder = "no file"),
        actionButton(ns("load_sample"), "Load sample BOQ",
                     class = "btn-outline-secondary", icon = icon("file-import"))
      ),
      DT::DTOutput(ns("boq_table"))
    ),
    bslib::layout_columns(
      col_widths = c(6, 6),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("bar-chart"), " Collection by trade"),
        DT::DTOutput(ns("trade_summary"))
      ),
      bslib::card(
        bslib::card_header(bsicons::bs_icon("calculator"), " Summary page"),
        DT::DTOutput(ns("summary_page")),
        downloadButton(ns("export_xlsx"), "Export priced BOQ (Excel)",
                       class = "btn-primary mt-3"),
        downloadButton(ns("export_csv"),  "Export raw CSV",
                       class = "btn-outline-secondary mt-2")
      )
    )
  )
}

mod_boq_server <- function(id, settings, app_state) {
  moduleServer(id, function(input, output, session) {
    ns <- session$ns

    # Reactive BOQ data ----------------------------------------------------
    boq <- reactiveVal(
      tibble::tibble(
        item_no = character(), trade = character(), description = character(),
        unit = character(), quantity = numeric(), rate = numeric()
      )
    )

    # Share the live BOQ with other modules (IPC, Valuations, etc.)
    observe({ app_state$boq <- boq() })

    # Add / delete rows ----------------------------------------------------
    observeEvent(input$add_row, {
      trades <- TRADE_GROUPS_DF %>%
        dplyr::filter(.data$standard == settings$measurement_std) %>%
        dplyr::pull(.data$trade)
      default_trade <- if (length(trades)) trades[1] else "Preliminaries"
      new_row <- tibble::tibble(
        item_no = sprintf("X%02d", nrow(boq()) + 1),
        trade   = default_trade,
        description = "New item",
        unit = "nr", quantity = 1, rate = 0
      )
      boq(dplyr::bind_rows(boq(), new_row))
    })

    observeEvent(input$del_row, {
      sel <- input$boq_table_rows_selected
      if (!length(sel)) {
        showNotification("Select one or more rows first.", type = "warning")
        return()
      }
      boq(boq()[-sel, , drop = FALSE])
    })

    observeEvent(input$load_sample, {
      # Try the pre-loaded copy first, then re-read from disk in case
      # the working directory wasn't set when global.R was sourced.
      df <- SAMPLE_BOQ_DF
      if (is.null(df) || !nrow(df)) {
        df <- tryCatch(
          readr::read_csv("data/sample_boq.csv", show_col_types = FALSE),
          error = function(e) NULL
        )
      }
      if (is.null(df) || !nrow(df)) {
        showNotification(
          paste0("Could not load data/sample_boq.csv. ",
                 "Working directory is currently: '", getwd(), "'. ",
                 "Set it to the OnukpaTay project root (where app.R lives) ",
                 "and reload the app."),
          type = "error", duration = 15)
        return()
      }
      boq(df)
      showNotification(sprintf("Sample BOQ loaded - %d items.", nrow(df)),
                       type = "message")
    })

    observeEvent(input$import_csv, {
      req(input$import_csv)
      df <- tryCatch(readr::read_csv(input$import_csv$datapath,
                                     show_col_types = FALSE),
                     error = function(e) NULL)
      if (is.null(df)) {
        showNotification("Could not read CSV.", type = "error"); return()
      }
      required <- c("item_no", "trade", "description", "unit", "quantity", "rate")
      missing <- setdiff(required, names(df))
      if (length(missing)) {
        showNotification(
          paste("Missing columns:", paste(missing, collapse = ", ")),
          type = "error"); return()
      }
      boq(df[required])
      showNotification(sprintf("Loaded %d items.", nrow(df)), type = "message")
    })

    # Editable DataTable ---------------------------------------------------
    output$boq_table <- DT::renderDT({
      df <- boq() %>% boq_compute_amount() %>%
        dplyr::select(.data$item_no, .data$trade, .data$description,
                      .data$quantity, .data$unit, .data$rate, .data$amount)
      DT::datatable(
        df,
        editable = list(target = "cell",
                        disable = list(columns = which(names(df) == "amount") - 1)),
        selection = "multiple",
        rownames = FALSE,
        options = dt_editable_opts(),
        colnames = c("Item", "Trade / Section", "Description",
                     "Qty", "Unit", "Rate", "Amount")
      ) %>%
        DT::formatCurrency(c("rate", "amount"),
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",") %>%
        DT::formatRound("quantity", digits = 2)
    }, server = FALSE)

    observeEvent(input$boq_table_cell_edit, {
      info <- input$boq_table_cell_edit
      df <- boq()
      # Display order is item_no, trade, description, quantity, unit, rate
      # but underlying data order is item_no, trade, description, unit,
      # quantity, rate - so map by name not position.
      display_to_data <- c("item_no", "trade", "description",
                           "quantity", "unit", "rate")
      col_name <- display_to_data[info$col + 1]
      if (col_name %in% c("quantity", "rate")) {
        df[info$row, col_name] <- as_num(info$value)
      } else {
        df[info$row, col_name] <- info$value
      }
      boq(df)
    })

    # Trade summary & grand total ------------------------------------------
    output$trade_summary <- DT::renderDT({
      df <- boq_summary_by_trade(boq())
      if (!nrow(df)) return(DT::datatable(df))
      DT::datatable(df, rownames = FALSE,
                    options = list(dom = "t", pageLength = 50),
                    colnames = c("Trade", "Items", "Total")) %>%
        DT::formatCurrency("total",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$summary_page <- DT::renderDT({
      df <- boq() %>% boq_compute_amount()
      subtotal <- sum(df$amount, na.rm = TRUE)
      contingency <- subtotal * 0.05
      ohp <- subtotal * (settings$overhead_pct + settings$profit_pct) / 100
      net <- subtotal + contingency + ohp
      vat <- net * (settings$vat_pct + settings$nhil_getfl_pct) / 100
      tot <- net + vat
      rows <- tibble::tibble(
        Item   = c("Measured works (sum of all trades)",
                   "Contingency @ 5%",
                   sprintf("Overheads & profit @ %.1f%%",
                           settings$overhead_pct + settings$profit_pct),
                   "Net contract sum",
                   sprintf("VAT + NHIL + GETFund @ %.1f%%",
                           settings$vat_pct + settings$nhil_getfl_pct),
                   "Tender total"),
        Amount = c(subtotal, contingency, ohp, net, vat, tot)
      )
      DT::datatable(rows, rownames = FALSE,
                    options = list(dom = "t", pageLength = 10)) %>%
        DT::formatCurrency("Amount",
                           currency = paste0(settings$currency_symbol, " "),
                           interval = 3, mark = ",")
    })

    output$grand_total <- renderText({
      total <- sum(boq_compute_amount(boq())$amount, na.rm = TRUE)
      fmt_money(total, settings$currency_symbol)
    })

    # Exports --------------------------------------------------------------
    output$export_xlsx <- downloadHandler(
      filename = function()
        sprintf("BOQ_%s_%s.xlsx",
                gsub("[^A-Za-z0-9]+", "_", input$project_ref %||% "project"),
                format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        df <- boq() %>% boq_compute_amount()
        write_boq_xlsx(df, settings, input$project_name, file,
                       client = input$employer,
                       location = input$location,
                       date = input$date,
                       prelims_pct = input$prelims_pct,
                       contingency_pct = input$contingency_pct,
                       markup_pct = input$markup_pct,
                       disclaimer = settings$disclaimer_text)
      }
    )

    output$export_csv <- downloadHandler(
      filename = function()
        sprintf("BOQ_%s_%s.csv",
                gsub("[^A-Za-z0-9]+", "_", input$project_ref %||% "project"),
                format(Sys.Date(), "%Y%m%d")),
      content = function(file) {
        readr::write_csv(boq(), file)
      }
    )
  })
}
