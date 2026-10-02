import json,re,copy
from openpyxl import load_workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter as CL, column_index_from_string as CI

W=json.load(open('walls.json')); FIN=json.load(open('finishes.json')); RB=json.load(open('rebar_split.json'))
rb=lambda s,e,d: round(RB.get('%s|%s|%d'%(s,e,d),0),3)
CH=json.load(open('colheights.json'))

wb=load_workbook('boq.xlsx')
AR='Times New Roman'
TF=Font(name='Arial',size=9); TB=Font(name='Arial',size=9,bold=True); BLUE=Font(name='Arial',size=9,color='0000FF')
thin=Side(style='thin',color='999999'); BD=Border(left=thin,right=thin,top=thin,bottom=thin)
HDR=PatternFill('solid',fgColor='1F3864'); VER=PatternFill('solid',fgColor='E2EFDA'); NEWF=PatternFill('solid',fgColor='FFF2CC'); CHG=PatternFill('solid',fgColor='FCE4D6')

# ---------------- Verification take-off sheet ----------------
T=wb.create_sheet('Verification Take-off')
T['A1']='VERIFICATION TAKE-OFF - PROPOSED KANESHIE BLOCK N REDEVELOPMENT'; T['A1'].font=Font(name='Arial',size=12,bold=True)
T['A2']='Every verified quantity in the BOQ links to the Result column of this sheet. Calculations are shown as formulas (dimensions in metres unless noted). Blue = dimensions taken from drawings.'; T['A2'].font=Font(name='Arial',size=9,italic=True)
heads=['Ref','BOQ sheet / item','Description','Calculation (dimensions)','Result','Unit','Source / basis']
for j,h in enumerate(heads,1):
    c=T.cell(4,j,h); c.font=Font(name='Arial',size=9,bold=True,color='FFFFFF'); c.fill=HDR; c.border=BD; c.alignment=Alignment(wrap_text=True,vertical='center')
for j,w in enumerate([8,22,48,70,13,7,60],1): T.column_dimensions[CL(j)].width=w
T.freeze_panes='C5'
TR=[5]; REF={}; ROW={}
def sect(title):
    r=TR[0]; T.cell(r,1,title).font=Font(name='Arial',size=10,bold=True); TR[0]+=1
def line(key,boq,desc,formula,unit,src):
    r=TR[0]
    T.cell(r,1,key); T.cell(r,2,boq); T.cell(r,3,desc)
    shown=formula if isinstance(formula,str) else str(formula)
    T.cell(r,4,"'"+shown if shown.startswith('=') else shown)
    T.cell(r,5,formula if (isinstance(formula,str) and formula.startswith('=')) else formula)
    T.cell(r,6,unit); T.cell(r,7,src)
    for j in range(1,8):
        c=T.cell(r,j); c.font=TF; c.border=BD; c.alignment=Alignment(wrap_text=True,vertical='top')
    T.cell(r,5).number_format='#,##0.00'; T.cell(r,5).font=TB
    REF[key]="='Verification Take-off'!E%d"%r; ROW[key]=r
    TR[0]+=1; return r

