"""Build the Priority Insurance cash flow on the Thoroughbred Place workbook template."""
import sys, copy, datetime
import openpyxl
from openpyxl.utils import get_column_letter as CL
from openpyxl.formatting.rule import ColorScaleRule

ref_path, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(ref_path, keep_links=False)

# drop the thousands of broken external defined names carried in the template
for n in list(wb.defined_names.keys()):
    del wb.defined_names[n]
for ws in wb:
    for n in list(ws.defined_names.keys()):
        del ws.defined_names[n]

TITLE = 'CASHFLOW FORECAST FOR PROPOSED HEAD OFFICE FOR PRIORITY INSURANCE'
DATE_TXT = 'OCTOBER, 2026'

def snapshot(ws, max_row, max_col):
    st = {}
    for r in range(1, max_row + 1):
        for c in range(1, max_col + 1):
            cell = ws._cells.get((r, c))
            if cell is not None:
                st[(r, c)] = copy.copy(cell._style)
    heights = {r: ws.row_dimensions[r].height for r in range(1, max_row + 1)}
    return st, heights

def wipe(ws):
    for m in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(m))
    ws._cells.clear()
    ws.conditional_formatting = type(ws.conditional_formatting)()
    for r in list(ws.row_dimensions.keys()):
        del ws.row_dimensions[r]

def put(ws, st, r, c, ref_rc, value=None, height_src=None):
    cell = ws.cell(row=r, column=c)
    if ref_rc in st:
        cell._style = copy.copy(st[ref_rc])
    if value is not None:
        cell.value = value
    return cell

def set_header(ws):
    for hdr in (ws.oddHeader, ws.firstHeader):
        if hdr.center.text: hdr.center.text = TITLE
        if hdr.right.text: hdr.right.text = DATE_TXT

# ============================== GEN SUMMARY. ==============================
gs = wb['GEN SUMMARY.']
gst, gsh = snapshot(gs, 75, 26)
wipe(gs)
items = [  # (description, estimate amount US$ before discount) from Preliminary Estimate rev 6, OPTION 1rev col E
 ('BILL NO. 1- PRELIMINARIES AND GENERAL ITEMS', '=366625+50000'),
 ('BILL NO. 2- DEMOLITIONS AND ALTERATIONS', 50000),
 ('BILL NO. 3 -SUBSTRUCTURE (ALL PROVISIONAL)', '=1585*350'),
 ('BILL NO. 4 -SUB-BASEMENT FLOOR', '=1585*400'),
 ('BILL NO. 5 - GROUND FLOOR', '=450*500'),
 ('BILL NO. 6 - FIRST FLOOR', '=600*500'),
 ('BILL NO. 7- SECOND FLOOR', '=600*500'),
 ('BILL NO. 8 -THIRD FLOOR', '=600*500'),
 ('BILL NO. 9 -FOURTH FLOOR', '=600*500'),
 ('BILL NO. 10 - FIFTH FLOOR', '=600*500'),
 ('BILL NO. 11 - KITCHEN CABINETRY/WALL CLADDING', 134515.22004867764),
 ('BILL NO. 12. PLUMBING, FIRE-FIGHTING AND MECHANICAL', '=659925+125000'),
 ('BILL NO. 13: ELECTRICAL WORKS', '=1026550+50000'),
 ('BILL NO. 14. EXTERNAL FAÇADE WORKS', '=606968.250712613+50000'),
 ('BILL NO. 15.- EXTERNAL WORKS (ALL PROVISIONAL)', 47193.43552502702),
 ('DESIGN FEES', 194211.36000723258),
 ('PROJECT MANAGEMENT FEES', '=623262.5-175000'),
]
LET = list('ABCDEFGHJKLMNPQRS')
for r in range(1, 5):
    put(gs, gst, r, 1, (r, 1))
