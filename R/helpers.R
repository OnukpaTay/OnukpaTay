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

#' Summarise a BOQ data frame by trade in SMM7 construction-sequence order
#' (D Groundwork, E In situ concrete, F Masonry, ...).
boq_summary_by_trade <- function(df) {
  out <- df %>%
    boq_compute_amount() %>%
    dplyr::group_by(trade) %>%
    dplyr::summarise(items = dplyr::n(),
                     total = sum(.data$amount, na.rm = TRUE),
                     .groups = "drop")
  if (nrow(out))
    out <- out[order_trades_smm7(out$trade), , drop = FALSE]
  out
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

#' Write a Main Contractor IPC styled to match the Barry Callebaut /
#' SPEKTRA template, with the "I/We certify" legal block and signature
#' blocks at the foot of the certificate.
write_main_contractor_ipc <- function(file, settings, project, location,
                                      employer, contractor, contractor_addr,
                                      architect, cert_no, serial,
                                      val_date, due_date,
                                      val_table, mos_table, cert_body,
                                      contract_sum) {
  wb <- openxlsx::createWorkbook()
  sym <- settings$currency_symbol

  title_s   <- openxlsx::createStyle(textDecoration = "bold", fontSize = 14,
                                     halign = "center")
  hdr_s     <- openxlsx::createStyle(textDecoration = "bold",
                                     fgFill = "#1f4e79", fontColour = "white",
                                     halign = "center", border = "TopBottomLeftRight")
  label_s   <- openxlsx::createStyle(textDecoration = "bold")
  money_s   <- openxlsx::createStyle(numFmt = paste0('"', sym, ' "#,##0.00'))
  big_money <- openxlsx::createStyle(numFmt = paste0('"', sym, ' "#,##0.00'),
                                     textDecoration = "bold", fontSize = 12,
                                     fgFill = "#fff8d6")
  bordered  <- openxlsx::createStyle(border = "TopBottomLeftRight")

  # --- Sheet 1: Certificate ---------------------------------------------
  openxlsx::addWorksheet(wb, "Certificate")

  r <- 1
  openxlsx::writeData(wb, "Certificate",
                      "INTERIM PAYMENT CERTIFICATE", startRow = r, startCol = 2)
  openxlsx::addStyle(wb, "Certificate", title_s, rows = r, cols = 2)
  r <- r + 2

  header_pairs <- list(
    list("Architect / consultant",   architect %||% ""),
    list("Architect address",        settings$architect_addr %||% ""),
    list("Project title",            project),
    list("Location",                 location),
    list("Employer",                 employer),
    list("Main Contractor",          contractor),
    list("Contractor address",       contractor_addr %||% ""),
    list("Certificate no.",          as.character(cert_no)),
    list("Serial / reference",       serial),
    list("Valuation date",           format(val_date, "%d %B %Y")),
    list("Date of issue",            format(Sys.Date(), "%d %B %Y")),
    list("Due date for payment",     format(due_date, "%d %B %Y"))
  )
  for (kv in header_pairs) {
    openxlsx::writeData(wb, "Certificate", kv[[1]], startRow = r, startCol = 1)
    openxlsx::writeData(wb, "Certificate", kv[[2]], startRow = r, startCol = 2)
    openxlsx::addStyle(wb, "Certificate", label_s, rows = r, cols = 1)
    r <- r + 1
  }
  r <- r + 1

  # I/We certify block
  openxlsx::writeData(wb, "Certificate",
                      "I / We hereby CERTIFY THAT under the terms of the Contract",
                      startRow = r, startCol = 1); r <- r + 1
  openxlsx::writeData(wb, "Certificate",
                      paste0("for the works known as '", project,
                             "' situated at ", location, ", the INTERIM"),
                      startRow = r, startCol = 1); r <- r + 1
  openxlsx::writeData(wb, "Certificate",
                      paste0("payment detailed below is due from the Employer (",
                             employer, ") to the Main Contractor (",
                             contractor, ")."),
                      startRow = r, startCol = 1); r <- r + 2

  openxlsx::writeData(wb, "Certificate", "Total Contract Sum",
                      startRow = r, startCol = 1)
  openxlsx::writeData(wb, "Certificate", contract_sum, startRow = r, startCol = 2)
  openxlsx::addStyle(wb, "Certificate", label_s,   rows = r, cols = 1)
  openxlsx::addStyle(wb, "Certificate", money_s,   rows = r, cols = 2)
  r <- r + 2

  # Certificate body table
  openxlsx::writeData(wb, "Certificate",
                      data.frame(Code = cert_body$code,
                                 Item = cert_body$Item,
                                 Amount = cert_body$Amount),
                      startRow = r, startCol = 1)
  openxlsx::addStyle(wb, "Certificate", hdr_s, rows = r, cols = 1:3,
                     gridExpand = TRUE)
  body_rows <- (r + 1):(r + nrow(cert_body))
  openxlsx::addStyle(wb, "Certificate", money_s, rows = body_rows, cols = 3,
                     gridExpand = TRUE, stack = TRUE)
  # Highlight the final amount-due row
  openxlsx::addStyle(wb, "Certificate", big_money,
                     rows = r + nrow(cert_body), cols = 3, stack = TRUE)
  openxlsx::addStyle(wb, "Certificate", label_s,
                     rows = r + nrow(cert_body), cols = 1:2, gridExpand = TRUE,
                     stack = TRUE)
  r <- r + nrow(cert_body) + 3

  # Signature block
  sig_rows <- list(
    list("Prepared by:", settings$qs_name, "Date:", format(Sys.Date(), "%d %b %Y"),
         "Signature:", ""),
    list("Accountant:",  settings$accountant_name %||% "", "Date:", "",
         "Signature:", ""),
    list("Approved by:", settings$approver_name %||% "",   "Date:", "",
         "Signature:", "")
  )
  openxlsx::writeData(wb, "Certificate", "SIGNATURES",
                      startRow = r, startCol = 1)
  openxlsx::addStyle(wb, "Certificate", label_s, rows = r, cols = 1)
  r <- r + 1
  for (sr in sig_rows) {
    for (i in seq_along(sr))
      openxlsx::writeData(wb, "Certificate", sr[[i]],
                          startRow = r, startCol = i)
    openxlsx::addStyle(wb, "Certificate", label_s,
                       rows = r, cols = c(1, 3, 5), gridExpand = TRUE,
                       stack = TRUE)
    r <- r + 2
  }

  openxlsx::setColWidths(wb, "Certificate", cols = 1:6,
                         widths = c(28, 38, 14, 16, 16, 16))

  # --- Sheet 2: Valuation -----------------------------------------------
  openxlsx::addWorksheet(wb, "Valuation")

  openxlsx::writeData(wb, "Valuation",
                      paste("VALUATION DETAILS -",
                            format(val_date, "%d %B %Y")),
                      startRow = 1, startCol = 1)
  openxlsx::addStyle(wb, "Valuation", title_s, rows = 1, cols = 1)

  openxlsx::writeData(wb, "Valuation",
                      data.frame(
                        Item        = val_table$item,
                        Description = val_table$description,
                        BOQ_Amount  = val_table$boq_amount,
                        Prev_Done   = val_table$cum_prev_amount,
                        This_Period = val_table$current_amount,
                        Cum_Total   = val_table$cum_total),
                      startRow = 3, startCol = 1)
  openxlsx::addStyle(wb, "Valuation", hdr_s, rows = 3, cols = 1:6,
                     gridExpand = TRUE)
  val_rows <- 4:(3 + nrow(val_table))
  openxlsx::addStyle(wb, "Valuation", money_s, rows = val_rows, cols = 3:6,
                     gridExpand = TRUE, stack = TRUE)
  # Total row
  tot_row <- 3 + nrow(val_table) + 1
  openxlsx::writeData(wb, "Valuation", "TOTAL",
                      startRow = tot_row, startCol = 2)
  openxlsx::writeData(wb, "Valuation",
                      sum(val_table$boq_amount, na.rm = TRUE),
                      startRow = tot_row, startCol = 3)
  openxlsx::writeData(wb, "Valuation",
                      sum(val_table$cum_prev_amount, na.rm = TRUE),
                      startRow = tot_row, startCol = 4)
  openxlsx::writeData(wb, "Valuation",
                      sum(val_table$current_amount, na.rm = TRUE),
                      startRow = tot_row, startCol = 5)
  openxlsx::writeData(wb, "Valuation",
                      sum(val_table$cum_total, na.rm = TRUE),
                      startRow = tot_row, startCol = 6)
  openxlsx::addStyle(wb, "Valuation", big_money, rows = tot_row, cols = 3:6,
                     gridExpand = TRUE, stack = TRUE)
  openxlsx::setColWidths(wb, "Valuation", cols = 1:6,
                         widths = c(8, 50, 16, 16, 16, 18))

  # --- Sheet 3: Materials on site ---------------------------------------
  openxlsx::addWorksheet(wb, "Materials_on_Site")
  openxlsx::writeData(wb, "Materials_on_Site", "MATERIALS ON SITE",
                      startRow = 1, startCol = 1)
  openxlsx::addStyle(wb, "Materials_on_Site", title_s, rows = 1, cols = 1)

  openxlsx::writeData(wb, "Materials_on_Site",
                      data.frame(
                        Description = mos_table$description,
                        Quantity    = mos_table$quantity,
                        Unit        = mos_table$unit,
                        Rate        = mos_table$rate,
                        Amount      = mos_table$amount),
                      startRow = 3, startCol = 1)
  openxlsx::addStyle(wb, "Materials_on_Site", hdr_s, rows = 3, cols = 1:5,
                     gridExpand = TRUE)
  if (nrow(mos_table)) {
    mos_rows <- 4:(3 + nrow(mos_table))
    openxlsx::addStyle(wb, "Materials_on_Site", money_s, rows = mos_rows,
                       cols = 4:5, gridExpand = TRUE, stack = TRUE)
    mos_total <- 3 + nrow(mos_table) + 1
    openxlsx::writeData(wb, "Materials_on_Site", "TOTAL",
                        startRow = mos_total, startCol = 1)
    openxlsx::writeData(wb, "Materials_on_Site",
                        sum(mos_table$amount, na.rm = TRUE),
                        startRow = mos_total, startCol = 5)
    openxlsx::addStyle(wb, "Materials_on_Site", big_money,
                       rows = mos_total, cols = 5, stack = TRUE)
  }
  openxlsx::setColWidths(wb, "Materials_on_Site", cols = 1:5,
                         widths = c(40, 12, 10, 14, 16))

  openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
}


#' Write a Subcontractor IPC matching the Thoroughbred / Results Plumbing
#' format - simpler single-sheet certificate with A-G letter coding and
#' an advance payment recovery block.
write_subcontractor_ipc <- function(file, settings, project, scope,
                                    subcontractor, serial, cert_no,
                                    date, prepared_by, val_table, cert_body,
                                    contract_sum, advance_pct) {
  wb <- openxlsx::createWorkbook()
  sym <- settings$currency_symbol

  title_s   <- openxlsx::createStyle(textDecoration = "bold", fontSize = 14,
                                     halign = "center")
  hdr_s     <- openxlsx::createStyle(textDecoration = "bold",
                                     fgFill = "#1f4e79", fontColour = "white",
                                     halign = "center", border = "TopBottomLeftRight")
  label_s   <- openxlsx::createStyle(textDecoration = "bold")
  money_s   <- openxlsx::createStyle(numFmt = paste0('"', sym, ' "#,##0.00'))
  big_money <- openxlsx::createStyle(numFmt = paste0('"', sym, ' "#,##0.00'),
                                     textDecoration = "bold", fontSize = 12,
                                     fgFill = "#fff8d6")

  # --- Sheet 1: Certificate ---------------------------------------------
  openxlsx::addWorksheet(wb, "IPC")

  r <- 1
  openxlsx::writeData(wb, "IPC",
                      sprintf("INTERIM PAYMENT CERTIFICATE NO.%s", cert_no),
                      startRow = r, startCol = 2)
  openxlsx::addStyle(wb, "IPC", title_s, rows = r, cols = 2)
  r <- r + 2

  header_pairs <- list(
    list("Project",                project),
    list("Detailed scope",         scope),
    list("Subcontractor name",     subcontractor),
    list("Certificate ref",        serial),
    list("Date",                   format(date, "%d %B %Y")),
    list("Contract sum (provisional)", contract_sum),
    list("Advance payment %",
         sprintf("%.0f%% mobilisation paid in advance",
                 advance_pct))
  )
  for (kv in header_pairs) {
    openxlsx::writeData(wb, "IPC", kv[[1]], startRow = r, startCol = 1)
    openxlsx::writeData(wb, "IPC", kv[[2]], startRow = r, startCol = 2)
    openxlsx::addStyle(wb, "IPC", label_s, rows = r, cols = 1)
    if (kv[[1]] == "Contract sum (provisional)")
      openxlsx::addStyle(wb, "IPC", money_s, rows = r, cols = 2, stack = TRUE)
    r <- r + 1
  }
  r <- r + 1

  # Certificate body
  openxlsx::writeData(wb, "IPC",
                      data.frame(Code = cert_body$code,
                                 Item = cert_body$Item,
                                 Amount = cert_body$Amount),
                      startRow = r, startCol = 1)
  openxlsx::addStyle(wb, "IPC", hdr_s, rows = r, cols = 1:3, gridExpand = TRUE)
  body_rows <- (r + 1):(r + nrow(cert_body))
  openxlsx::addStyle(wb, "IPC", money_s, rows = body_rows, cols = 3,
                     gridExpand = TRUE, stack = TRUE)
  openxlsx::addStyle(wb, "IPC", big_money,
                     rows = r + nrow(cert_body), cols = 3, stack = TRUE)
  openxlsx::addStyle(wb, "IPC", label_s,
                     rows = r + nrow(cert_body), cols = 1:2,
                     gridExpand = TRUE, stack = TRUE)
  r <- r + nrow(cert_body) + 3

  # Signature block
  sig_rows <- list(
    list(sprintf("Prepared by: %s", prepared_by), "",
         "Accountant:", ""),
    list(sprintf("Date: %s", format(date, "%d %b %Y")), "",
         "Date:",       ""),
    list("Signature:", "",
         "Signature:", "")
  )
  for (sr in sig_rows) {
    for (i in seq_along(sr))
      openxlsx::writeData(wb, "IPC", sr[[i]],
                          startRow = r, startCol = i)
    r <- r + 1
  }
  r <- r + 1
  openxlsx::writeData(wb, "IPC",
                      sprintf("Approved by: %s",
                              settings$approver_name %||% ""),
                      startRow = r, startCol = 1)
  r <- r + 1
  openxlsx::writeData(wb, "IPC",
                      sprintf("Date: %s", format(date, "%d %b %Y")),
                      startRow = r, startCol = 1); r <- r + 1
  openxlsx::writeData(wb, "IPC", "Signature:",
                      startRow = r, startCol = 1)

  openxlsx::setColWidths(wb, "IPC", cols = 1:5,
                         widths = c(28, 48, 16, 16, 16))

  # --- Sheet 2: Valuation breakdown -------------------------------------
  openxlsx::addWorksheet(wb, "Valuation")
  openxlsx::writeData(wb, "Valuation",
                      data.frame(
                        Item            = val_table$item,
                        Description     = val_table$description,
                        Unit            = val_table$unit,
                        Budget          = val_table$budget_amount,
                        Prev_pct        = val_table$prev_pct,
                        Current_pct     = val_table$current_pct,
                        Cum_pct         = val_table$cum_pct,
                        Prev_amount     = val_table$prev_amount,
                        Current_amount  = val_table$current_amount,
                        Cum_amount      = val_table$cum_amount),
                      startRow = 1, startCol = 1)
  openxlsx::addStyle(wb, "Valuation", hdr_s, rows = 1, cols = 1:10,
                     gridExpand = TRUE)
  if (nrow(val_table)) {
    money_cols_rows <- 2:(1 + nrow(val_table))
    openxlsx::addStyle(wb, "Valuation", money_s,
                       rows = money_cols_rows,
                       cols = c(4, 8, 9, 10), gridExpand = TRUE, stack = TRUE)
  }
  openxlsx::setColWidths(wb, "Valuation", cols = 1:10,
                         widths = c(8, 40, 8, 14, 10, 10, 10, 14, 14, 14))

  openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
}


#' Order trades using SMM7 section letter prefix where present.
#' e.g. "D. Groundwork" sorts before "E. In situ concrete" before "F. Masonry"
#' Trades without a recognisable section letter fall back to alphabetical.
order_trades_smm7 <- function(trades) {
  # Extract leading section code: D, E, F, ..., or D20, E10, etc.
  prefix <- toupper(sub("^\\s*([A-Z][A-Z]?[0-9]*)\\b.*$", "\\1", trades))
  # Treat non-SMM7-coded trades as section "Z" so they sort last
  has_code <- grepl("^[A-Z]", prefix)
  prefix[!has_code] <- "Z"
  order(prefix, trades)
}

#' Save an editable BOQ data frame as an Excel workbook formatted to mirror
#' the user's hand-prepared format - PRIME COST + MARKUP dual columns,
#' SMM7-ordered trades, Qty before Unit, and a disclaimer at the foot.
write_boq_xlsx <- function(boq_df, settings, project, file,
                           client = "", location = "",
                           date = Sys.Date(),
                           prelims_pct = settings$prelims_pct %||% 7,
                           contingency_pct = settings$contingency_pct %||% 5,
                           markup_pct = settings$markup_pct %||% 20,
                           disclaimer = settings$disclaimer_text %||% "") {
  wb <- openxlsx::createWorkbook()
  sym <- settings$currency_symbol
  openxlsx::addWorksheet(wb, "BOQ")

  hdr_style   <- openxlsx::createStyle(textDecoration = "bold",
                                       fgFill = "#1f4e79", fontColour = "white",
                                       halign = "center",
                                       border = "TopBottomLeftRight",
                                       wrapText = TRUE)
  banner_s    <- openxlsx::createStyle(textDecoration = "bold",
                                       halign = "center",
                                       fgFill = "#bdd7ee")
  money_style <- openxlsx::createStyle(numFmt = paste0('"', sym, ' "#,##0.00'))
  trade_style <- openxlsx::createStyle(textDecoration = "bold",
                                       fgFill = "#d9e2f3")
  coll_style  <- openxlsx::createStyle(textDecoration = "bold",
                                       fgFill = "#fff2cc")
  title_style <- openxlsx::createStyle(textDecoration = "bold", fontSize = 13)
  total_style <- openxlsx::createStyle(textDecoration = "bold",
                                       fgFill = "#ffe699")
  disc_style  <- openxlsx::createStyle(fontSize = 10, textDecoration = "italic",
                                       wrapText = TRUE)

  use_markup <- as_num(markup_pct) > 0
  markup_factor <- 1 + as_num(markup_pct) / 100

  # ---- Header block ----------------------------------------------------
  meta <- c(
    sprintf("PROJECT:   %s", project),
    sprintf("CLIENT:    %s", client %||% ""),
    sprintf("LOCATION:  %s", location %||% ""),
    sprintf("DATE:      %s", format(date, "%d %B %Y")),
    sprintf("PRACTICE:  %s | %s", settings$practice_name, settings$qs_name)
  )
  for (i in seq_along(meta))
    openxlsx::writeData(wb, "BOQ", meta[i], startRow = i, startCol = 1)
  openxlsx::addStyle(wb, "BOQ", title_style, rows = 1, cols = 1)

  # PRIME COST / MARKUP banner row (row 6)
  if (use_markup) {
    openxlsx::writeData(wb, "BOQ", "PRIME COST", startRow = 6, startCol = 6)
    openxlsx::writeData(wb, "BOQ",
                        sprintf("%.0f%% MARKUP", as_num(markup_pct)),
                        startRow = 6, startCol = 8)
    openxlsx::addStyle(wb, "BOQ", banner_s, rows = 6, cols = 5:6,
                       gridExpand = TRUE, stack = TRUE)
    openxlsx::addStyle(wb, "BOQ", banner_s, rows = 6, cols = 7:8,
                       gridExpand = TRUE, stack = TRUE)
  }
  start_row <- 8

  # ---- Column headers --------------------------------------------------
  # Order matches user's BOQ: Item | Description | QTY | UNIT | RATE | AMOUNT
  # When markup enabled, two more columns: RATE | AMOUNT (marked-up)
  if (use_markup) {
    openxlsx::writeData(wb, "BOQ",
                        data.frame(c1 = "ITEM", c2 = "DESCRIPTION",
                                   c3 = "QTY", c4 = "UNIT",
                                   c5 = "RATE",
                                   c6 = sprintf("AMOUNT %s", sym),
                                   c7 = "RATE",
                                   c8 = sprintf("AMOUNT %s", sym)),
                        startRow = start_row, startCol = 1, colNames = FALSE)
    openxlsx::addStyle(wb, "BOQ", hdr_style, rows = start_row, cols = 1:8,
                       gridExpand = TRUE)
  } else {
    openxlsx::writeData(wb, "BOQ",
                        data.frame(c1 = "ITEM", c2 = "DESCRIPTION",
                                   c3 = "QTY", c4 = "UNIT",
                                   c5 = "RATE",
                                   c6 = sprintf("AMOUNT %s", sym)),
                        startRow = start_row, startCol = 1, colNames = FALSE)
    openxlsx::addStyle(wb, "BOQ", hdr_style, rows = start_row, cols = 1:6,
                       gridExpand = TRUE)
  }

  # ---- Items grouped by trade (SMM7-ordered) ---------------------------
  r <- start_row + 1
  trade_groups <- split(boq_df, boq_df$trade)
  trade_groups <- trade_groups[order_trades_smm7(names(trade_groups))]
  grand_prime  <- 0
  grand_markup <- 0

  for (tg in names(trade_groups)) {
    # Trade group banner
    openxlsx::writeData(wb, "BOQ", tg, startRow = r, startCol = 2)
    openxlsx::addStyle(wb, "BOQ", trade_style, rows = r,
                       cols = if (use_markup) 1:8 else 1:6,
                       gridExpand = TRUE)
    r <- r + 1

    sub <- trade_groups[[tg]] %>% boq_compute_amount()
    for (i in seq_len(nrow(sub))) {
      openxlsx::writeData(wb, "BOQ", as.character(sub$item_no[i]),
                          startRow = r, startCol = 1)
      openxlsx::writeData(wb, "BOQ", as.character(sub$description[i]),
                          startRow = r, startCol = 2)
      openxlsx::writeData(wb, "BOQ", sub$quantity[i],
                          startRow = r, startCol = 3)
      openxlsx::writeData(wb, "BOQ", as.character(sub$unit[i]),
                          startRow = r, startCol = 4)
      openxlsx::writeData(wb, "BOQ", sub$rate[i],
                          startRow = r, startCol = 5)
      openxlsx::writeData(wb, "BOQ", sub$amount[i],
                          startRow = r, startCol = 6)
      openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = c(5, 6),
                         gridExpand = TRUE, stack = TRUE)
      if (use_markup) {
        marked_rate   <- round(sub$rate[i]   * markup_factor, 2)
        marked_amount <- round(sub$amount[i] * markup_factor, 2)
        openxlsx::writeData(wb, "BOQ", marked_rate,
                            startRow = r, startCol = 7)
        openxlsx::writeData(wb, "BOQ", marked_amount,
                            startRow = r, startCol = 8)
        openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = c(7, 8),
                           gridExpand = TRUE, stack = TRUE)
      }
      r <- r + 1
    }

    sub_total_prime <- sum(sub$amount, na.rm = TRUE)
    sub_total_mark  <- if (use_markup) sub_total_prime * markup_factor else NA
    openxlsx::writeData(wb, "BOQ",
                        paste("Carried to collection -", tg),
                        startRow = r, startCol = 2)
    openxlsx::writeData(wb, "BOQ", sub_total_prime, startRow = r, startCol = 6)
    openxlsx::addStyle(wb, "BOQ", coll_style, rows = r,
                       cols = if (use_markup) 1:8 else 1:6,
                       gridExpand = TRUE, stack = TRUE)
    openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = 6,
                       stack = TRUE)
    if (use_markup) {
      openxlsx::writeData(wb, "BOQ", round(sub_total_mark, 2),
                          startRow = r, startCol = 8)
      openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = 8,
                         stack = TRUE)
      grand_markup <- grand_markup + sub_total_mark
    }
    r <- r + 2
    grand_prime <- grand_prime + sub_total_prime
  }

  # ---- General Summary block ------------------------------------------
  r <- r + 1
  openxlsx::writeData(wb, "BOQ", "GENERAL SUMMARY", startRow = r, startCol = 1)
  openxlsx::addStyle(wb, "BOQ", title_style, rows = r, cols = 1); r <- r + 2

  prelims_p     <- grand_prime * as_num(prelims_pct) / 100
  subtotal_2_p  <- grand_prime + prelims_p
  contingency_p <- subtotal_2_p * as_num(contingency_pct) / 100
  grand_total_p <- subtotal_2_p + contingency_p

  prelims_m     <- if (use_markup) grand_markup * as_num(prelims_pct) / 100
                   else NA
  subtotal_2_m  <- if (use_markup) grand_markup + prelims_m else NA
  contingency_m <- if (use_markup) subtotal_2_m * as_num(contingency_pct) / 100
                   else NA
  grand_total_m <- if (use_markup) subtotal_2_m + contingency_m else NA

  for (kv in list(
    list("MEASURED WORKS (sum of trades)", grand_prime, grand_markup),
    list(sprintf("ADD PRELIMINARIES @ %.1f%%", as_num(prelims_pct)),
         prelims_p, prelims_m),
    list("SUB-TOTAL",                 subtotal_2_p, subtotal_2_m),
    list(sprintf("ADD CONTINGENCY @ %.1f%%", as_num(contingency_pct)),
         contingency_p, contingency_m),
    list("TOTAL COST OF WORKS",       grand_total_p, grand_total_m)
  )) {
    openxlsx::writeData(wb, "BOQ", kv[[1]], startRow = r, startCol = 2)
    openxlsx::writeData(wb, "BOQ", round(kv[[2]], 2),
                        startRow = r, startCol = 6)
    openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = 6, stack = TRUE)
    if (use_markup && !is.na(kv[[3]])) {
      openxlsx::writeData(wb, "BOQ", round(kv[[3]], 2),
                          startRow = r, startCol = 8)
      openxlsx::addStyle(wb, "BOQ", money_style, rows = r, cols = 8,
                         stack = TRUE)
    }
    r <- r + 1
  }
  openxlsx::addStyle(wb, "BOQ", total_style, rows = r - 1,
                     cols = if (use_markup) 1:8 else 1:6,
                     gridExpand = TRUE, stack = TRUE)

  # ---- Disclaimer ------------------------------------------------------
  if (nzchar(disclaimer)) {
    r <- r + 2
    openxlsx::writeData(wb, "BOQ", "Disclaimer:", startRow = r, startCol = 1)
    openxlsx::addStyle(wb, "BOQ",
                       openxlsx::createStyle(textDecoration = "bold"),
                       rows = r, cols = 1)
    r <- r + 1
    openxlsx::writeData(wb, "BOQ", disclaimer, startRow = r, startCol = 1)
    openxlsx::addStyle(wb, "BOQ", disc_style, rows = r, cols = 1)
    if (use_markup) {
      openxlsx::mergeCells(wb, "BOQ", rows = r, cols = 1:8)
    } else {
      openxlsx::mergeCells(wb, "BOQ", rows = r, cols = 1:6)
    }
  }

  widths <- if (use_markup) c(8, 60, 10, 8, 14, 18, 14, 18) else
                            c(8, 60, 10, 8, 14, 18)
  openxlsx::setColWidths(wb, "BOQ", cols = seq_along(widths), widths = widths)
  openxlsx::freezePane(wb, "BOQ", firstActiveRow = start_row + 1)
  openxlsx::saveWorkbook(wb, file, overwrite = TRUE)
}