# ---- constants
Ar='(41.0*36.0)'; Ae='(45.0*40.0)'
sect('A. SUBSTRUCTURE - EARTHWORKS (STR-001 raft GA & Section A-A; ARCH-101/102 site & block plan)')
line('S1','STR A','Site clearance: Block N plot + Parking-22 forecourt','=40.85*38.27+35.2*20.9','m2','ARCH-102 block plan: plot 3945+36900 wide x 38272 deep; Parking-22 5549+28051+1619 x (4900+5000+6000+5000)')
line('S2','STR B','Strip topsoil 150mm over excavation footprint (raft 41.0 x 36.0 + 2.0m working space each side)','=(41.0+2*2.0)*(36.0+2*2.0)','m2','STR-001 Section A-A: raft width 41,000; width of excavation 45,000 (2,000 allowance each side). Raft depth 36.0 m measured on STR-001 at 1:100')
line('S3','STR C','Excavate to reduce levels, max depth 4.00m','=(45.0*40.0)*4.0','m3','STR-001: bottom of excavation -4,000mm')
line('S4','STR D','Fill to make up levels over raft to underside of hardcore (raft top -1.000 to -0.000)','=41.0*36.0*1.0-(69.445*0.25*1.0)-(13.294*1.0)','m3','Raft top SSL -1.000 (STR-007/017), GF +0.300 less 150 bed & 150 hardcore; core walls (69.445m x 0.25) and columns (13.294 m2 plan) deducted')
line('S5','STR E','Crushed rock / geogrid layers between raft underside (-2.300) and formation (-4.000), full excavation width','=(45.0*40.0)*1.7','m3','STR-001 Section A-A layer build-up. NB section dims show 2,700 below raft; levels give 1,700 - RFI')
line('S6','STR F','Backfill around raft in working space (outside raft, above crushed-rock layer)','=((45.0*40.0)-(41.0*36.0))*(4.0-1.7)','m3','Working-space area x depth from NGL to top of crushed rock')
line('S7','STR G','Disposal of surplus excavated material','=(45.0*40.0)*4.0-((45.0*40.0)-(41.0*36.0))*(4.0-1.7)','m3','Excavation less re-used backfill (fills D/E/H are imported)')
line('S8','STR H','Hardcore 150mm under GF bed','=41.0*36.0*0.15','m3','GF bed footprint taken as raft footprint')
line('S9','STR J','Blinding under raft - 100mm min. (General Notes 1.0 item 3)','=41.0*36.0*0.10','m3','STR-000: "minimum 100mm thick blinding" - BOQ describes 50mm')
line('S10','STR K','150mm thick bed (GF slab on fill)','=41.0*36.0*0.15','m3','No GF slab detail on structural drawings - RFI')
sect('B. SUBSTRUCTURE - CONCRETE, REINFORCEMENT, FORMWORK, BLOCKWORK')
line('S11','STR A (p2)','Concrete walls from raft top (-1.000) to GF (+0.300): main core shear 22.05m + lift 21.825m + emergency core 25.57m, 250 thk','=(22.05+21.825+25.57)*0.25*1.3','m3','Wall lengths from raft GA STR-002 dims; walls 250 thk')
line('S12','STR B (p2)','Raft 1300 thick','=41.0*36.0*1.3','m3','Sump/lift-pit transitions (STR-003) not adjusted - same thickness folded')
line('S13','STR C (p2)','Columns raft to GF: 9 nr type-01 (750x500) + 25 nr type-02 (1200x300) + SWC-01A L-shape','=(9*0.75*0.5+25*1.2*0.3+(2.85*0.25+(1.075-0.25)*0.25))*1.3','m3','STR-007..012 sections; counts STR-002')
line('S14','STR D (p2)','Y20 in raft','=%s'%rb('SUB','Raft Foundation',20),'t','Reinforcement take-off (raft BBS STR-004..006)')
line('S15','STR E (p2)','Y25 in raft','=%s'%rb('SUB','Raft Foundation',25),'t','Reinforcement take-off (raft BBS)')
line('S16','STR F (p2)','Y10 links - columns & walls (substructure)','=%s+%s+%s'%(rb('SUB','Columns',10),rb('SUB','Lift Walls',10),rb('SUB','Shear Walls',10)),'t','Columns + lift walls + shear walls, Foundation-GF storey')
line('S17','STR G (p2)','Y12 - walls (substructure)','=%s+%s'%(rb('SUB','Lift Walls',12),rb('SUB','Shear Walls',12)),'t','Wall horizontal bars')
line('S18','STR H (p2)','Y25 - columns & walls (substructure starters)','=%s+%s+%s'%(rb('SUB','Columns',25),rb('SUB','Lift Walls',25),rb('SUB','Shear Walls',25)),'t','Column & wall vertical starters')
line('S19','STR NEW','Y20 - columns (substructure, SWC/type-02 starters)','=%s'%rb('SUB','Columns',20),'t','Not in BOQ')
line('S20','STR (p2) Walls fwk','Formwork to concrete walls (substructure), both faces','=2*(22.05+21.825+25.57)*1.3','m2','')
line('S21','STR J (p2)','Edges of GF bed 150mm high (perimeter)','=2*(41.0+36.0)','m','Edge <=250 high - measured linear (m), not m2')
line('S22','STR NEW','Formwork to edges of raft 1300 high','=2*(41.0+36.0)*1.3','m2','Not in BOQ')
line('S23','STR NEW','Formwork to columns raft to GF','=(9*2*(0.75+0.5)+25*2*(1.2+0.3)+2*(2.85+1.075))*1.3','m2','Not in BOQ')
line('S24','STR K (p2)','150mm blockwork to plinth (GF perimeter, -1.000 to +0.300)','=2*(41.0+36.0)*1.3','m2','Perimeter of raft x plinth height')
sect('C. SUPERSTRUCTURE - CONCRETE (C40)')
# openings
DOORS=[('D1',1.8,2.4,1),('D2',1.0,2.2,59),('D3',0.9,2.2,126),('D4',0.9,2.35,1),('D5',3.2,2.2,1),('D6',0.75,2.2,172),('D7',0.7,2.2,12),('D8',1.2,2.2,21),('ED1',1.0,2.2,36),('ED2',1.0,2.2,20),('D9',0.9,2.2,13),('MD1',1.8,2.2,3),('FD1',1.5,2.2,7),('M1',0.9,2.2,18),('M2',0.75,2.2,36),('M3',0.45,2.2,8),('M5',0.6,2.2,24),('GD1',1.8,2.2,2),('DW1',2.4,2.2,2),('DW2',5.05,2.2,1),('SD1',3.0,2.2,8),('SD2',1.6,2.2,28),('SD3',1.3,2.2,16),('SD4',1.8,2.2,30),('SD5',1.2,2.2,7),('RD1',4.2,2.157,2)]
WINS=[('W1',3.6,1.9,1),('W2',1.8,1.3,44),('W3',1.8,1.5,1),('W4',0.9,1.3,77),('W5',1.8,1.9,1),('W6',3.5,1.5,1),('W7',1.8,1.6,12),('W8',1.2,1.9,22),('W9',1.2,1.15,61),('W10',1.2,1.2,8),('W11',1.5,1.3,47),('W12',1.5,1.15,27),('W13',2.4,1.3,6),('W14',3.6,2.2,3),('W15',3.0,1.6,8),('W16',2.4,1.9,2),('W17',1.8,1.9,22),('W18',0.75,1.3,7),('W19',2.1,0.9,2),('W20',1.45,1.9,6),('HW1',0.9,0.6,104),('HW2',0.75,0.6,40),('HW3',0.6,0.6,12),('HW4',1.2,0.6,12)]
lint_terms='+'.join('%d*(%g+0.3)'%(q,w) for n,w,h,q in DOORS+WINS)
line('C1','STR A (sup)','Lintels 150x225 over all door & window openings (opening width + 150 bearing each end)','=(%s)*0.15*0.225'%lint_terms,'m3','Door schedule ARCH-501, window schedule ARCH-502')
cols=[('COL-01A','01'),('COL-01B','01'),('COL-01C','01'),('COL-01D','01'),('COL-02A','02'),('COL-02B','02'),('COL-02C','02'),('COL-02D','02'),('SWC-01A','SW')]
AREA={'01':'0.75*0.5','02':'1.2*0.3','SW':'(2.85*0.25+0.825*0.25)'}; PER={'01':'2*(0.75+0.5)','02':'2*(1.2+0.3)','SW':'2*(2.85+1.075)'}
cterms='+'.join('%d*%s*%g'%(CH[t][0],AREA[s],CH[t][2]) for t,s in cols)
line('C2','STR B (sup)','Columns GF to top: nos x section area x sum of clear storey heights (storey - 0.25 slab)','='+cterms,'m3','Clear heights per column type from elevations STR-007..012: '+'; '.join('%s %d nr %.2fm'%(t,CH[t][0],CH[t][2]) for t,_ in cols))
line('C3','STR C (sup)','Concrete walls GF-roof: main stair core 22.05m x 37.15m clear; lift walls 21.825m x 41.20m; emergency core 25.57m x 37.20m; 250 thk','=(22.05*37.15+21.825*41.2+25.57*37.2)*0.25','m3','Clear heights = sum(storey heights) - 0.25 per slab (STR-014/016/017 elevations)')
line('C4','STR D (sup)','Stairs: per storey 2 flights (waist 175, 1800 wide, 3.0m going) + 2 landings; scaled to storey height. Main 11 storeys (sum H 37.0m), emergency 12 storeys (sum H 37.3m)','=2.966*(37.0+37.3)/3.3+2.625*(11+12)','m3','STR-018..039 GA: waist 175, treads 300, risers 150-160; per 3.3m storey: flights 2.966 m3, landings 2.625 m3')
SL=[('M1',41,689.1),('1st',47,737.6),('M2',53,650.6),('2nd',59,737.5),('Mezz',65,554.9),('3rd',71,1273.9),('4th-8th (x5)',77,1134.6*5),('9th',84,1134.4),('10th',92,868.4),('Roof terrace',98,868.1)]
line('C5','STR E (sup)','Suspended slabs 250 thk (areas measured from GA sheets, voids/stair & lift openings excluded) + roof 150 thk (176.3 m2) + lift-core top 150 thk (16.3 m2)','=(689.1+737.6+650.6+737.5+554.9+1273.9+1134.6*5+1134.4+868.4+868.1)*0.25+(176.3+16.3)*0.15','m3','Slab areas measured on STR-040/046/052/058/064/070/076/083/091/097/104/107 (scale calibrated on gridlines 1-12 = 36,500)')
line('C6','STR F (sup)','Copings 300x150 to parapets: roof terrace perimeter 182.5 + roof 105.0 + lift core 17.3','=(182.5+105.0+17.3)*0.3*0.15','m3','Slab outer perimeters measured on GA sheets')
BM='(67.8+81.1+63.6+79.9+64.3+97.4+166.8*5+186.5+122.2+125.7)'
line('C7','STR NEW','Beams (downstands below 250 slab): 300x600 = %s m; 200x600 = (43.5+43.0+33.1+33.1*5+33.1+14.2+14.2) m; roof 250x600 31.4m & 200x450 34.0m below 150 slab'%BM,'=%s*0.3*0.35+(43.5+43.0+33.1+33.1*5+33.1+14.2+14.2)*0.2*0.35+31.4*0.25*0.45+34.0*0.2*0.3'%BM,'m3','Beam lengths measured from dashed beam outlines on GA sheets. NOT IN BOQ')
sect('D. SUPERSTRUCTURE - REINFORCEMENT (from Reinforcement Take-off workbook)')
line('R1','STR G (sup)','Y10 in columns','=%s'%rb('SUP','Columns',10),'t','')
line('R2','STR H (sup)','Y20 in columns','=%s'%rb('SUP','Columns',20),'t','')
line('R3','STR J (sup)','Y25 in columns','=%s'%rb('SUP','Columns',25),'t','')
line('R4','STR K (sup)','Y12 in stairs (BOQ says 10mm - stairs use Y12 & Y16)','=%s'%rb('SUP','Staircases',12),'t','Stair BBS STR-019..039')
line('R5','STR L (sup)','Y16 in stairs','=%s'%rb('SUP','Staircases',16),'t','')
line('R6','STR M (sup)','Y10 in shear & lift walls (links)','=%s+%s'%(rb('SUP','Shear Walls',10),rb('SUP','Lift Walls',10)),'t','')
line('R7','STR N (sup)','Y12 in shear, lift & ramp walls','=%s+%s+%s'%(rb('SUP','Shear Walls',12),rb('SUP','Lift Walls',12),rb('SUP','Retaining / Ramp Walls',12)),'t','')
line('R8','STR P (sup)','Y25 in shear & lift walls','=%s+%s'%(rb('SUP','Shear Walls',25),rb('SUP','Lift Walls',25)),'t','')
line('R9','STR Q (sup)','Y12 in suspended slabs (incl. lift core slab)','=%s+%s'%(rb('SUP','Floor Slabs',12),rb('SUP','Lift Core Roof Slab',12)),'t','')
line('R10','STR R (sup)','Y16 in suspended slabs','=%s'%rb('SUP','Floor Slabs',16),'t','')
line('R11','STR NEW','Y20 in shear & lift walls','=%s+%s'%(rb('SUP','Shear Walls',20),rb('SUP','Lift Walls',20)),'t','NOT IN BOQ')
for k,dd in (('R12',10),('R13',16),('R14',20),('R15',25)):
    line(k,'STR NEW','Y%d in beams'%dd,'=%s'%rb('SUP','Beams',dd),'t','NOT IN BOQ - beam BBS per floor')
