exec(open('build.py').read())
from openpyxl.comments import Comment
wb=Workbook()
AR='Arial'
def F(**k): return Font(name=AR,**k)
thin=Side(style='thin',color='999999'); BD=Border(left=thin,right=thin,top=thin,bottom=thin)
HDR=PatternFill('solid',fgColor='1F3864'); SUB=PatternFill('solid',fgColor='D9E1F2'); TOT=PatternFill('solid',fgColor='FFF2CC'); INP=PatternFill('solid',fgColor='F2F2F2')
BLUE=F(color='0000FF',size=9); BLK=F(size=9); GRN=F(color='008000',size=9)
def hdr(ws,r,vals,widths=None):
    for i,v in enumerate(vals,1):
        c=ws.cell(r,i,v); c.font=F(bold=True,color='FFFFFF',size=9); c.fill=HDR; c.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center'); c.border=BD
    if widths:
        for i,w in enumerate(widths,1): ws.column_dimensions[CL(i)].width=w

# ---------- Notes sheet ----------
ns=wb.active; ns.title='Notes & Assumptions'
NOTES=[
('PROPOSED KANESHIE BLOCK N REDEVELOPMENT - REINFORCEMENT TAKE-OFF',True),
('Source: Structural drawings SHC-KANESHIE-STR-000 to STR-107 (108 sheets, Documents.pdf). Take-off prepared floor by floor; all quantities in tonnes.',False),
('',False),
('METHOD OF MEASUREMENT',True),
('1. Every take-off line shows: No. of members x No. of bars per member = Total bars; Total bars x Cut length = Total length; Total length x Unit mass = kg; kg / 1000 = tonnes.',False),
('2. Unit mass of bar (kg/m) = d^2 / 162 (d in mm), calculated by formula in column L of every floor sheet (0.617 kg/m Y10, 0.888 Y12, 1.580 Y16, 2.469 Y20, 3.858 Y25).',False),
('3. Raft, floor slabs, beams, staircases and lift-core slab are taken from the Bar Bending Schedules (BBS) on the drawings (bar mark, diameter, quantity, cut length). Cut lengths already include laps/bends as scheduled.',False),
('4. Floors 4th to 8th are typical (STR-076 to STR-082): the typical schedules are measured once on each of the five floor sheets.',False),
('5. Main staircase typical flight (STR-027, 4th-10th) measured on 4th, 5th, 6th, 7th, 8th and 9th floors (6 storeys). Emergency stair typical flight M1-3rd (STR-033) measured at M1, M2 and Mezzanine; typical 4th-10th (STR-037) on 6 storeys. Staircase BBS quantities are per storey (e.g. 1201: 30 no = 2x15 in plan).',False),
('6. Elements are allocated to the floor they rise FROM: columns, walls and stair flights between level X and the level above are measured under level X. Column/wall starters from the raft to Ground level are measured under Substructure.',False),
('7. Structural levels used (SSL): Raft top -1000, NGL 0, GF +300, M1 +2500, 1st +4150, M2 +5200, 2nd +6850, Mezz +7900, 3rd +10900, 4th +14200 then +3300 per floor to 10th +34000, Roof top terrace +37300, Roof +40450, Top of lift core +44650.',False),
('',False),
('COLUMNS (STR-007 to STR-012)',True),
('8. Number of links and main bars per storey taken from the column elevations (text callouts) x number of columns of each type; cut lengths from the column BBS. Column count confirmed on raft GA STR-002: 01A x5, 01B x1, 01C x2, 01D x1, 02A x3, 02B x6, 02C x1, 02D x15, SWC-01A x1 (35 no.).',False),
('9. Sheet STR-009 is a duplicate of STR-008 (identical column types 01C/01D, same schedule, only section numbers differ) - measured once only.',False),
('10. Cross-ties Y1005 per link set: BBS ratio used (02A/02B = 5 per set per STR-010 BBS; 02C/02D = 3 per set per STR-011 BBS). SWC-01A: 7 no. Y1003 + 4 no. Y1004 per set per STR-012 BBS. See Column Check sheet for reconciliation against BBS totals.',False),
('11. SWC-01A top lift labelled "48-Y2004" on elevation is taken as bar mark 2011 (Y25, 3370) per BBS.',False),
('',False),
('SHEAR WALLS / LIFT WALLS (STR-013 to STR-017) - NO BBS ISSUED; MEASURED FROM DETAILS',True),
('12. Wall lengths from raft GA STR-002 figured dimensions; heights from wall elevations. Horizontal bars per face per storey = count shown on elevations CW-01/CW-03 (main core) and CW-13 (emergency core); vertical bars per face = 29 no. (3600 walls, per elevations), 52 no. (CW-13) or ROUNDUP(L/150)+1 elsewhere, both faces (NF/FF).',False),
('13. Horizontal bar cut length = wall length - 2 x 30 cover + 40d (one lap/corner anchorage). Vertical bar cut length = storey height + 40d lap (note 3.0: min lap 40d). Starters from raft = 1250 embedment + 350 bend + storey height + 40d.',False),
('14. Vertical bar size per elevations: Y25 up to 4th floor (lift walls to 5th), Y20 above.',False),
('15. Confinement links "Y10xx@150 stirrups": 52 positions in main core plan (STR-015; split 26 stair/26 lift by wall length) and 33 positions in emergency core plan (STR-013); vertical spacing 150; assumed cut length 1.80 m each (link around 2 bars within 250 wall, incl. hooks) - no BBS issued.',False),
('16. Lift walls (CW-02, 03, 04, 06, 08 and lift section of CW-07) continue to Top of Lift Core +44650; stair-core walls stop at Roof +40450.',False),
('17. Retaining walls: none shown on the drawings. RAMP-01 wall (250 x 7400, raft GA) has no reinforcement detail - measured PROVISIONALLY as Y12@150 NF/FF both ways.',False),
('',False),
('EXCLUSIONS / QUERIES (RFI)',True),
('18. Ground floor slab-on-grade: no reinforcement drawing issued - not measured.',False),
('19. STR-010 (02A/B) BBS shows 5 cross-ties per set while STR-011 (02C/D) BBS shows 3 for the same section detail - confirm. If 5 apply to 02C/02D, add approx. 5,800 x 2 x 1.008 m Y10 = 7.2 t.',False),
('20. STR-008 (01C/01D) BBS lists 512 no. Y2001 while elevations show 368 no. (appears copied from 01A/01B). Elevations used.',False),
('21. Wall links, wall laps and ramp wall are the only items measured without a BBS; tie wire, chairs/spacers and wastage are NOT included (add allowance as required, typically 2.5-5%).',False),
('',False),
('Colour code: blue text = figures transcribed from drawings (inputs); black = formulas.',False),
]
for i,(t,b) in enumerate(NOTES,1):
    c=ns.cell(i,1,t); c.font=F(bold=b,size=12 if i==1 else 10); c.alignment=Alignment(wrap_text=True,vertical='top')