gs['A1'] = 'PROJECT: PROPOSED HEAD OFFICE FOR PRIORITY INSURANCE'
gs['A2'] = 'LOCATION: RIDGE, ACCRA'
gs['A3'] = 'CLIENT: PRIORITY INSURANCE'
gs['A4'] = 'DATE: 07/10/2026 (PRELIMINARY ESTIMATE REV. 6)'
for c in range(1, 7):
    put(gs, gst, 5, c, (5, c))
gs['A5'] = 'ITEM'; gs['B5'] = 'GENERAL SUMMARY'; gs['D5'] = 'AMOUNT USD'; gs['E5'] = 'DISCOUNTED AMOUNT USD'
gs['E5']._style = copy.copy(gst[(5, 4)])
for c in range(1, 7): put(gs, gst, 6, c, (6, c))
GS_ROWS = []
r = 7
for i, (desc, amt) in enumerate(items):
    for c in range(1, 7):
        put(gs, gst, r, c, (7, c)); put(gs, gst, r + 1, c, (8, c))
    gs.cell(r, 5)._style = copy.copy(gst[(7, 4)])
    gs.cell(r, 1).value = LET[i]; gs.cell(r, 2).value = desc; gs.cell(r, 4).value = amt
    GS_ROWS.append(r); r += 2
last_item = r - 2
SUB1, DISC, AGREED, TOTW, SIGN, DATER = r + 3, r + 5, r + 7, r + 10, r + 13, r + 16
for rr, src in ((SUB1, 48), (DISC, 50), (AGREED, 50), (TOTW, 64), (SIGN, 67), (DATER, 70)):
    for c in range(1, 7):
        put(gs, gst, rr, c, (src, c))
    if (src, 4) in gst: gs.cell(rr, 5)._style = copy.copy(gst[(src, 4)])
gs[f'B{SUB1}'] = 'SUB - TOTAL (1)'; gs[f'C{SUB1}'] = 'US $'
gs[f'D{SUB1}'] = f'=SUM(D7:D{last_item + 1})'; gs[f'E{SUB1}'] = f'=SUM(E7:E{last_item + 1})'
gs[f'B{DISC}'] = 'LESS: DISCOUNT'; gs[f'D{DISC}'] = f'=D{SUB1}-D{AGREED}'
gs[f'B{AGREED}'] = 'AGREED DISCOUNTED CONTRACT SUM'; gs[f'D{AGREED}'] = 6250000
gs[f'B{TOTW}'] = 'TOTAL COST OF THE WORKS (EXCLUDING TAXES)'; gs[f'C{TOTW}'] = 'US $'
gs[f'D{TOTW}'] = f'=D{SUB1}-D{DISC}'; gs[f'E{TOTW}'] = f'=E{SUB1}'
gs[f'B{SIGN}'] = 'SIGNED: ……………………………………………………………'
gs[f'B{DATER}'] = 'DATE: ………………………………………...........………….'
for rr in GS_ROWS:   # discount spread pro-rata, as in the estimate
    gs[f'E{rr}'] = f'=D{rr}*$D${AGREED}/$D${SUB1}'
for rr, h in gsh.items():
    if h: gs.row_dimensions[rr].height = h
gs.column_dimensions['E'].width = gs.column_dimensions['D'].width
gs.print_area = f'A1:F{DATER + 2}'

# ============================== CASHFLOW ==============================
cf = wb[' CASHFLOW']
cst, csh = snapshot(cf, 120, 56)
wipe(cf)
NMONTH = 25                     # months 0..24
MC = [5 + k for k in range(NMONTH)]           # E..AC
REL1, REL2 = 5 + NMONTH, 6 + NMONTH           # AD, AE
TOT = REL2 + 1                                # AF
PS, PD = TOT + 2, TOT + 3                     # AH start month, AI duration
ALLM = MC + [REL1, REL2]
fL, lL, totL = CL(MC[0]), CL(REL2), CL(TOT)
def refcol(c):  # template column whose style a new column takes
    if c <= 4: return c
    if c in MC: return c
    if c == REL1: return 42
    if c == REL2: return 43
    if c == TOT: return 44
    return 44