sect('E. SUPERSTRUCTURE - FORMWORK')
line('F1','STR S (sup)','Lintels: sides 2x0.225 + soffit 0.15 per m; copings: sides 2x0.15 per m','=(%s)*(2*0.225+0.15)+(182.5+105.0+17.3)*2*0.15'%lint_terms,'m2','')
line('F2','STR T (sup)','Columns: nos x perimeter x clear height','='+'+'.join('%d*%s*%g'%(CH[t][0],PER[s],CH[t][2]) for t,s in cols),'m2','')
line('F3','STR U (sup)','Soffits of suspended slabs (same areas as concrete)','=(689.1+737.6+650.6+737.5+554.9+1273.9+1134.6*5+1134.4+868.4+868.1)+(176.3+16.3)','m2','')
line('F4','STR V (sup)','Concrete walls, both faces','=2*(22.05*37.15+21.825*41.2+25.57*37.2)','m2','BOQ formula =C98/0.25 refers to the columns line - error')
line('F5','STR NEW','Beams: sides of downstand + soffit','=%s*(2*0.35+0.3)+(43.5+43.0+33.1+33.1*5+33.1+14.2+14.2)*(2*0.35+0.2)+31.4*(2*0.45+0.25)+34.0*(2*0.3+0.2)'%BM,'m2','NOT IN BOQ')
line('F6','STR NEW','Edges of suspended slabs 250 high (outer + void edges)','=238.4+185.9+224.9+186.5+216.4+232.4+294.6*5+294.5+252.6+252.9+159.3+17.3','m','Perimeters measured on GA sheets. NOT IN BOQ')
line('F7','STR NEW','Stair soffits & risers (per storey 33.3 m2 x 23 storey-flights)','=(2*3.424*1.8+15.0+22*0.15*1.8)*23','m2','NOT IN BOQ')
# ---------------- ARCHITECTURAL ----------------
sect('F. ARCHITECTURAL - BLOCKWORK & WALL FINISHES (walls measured on ARCH-103..125 plans at 1:100; openings already excluded from lengths)')
HH={'GF':3.85,'1F':2.7,'2F':2.7,'MEZZ':2.7,'3F':3.3,'4F':3.3,'5F':3.3,'6F':3.3,'7F':3.3,'8F':3.3,'9F':3.3,'10F':3.3,'RT':3.15,'ROOF':1.2}
L150='+'.join('%.1f*%g'%(W[f]['w150'],HH[f]-(0.25 if f!='ROOF' else 0)) for f in W)
L200='+'.join('%.1f*%g'%(W[f]['w200'],HH[f]-(0.25 if f!='ROOF' else 0)) for f in W)
dadd='+'.join('%d*%g*(3.05-%g)'%(q,w,h) for n,w,h,q in DOORS)
wadd='+'.join('%d*%g*(3.05-%g)'%(q,w,h) for n,w,h,q in WINS)
r150=line('A0a','ARCH calc','150 walls: sum(length x clear height) per floor',"="+L150,'m2','Lengths per floor: '+'; '.join('%s %.0fm'%(f,W[f]['w150']) for f in W))
r200=line('A0b','ARCH calc','200 walls: sum(length x clear height) per floor',"="+L200,'m2','Lengths per floor: '+'; '.join('%s %.0fm'%(f,W[f]['w200']) for f in W))
rad=line('A0c','ARCH calc','Add back walling above/below openings (avg clear height 3.05m)','=%s+%s'%(dadd,wadd),'m2','Door & window schedules')
sh150=W and sum(W[f]['w150'] for f in W)/sum(W[f]['w150']+W[f]['w200'] for f in W)
import qty as _q
line('A1','ARCH A','150mm sandcrete blockwork (sum of floor-by-floor measurement incl. add-back over openings per floor)','='+'+'.join(t for s_ in _q.SHEETS for t in _q.Q[s_].get('blk150',[])),'m2','Per-floor lengths x clear heights + walling above/below openings allocated to each floor')
line('A1b','ARCH NEW','200mm sandcrete blockwork (floor-by-floor)','='+'+'.join(t for s_ in _q.SHEETS for t in _q.Q[s_].get('blk200',[])),'m2','Wall band 200-225 thick on plans. NOT IN BOQ')
LEXT={'GF':142.2,'1F':134.3,'2F':134.0,'MEZZ':191.5,'3F':148.0,'4F':224.2,'5F':224.2,'6F':224.2,'7F':224.2,'8F':224.2,'9F':224.1,'10F':181.8,'RT':182.5}
wet={f:FIN[f]['res'].get('40x40 non-slip porcelain (wet areas)',0) for f in FIN}
winA='+'.join('%d*%g*%g'%(q,w,h) for n,w,h,q in WINS); dorA='+'.join('%d*%g*%g'%(q,w,h) for n,w,h,q in DOORS)
rwin=line('A0d','ARCH calc','Total window area (schedule)','='+winA,'m2','')
rdor=line('A0e','ARCH calc','Total door area (schedule)','='+dorA,'m2','')
intf='+'.join('(2*(%.1f+%.1f)+2*%.1f-16.8-%.1f)*%g'%(W[f]['w150'],W[f]['w200'],W[f]['rc'],LEXT[f],HH[f]-0.25) for f in LEXT)
rint=line('A0f','ARCH calc','Internal wall faces: (2 x block length + 2 x RC core length - 16.8 lift-shaft faces - external wall length) x clear height, per floor','='+intf,'m2','External wall length = measured slab outer perimeter per floor')
wetw='+'.join('%.1f/3.8*8.0*%g'%(wet[f],HH[f]-0.25) for f in wet if wet[f]>0)
rwet=line('A0g','ARCH calc','Washroom wall faces: nr washrooms (wet area/3.8 m2 each) x 8.0m perimeter x clear height','='+wetw,'m2','Wet areas per floor from tiling layouts: '+'; '.join('%s %.0f'%(f,wet[f]) for f in wet if wet[f]>0))
line('A2','ARCH B','Render to interior walls (excl. washrooms)','=E%d-E%d-2*E%d-E%d'%(rint,rwet,rdor,rwin),'m2','Internal faces less washroom walls, doors (2 faces) and windows (1 face)')
line('A3','ARCH C','Render to washroom walls','=E%d-%s*0.75*2.2'%(rwet,round(sum(wet.values())/3.8,1)),'m2','Less washroom doors 750x2200')
rext=line('A4','ARCH NEW','External render (12.5mm cement-sand) to external walls','='+'+'.join('%.1f*%g'%(LEXT[f],HH[f]) for f in LEXT)+'-E%d'%rwin,'m2','NOT IN BOQ: external wall length x storey height less windows')
TILED='(%.1f)'%(sum(wet.values()))
sect('G. ARCHITECTURAL - FLOOR FINISHES (tile types per legend ARCH-401..409; rooms measured on plans and classified by room label / hatch)')
tot=lambda k: sum(FIN[f]['res'].get(k,0) for f in FIN)
WETA=tot('40x40 non-slip porcelain (wet areas)'); LOB=tot('60x120 semi-polished porcelain (lobbies)')-337.4
NSL=tot('60x60 non-slip porcelain R11 (corridors/terraces/service)')-412.1-176.8+47.0
SEMI=tot('60x60 semi-polished porcelain (habitable rooms)')+86.2
INT=337.4+412.1+tot('interlocking/PU (unlabelled grey)'); PU=tot('PU resin / coating (parking & ramps)')+176.8
STAIR='(2*1.8*3.0+22*0.15*1.8+2.2*3.75+1.8*3.75)*23'
line('T1','ARCH Q','40x40 non-slip porcelain - washrooms/WCs','=%.1f'%WETA,'m2','Per floor: '+'; '.join('%s %.1f'%(f,wet[f]) for f in wet if wet[f]>0))
line('T2','ARCH R','50x50 matte R11 porcelain - staircases (treads, risers, landings): 23 storey-flights (main 11, emergency 12) x 31.74 m2','='+STAIR,'m2','Legend: 50x50 R11 used on stair cores')
line('T3','ARCH S','60x60 semi-polished porcelain - habitable rooms, shops, offices','=%.1f'%SEMI,'m2','Incl. GF Shop 2 86.2 m2 added manually')
line('T4','ARCH T','60x120 semi-polished porcelain - FLOOR to stair/lift lobbies & reception','=%.1f'%LOB,'m2','Legend shows 60x120 as floor tile in lobbies (BOQ says wall)')
line('T5','ARCH U','60x60 non-slip R11 - corridors, terraces, verandah, service rooms','=%.1f'%NSL,'m2','RT outdoor sitting (412.1) and Mezz parking (176.8) re-allocated; GF verandah 47.0 added')
line('T6','ARCH V','Interlocking composite tiles - 9th floor play area & roof-top outdoor sitting','=%.1f'%INT,'m2','ARCH-601..606 details')
line('T7','ARCH NEW','Seamless PU resin screed / PU coating to parking decks & ramps','=%.1f'%PU,'m2','Legend items; NOT IN BOQ')
rtile=line('T8','ARCH calc','Total tiled floor area (excl. stairs, interlocking, PU)','=%.1f+%.1f+%.1f+%.1f'%(WETA,SEMI,LOB,NSL),'m2','')
line('A5','ARCH D','25mm cement-sand screed to tiled floors','=E%d'%rtile,'m2','BOQ 17,600 appears to be gross slab area')
line('A6','ARCH P','12mm bed to receive floor tiles (floors + stairs)','=E%d+%s'%(rtile,STAIR),'m2','')
rwt=line('A7','ARCH N','12mm backing to receive wall tiles - washroom walls to 2.4m high','=%s/3.8*8.0*2.4-%s/3.8*0.75*2.2'%(round(sum(wet.values()),1),round(sum(wet.values()),1)),'m2','Wall tile height assumed 2.4m (not dimensioned on drawings)')
line('A8','ARCH NEW','Wall tiles to washrooms (type to be confirmed)','=E%d'%rwt,'m2','NOT IN BOQ as wall item (BOQ T is a floor tile per legend)')
sect('H. ARCHITECTURAL - PAINTING & CEILINGS')
line('P1','ARCH E','Emulsion paint to interior walls (same as render B)','=E%d'%ROW['A2'],'m2','')
line('P2','ARCH F','Emulsion to washroom walls above 2.4m tiling','=E%d-E%d'%(ROW['A3'],ROW['A7']),'m2','')
line('P3','ARCH G','Emulsion/exterior paint to external walls','=E%d'%ROW['A4'],'m2','')
pk=[('COL-01A',['GROUND','FIRST','SECOND']),('COL-01B',['GROUND','FIRST','SECOND']),('COL-01C',['GROUND','FIRST','SECOND']),('COL-01D',['GROUND','M1','M2','MEZZ']),('COL-02A',['GROUND','FIRST','SECOND']),('COL-02B',['GROUND','FIRST','SECOND']),('COL-02C',['GROUND','FIRST','SECOND']),('COL-02D',['GROUND','M1','M2','MEZZ'])]
SZ={'COL-01':'2*(0.75+0.5)','COL-02':'2*(1.2+0.3)'}
pt=[]
for t,sts in pk:
    hs=sum(h-0.25 for s,h in CH[t][3] if s in sts)
    pt.append('%d*%s*%.2f'%(CH[t][0],SZ[t[:6]],hs))