ns.column_dimensions['A'].width=150

# ---------- floor sheets ----------
COLS=['Item','Element','Drawing','Description / location','Bar mark','Dia (mm)','No. of members','No. of bars per member','Total no. of bars','Cut length per bar (m)','Total length (m)','Unit mass (kg/m)','Weight (kg)','Weight (t)','Source']
WID=[6,20,11,70,9,8,9,11,10,11,12,10,12,11,22]
FIRST=6
SHEETNAMES={}; MATRIX={}
for fk,short,long_ in FLOORS:
    sn='%s %s'%(fk,short)
    SHEETNAMES[fk]=sn
    ws=wb.create_sheet(sn)
    ws['A1']='REINFORCEMENT TAKE-OFF - %s'%long_.upper(); ws['A1'].font=F(bold=True,size=12)
    ws['A2']='Proposed Kaneshie Block N Redevelopment'; ws['A2'].font=F(size=10)
    ws['A3']='Calculation per line: Total bars = members x bars/member; Total length = bars x cut length; kg = length x d^2/162; t = kg/1000'; ws['A3'].font=F(italic=True,size=9)
    hdr(ws,FIRST-1,COLS,WID)
    ws.freeze_panes=ws.cell(FIRST,5)
    r=FIRST
    order={e:i for i,e in enumerate(ELEMENTS)}
    data=sorted(rows[fk],key=lambda d:order[d['el']])
    for i,d in enumerate(data,1):
        vals=[i,d['el'],d['ref'],d['desc'],d['mark'],d['dia'],d['mem'],d['bars'],'=G%d*H%d'%(r,r),d['len'],'=I%d*J%d'%(r,r),'=F%d^2/162'%r,'=K%d*L%d'%(r,r),'=M%d/1000'%r,d['note']]
        for j,v in enumerate(vals,1):
            c=ws.cell(r,j,v); c.border=BD
            c.font=BLUE if j in (5,6,7,8,10) else BLK
        for j,fmt in ((10,'0.000'),(11,'#,##0.00'),(12,'0.000'),(13,'#,##0.00'),(14,'0.000')): ws.cell(r,j).number_format=fmt
        r+=1
    last=r-1
    r+=1
    ws.cell(r,4,'SUMMARY - %s: ELEMENT BY BAR SIZE (TONNES)'%short.upper()).font=F(bold=True,size=10); r+=1
    hr=r
    for j,v in enumerate(['Element']+DIAS+['Total (t)'],4):
        c=ws.cell(r,j,v); c.font=F(bold=True,color='FFFFFF',size=9); c.fill=HDR; c.border=BD; c.alignment=Alignment(horizontal='center')
        if isinstance(v,int): c.number_format='"Y"0'
    r+=1; e0=r
    for e in ELEMENTS:
        ws.cell(r,4,e).font=BLK; ws.cell(r,4).border=BD
        for j in range(5,5+len(DIAS)):
            c=ws.cell(r,j,'=SUMIFS($N$%d:$N$%d,$B$%d:$B$%d,$D%d,$F$%d:$F$%d,%s$%d)'%(FIRST,last,FIRST,last,r,FIRST,last,CL(j),hr))
            c.number_format='0.000;-0.000;"-"'; c.font=BLK; c.border=BD
        c=ws.cell(r,5+len(DIAS),'=SUM(E%d:%s%d)'%(r,CL(4+len(DIAS)),r)); c.number_format='0.000;-0.000;"-"'; c.font=F(bold=True,size=9); c.border=BD
        r+=1
    ws.cell(r,4,'TOTAL - %s'%short.upper())
    for j in range(5,6+len(DIAS)):
        c=ws.cell(r,j,'=SUM(%s%d:%s%d)'%(CL(j),e0,CL(j),r-1)); c.number_format='0.000'
    for j in range(4,6+len(DIAS)):
        c=ws.cell(r,j); c.fill=TOT; c.font=F(bold=True,size=10); c.border=BD
    ws.cell(r,5+len(DIAS)+1,'Check vs detail (should be 0):').font=BLK
    ws.cell(r,5+len(DIAS)+4,'=ROUND(SUM(N%d:N%d)-%s%d,6)'%(FIRST,last,CL(5+len(DIAS)),r)).font=BLK
    MATRIX[fk]=(sn,e0)
    ws.sheet_properties.tabColor='4472C4'
    SHEETNAMES[fk]=(sn,FIRST,last)

