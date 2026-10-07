import sys, copy, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, LineChart, Reference

src, out = sys.argv[1], sys.argv[2]
swb = openpyxl.load_workbook(src)
sws = swb['OPTION 1rev']

wb = openpyxl.Workbook()
BOLD = Font(bold=True); HDR = Font(bold=True, color='FFFFFF')
HFILL = PatternFill('solid', fgColor='1F3864'); INFILL = PatternFill('solid', fgColor='FFF2CC')
SUBFILL = PatternFill('solid', fgColor='D9E1F2'); TOTFILL = PatternFill('solid', fgColor='E2EFDA')
thin = Side(style='thin', color='999999'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
MONEY = '#,##0.00;[Red](#,##0.00);"-"'
CTR = Alignment(horizontal='center', vertical='center', wrap_text=True)

# ---------------- GEN SUMMARY (copy of the estimate, formulas kept) ----------------
gs = wb.active; gs.title = 'GEN SUMMARY'
for row in sws.iter_rows(min_row=1, max_row=60, max_col=10):
    for c in row:
        if c.value is None and not c.has_style: continue
        n = gs.cell(row=c.row, column=c.column, value=c.value)
        if c.has_style:
            n.font = copy.copy(c.font); n.fill = copy.copy(c.fill); n.border = copy.copy(c.border)
            n.alignment = copy.copy(c.alignment); n.number_format = c.number_format
for k, d in sws.column_dimensions.items():
    gs.column_dimensions[k].width = d.width
for m in sws.merged_cells.ranges:
    if m.max_row <= 60: gs.merge_cells(str(m))
gs['J5'] = 'Source: Preliminary Estimate for Priority Insurance - 2026-10-07 (rev 6), sheet "OPTION 1rev". Column H (discounted) drives the cash flow.'
gs['J5'].font = Font(italic=True, color='808080')

# ---------------- INPUTS ----------------
ip = wb.create_sheet('INPUTS')
ip['A1'] = 'PRIORITY INSURANCE HEAD OFFICE, RIDGE, ACCRA - CASH FLOW INPUTS'; ip['A1'].font = Font(bold=True, size=13)
ip['A2'] = 'Yellow cells are inputs. Everything else in the workbook is calculated from these cells and from GEN SUMMARY.'
ip['A2'].font = Font(italic=True, color='808080')
for col, h in zip('ABCD', ['NAME', 'DESCRIPTION', 'VALUE', 'NOTE']):
    c = ip[f'{col}4']; c.value = h; c.font = HDR; c.fill = HFILL; c.alignment = CTR
inputs = [
 # name, desc, value, fmt, is_input, note
 ('ContractSum', 'Contract sum (discounted, excl. taxes)', "='GEN SUMMARY'!H50", MONEY, False, 'Linked to GEN SUMMARY H50'),
 ('TargetSum', 'Target discounted contract sum', 6250000, MONEY, True, 'Agreed discounted amount'),
 ('StartDate', 'Commencement / contract signing date', datetime.date(2026, 9, 30), 'dd mmm yyyy', True, 'Month 0'),
 ('Duration', 'Contract period (months)', 24, '0', True, ''),
 ('CompletionDate', 'Practical completion date', '=EOMONTH(StartDate,Duration)', 'dd mmm yyyy', False, ''),
 ('DLP', 'Defects liability period (months)', 6, '0', True, ''),
 ('DLPEndDate', 'End of defects liability period', '=EOMONTH(CompletionDate,DLP)', 'dd mmm yyyy', False, ''),
 ('AdvPct', 'Advance mobilisation payment (% of contract sum)', 0.25, '0.00%', True, 'As Thoroughbred Place reference (25%)'),
 ('AdvAmt', 'Advance mobilisation amount', '=ROUND(AdvPct*ContractSum,2)', MONEY, False, ''),
 ('AdvMonth', 'Advance paid in month no.', 0, '0', True, '0 = on contract signing'),
 ('RecStart', 'Advance recovery starts in month no.', 3, '0', True, ''),
 ('RecMonths', 'Advance recovered over (months)', 18, '0', True, 'Equal monthly deductions'),
 ('RecEnd', 'Advance recovery ends in month no.', '=RecStart+RecMonths-1', '0', False, 'Must be on or before Duration'),
 ('RetRate', 'Retention deducted per valuation', 0.10, '0.00%', True, ''),
 ('RetLimitPct', 'Limit of retention (% of contract sum)', 0.05, '0.00%', True, ''),
 ('RetLimit', 'Limit of retention', '=ROUND(RetLimitPct*ContractSum,2)', MONEY, False, ''),
 ('Rel1Pct', 'Retention released at practical completion', 0.5, '0.00%', True, 'Balance released at end of DLP'),
 ('Rel1Month', '1st retention release - month no.', '=Duration+1', '0', False, 'Month after practical completion (can be overwritten)'),
 ('Rel2Month', '2nd retention release - month no.', '=Duration+DLP', '0', False, 'End of DLP'),
 ('PeriodMonths', 'Months per aggregated payment (summary sheet)', 4, '0', True, 'Reference used 4-monthly payments'),
]
r = 5
for name, desc, val, fmt, is_in, note in inputs:
    ip[f'A{r}'] = name; ip[f'B{r}'] = desc; ip[f'C{r}'] = val; ip[f'D{r}'] = note
    ip[f'C{r}'].number_format = fmt
    for col in 'ABCD': ip[f'{col}{r}'].border = BOX
    if is_in: ip[f'C{r}'].fill = INFILL
    wb.defined_names[name] = DefinedName(name, attr_text=f"INPUTS!$C${r}")
    r += 1
for col, w in zip('ABCD', [16, 50, 18, 48]): ip.column_dimensions[col].width = w
ip['A4'].alignment = CTR
CHECK_ROW0 = r + 2

# ---------------- CASHFLOW ----------------
cf = wb.create_sheet(' CASHFLOW')
NM = 37                      # months 0..36 (covers 24 + 6 DLP with room to extend)
FC = 11                      # first month column = K
LC = FC + NM - 1             # last month column
TOT = LC + 1; CHK = LC + 2; END = LC + 3
fcL, lcL, totL, chkL, endL = CL(FC), CL(LC), CL(TOT), CL(CHK), CL(END)

cf['A1'] = 'PROJECT: PROPOSED HEAD OFFICE FOR PRIORITY INSURANCE'
cf['A2'] = 'LOCATION: RIDGE, ACCRA     CLIENT: PRIORITY INSURANCE'
cf['A3'] = '="CASH FLOW FORECAST - CONTRACT SUM US$ "&TEXT(ContractSum,"#,##0.00")&" - "&TEXT(StartDate,"dd mmm yyyy")&" TO "&TEXT(CompletionDate,"dd mmm yyyy")&", DLP TO "&TEXT(DLPEndDate,"mmm yyyy")'
for a in ('A1', 'A2', 'A3'): cf[a].font = BOLD

heads = ['ITEM', 'DESCRIPTION', 'AMOUNT (US$)', 'PH.1 START MONTH', 'PH.1 DURATION (MONTHS)', 'PH.1 %',
         'PH.2 START MONTH', 'PH.2 DURATION (MONTHS)', 'PH.2 %', '']
for i, h in enumerate(heads, 1):
    c = cf.cell(row=5, column=i, value=h)
for i in range(1, END + 1):
    c = cf.cell(row=5, column=i); c.font = HDR; c.fill = HFILL; c.alignment = CTR; c.border = BOX
cf.cell(row=5, column=TOT, value='TOTAL'); cf.cell(row=5, column=CHK, value='CHECK (TOTAL - AMOUNT)')
cf.cell(row=5, column=END, value='LAST MONTH')
cf['B6'] = 'Month no.'; cf['B7'] = 'Month ending'
for k in range(NM):
    col = FC + k; L = CL(col)
    cf.cell(row=5, column=col, value=f'M{k}')
    cf.cell(row=6, column=col, value=0 if k == 0 else f'={CL(col-1)}6+1').alignment = CTR
    d = cf.cell(row=7, column=col, value=f'=EOMONTH(StartDate,{L}$6)'); d.number_format = 'mmm-yy'; d.alignment = CTR
    cf.column_dimensions[L].width = 12.5
for rr in (6, 7):
    for col in range(1, END + 1): cf.cell(row=rr, column=col).fill = SUBFILL; cf.cell(row=rr, column=col).font = BOLD

# bill rows: (GEN SUMMARY row, p1start, p1dur, p1pct, p2start, p2dur, basis note)
bills = [
 (7, 1, 1, 0.50, 2, 23),   # Prelims: 50% possession/hoarding/set-up in M1, 50% maintenance M2-M24
 (9, 1, 1, 0.80, 2, 1),    # Demolitions 80% start / 20% completion
 (11, 1, 2, 0.50, 3, 2),   # Substructure: procurement 50%, works 50%
 (13, 3, 4, 0.50, 7, 12),  # Sub-basement: structure 50%, finishes & MEP 50%
 (15, 5, 3, 0.50, 8, 13),  # Ground
 (17, 7, 3, 0.50, 10, 12), # First
 (19, 9, 3, 0.50, 12, 10), # Second
 (21, 11, 3, 0.50, 14, 9), # Third
 (23, 13, 3, 0.50, 16, 7), # Fourth
 (25, 15, 3, 0.50, 18, 5), # Fifth
 (27, 16, 1, 0.70, 20, 3), # Kitchen cabinetry: 70% order, 30% install
 (29, 4, 15, 0.60, 19, 5), # Plumbing/FF/mech: 1st fix 60%, 2nd fix & commissioning 40%
 (31, 4, 15, 0.60, 19, 5), # Electrical
 (33, 12, 3, 0.70, 15, 8), # Facade: procurement 70%, installation 30%
 (35, 20, 3, 0.50, 23, 2), # External works
 (37, 1, 1, 0.50, 2, 11),  # Design fees
 (39, 1, 12, 0.50, 13, 12),# PM fees - even over 24 months
]
R0 = 9
for i, (g, s1, d1, p1, s2, d2) in enumerate(bills):
    rr = R0 + i
    cf[f'A{rr}'] = f"='GEN SUMMARY'!A{g}"
    cf[f'B{rr}'] = f"=TRIM('GEN SUMMARY'!B{g})"
    cf[f'C{rr}'] = f"='GEN SUMMARY'!H{g}"
    cf[f'D{rr}'] = s1; cf[f'E{rr}'] = d1; cf[f'F{rr}'] = p1
    cf[f'G{rr}'] = s2; cf[f'H{rr}'] = d2; cf[f'I{rr}'] = f'=1-F{rr}'
    for col in 'DEFGH': cf[f'{col}{rr}'].fill = INFILL
    for col in 'FI': cf[f'{col}{rr}'].number_format = '0%'
    cf[f'C{rr}'].number_format = MONEY
    for k in range(NM):
        L = CL(FC + k)
        cf[f'{L}{rr}'] = (f'=IF(AND($E{rr}>0,{L}$6>=$D{rr},{L}$6<$D{rr}+$E{rr}),$C{rr}*$F{rr}/$E{rr},0)'
                          f'+IF(AND($H{rr}>0,{L}$6>=$G{rr},{L}$6<$G{rr}+$H{rr}),$C{rr}*$I{rr}/$H{rr},0)')
        cf[f'{L}{rr}'].number_format = MONEY
    cf[f'{totL}{rr}'] = f'=SUM({fcL}{rr}:{lcL}{rr})'
    cf[f'{chkL}{rr}'] = f'=ROUND({totL}{rr}-C{rr},2)'
    cf[f'{endL}{rr}'] = f'=MAX(IF(E{rr}>0,D{rr}+E{rr}-1,0),IF(H{rr}>0,G{rr}+H{rr}-1,0))'
    for col in (TOT, CHK): cf.cell(row=rr, column=col).number_format = MONEY
RN = R0 + len(bills) - 1      # last bill row (25)
RT = RN + 1                   # bill total row
cf[f'B{RT}'] = 'TOTAL OF BILLS (= CONTRACT SUM)'
cf[f'C{RT}'] = f'=SUM(C{R0}:C{RN})'; cf[f'C{RT}'].number_format = MONEY

# summary rows
rows = {}
def srow(key, label, fn, fill=None, bold=False, fmt=MONEY, total=True):
    rr = srow.r; rows[key] = rr; srow.r += 1
    cf[f'B{rr}'] = label
    for k in range(NM):
        L, P = CL(FC + k), CL(FC + k - 1)
        cf[f'{L}{rr}'] = fn(L, P, k); cf[f'{L}{rr}'].number_format = fmt
    if total:
        cf[f'{totL}{rr}'] = f'=SUM({fcL}{rr}:{lcL}{rr})'; cf[f'{totL}{rr}'].number_format = fmt
    for col in range(1, END + 1):
        c = cf.cell(row=rr, column=col)
        if fill: c.fill = fill
        if bold: c.font = BOLD
srow.r = RT
# reuse RT row for monthly valuation total
cf[f'B{RT}'] = 'ESTIMATED MONTHLY VALUATION (WORK DONE)'
srow('val', 'ESTIMATED MONTHLY VALUATION (WORK DONE)', lambda L, P, k: f'=SUM({L}{R0}:{L}{RN})', SUBFILL, True)
srow('cumval', 'CUMULATIVE VALUATION', lambda L, P, k: (f'={L}{RT}' if k == 0 else f'={P}{RT+1}+{L}{RT}'), total=False)
srow('pct', 'CUMULATIVE % COMPLETE', lambda L, P, k: f'={L}{RT+1}/ContractSum', fmt='0.0%', total=False)
srow.r += 1
v = rows['val']
srow('adv', 'ADD: ADVANCE MOBILISATION PAYMENT', lambda L, P, k: f'=IF({L}$6=AdvMonth,AdvAmt,0)')
srow('ret', 'LESS: RETENTION DEDUCTED', None or (lambda L, P, k: '0'), total=True)  # placeholder, filled below
srow('cumret', 'CUMULATIVE RETENTION DEDUCTED', lambda L, P, k: '0', total=False)
srow('rel', 'ADD: RETENTION RELEASED', lambda L, P, k: '0')
srow('held', 'RETENTION HELD (BALANCE)', lambda L, P, k: '0', total=False)
srow('rec', 'LESS: ADVANCE RECOVERY', lambda L, P, k: f'=IF(AND({L}$6>=RecStart,{L}$6<=RecEnd),AdvAmt/RecMonths,0)')
srow('cumrec', 'CUMULATIVE ADVANCE RECOVERED', lambda L, P, k: '0', total=False)
srow.r += 1
srow('pay', 'ESTIMATED MONTHLY PAYMENT', lambda L, P, k: '0', TOTFILL, True)
srow('cumpay', 'CUMULATIVE MONTHLY PAYMENT', lambda L, P, k: '0', TOTFILL, True, total=False)
R = rows
for k in range(NM):
    L, P = CL(FC + k), CL(FC + k - 1)
    prev = lambda key: ('0' if k == 0 else f'{P}{R[key]}')
    cf[f'{L}{R["ret"]}'] = f'=MIN(RetRate*{L}{v},MAX(0,RetLimit-{prev("cumret")}))'
    cf[f'{L}{R["cumret"]}'] = f'={prev("cumret")}+{L}{R["ret"]}'
    cf[f'{L}{R["rel"]}'] = (f'=IF({L}$6=Rel1Month,ROUND(Rel1Pct*{L}{R["cumret"]},2),0)'
                            f'+IF({L}$6=Rel2Month,{L}{R["cumret"]}-SUM(${fcL}{R["rel"]}:{P if k else L}{R["rel"]})*{0 if k == 0 else 1},0)')
    if k == 0:
        cf[f'{L}{R["rel"]}'] = (f'=IF({L}$6=Rel1Month,ROUND(Rel1Pct*{L}{R["cumret"]},2),0)'
                                f'+IF({L}$6=Rel2Month,{L}{R["cumret"]},0)')
    cf[f'{L}{R["held"]}'] = f'={L}{R["cumret"]}-SUM(${fcL}{R["rel"]}:{L}{R["rel"]})'
    cf[f'{L}{R["cumrec"]}'] = f'={prev("cumrec")}+{L}{R["rec"]}'
    cf[f'{L}{R["pay"]}'] = f'={L}{v}+{L}{R["adv"]}-{L}{R["ret"]}+{L}{R["rel"]}-{L}{R["rec"]}'
    cf[f'{L}{R["cumpay"]}'] = f'={prev("cumpay")}+{L}{R["pay"]}'
for key in ('ret', 'rel', 'rec', 'pay'):
    cf[f'{chkL}{R[key]}'] = None
cf[f'{chkL}{R["pay"]}'] = f'=ROUND({totL}{R["pay"]}-ContractSum,2)'; cf[f'{chkL}{R["pay"]}'].number_format = MONEY
cf[f'{chkL}{v}'] = f'=ROUND({totL}{v}-ContractSum,2)'; cf[f'{chkL}{v}'].number_format = MONEY

# notes / basis
nr = R['cumpay'] + 3
notes = [
 'NOTES:',
 '1. Taxes (VAT, NHIL, GETFund, COVID levies) are NOT included. Amounts are the discounted figures in GEN SUMMARY column H.',
 '2. Each bill is spread over two phases: Phase 1 (start month, duration, %) and Phase 2 (start month, duration, balance %). Edit the yellow cells to re-programme.',
 '3. Phasing basis: Floors 50% structure / 50% finishes & MEP fit-out; MEP 60% first fix / 40% second fix & commissioning; Facade 70% procurement / 30% installation; Kitchen 70% order / 30% installation; Prelims 50% possession & set-up / 50% maintenance.',
 '4. Retention at RetRate of each valuation, stopping when the limit (RetLimit) is reached; Rel1Pct released the month after practical completion, balance at the end of the DLP.',
 '5. Advance mobilisation paid on signing and recovered in equal monthly deductions from RecStart to RecEnd.',
 '6. Payments shown in the month of the valuation (month ending dates). Months beyond the end of the DLP are shaded grey and should total zero.',
]
for i, t in enumerate(notes):
    cf[f'B{nr+i}'] = t
    if i == 0: cf[f'B{nr+i}'].font = BOLD

cf.column_dimensions['A'].width = 6; cf.column_dimensions['B'].width = 46; cf.column_dimensions['C'].width = 15
for col in 'DEFGHI': cf.column_dimensions[col].width = 9.5
cf.column_dimensions['J'].width = 2
cf.column_dimensions[totL].width = 15; cf.column_dimensions[chkL].width = 13; cf.column_dimensions[endL].width = 9
cf.row_dimensions[5].height = 45
cf.freeze_panes = f'{fcL}8'
grey = PatternFill('solid', fgColor='EDEDED')
cf.conditional_formatting.add(f'{fcL}5:{lcL}{R["cumpay"]}',
    FormulaRule(formula=[f'{fcL}$6>Rel2Month'], fill=grey, font=Font(color='A6A6A6')))
red = PatternFill('solid', fgColor='F8CBAD')
cf.conditional_formatting.add(f'{chkL}{R0}:{chkL}{R["pay"]}', FormulaRule(formula=[f'ABS({chkL}{R0})>0.005'], fill=red))
cf.conditional_formatting.add(f'{endL}{R0}:{endL}{RN}', FormulaRule(formula=[f'{endL}{R0}>Duration'], fill=red))
cf.conditional_formatting.add(f'{fcL}{R["pay"]}:{lcL}{R["pay"]}', FormulaRule(formula=[f'{fcL}{R["pay"]}<0'], fill=red))

# ---------------- CASHFLOW SUMMARY ----------------
sm = wb.create_sheet('CASHFLOW SUMMARY', 1)
sm['A1'] = 'PRIORITY INSURANCE HEAD OFFICE - PROPOSED CASH FLOW'; sm['A1'].font = Font(bold=True, size=13)
sm['A2'] = '="Contract sum (discounted, excl. taxes): US$ "&TEXT(ContractSum,"#,##0.00")'
sm['A4'] = 'PROPOSED CASH FLOW AGGREGATED'; sm['A4'].font = BOLD
sm['A5'] = '="Every "&PeriodMonths&" months (change PeriodMonths on INPUTS)"'; sm['A5'].font = Font(italic=True, color='808080')
for col, h in zip('ABCDE', ['PAYMENT NO.', 'PAYMENT DATE', 'MONTHS COVERED', 'AMOUNT (US$)', 'CUMULATIVE (US$)']):
    c = sm[f'{col}6']; c.value = h; c.font = HDR; c.fill = HFILL; c.alignment = CTR; c.border = BOX
MROW = f"' CASHFLOW'!${fcL}$6:${lcL}$6"
PROW = f"' CASHFLOW'!${fcL}${R['pay']}:${lcL}${R['pay']}"
VROW = f"' CASHFLOW'!${fcL}${v}:${lcL}${v}"
NP = 12
# payment 1 = advance month(s) up to AdvMonth, then periods
a0 = 7
sm[f'A{a0}'] = 'PMT 1 (ADV.)'
sm[f'B{a0}'] = '=EOMONTH(StartDate,AdvMonth)'
sm[f'C{a0}'] = '="M0 - M"&AdvMonth'
sm[f'D{a0}'] = f'=SUMPRODUCT(({MROW}<=AdvMonth)*{PROW})'
sm[f'E{a0}'] = f'=D{a0}'
for i in range(1, NP + 1):
    rr = a0 + i
    lo = f'(AdvMonth+1+({i}-1)*PeriodMonths)'; hi = f'MIN(AdvMonth+{i}*PeriodMonths,Rel2Month)'
    show = f'{lo}<=Rel2Month'
    sm[f'A{rr}'] = f'=IF({show},"PMT {i+1}","")'
    sm[f'B{rr}'] = f'=IF({show},EOMONTH(StartDate,{hi}),"")'
    sm[f'C{rr}'] = f'=IF({show},"M"&{lo}&" - M"&{hi},"")'
    sm[f'D{rr}'] = f'=IF({show},SUMPRODUCT(({MROW}>={lo})*({MROW}<={hi})*{PROW}),"")'
    sm[f'E{rr}'] = f'=IF({show},E{rr-1}+D{rr},"")'
at = a0 + NP + 1
sm[f'A{at}'] = 'TOTAL PAYMENT'; sm[f'D{at}'] = f'=SUM(D{a0}:D{at-1})'
sm[f'C{at}'] = 'Check vs contract sum:'; sm[f'E{at}'] = f'=ROUND(D{at}-ContractSum,2)'
for col in 'ABCDE':
    sm[f'{col}{at}'].font = BOLD; sm[f'{col}{at}'].fill = TOTFILL
for rr in range(a0, at + 1):
    sm[f'B{rr}'].number_format = 'mmmm, yyyy'
    for col in 'DE': sm[f'{col}{rr}'].number_format = MONEY
    for col in 'ABCDE': sm[f'{col}{rr}'].border = BOX

m0 = at + 3
sm[f'A{m0}'] = 'PROPOSED CASH FLOW MONTHLY'; sm[f'A{m0}'].font = BOLD
for col, h in zip('ABCDEF', ['MONTH NO.', 'MONTH ENDING', 'VALUATION (US$)', 'PAYMENT (US$)', 'CUMULATIVE PAYMENT (US$)', '% OF CONTRACT PAID']):
    c = sm[f'{col}{m0+1}']; c.value = h; c.font = HDR; c.fill = HFILL; c.alignment = CTR; c.border = BOX
for k in range(NM):
    rr = m0 + 2 + k
    sm[f'A{rr}'] = k
    sm[f'B{rr}'] = f'=EOMONTH(StartDate,A{rr})'; sm[f'B{rr}'].number_format = 'mmmm, yyyy'
    sm[f'C{rr}'] = f'=INDEX({VROW},1,A{rr}+1)'
    sm[f'D{rr}'] = f'=INDEX({PROW},1,A{rr}+1)'
    sm[f'E{rr}'] = f'=D{rr}' if k == 0 else f'=E{rr-1}+D{rr}'
    sm[f'F{rr}'] = f'=E{rr}/ContractSum'; sm[f'F{rr}'].number_format = '0.0%'
    for col in 'CDE': sm[f'{col}{rr}'].number_format = MONEY
    for col in 'ABCDEF': sm[f'{col}{rr}'].border = BOX
mt = m0 + 2 + NM
sm[f'A{mt}'] = 'TOTAL'; sm[f'C{mt}'] = f'=SUM(C{m0+2}:C{mt-1})'; sm[f'D{mt}'] = f'=SUM(D{m0+2}:D{mt-1})'
for col in 'ABCDEF': sm[f'{col}{mt}'].font = BOLD; sm[f'{col}{mt}'].fill = TOTFILL
for col in 'CD': sm[f'{col}{mt}'].number_format = MONEY
sm.conditional_formatting.add(f'A{m0+2}:F{mt-1}', FormulaRule(formula=[f'$A{m0+2}>Rel2Month'], fill=grey, font=Font(color='A6A6A6')))
for col, w in zip('ABCDEF', [16, 18, 20, 18, 22, 14]): sm.column_dimensions[col].width = w

# chart: monthly payment bars + cumulative line
bar = BarChart(); bar.title = 'Monthly payment and cumulative payment (US$)'; bar.y_axis.title = 'Monthly (US$)'
last = m0 + 2 + 30  # chart to end of DLP (month 30)
bar.add_data(Reference(sm, min_col=4, min_row=m0 + 1, max_row=last), titles_from_data=True)
bar.set_categories(Reference(sm, min_col=2, min_row=m0 + 2, max_row=last))
ln = LineChart(); ln.add_data(Reference(sm, min_col=5, min_row=m0 + 1, max_row=last), titles_from_data=True)
ln.y_axis.axId = 200; ln.y_axis.title = 'Cumulative (US$)'; ln.y_axis.crosses = 'max'
bar.x_axis.number_format = 'mmm-yy'; bar += ln
bar.height = 10; bar.width = 24
sm.add_chart(bar, 'H4')

# ---------------- CHECKS on INPUTS ----------------
c0 = CHECK_ROW0
ip[f'A{c0}'] = 'CHECKS (all should read OK)'; ip[f'A{c0}'].font = BOLD
CFn = "' CASHFLOW'!"
checks = [
 ('Contract sum = target US$ 6,250,000.00', 'ContractSum', 'TargetSum'),
 ('Total of bills = contract sum', f"{CFn}C{RT}", 'ContractSum'),
 ('Total valuations = contract sum', f"{CFn}{totL}{v}", 'ContractSum'),
 ('Total payments = contract sum', f"{CFn}{totL}{R['pay']}", 'ContractSum'),
 ('Summary aggregated total = contract sum', f"'CASHFLOW SUMMARY'!D{at}", 'ContractSum'),
 ('Summary monthly total = contract sum', f"'CASHFLOW SUMMARY'!D{mt}", 'ContractSum'),
 ('Advance fully recovered', f"{CFn}{totL}{R['rec']}", 'AdvAmt'),
 ('Retention deducted = limit of retention', f"{CFn}{totL}{R['ret']}", 'RetLimit'),
 ('Retention fully released', f"{CFn}{totL}{R['rel']}", f"{CFn}{totL}{R['ret']}"),
]
for col, h in zip('ABCD', ['CHECK', 'VALUE', 'SHOULD EQUAL', 'RESULT']):
    c = ip[f'{col}{c0+1}']; c.value = h; c.font = HDR; c.fill = HFILL
for i, (lab, a, b) in enumerate(checks):
    rr = c0 + 2 + i
    ip[f'A{rr}'] = lab; ip[f'B{rr}'] = f'={a}'; ip[f'C{rr}'] = f'={b}'
    ip[f'D{rr}'] = f'=IF(ROUND(B{rr}-C{rr},2)=0,"OK","CHECK")'
    for col in 'BC': ip[f'{col}{rr}'].number_format = MONEY
rr = c0 + 2 + len(checks)
extra = [
 ('No negative monthly payment', f"=MIN({CFn}{fcL}{R['pay']}:{lcL}{R['pay']})", 0, f'=IF(B{{r}}>=0,"OK","CHECK")'),
 ('All bills finish by practical completion', f"=MAX({CFn}{endL}{R0}:{endL}{RN})", '=Duration', f'=IF(B{{r}}<=C{{r}},"OK","CHECK")'),
 ('Advance recovered before completion', '=RecEnd', '=Duration', f'=IF(B{{r}}<=C{{r}},"OK","CHECK")'),
 ('Nothing paid after end of DLP', f"=SUMPRODUCT(({CFn}{fcL}6:{lcL}6>Rel2Month)*ABS({CFn}{fcL}{R['pay']}:{lcL}{R['pay']}))", 0, f'=IF(ROUND(B{{r}},2)=0,"OK","CHECK")'),
]
for lab, a, b, res in extra:
    ip[f'A{rr}'] = lab; ip[f'B{rr}'] = a; ip[f'C{rr}'] = b; ip[f'D{rr}'] = res.format(r=rr)
    rr += 1
ip.conditional_formatting.add(f'D{c0+2}:D{rr}', FormulaRule(formula=[f'D{c0+2}="CHECK"'], fill=red))
ip.conditional_formatting.add(f'D{c0+2}:D{rr}', FormulaRule(formula=[f'D{c0+2}="OK"'], fill=TOTFILL))
ip.column_dimensions['A'].width = 42

wb._sheets = [wb[n] for n in ['INPUTS', 'CASHFLOW SUMMARY', ' CASHFLOW', 'GEN SUMMARY']]
wb.active = wb.sheetnames.index('CASHFLOW SUMMARY')
wb.calculation.fullCalcOnLoad = True
wb.save(out)
print('saved', out, 'rows', R, 'RT', RT, 'agg total row', at, 'monthly total row', mt)