line('P4','ARCH H','Paint to exposed faces of columns in GF & parking levels (girth exceeds 300mm)','='+'+'.join(pt),'m2','Columns GF to 3rd floor; all columns have girth > 300 mm so measured in m2')
line('P5','ARCH J','Plasterboard ceiling soffits - habitable rooms, corridors, lobbies (excl. parking)','=%.1f+%.1f+%.1f-22.2-20.0'%(SEMI,LOB,NSL),'m2','Excludes 1st/Mezz parking-level tiled lobbies (est. 42 m2)')
line('P6','ARCH K','Plasterboard ceiling soffits - washrooms','=%.1f'%WETA,'m2','')
tdoor='126*0.9*2.2*2+1*0.9*2.35*2+172*0.75*2.2*2+7*1.5*2.2*2'
frames='126*(2*2.2+0.9)+1*(2*2.35+0.9)+172*(2*2.2+0.75)+7*(2*2.2+1.5)'
line('P7','ARCH L','Gloss paint to timber doors (D3, D4, D6, FD1 both faces) and frames (girth 0.25m)','=%s+(%s)*0.25'%(tdoor,frames),'m2','Door schedule ARCH-501')
line('P8','ARCH M','Primer/paint to burglar-proof bars over window openings','=E%d'%ROW['A0d'],'m2','Measured as area of window openings (all windows) - confirm extent with client (BOQ item D says GF only)')
sect('I. DOORS, IRONMONGERY, WINDOWS (schedules ARCH-501/502)')
line('J1','ARCH G (doors)','50x150 frames to timber doors (D3,D4,D6,FD1): 2 jambs + head','='+frames,'m','')
line('J2','ARCH H (doors)','50x12 door stops (same as frames)','='+frames,'m','')
line('J3','ARCH A (ironm.)','Pairs 100mm brass butt hinges: 1.5 pairs per timber leaf (299 leaves), rounded up per floor','='+'+'.join(t for s_ in _q.SHEETS for t in _q.Q[s_].get('hinge',[])),'pr','Steel doors are supplied as assemblies with hinges')
line('J4','ARCH B (ironm.)','Ordinary mortice locks - timber panel doors D3 & D4','=126+1','nr','')
line('J5','ARCH C (ironm.)','Mortice indicator (bathroom) locks - washroom flush doors D6','=172','nr','')
sect('J. WATERPROOFING & LIFTS')
line('K1','ARCH A (wp)','Liquid waterproofing: roof-top outdoor sitting 412.1 + 9th-floor play area 337.4 + roof slab 176.3 + lift-core top 16.3','=412.1+337.4+176.3+16.3','m2','Floor terraces within units excluded (covered) - confirm')
line('K2','ARCH B (wp)','Protective screed over waterproofing','=412.1+337.4+176.3+16.3','m2','')
line('K3','ARCH C (wp)','Flashings/upstands at parapets: roof terrace 182.5 + roof 105.0 + lift core 17.3','=182.5+105.0+17.3','m','')
line('K4','ARCH D (wp)','Perimeter gutters/drainage channels (same perimeters)','=182.5+105.0+17.3','m','No roof drainage layout on drawings - RFI')
line('K5','ARCH E (lifts)','Passenger lifts (LIFT 1, LIFT 2 on plans)','=2','nr','')
line('K6','ARCH F (lifts)','Service/goods lift','=0','nr','Not shown on any plan - only 2 lift shafts in core. RFI')