def row_style(r_new, r_ref, upto=TOT):
    for c in range(1, upto + 1):
        put(cf, cst, r_new, c, (r_ref, refcol(c)))
    if csh.get(r_ref): cf.row_dimensions[r_new].height = csh[r_ref]

# parameters table location is fixed after bills; compute bills first
# sub-row spec: (description, %, start month, duration)
def floor(name, s, L, f, F):
    return [(f'(0%) Start of {name} Structure', 0.3, s, L - 1), ('(100%) Completion of Structure', 0.2, s + L - 1, 1),
            ('(0%) Start of Finishings and MEP', 0.3, f, F - 2), ('(100%) Completion of Finishings and MEP', 0.2, f + F - 2, 2)]
bills = [
 [('(100%) Site Possession and Hoarding', 0.3, 1, 1), ('(100%) Site Setup and Mobilization', 0.2, 2, 1), ('(100%) Site Maintenance', 0.5, 3, 22)],
 [('(0%) Start of Demolition Works', 0.8, 1, 1), ('(100%) End of Demolition Works', 0.2, 2, 1)],
 [('Procurement Phase I (Substructure materials on site and in transit) (0%)', 0.5, 1, 2), ('(50%) Completion of Ground Works', 0.25, 3, 1), ('(100%) Completion of Substructure Concrete Works', 0.25, 4, 1)],
 floor('Sub-Basement Floor', 3, 4, 7, 12),
 floor('Ground Floor', 5, 3, 8, 13),
 floor('First Floor', 7, 3, 10, 12),
 floor('Second Floor', 9, 3, 12, 10),
 floor('Third Floor', 11, 3, 14, 9),
 floor('Fourth Floor', 13, 3, 16, 7),
 floor('Fifth Floor', 15, 3, 18, 5),
 [('(0%) Start of Kitchen Cabinetry/Wall Cladding works', 0.7, 16, 1), ('100% of works fabricated', 0.2, 19, 2), ('100% of works installed on site', 0.1, 22, 1)],
 [('First fix, sleeves and pipework', 0.6, 4, 15), ('Second fix, testing and commissioning', 0.4, 19, 5)],
 [('First fix, conduits and containment', 0.6, 4, 15), ('Second fix, testing and commissioning', 0.4, 19, 5)],
 [('Procurement and fabrication of facade materials', 0.7, 12, 3), ('Installation of facade', 0.3, 15, 8)],
 [('(50%) External works', 0.5, 20, 3), ('(100%) Completion of External works', 0.5, 23, 2)],
 [('Design fees - 1st instalment', 0.5, 1, 1), ('Design fees - balance', 0.5, 2, 11)],
 [('Monthly project management', 1.0, 1, 24)],
]
# layout rows
r = 3
ADV_ROW, ADV_SUB = 3, 4
r = 6
bill_rows = []
for subs in bills:
    bill_rows.append((r, list(range(r + 1, r + 1 + len(subs)))))
    r += len(subs) + 2
