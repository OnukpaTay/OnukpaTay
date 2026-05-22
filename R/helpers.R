# Shared helpers used across modules.

#' Null/empty coalesce - returns `b` if `a` is NULL or an empty string.
`%||%` <- function(a, b) if (is.null(a) || !nzchar(a)) b else a

#' Compute amount column from quantity x rate, NA-safe.
boq_compute_amount <- function(df) {
  df %>%
    dplyr::mutate(
      quantity = as_num(.data$quantity),
      rate     = as_num(.data$rate),
      amount   = round(.data$quantity * .data$rate, 2)
    )
}

#' Summarise a BOQ data frame by trade.
boq_summary_by_trade <- function(df) {
  df %>%
    boq_compute_amount() %>%
    dplyr::group_by(trade) %>%
    dplyr::summarise(items = dplyr::n(),
                     total = sum(.data$amount, na.rm = TRUE),
                     .groups = "drop") %>%
    dplyr::arrange(dplyr::desc(.data$total))
}

#' Build the workbook header for a printable BOQ / Certificate / Claim.
doc_header_html <- function(settings, doc_title, doc_ref, project, employer = "",
                            contractor = "", date = Sys.Date()) {
  tags$div(
    class = "doc-header",
    tags$div(class = "doc-practice",
             tags$strong(settings$practice_name), tags$br(),
             settings$practice_addr, tags$br(),
             tags$em(settings$qs_name), " | ", settings$qs_credentials),
    tags$h3(doc_title, class = "doc-title"),
    tags$div(class = "doc-meta",
             tags$div(tags$strong("Reference: "), doc_ref),
             tags$div(tags$strong("Project: "), project),
             tags$div(tags$strong("Employer: "), employer),
             tags$div(tags$strong("Contractor: "), contractor),
             tags$div(tags$strong("Date: "), format(date, "%d %B %Y"))),
    tags$hr()
  )
}

#' Editable DT options used widely.
dt_editable_opts <- function(page_length = 25) {
  list(
    pageLength = page_length,
    lengthMenu = c(10, 25, 50, 100, 250),
    scrollX    = TRUE,
    autoWidth  = FALSE,
    dom        = "lftipB",
    columnDefs = list(list(className = "dt-right",
                           targets   = "_all"))
  )
}

#' Add a row to a reactive data frame held in a reactiveVal.
add_blank_row <- function(rv, template_row) {
  cur <- rv()
  rv(dplyr::bind_rows(cur, template_row))
}

#' Currency input helper - shows the configured symbol as prefix.
currency_input <- function(id, label, value = 0, settings = DEFAULT_SETTINGS) {
  numericInput(id, label = paste0(label, " (", settings$currency_symbol, ")"),
               value = value, min = 0, step = 0.01)
}

#' Save an editable BOQ data frame as an Excel workbook.
write_boq_xlsx <- function(boq_df, settings, project, file) {
  wb <- openxlsx::createWorkbook()
  openxlsx::addWorksheet(wb, "BOQ")

  hdr_style <- openxlsx::createStyle(textDecoration = "bold",
                                     fgFill = "#1f4e79", fontColour = "white",
                                     halign = "center", border = "TopBottomLeftRight")
  money_style <- openxlsx::createStyle(numFmt = paste0('"', settings$currency_symbol,
                                                       ' "#,##0.00'))
  trade_style <- openxlsx::createStyle(textDecoration = "bold",
                                       fgFill = "#d9e2f3")

  rows <- list()
  rows[[1]] <- c("Item", "Description", "Unit", "Quantity", "Rate", "Amount")
  trade_groups <- split(boq_df, boq_df$trade)
  grand <- 0
  row_idx <- 2
  trade_rows <- integer()
  for (tg in names(trade_groups)) {
    rows[[length(rows) + 1]] <- c(tg, "", "", "", "", "")
    trade_rows <- c(trade_rows, row_idx)
    row_idx <- row_idx + 1
    sub <- trade_groups[[tg]] %>% boq_compute_amount()
    for (i in seq_len(nrow(sub))) {
      rows[[length(rows) + 1]] <- c(
        as.character(sub$item_no[i]),
        as.character(sub$description[i]),
        as.character(sub$unit[i]),
        as.character(sub$quantity[i]),
        as.character(sub$rate[i]),
        as.character(sub$amount[i])
      )
      row_idx <- row_idx + 1
    }
    sub_total <- sum(sub$amount, na.rm = TRUE)
    rows[[length(rows) + 1]] <- c("", paste("Collection to", tg), "", "", "", as.character(sub_total))
    row_idx <- row_idx + 1
    grand <- grand + sub_total
  }
  rows[[length(rows) + 1]] <- c("", "GRAND TOTAL CARRIED TO SUMMARY", "", "", "", as.character(grand))

  mat <- do.call(rbind, rows)
  openxlsx::writeData(wb, "BOQ", mat, colNames = FALSE)
  openxlsx::addStyle(wb, "BOQ", hdr_style, rows = 1, cols = 1:6, gridExpand = TRUE)
  if (length(trade_rows))
    openxlsx::addStyle(wb, "BOQ", trade_style, rows = trade_rows, cols = 1:6, gridExpand = TRUE)
  openxlsx::addStyle(wb, "BOQ", money_style,
                     rows = 2:(nrow(mat)), cols = 5:6, gridExpand = TRUE, stack = TRUE)
  openxlsx::setColWidths(wb, "BOQ",
                         cols = 1:6,
                         widths = c(8, 60, 8, 12, 14, 16))
  openxlsx::freezePane(wb, "BOQ", firstActiveRow = 2)
  openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
}