# ---------------- restructure BOQ sheets ----------------
COLMAP={'A':'A','B':'B','C':'C','D':'E','E':'G','F':'H'}
def mapcol(c):
    if c in COLMAP: return COLMAP[c]
    i=CI(c); return CL(i+3) if i>6 else c
refre=re.compile(r"(?<![A-Za-z_!'])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![\d(])")
def remap(f,local=True):
    if not isinstance(f,str) or not f.startswith('='): return f
    out=[];i=0
    # handle sheet-qualified refs for target sheets
    def sub_q(m):
        sheet=m.group(1); rest=m.group(2)
        if sheet.strip("'") in ('structural works','architectural works'):
            return sheet+'!'+refre.sub(lambda mm: mm.group(1)+mapcol(mm.group(2))+mm.group(3)+mm.group(4),rest)
        return m.group(0)
    f=re.sub(r"('[^']+'|[A-Za-z]+)!(\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)",sub_q,f)
    if local:
        # local refs: protect sheet-qualified parts
        parts=re.split(r"('[^']+'![^,)+\-*/]+|[A-Za-z]+![^,)+\-*/]+)",f)
        f=''.join(p if '!' in p else refre.sub(lambda mm: mm.group(1)+mapcol(mm.group(2))+mm.group(3)+mm.group(4),p) for p in parts)
    return f