LASTB = r - 1
V = r              # ESTIMATED MONTHLY VALUATION
CV, RET, CRET, SUBT, ADVR, CADV, PAY, CPAY = V + 1, V + 2, V + 3, V + 4, V + 5, V + 6, V + 7, V + 8
T0 = CPAY + 2      # parameter table header
P = {}             # parameter name -> row
params = [
 ('CSUM', 'A', 'AGREED CONTRACT SUM (DISCOUNTED, LESS TAXES)', f"='GEN SUMMARY.'!D{TOTW}", 'money'),
 ('RLIM', 'B', 'LIMIT OF RETENTION', None, 'money'),
 ('ADVP', 'C', 'ADVANCE MOBILIZATION (% OF CONTRACT SUM)', 0.25, 'pct'),
 ('RETP', 'D', 'RETENTION DEDUCTED PER VALUATION', 0.10, 'pct'),
 ('RLIMP', 'E', 'LIMIT OF RETENTION (% OF CONTRACT SUM)', 0.05, 'pct'),
 ('REL1P', 'F', 'RETENTION RELEASED AT PRACTICAL COMPLETION', 0.5, 'pct'),
 ('START', 'G', 'COMMENCEMENT DATE (MONTH 0)', datetime.date(2026, 9, 30), 'date'),
 ('DUR', 'H', 'CONTRACT PERIOD (MONTHS)', 24, 'num'),
 ('PCD', 'J', 'PRACTICAL COMPLETION DATE', None, 'date'),
 ('DLP', 'K', 'DEFECTS LIABILITY PERIOD (MONTHS)', 6, 'num'),
 ('DLPD', 'L', 'END OF DEFECTS LIABILITY PERIOD', None, 'date'),
 ('RS', 'M', 'ADVANCE REPAYMENT STARTS (MONTH NO.)', 3, 'num'),
 ('RN', 'N', 'ADVANCE REPAYMENT PERIOD (MONTHS)', 18, 'num'),
]
for i, p in enumerate(params): P[p[0]] = T0 + 1 + i
A = lambda k: f'$C${P[k]}'
cf.cell(1, 1)
# ---- header rows 1-2
row_style(1, 1); row_style(2, 2)
cf['A1'] = 'ITEM '; cf['B1'] = 'DESCRIPTION'; cf['D1'] = 'TOTAL'
for k, c in enumerate(ALLM):
    L = CL(c)
    if c in MC:
        cf.cell(2, c).value = 0 if k == 0 else f'={CL(c-1)}2+1'
    cf.cell(1, c).value = f'=EOMONTH({A("START")},{L}2)'
cf.cell(2, REL1).value = f'={A("DUR")}+1'
cf.cell(2, REL2).value = f'={A("DUR")}+{A("DLP")}'
cf.cell(1, TOT).value = 'TOTAL'
for c, h in ((PS, 'START MONTH'), (PD, 'DURATION (MONTHS)')):
    cf.cell(1, c)._style = copy.copy(cst[(1, 44)]); cf.cell(1, c).value = h
    cf.cell(2, c)._style = copy.copy(cst[(2, 44)])
    cf.column_dimensions[CL(c)].width = 22

def month_formula(L, br, subs):
    terms = [f'IF(AND({L}$2>=${CL(PS)}{s},{L}$2<${CL(PS)}{s}+${CL(PD)}{s}),$D{s}/${CL(PD)}{s},0)' for s in subs]
    return '=' + '+'.join(terms)

def write_bill(br, subs, item, desc_f, amt_f, sub_specs, hdr_ref=6, sub_ref=7, blank_ref=10):
    row_style(br, hdr_ref)
    cf.cell(br, 1).value = item; cf.cell(br, 2).value = desc_f; cf.cell(br, 4).value = amt_f
    for c in ALLM:
        cf.cell(br, c).value = month_formula(CL(c), br, subs)
    cf.cell(br, TOT).value = f'=SUM({fL}{br}:{lL}{br})'
    for s, (d, pct, st, du) in zip(subs, sub_specs):
        row_style(s, sub_ref)
        cf.cell(s, 2).value = d; cf.cell(s, 3).value = pct; cf.cell(s, 3).number_format = '0%'
        cf.cell(s, 4).value = f'=C{s}*$D${br}'
        for c, v in ((PS, st), (PD, du)):
            x = cf.cell(s, c); x._style = copy.copy(cst[(7, 44)]); x.value = v; x.number_format = '0'
    row_style(subs[-1] + 1, blank_ref)