# ---------- Summary ----------
sm=wb.create_sheet('Summary',1)
sm['A1']='REINFORCEMENT SUMMARY - FLOOR BY FLOOR (TONNES)'; sm['A1'].font=F(bold=True,size=12)
sm['A2']='Proposed Kaneshie Block N Redevelopment - High yield steel BS4449 grade 500. Values link to the floor sheets (green).'; sm['A2'].font=F(size=9,italic=True)
H=['Ref','Floor / level']+ELEMENTS+['TOTAL (t)']
hdr(sm,4,H,[6,34]+[13]*len(ELEMENTS)+[13])
r=5
for fk,short,long_ in FLOORS:
    sn,a,b=SHEETNAMES[fk]
    sm.cell(r,1,fk).font=BLK; sm.cell(r,2,long_).font=BLK
    for j,e in enumerate(ELEMENTS,3):
        c=sm.cell(r,j,"=SUMIF('%s'!$B$%d:$B$%d,\"%s\",'%s'!$N$%d:$N$%d)"%(sn,a,b,e,sn,a,b)); c.font=GRN; c.number_format='0.000;-0.000;"-"'; c.border=BD
    c=sm.cell(r,3+len(ELEMENTS),'=SUM(C%d:%s%d)'%(r,CL(2+len(ELEMENTS)),r)); c.number_format='0.000'; c.font=F(bold=True,size=9); c.border=BD
    r+=1
sm.cell(r,2,'GRAND TOTAL').font=F(bold=True,size=10)
for j in range(3,4+len(ELEMENTS)):
    c=sm.cell(r,j,'=SUM(%s5:%s%d)'%(CL(j),CL(j),r-1)); c.number_format='#,##0.000'; c.font=F(bold=True,size=10); c.fill=TOT; c.border=BD