for sn in ('structural works','architectural works'):
    ws=wb[sn]
    # capture
    cells={}
    for row in ws.iter_rows(min_row=1,max_row=ws.max_row,max_col=6):
        for c in row:
            cells[(c.row,c.column)]=(c.value,copy.copy(c.font),copy.copy(c.alignment),copy.copy(c.border),copy.copy(c.fill),c.number_format)
    for (r,cidx),(v,fo,al,bo,fi,nf) in cells.items():
        ws.cell(r,cidx).value=None
    for (r,cidx),(v,fo,al,bo,fi,nf) in cells.items():
        nc=CI(mapcol(CL(cidx)))
        c=ws.cell(r,nc); c.value=remap(v); c.font=fo; c.alignment=al; c.border=bo; c.fill=fi; c.number_format=nf
        if cidx==4:  # unit -> also style verified unit col F
            c2=ws.cell(r,6); c2.font=copy.copy(fo); c2.alignment=copy.copy(al); c2.border=copy.copy(bo)
        if cidx==3:
            c2=ws.cell(r,4); c2.font=copy.copy(fo); c2.alignment=copy.copy(al); c2.border=copy.copy(bo); c2.number_format=nf
    for col,w in zip('ABCDEFGHI',[6,52,11,13,7,8,11,16,60]): ws.column_dimensions[col].width=w
    # headers
    for r in range(1,ws.max_row+1):
        if ws.cell(r,1).value=='Item' and ws.cell(r,2).value=='Description':
            for col,txt in ((4,'Verified Qty'),(6,'Verified Unit'),(9,'Verification remarks')):
                c=ws.cell(r,col,txt); c.font=copy.copy(ws.cell(r,3).font); c.font=Font(name=AR,size=12,bold=True); c.alignment=Alignment(wrap_text=True,horizontal='center'); c.fill=VER
for c in wb['general summary']['H']: pass
gs=wb['general summary']
for row in gs.iter_rows():
    for c in row:
        if isinstance(c.value,str) and c.value.startswith('='): c.value=remap(c.value,local=False)

# ---------------- assign verified quantities ----------------
def setv(sheet,row,key,unit=None,desc=None,remark='',new=None):
    ws=wb[sheet]
    if new:
        item,d,u=new
        ws.cell(row,1,item); ws.cell(row,2,d); ws.cell(row,5,'-'); ws.cell(row,3,None)
        for col in range(1,10): ws.cell(row,col).fill=NEWF
        ws.cell(row,2).font=Font(name=AR,size=12,color='C00000'); ws.cell(row,2).alignment=Alignment(wrap_text=True)
        ws.cell(row,8,'=G%d*D%d'%(row,row)); ws.cell(row,8).number_format='#,##0.00'
        unit=u
    c=ws.cell(row,4,REF[key] if key else None); c.fill=VER; c.number_format='#,##0.00'; c.font=Font(name=AR,size=12,bold=True)
    old_unit=ws.cell(row,5).value
    ws.cell(row,6,unit if unit else old_unit).fill=VER
    if unit and unit!=old_unit and not new: ws.cell(row,6).font=Font(name=AR,size=12,bold=True,color='C00000')
    if desc:
        b=ws.cell(row,2); b.value=(b.value or '')+'\n[PER DRAWINGS: '+desc+']'; b.alignment=Alignment(wrap_text=True,vertical='top'); b.font=Font(name=AR,size=12,color='C00000') if not new else b.font
    r=ws.cell(row,9,remark); r.font=Font(name='Arial',size=9); r.alignment=Alignment(wrap_text=True,vertical='top')
    # amount on verified qty
    if not new and ws.cell(row,8).value and isinstance(ws.cell(row,8).value,str) and ws.cell(row,8).value.startswith('='):
        ws.cell(row,8).value='=G%d*D%d'%(row,row)