# advance
write_bill(ADV_ROW, [ADV_SUB], 'A', 'ADVANCE MOBILIZATION', f'={A("ADVP")}*{A("CSUM")}',
           [('Contract Signing ', 1, 0, 1)], hdr_ref=3, sub_ref=4, blank_ref=5)
for i, ((br, subs), specs) in enumerate(zip(bill_rows, bills)):
    g = GS_ROWS[i]
    write_bill(br, subs, f"='GEN SUMMARY.'!A{g}", f"='GEN SUMMARY.'!B{g}", f"='GEN SUMMARY.'!E{g}", specs)
    cf.cell(br, 1).value = LET[i + 1] if i + 1 < len(LET) else 'T'
LETS = list('BCDEFGHJKLMNPQRST')
for i, (br, _) in enumerate(bill_rows): cf.cell(br, 1).value = LETS[i]

# ---- summary rows (template rows 96-104)
for new, ref in zip(range(V, CPAY + 1), range(96, 105)):
    row_style(new, ref)
labels = ['ESTIMATED MONTHLY VALUATION (EXCL. ADVANCE)', 'CUMULATIVE VALUATION', 'DEDUCT RETENTION', 'CUMULATIVE RETENTION',
          'SUB TOTAL ', 'ADVANCE REPAYMENT', 'CUMULATIVE ADVANCE REPAYMENT', 'ESTIMATED MONTHLY PAYMENT', 'CUMULATIVE MONTHLY PAYMENT']
for rr, t in zip(range(V, CPAY + 1), labels): cf.cell(rr, 2).value = t
billset = [ADV_ROW] + [b for b, _ in bill_rows]
for idx, c in enumerate(ALLM):
    L = CL(c); Pv = CL(c - 1)
    first = idx == 0
    cf[f'{L}{V}'] = '=' + '+'.join(f'{L}{b}' for b in billset[1:])
    work = f'{L}{V}'
    cf[f'{L}{CV}'] = f'={work}' if first else f'={Pv}{CV}+{work}'
    prev_cret = '0' if first else f'{Pv}{CRET}'
    if c == REL1:
        cf[f'{L}{RET}'] = f'=-ROUND({prev_cret}*{A("REL1P")},2)'
    elif c == REL2:
        cf[f'{L}{RET}'] = f'=-{prev_cret}'
    else:
        cf[f'{L}{RET}'] = f'=MIN({A("RETP")}*{work},MAX(0,{A("RLIM")}-{prev_cret}))'
    cf[f'{L}{CRET}'] = f'={prev_cret}+{L}{RET}'
    cf[f'{L}{SUBT}'] = f'={L}{ADV_ROW}+{L}{V}-{L}{RET}'
    cf[f'{L}{ADVR}'] = f'=IF(AND({L}$2>={A("RS")},{L}$2<{A("RS")}+{A("RN")}),$D${ADV_ROW}/{A("RN")},0)'
    cf[f'{L}{CADV}'] = f'={L}{ADVR}' if first else f'={Pv}{CADV}+{L}{ADVR}'
    cf[f'{L}{PAY}'] = f'={L}{SUBT}-{L}{ADVR}'
    cf[f'{L}{CPAY}'] = f'={L}{PAY}' if first else f'={Pv}{CPAY}+{L}{PAY}'
for rr in (V, RET, SUBT, ADVR, PAY):
    cf[f'{totL}{rr}'] = f'=SUM({fL}{rr}:{lL}{rr})'
cf.conditional_formatting.add(f'{fL}{PAY}:{totL}{PAY}', ColorScaleRule(start_type='min', start_color='F8696B', mid_type='percentile', mid_value=50, mid_color='FFEB84', end_type='max', end_color='63BE7B'))
cf.conditional_formatting.add(f'D{PAY}:{totL}{PAY}', ColorScaleRule(start_type='min', start_color='F8696B', mid_type='percentile', mid_value=50, mid_color='FFEB84', end_type='max', end_color='63BE7B'))