GT=r
r+=3
sm.cell(r,1,'SUMMARY BY BAR DIAMETER (TONNES)').font=F(bold=True,size=11); r+=1
hdr(sm,r,['Ref','Floor / level']+['Y%d'%d for d in DIAS]+['TOTAL (t)']); r+=1
d0=r
for fk,short,long_ in FLOORS:
    sn,a,b=SHEETNAMES[fk]
    sm.cell(r,1,fk).font=BLK; sm.cell(r,2,long_).font=BLK
    for j,dd in enumerate(DIAS,3):
        c=sm.cell(r,j,"=SUMIF('%s'!$F$%d:$F$%d,%d,'%s'!$N$%d:$N$%d)"%(sn,a,b,dd,sn,a,b)); c.font=GRN; c.number_format='0.000;-0.000;"-"'; c.border=BD
    c=sm.cell(r,3+len(DIAS),'=SUM(C%d:%s%d)'%(r,CL(2+len(DIAS)),r)); c.number_format='0.000'; c.font=F(bold=True,size=9); c.border=BD
    r+=1
sm.cell(r,2,'GRAND TOTAL').font=F(bold=True,size=10)
for j in range(3,4+len(DIAS)):
    c=sm.cell(r,j,'=SUM(%s%d:%s%d)'%(CL(j),d0,CL(j),r-1)); c.number_format='#,##0.000'; c.font=F(bold=True,size=10); c.fill=TOT; c.border=BD
r+=2
sm.cell(r,2,'Cross-check: element total minus diameter total (should be 0)').font=BLK
sm.cell(r,3,'=ROUND(%s%d-%s%d,6)'%(CL(3+len(ELEMENTS)),GT,CL(3+len(DIAS)),r-2)).font=BLK
sm.freeze_panes='C5'

r+=3
sm.cell(r,1,'ALL FLOORS - TOTAL BY ELEMENT AND BAR SIZE (TONNES)').font=F(bold=True,size=11); r+=1
hdr(sm,r,['','Element']+['Y%d'%d for d in DIAS]+['TOTAL (t)']); r+=1
m0=r
for i,e in enumerate(ELEMENTS):
    sm.cell(r,2,e).font=BLK; sm.cell(r,2).border=BD
    for j in range(len(DIAS)):
        f='='+'+'.join("'%s'!%s%d"%(MATRIX[fk][0],CL(5+j),MATRIX[fk][1]+i) for fk,_,_ in FLOORS)
        c=sm.cell(r,3+j,f); c.font=GRN; c.number_format='#,##0.000;-#,##0.000;"-"'; c.border=BD
    c=sm.cell(r,3+len(DIAS),'=SUM(C%d:%s%d)'%(r,CL(2+len(DIAS)),r)); c.font=F(bold=True,size=9); c.number_format='#,##0.000'; c.border=BD
    r+=1
sm.cell(r,2,'GRAND TOTAL - ALL FLOORS')
for j in range(3,4+len(DIAS)):
    sm.cell(r,j,'=SUM(%s%d:%s%d)'%(CL(j),m0,CL(j),r-1)).number_format='#,##0.000'
for j in range(2,4+len(DIAS)):
    c=sm.cell(r,j); c.fill=TOT; c.font=F(bold=True,size=10); c.border=BD
r+=1
sm.cell(r,2,'Cross-check vs floor totals (should be 0)').font=BLK
sm.cell(r,3,'=ROUND(%s%d-%s%d,6)'%(CL(3+len(DIAS)),r-1,CL(3+len(ELEMENTS)),GT)).font=BLK

# ---------- Element x Size by Floor ----------
es=wb.create_sheet('Element x Size by Floor',2)
es['A1']='EACH ELEMENT BY FLOOR AND BAR SIZE (TONNES) - with totals for all floors'; es['A1'].font=F(bold=True,size=12)
es['A2']='Values link to the element/bar-size summary at the foot of each floor sheet (green).'; es['A2'].font=F(size=9,italic=True)
es.column_dimensions['A'].width=6; es.column_dimensions['B'].width=44
for j in range(3,4+len(DIAS)): es.column_dimensions[CL(j)].width=13
r=4
for i,e in enumerate(ELEMENTS):
    es.cell(r,1,e.upper()).font=F(bold=True,size=11); r+=1
    hdr(es,r,['Ref','Floor / level']+['Y%d'%d for d in DIAS]+['TOTAL (t)']); r+=1
    b0=r
    for fk,short,long_ in FLOORS:
        es.cell(r,1,fk).font=BLK; es.cell(r,2,long_).font=BLK
        for j in range(len(DIAS)):
            c=es.cell(r,3+j,"='%s'!%s%d"%(MATRIX[fk][0],CL(5+j),MATRIX[fk][1]+i)); c.font=GRN; c.number_format='0.000;-0.000;"-"'; c.border=BD
        c=es.cell(r,3+len(DIAS),'=SUM(C%d:%s%d)'%(r,CL(2+len(DIAS)),r)); c.font=F(bold=True,size=9); c.number_format='0.000;-0.000;"-"'; c.border=BD
        r+=1
    es.cell(r,2,'TOTAL %s - ALL FLOORS'%e.upper())
    for j in range(3,4+len(DIAS)):
        es.cell(r,j,'=SUM(%s%d:%s%d)'%(CL(j),b0,CL(j),r-1)).number_format='#,##0.000'
    for j in range(2,4+len(DIAS)):
        c=es.cell(r,j); c.fill=TOT; c.font=F(bold=True,size=10); c.border=BD
    r+=3