S='structural works'; A='architectural works'
setv(S,8,'S1',remark='Plot + Parking-22 forecourt')
setv(S,10,'S2',remark='BOQ 1,477 m2 = raft only; excavation footprint 45 x 40 m')
setv(S,12,'S3')
setv(S,14,'S4',desc='fill over raft is c.1.0m thick (raft top -1.000 to underside of hardcore -0.000)',remark='BOQ uses 1.1 x oversite area')
setv(S,16,'S5',desc='crushed rock/geogrid layers are c.1,700 thick between raft underside (-2.300) and formation (-4.000)',remark='RFI: Section A-A dims show 2,700')
setv(S,19,'S6'); setv(S,22,'S7'); setv(S,28,'S8')
setv(S,34,'S9',desc='blinding minimum 100mm thick (General Notes item 1.0/3)')
setv(S,37,'S10',remark='No GF slab detail issued - RFI')
setv(S,48,'S11'); setv(S,50,'S12'); setv(S,52,'S13',remark='BOQ 7 m3 too low: 35 columns x 1.3m')
setv(S,56,'S14'); setv(S,58,'S15'); setv(S,60,'S16',desc='Y10 links to columns & walls (raft to GF)'); setv(S,62,'S17',desc='Y12 to walls (raft to GF)'); setv(S,64,'S18',desc='Y25 to columns & walls (raft to GF)')
setv(S,67,'S20',remark='Both faces, 1.3m high')
setv(S,69,'S21',unit='m',desc='edge 150mm high - measured in linear metres',remark='Unit corrected m2 -> m (edge not exceeding 250mm)')
setv(S,74,'S24')
setv(S,71,'S19',new=('N1','Y20 in columns (raft to GF)','t'))
setv(S,72,'S22',new=('N2','Formwork to edges of raft 1300mm high','m2'))
setv(S,76,'S23',new=('N3','Formwork to sides of columns (raft to GF)','m2'))
setv(S,96,'C1',desc='lintels 150x225 over all door/window openings',remark='BOQ 5 x 72 = 360 m3 is excessive')
setv(S,98,'C2',remark='BOQ multiplies by 5 in error; measured all floors')
setv(S,100,'C3',remark='Shear, lift & emergency core walls all floors')
setv(S,102,'C4'); setv(S,104,'C5'); setv(S,106,'C6')
setv(S,110,'R1',remark='BOQ x5 multiplier is an error - figure already covers all floors')
setv(S,112,'R2',remark='BOQ x5 multiplier is an error'); setv(S,114,'R3',remark='BOQ x5 multiplier is an error')
setv(S,116,'R4',desc='stairs use 12mm (Y12) and 16mm bars - no 10mm in stair BBS')
setv(S,118,'R5')
setv(S,120,'R6',desc='10mm links in shear & lift walls'); setv(S,122,'R7',desc='12mm horizontal bars in shear, lift & ramp walls'); setv(S,124,'R8',desc='25mm vertical bars in shear & lift walls')
setv(S,126,'R9'); setv(S,128,'R10')
setv(S,134,'F1'); setv(S,136,'F2',remark='BOQ x5 multiplier is an error'); setv(S,138,'F3')
setv(S,140,'F4',remark='BOQ formula =C98/0.25 refers to column concrete - error')
newS=[(142,'C7','N4','Vibrated in-situ concrete C40 in beams (downstands)','m3'),(143,'R11','N5','20mm diameter in shear & lift walls','t'),
      (144,'R12','N6','10mm diameter in beams (links)','t'),(145,'R13','N7','16mm diameter in beams','t'),(146,'R14','N8','20mm diameter in beams','t'),(147,'R15','N9','25mm diameter in beams','t'),
      (148,'F5','N10','Formwork to sides and soffits of beams','m2'),(149,'F6','N11','Formwork to edges of suspended slabs 250mm high','m'),(150,'F7','N12','Formwork to soffits of stair flights, landings and risers','m2')]
for r,k,it,d,u in newS: setv(S,r,k,new=(it,d,u),remark='ADDED - omitted from BOQ')
setv(A,12,'A1'); setv(A,13,'A1b',new=('A1','200mm thick wall','m2'),remark='ADDED - 200/225 walls on plans')
setv(A,19,'A2'); setv(A,21,'A3'); setv(A,27,'A4',new=('D1','12.5mm cement & sand (1:3) rendering to external walls','m2'),remark='ADDED - no external render item in BOQ')
setv(A,25,'A5',remark='BOQ 17,600 m2 appears to be gross slab area; screed measured to tiled floors')
setv(A,32,'P1'); setv(A,34,'P2'); setv(A,36,'P3')
setv(A,38,'P4',desc='columns are girth exceeding 300mm - measured in m2 (exposed faces GF & parking levels)')
setv(A,40,'P5'); setv(A,42,'P6'); setv(A,51,'P7')
setv(A,55,'P8',desc='measured over area of window openings')
setv(A,60,'A7',remark='Wall tiling height assumed 2.4m')
setv(A,62,'A6',remark='BOQ =9*89 (801) far too low')
setv(A,68,'T1',desc='400x400 non-slip porcelain to washrooms & WCs (legend ARCH-401..409)')
setv(A,70,'T2',desc='50x50 matte R11 porcelain to staircases (treads, risers & landings)')
setv(A,72,'T3',desc='600x600 semi-polished porcelain to habitable rooms, shops & offices (BOQ "60x60mm" should read 600x600mm)')
setv(A,74,'T4',desc='600x1200 semi-polished porcelain FLOOR tiles to stair/lift lobbies & reception - legend shows floor, not wall')
setv(A,76,'T5',desc='600x600 non-slip R11 porcelain to corridors, terraces, verandah & service rooms')
setv(A,78,'T6',desc='interlocking composite tiles to roof-top outdoor sitting & 9th floor play area (ARCH-601..606)')
setv(A,80,'T7',new=('W','Seamless polyurethane (PU) resin screed / PU coating to parking decks & ramps','m2'),remark='ADDED - shown on tiling legend')
setv(A,81,'A8',new=('X','Ceramic/porcelain wall tiles to washrooms, adhesive & grout (type TBC)','m2'),remark='ADDED - wall tiling to washrooms')
# doors (schedule)
DQ={87:('=1','2-hour fire-rated double-leaf galvanised steel door (D1) - not glazed entrance door'),89:('=59','D2: 1-hour fire-rated galvanised steel single-leaf security door - not D3'),
    91:('=126',None),93:('=1','D4 is a single leaf timber PANEL door with fanlight'),95:('=1','D5: 4-panel galvanised steel framed tempered glass sliding door (not flush)'),
    97:('=172','D6: single leaf timber flush door'),103:('=12','D7: single-leaf 2-hour fire-rated galvanised steel door'),105:('=21','D8: 1-hour fire-rated leaf-and-a-half galvanised steel security door'),
    107:('=36','ED1: 1-hour fire-rated galvanised steel SINGLE-leaf security door (emergency stairs)'),109:('=20',None),111:('=13',None),113:('=3','MD1: double-leaf 2-hour fire-rated galvanised steel refuse room door'),
    115:('=7',None),117:('=18',None),119:('=36',None),121:('=8',None),123:('=24',None),125:('=2',None),127:('=2',None),
    129:('=1','DW2: 1 nr only, with fanlight and fixed side windows'),131:('=8',None),133:('=28',None),135:('=16',None),137:('=30',None),139:('=7',None),142:('=4200*0+2',None)}
ws=wb[A]
for r,(q,dsc) in DQ.items():
    if r==142: q='=2'
    line_key='DOOR%d'%r
    rr=line(line_key,'ARCH doors row %d'%r,'Door per schedule ARCH-501: %s'%(ws.cell(r,2).value or '')[:80],q,'nr','Schedule quantity (doors are not tagged on plans)')
    setv(A,r,line_key,desc=dsc)