# ---- parameter table (template rows 106-108)
row_style(T0, 106, upto=4)
cf[f'A{T0}'] = 'ITEM'; cf[f'B{T0}'] = 'DESCRIPTION'; cf[f'C{T0}'] = 'AMOUNT'
for key, item, desc, val, kind in params:
    rr = P[key]; row_style(rr, 107, upto=4)
    cf[f'A{rr}'] = item; cf[f'B{rr}'] = desc; cf[f'C{rr}'] = val
    cf[f'C{rr}'].number_format = {'money': cst[(107, 3)] and cf[f'C{rr}'].number_format, 'pct': '0%', 'date': 'dd mmmm yyyy', 'num': '0'}[kind]
cf[f'C{P["RLIM"]}'] = f'={A("RLIMP")}*{A("CSUM")}'
cf[f'C{P["PCD"]}'] = f'=EOMONTH({A("START")},{A("DUR")})'
cf[f'C{P["DLPD"]}'] = f'=EOMONTH(C{P["PCD"]},{A("DLP")})'
CHK = T0 + len(params) + 2
row_style(CHK, 108, upto=4)
cf[f'A{CHK}'] = ''; cf[f'B{CHK}'] = 'CHECK: TOTAL PAYMENT LESS CONTRACT SUM (MUST BE NIL)'
cf[f'C{CHK}'] = f'=ROUND({totL}{PAY}-{A("CSUM")},2)'
NT = CHK + 3
notes = ['NOTES:', '1. TAXES NOT INCLUDED ', '2. PAYMENTS PROJECTED TO BE AT THE END OF THE RESPECTIVE MONTHS.',
         f'3. EACH BILL IS SPREAD OVER ITS SUB-ITEMS USING THE START MONTH AND DURATION IN COLUMNS {CL(PS)} AND {CL(PD)}; AMOUNTS LINK TO GEN SUMMARY.',
         '4. RETENTION IS DEDUCTED UNTIL THE LIMIT OF RETENTION IS REACHED; HALF IS RELEASED THE MONTH AFTER PRACTICAL COMPLETION AND THE BALANCE AT THE END OF THE DEFECTS LIABILITY PERIOD.']
for i, t in enumerate(notes):
    row_style(NT + i, 111 + min(i, 2), upto=4); cf[f'B{NT + i}'] = t

# column widths: month columns take the template widths of the matching columns
oldw = {k: v.width for k, v in cf.column_dimensions.items()}
for k in list(cf.column_dimensions.keys()):
    if openpyxl.utils.column_index_from_string(k) > 4: del cf.column_dimensions[k]
for c in ALLM + [TOT]:
    cf.column_dimensions[CL(c)].width = 24
cf.column_dimensions[CL(TOT + 1)].width = 4
for c in (PS, PD): cf.column_dimensions[CL(c)].width = 22
cf.print_area = f'A1:{totL}{NT + len(notes)}'
cf.freeze_panes = 'E3'

# ============================== CASHFLOW SUMMARY ==============================
sm = wb['CASHFLOW SUMMARY']
sst, ssh = snapshot(sm, 60, 6)
wipe(sm)
def srow(rn, rref, upto=4):
    for c in range(1, upto + 1): put(sm, sst, rn, c, (rref, c))
    if ssh.get(rref): sm.row_dimensions[rn].height = ssh[rref]
CFQ = "' CASHFLOW'!"
srow(1, 1); sm['A1'] = 'PROPOSED  CASH FLOW AGGREGATED'; sm.merge_cells('A1:C1')
srow(2, 2); sm['A2'] = 'PAYMENT NO. '; sm['B2'] = 'MONTH, YEAR'; sm['C2'] = 'AMOUNT (US$)'
groups = [(0, 0)] + [(1 + 4 * i, 4 + 4 * i) for i in range(6)]   # advance, then 4-monthly as reference
agg = []
for gi, (a, b) in enumerate(groups):
    agg.append((CL(MC[a]), CL(MC[b])))