# ---------- Column check ----------
cc=wb.create_sheet('Column Check')
cc['A1']='COLUMNS - RECONCILIATION OF ELEVATION TAKE-OFF WITH DRAWING BBS'; cc['A1'].font=F(bold=True,size=12)
hdr(cc,3,['Drawing','Bar mark','Dia','BBS qty (drawing)','Take-off qty (elevations)','Difference','Remark'],[12,10,7,16,20,12,60])
BBSQ={8:{'1001':1818,'1002':3636,'1003':1818,'2001':512,'2002':96,'2501':96,'2502':96,'2503':96,'2504':96},
 9:{'1001':1083,'1002':2166,'1003':1083,'2001':512,'2002':16,'2003':32,'2004':16,'2005':16,'2501':48,'2502':32,'2503':48,'2504':32,'2505':16},
 11:{'1004':3036,'1005':15426,'2001':1026,'2006':162,'2501':108,'2502':108,'2503':108,'2504':108},
 12:{'1004':5834,'1005':17412,'2001':2304,'2006':270,'2007':18,'2501':288,'2502':18,'2503':18,'2504':18,'2505':270,'2506':540},
 13:{'1001':292,'1002':292,'1003':2044,'1004':1168,'2001':240,'2004':48,'2008':48,'2009':48,'2010':48,'2011':48}}
r=4
for p,mm in BBSQ.items():
    for mk,q in mm.items():
        t=COLCHECK.get((p,mk),0)
        rem={(8,'1001'):'Elevation link counts (COL-01D M-levels) differ slightly from BBS - elevations used',(8,'1002'):'As 1001',(8,'1003'):'As 1001',
             (8,'2001'):'BBS 512 appears copied from STR-007; elevations show 368 - elevations used (RFI)',
             (10,'1005'):'Cross-ties taken at BBS ratio of 5 per link set',(10,'2501'):'BBS counts 6 cols (02B) only; 02A (3 nos) also shown with these bars on elevation',
             (10,'2502'):'As 2501',(10,'2503'):'As 2501',(10,'2504'):'As 2501',(11,'1004'):'Minor - elevation counts used',(11,'1005'):'Cross-ties at BBS ratio 3 per set'}.get((p,mk),'')
        vals=[dwg(p),mk,CLEN[p][mk][0],q,t,'=E%d-D%d'%(r,r),rem]
        for j,v in enumerate(vals,1):
            c=cc.cell(r,j,v); c.border=BD; c.font=BLUE if j in (4,5) else BLK
        r+=1

# ---------- Schedule register ----------
sr=wb.create_sheet('BBS Register')
sr['A1']='REGISTER OF BAR BENDING SCHEDULES TRANSCRIBED FROM DRAWINGS (single-floor quantities)'; sr['A1'].font=F(bold=True,size=12)
hdr(sr,3,['Drawing','Element','Schedule','Measured on floors','Bar mark','Dia','Qty','Length (mm)','Weight per floor (kg)'],[11,18,52,40,9,6,8,11,16])
r=4
for p,el,desc,fls,s in SCHED_LOG:
    for mk,(dia,qty,ln) in s.items():
        vals=[dwg(p),el,desc,', '.join(fls),mk,dia,qty,ln,'=G%d*H%d/1000*F%d^2/162'%(r,r,r)]
        for j,v in enumerate(vals,1):
            c=sr.cell(r,j,v); c.font=BLUE if j in (5,6,7,8) else BLK
        sr.cell(r,9).number_format='#,##0.00'
        r+=1
out='/home/user/OnukpaTay/Kaneshie_Block_N_Reinforcement_Takeoff.xlsx'
wb.calculation.fullCalcOnLoad=True
wb.save(out); print('saved',out,sum(len(v) for v in rows.values()),'lines')