setv(A,99,'J1',remark='BOQ =9*51 (459 m) - frames to timber doors measured from schedule')
setv(A,101,'J2'); setv(A,151,'J3',unit='pr',remark='Unit changed nr -> pairs'); setv(A,153,'J4',remark='Steel security/fire doors carry own lock sets'); setv(A,155,'J5')
WQ={184:1,186:44,188:1,190:77,192:1,194:1,196:12,198:22,200:61,202:8,204:47,206:27,208:6,210:3,212:8,214:2,216:22,218:7,220:2,222:6,224:104,226:40,228:12,230:12}
WD={210:'W14 is a 3-bay SLIDING window 3600x2200',212:'W15 is a 3-bay SLIDING window 3000x1600',214:'W16: 3x2 awning window 2400 x 1900 (not 240)'}
for r,q in WQ.items():
    k='WIN%d'%r; line(k,'ARCH windows row %d'%r,'Window per schedule ARCH-502: %s'%(ws.cell(r,2).value or '')[:70],'=%d'%q,'nr','Schedule quantity')
    setv(A,r,k,desc=WD.get(r))
setv(A,235,'K1',remark='BOQ 2,200 m2 not supported by drawings'); setv(A,237,'K2'); setv(A,239,'K3'); setv(A,241,'K4')
setv(A,244,'K5'); setv(A,246,'K6',remark='RFI - not shown on drawings')
for r in (163,251,256,261,267):
    ws.cell(r,6,'item').fill=VER; ws.cell(r,9,'Provisional sum - measured as item (no quantity)').font=Font(name='Arial',size=9)
# reorder sheets
wb.move_sheet('Verification Take-off',offset=-(len(wb.sheetnames)-1-4))
# notes sheet
N=wb.create_sheet('Verification Notes',0)
notes=[('BOQ VERIFICATION - PROPOSED KANESHIE BLOCK N REDEVELOPMENT',True),
('Drawings used: Structural SHC-KANESHIE-STR-000 to 107 (108 sheets); Architectural SHC-NORTH K-ARCH-101 to 606 (59 sheets).',False),
('',False),('HOW TO READ THE BOQ SHEETS',True),
('Column C = original BOQ quantity (unchanged). Column D "Verified Qty" (green) = quantity measured from the drawings; it links to the Verification Take-off sheet where every calculation is shown.',False),
('Column F "Verified Unit": red where the unit has been corrected (e.g. edges of bed m2 -> m; hinges nr -> pairs; provisional sums -> item).',False),
('Description text in red "[PER DRAWINGS: ...]" = the drawings describe the item differently; the original description is kept above it.',False),
('Rows shaded yellow (item codes N1..N12, A1, D1, W, X) are ADDED items omitted from the BOQ. They sit inside the existing page totals.',False),
('Column H "Amount" now = Rate x Verified Qty. Column I gives remarks.',False),
('',False),('KEY FINDINGS',True),
('1. Superstructure columns: BOQ multiplies concrete, formwork and reinforcement by 5. The base figures already represent all floors - the x5 overstates them five-fold.',False),
('2. Concrete walls (306 m3) understate the shear/lift/emergency core walls (c.667 m3 measured). The formwork formula refers to the column line.',False),
('3. Beams (c.211 m3 concrete, c.111 t steel, c.2,100 m2 formwork), Y20 wall bars (82 t), raft edge formwork, slab edges and stair formwork are not in the BOQ - added.',False),
('4. Lintels 360 m3 is excessive - lintels over all scheduled openings measure c.56 m3. Suspended slabs measure c.3,326 m3 (BOQ 2,790); slab reinforcement Y12 586 t (BOQ 315 t) per the bar bending schedules.',False),
('5. Doors and windows: quantities agree with the schedules except DW2 (1 nr, BOQ 2). Several door descriptions are mismatched with the schedule (fire ratings / leaf types) - corrected in red.',False),
('6. Floor tiles: the tile sizes in the BOQ read "60x60mm" etc. - drawings are 600x600mm. 60x120 tile is a FLOOR tile to lobbies (legend), not wall. PU resin to parking decks and wall tiles to washrooms are not billed - added.',False),
('',False),('MEASUREMENT METHOD',True),
('Slab areas, slab perimeters and beam lengths were measured directly from the structural GA sheets (vector/raster geometry calibrated on grid 1-12 = 36,500 mm and A1-Q = 34,350 mm).',False),
('Block wall lengths were measured from the architectural floor plans at 1:100 (wall outlines converted to centre-lines; door/window gaps excluded). Wall thickness classes: <=210mm band = 150 walls, 210-245 = 200 walls, >245 = RC core walls (excluded from blockwork).',False),
('Floor finishes: rooms segmented from the plans and classified by room label (washroom, corridor, bedroom...) using the tiling-layout legend; manual corrections are listed on the take-off sheet.',False),
('Reinforcement quantities come from the separate Reinforcement Take-off workbook (bar bending schedules, 1,306 t total).',False),
('Measured quantities are net (no waste). Measurement by digital scaling is accurate to about +/-3-5% on walls and finishes; check critical items before tender.',False),
('',False),('QUERIES FOR THE DESIGN TEAM (RFI)',True),
('a) Raft section A-A shows 2,700 of fill below the raft but levels (-1.000 raft top, -4.000 formation) give 1,700.',False),
('b) No GF slab / bed detail on structural drawings (BOQ items J, K).',False),
('c) Architectural M1/M2/M3 levels are 300 mm above structural SSLs (+2800/+5500/+8200 vs +2500/+5200/+7900).',False),
('d) Service/goods lift: only two lift shafts are shown.',False),
('e) Wall-tile height in washrooms, roof drainage layout and burglar-proofing extent are not dimensioned.',False)]
for i,(t,b) in enumerate(notes,1):
    c=N.cell(i,1,t); c.font=Font(name='Arial',size=12 if i==1 else 10,bold=b); c.alignment=Alignment(wrap_text=True,vertical='top')
N.column_dimensions['A'].width=150
wb.calculation.fullCalcOnLoad=True
out='/home/user/OnukpaTay/KANESHIE_BLOCK_N_BOQ_rev1_VERIFIED.xlsx'
wb.save(out); print('saved',out,TR[0])