agg += [(CL(REL1), CL(REL1)), (CL(REL2), CL(REL2))]
r = 3
for i, (ca, cb) in enumerate(agg):
    srow(r, 3 if i == 0 else 4)
    sm[f'A{r}'] = 'PMT 1 (ADV.)' if i == 0 else f'PMT {i + 1}'
    sm[f'B{r}'] = f'={CFQ}{cb}1'; sm[f'B{r}'].number_format = 'mmmm, yyyy'
    sm[f'C{r}'] = f'=SUM({CFQ}{ca}{PAY}:{cb}{PAY})'
    r += 1
AGT = r
srow(AGT, 14); sm[f'A{AGT}'] = 'TOTAL PAYMENT'; sm[f'C{AGT}'] = f'=SUM(C3:C{AGT - 1})'; sm.merge_cells(f'A{AGT}:B{AGT}')
M0 = AGT + 3
srow(M0, 17); sm[f'A{M0}'] = 'PROPOSED CASH FLOW MONTHLY'; sm.merge_cells(f'A{M0}:C{M0}')
srow(M0 + 1, 18); sm[f'A{M0+1}'] = 'PAYMENT NO. '; sm[f'B{M0+1}'] = 'MONTH, YEAR'; sm[f'C{M0+1}'] = ' AMOUNT (US$) '
r = M0 + 2
for i, c in enumerate(ALLM):
    srow(r, 19 if i == 0 else 20)
    L = CL(c)
    sm[f'A{r}'] = 'PMT 1 (ADV)' if i == 0 else f'PMT {i + 1}'
    sm[f'B{r}'] = f'={CFQ}{L}1'; sm[f'B{r}'].number_format = 'mmmm, yyyy'
    sm[f'C{r}'] = f'={CFQ}{L}{PAY}'
    sm[f'D{r}'] = f'={CFQ}{L}{CPAY}'
    r += 1
MT = r
srow(MT, 58); sm[f'A{MT}'] = 'TOTAL PAYMENT'; sm[f'C{MT}'] = f'=SUM(C{M0+2}:C{MT-1})'; sm.merge_cells(f'A{MT}:B{MT}')
sm.print_area = f'A{M0}:D{MT}'

# ============================== CHART ==============================
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
chs = wb['CASHFLOW SUMMARY CHART']
old = chs._charts[0]
bar = BarChart(); bar.type = 'col'; bar.title = 'PROPOSED MONTHLY CASHFLOW'; bar.legend = None
bar.add_data(Reference(sm, min_col=3, min_row=M0 + 2, max_row=MT - 1), titles_from_data=False)
bar.set_categories(Reference(sm, min_col=2, min_row=M0 + 2, max_row=MT - 1))
bar.series[0].graphicalProperties = GraphicalProperties(solidFill='ED7D31')
bar.x_axis.number_format = 'mmm yyyy'; bar.x_axis.delete = False; bar.y_axis.delete = False
bar.y_axis.number_format = '#,##0'; bar.y_axis.majorGridlines = openpyxl.chart.axis.ChartLines()
bar.gapWidth = 150
bar.anchor = old.anchor
chs._charts = [bar]

# ============================== COVER ==============================
cp = wb['Cover Page .']
cp['B9'] = 'CASHFLOW FORECAST FOR PROPOSED HEAD OFFICE FOR PRIORITY INSURANCE'
cp['F21'] = DATE_TXT
for ws in wb: set_header(ws)

wb.active = 0
wb.calculation.fullCalcOnLoad = True
wb.save(out)
print(dict(V=V, PAY=PAY, CPAY=CPAY, T0=T0, CHK=CHK, AGT=AGT, MT=MT, M0=M0, TOTW=TOTW, SUB1=SUB1, cols=(fL, lL, totL)))
