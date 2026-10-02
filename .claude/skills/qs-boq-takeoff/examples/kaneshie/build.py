import json, math
from data import FLOORS, STOREY, dwg, sched
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL

ELEMENTS=['Raft Foundation','Columns','Shear Walls','Lift Walls','Retaining / Ramp Walls','Beams','Floor Slabs','Staircases','Lift Core Roof Slab']
DIAS=[10,12,16,20,25]
rows={f[0]:[] for f in FLOORS}   # floor -> list of dict
def add(fl,el,ref,desc,mark,dia,members,bars,length,note=''):
    rows[fl].append(dict(el=el,ref=ref,desc=desc,mark=mark,dia=dia,mem=members,bars=bars,len=length,note=note))

# ---------------- schedules (raft, slabs, beams, stairs, lift core) ----------------
SP=[(5,['F00'],'Raft Foundation','Raft - bottom reinforcement'),
    (6,['F00'],'Raft Foundation','Raft - additional bottom reinforcement'),
    (7,['F00'],'Raft Foundation','Raft - top reinforcement'),
    (43,['F02'],'Beams','M1 Level beams'),
    (44,['F02'],'Floor Slabs','M1 slab - bottom reinforcement'),(45,['F02'],'Floor Slabs','M1 slab - top reinforcement'),(46,['F02'],'Floor Slabs','M1 slab - additional top reinforcement'),
    (49,['F03'],'Beams','First floor beams'),
    (50,['F03'],'Floor Slabs','First floor slab - bottom'),(51,['F03'],'Floor Slabs','First floor slab - top'),(52,['F03'],'Floor Slabs','First floor slab - additional top'),
    (55,['F04'],'Beams','M2 Level beams'),
    (56,['F04'],'Floor Slabs','M2 slab - bottom'),(57,['F04'],'Floor Slabs','M2 slab - top'),(58,['F04'],'Floor Slabs','M2 slab - additional top'),
    (61,['F05'],'Beams','Second floor beams'),
    (62,['F05'],'Floor Slabs','Second floor slab - bottom'),(63,['F05'],'Floor Slabs','Second floor slab - top'),(64,['F05'],'Floor Slabs','Second floor slab - additional top'),
    (67,['F06'],'Beams','Mezzanine floor beams'),
    (68,['F06'],'Floor Slabs','Mezzanine slab - bottom'),(69,['F06'],'Floor Slabs','Mezzanine slab - top'),(70,['F06'],'Floor Slabs','Mezzanine slab - additional top'),
    (73,['F07'],'Beams','Third floor beams'),
    (74,['F07'],'Floor Slabs','Third floor slab - bottom'),(75,['F07'],'Floor Slabs','Third floor slab - top'),(76,['F07'],'Floor Slabs','Third floor slab - additional top'),
    (79,['F08','F09','F10','F11','F12'],'Beams','Typical 4th-8th floor beams (sheet 1 of 2)'),
    (80,['F08','F09','F10','F11','F12'],'Beams','Typical 4th-8th floor beams (sheet 2 of 2)'),
    (81,['F08','F09','F10','F11','F12'],'Floor Slabs','Typical 4th-8th slab - bottom'),
    (82,['F08','F09','F10','F11','F12'],'Floor Slabs','Typical 4th-8th slab - top'),
    (83,['F08','F09','F10','F11','F12'],'Floor Slabs','Typical 4th-8th slab - additional top'),
    (86,['F13'],'Beams','Ninth floor beams (1 of 2)'),(88,['F13'],'Beams','Ninth floor beams (2 of 2)'),
    (89,['F13'],'Floor Slabs','Ninth floor slab - bottom'),(90,['F13'],'Floor Slabs','Ninth floor slab - top'),(91,['F13'],'Floor Slabs','Ninth floor slab - additional top'),
    (93,['F14'],'Beams','Tenth floor beams (1 of 2)'),(94,['F14'],'Beams','Tenth floor beams (2 of 2)'),
    (95,['F14'],'Floor Slabs','Tenth floor slab - bottom'),(96,['F14'],'Floor Slabs','Tenth floor slab - top'),(97,['F14'],'Floor Slabs','Tenth floor slab - additional top'),
    (100,['F15'],'Beams','Roof top terrace beams (1 of 2)'),(101,['F15'],'Beams','Roof top terrace beams (2 of 2)'),
    (102,['F15'],'Floor Slabs','Roof top terrace slab - bottom'),(103,['F15'],'Floor Slabs','Roof top terrace slab - top'),(104,['F15'],'Floor Slabs','Roof top terrace slab - additional top'),
    (106,['F16'],'Beams','Roof level beams'),
    (107,['F16'],'Floor Slabs','Roof level slab'),
    (108,['F17'],'Lift Core Roof Slab','Top of lift core slab'),
    (20,['F01'],'Staircases','Main staircase GF to 1st floor'),
    (22,['F03'],'Staircases','Main staircase 1st to 2nd floor'),
    (24,['F05'],'Staircases','Main staircase 2nd to 3rd floor'),
    (26,['F07'],'Staircases','Main staircase 3rd to 4th floor'),
    (28,['F08','F09','F10','F11','F12','F13'],'Staircases','Main staircase typical flight (4th to 10th, one storey)'),
    (30,['F14'],'Staircases','Main staircase 10th floor to roof top terrace'),
    (32,['F01'],'Staircases','Emergency staircase GF to M1'),
    (34,['F02','F04','F06'],'Staircases','Emergency staircase typical flight (M1 to 3rd, one storey)'),
    (36,['F07'],'Staircases','Emergency staircase 3rd to 4th floor'),
    (38,['F08','F09','F10','F11','F12','F13'],'Staircases','Emergency staircase typical flight (4th to 10th, one storey)'),
    (40,['F14'],'Staircases','Emergency staircase 10th floor to roof top terrace'),
]
SCHED_LOG=[]
for p,fls,el,desc in SP:
    s=sched(p)
    SCHED_LOG.append((p,el,desc,fls,s))
    for fl in fls:
        for mk,(dia,qty,ln) in s.items():
            add(fl,el,dwg(p),desc,mk,dia,1,qty,'=%d/1000'%ln,'BBS')

# ---------------- columns ----------------
cols=json.load(open('cols_final.json'))
CLEN={8:{'1001':(10,2330),'1002':(10,1330),'1003':(10,1830),'2001':(20,4500),'2002':(20,3670),'2501':(25,2850),'2502':(25,5050),'2503':(25,3900),'2504':(25,5250)},
 9:{'1001':(10,2330),'1002':(10,1330),'1003':(10,1830),'2001':(20,4500),'2002':(20,3670),'2003':(20,3520),'2004':(20,3900),'2005':(20,4200),'2501':(25,2850),'2502':(25,5050),'2503':(25,3900),'2504':(25,5250),'2505':(25,3700)},
 11:{'1004':(10,2910),'1005':(10,1008),'2001':(20,4500),'2006':(20,3470),'2501':(25,2850),'2502':(25,5050),'2503':(25,3900),'2504':(25,5250)},
 12:{'1004':(10,2910),'1005':(10,1008),'2001':(20,4500),'2006':(20,3470),'2007':(20,3320),'2501':(25,2850),'2502':(25,5050),'2503':(25,3900),'2504':(25,5250),'2505':(25,3700),'2506':(25,3900)},
 13:{'1001':(10,5930),'1002':(10,2480),'1003':(10,910),'1004':(10,770),'2001':(20,4500),'2004':(20,3900),'2008':(20,2850),'2009':(20,5050),'2010':(20,5250),'2011':(25,3370)}}
TIES={'COL-02A':5,'COL-02B':5,'COL-02C':3,'COL-02D':3}   # Y1005 cross-ties per Y1004 link set (ratio from BBS)
COLCHECK={}
SNAME={'FOUNDATION':'Foundation to GF','GROUND':'GF to next level','M1':'M1 to 1st/M2','FIRST':'1st to 2nd','M2':'M2 to Mezz','SECOND':'2nd to 3rd','MEZZ':'Mezz to 3rd','THIRD':'3rd to 4th','FOURTH':'4th to 5th','FIFTH':'5th to 6th','SIXTH':'6th to 7th','SEVENTH':'7th to 8th','EIGHT':'8th to 9th','NINTH':'9th to 10th','TENTH':'10th to roof top terrace','ROOF TOP':'Roof top terrace to roof level'}
for ct,v in cols.items():
    p=v['page']; nos=v['nos']
    for st,marks in v['st'].items():
        fl=STOREY[st]
        m=dict(marks)
        if ct=='SWC-01A':
            sets=m['1001']; m['1002']=sets; m['1003']=('=7*%d'%sets,7*sets); m['1004']=('=4*%d'%sets,4*sets)
            if st=='EIGHT' and '2004' in m: m['2011']=m.pop('2004')
        if ct in TIES:
            sets=m['1004']; m['1005']=('=%d*%d'%(TIES[ct],sets),TIES[ct]*sets)
        for mk in sorted(m):
            val=m[mk]
            bars,num=(val if isinstance(val,tuple) else (val,val))
            dia,ln=CLEN[p][mk]
            kind='links' if dia==10 else 'main bars'
            add(fl,'Columns',dwg(p),'%s (%d nos) %s - %s'%(ct,nos,SNAME.get(st,st),kind),mk,dia,nos,bars,'=%d/1000'%ln,'Elevation + BBS length')
            COLCHECK[(p,mk)]=COLCHECK.get((p,mk),0)+num*nos

# ---------------- walls ----------------
LAP=40; COVER=30
MAIN_SHEAR=[('CW-01',3600,29),('CW-05',7250,None),('CW-07 (stair section)',7250,None),('CW-09',1150,None),('CW-10',1150,None),('CW-11',1650,None)]
MAIN_LIFT=[('CW-02',3600,29),('CW-03',3600,29),('CW-04',3600,29),('CW-06',2025,None),('CW-08',4500,None),('CW-07 (lift section)',4500,None)]
EMERG=[('CW-12',7050,None),('CW-13',7810,52),('CW-14',3450,None),('CW-15',2425,None),('CW-16',775,None),('CW-17',360,None),('CW-18',1300,None),('CW-19',1100,None),('CW-20',1300,None)]
# key, floor, storey height, horizontal bars per face (from elevations), vert dia shear, vert dia lift
MAIN_ST=[('Foundation to GF','F00',1300,9,25,25,True),('GF to 1st','F01',3850,34,25,25,False),('1st to 2nd','F03',2700,16,25,25,False),
 ('2nd to 3rd','F05',4050,25,25,25,False),('3rd to 4th','F07',3300,20,25,25,False),('4th to 5th','F08',3300,20,20,25,False),
 ('5th to 6th','F09',3300,20,20,20,False),('6th to 7th','F10',3300,20,20,20,False),('7th to 8th','F11',3300,20,20,20,False),
 ('8th to 9th','F12',3300,20,20,20,False),('9th to 10th','F13',3300,22,20,20,False),('10th to roof top terrace','F14',3300,20,20,20,False),
 ('Roof top terrace to roof level','F15',3150,19,20,20,False),('Roof level to top of lift core','F16',4200,9,None,20,False)]
EM_ST=[('Foundation to GF','F00',1000,9,25,True),('GF to M1','F01',2500,15,25,False),('M1 to M2','F02',2700,16,25,False),('M2 to Mezz','F04',2700,16,25,False),
 ('Mezz to 3rd','F06',3000,18,25,False),('3rd to 4th','F07',3300,20,25,False),('4th to 5th','F08',3300,20,20,False),('5th to 6th','F09',3300,20,20,False),
 ('6th to 7th','F10',3300,20,20,False),('7th to 8th','F11',3300,20,20,False),('8th to 9th','F12',3300,20,20,False),('9th to 10th','F13',3300,22,20,False),
 ('10th to roof top terrace','F14',3300,20,20,False),('Roof top terrace to roof level','F15',3150,19,20,False)]
LINK_LEN=1800
def wall_rows(el,core,walls,label,H,nh,dv,fl,starter,links_pos,ref):
    for name,L,nv in walls:
        hl='=(%d-2*%d+%d*12)/1000'%(L,COVER,LAP)
        add(fl,el,ref,'%s %s (L=%dmm) %s - horizontal Y12@150 NF/FF'%(core,name,L,label),'H-Y12',12,1,'=2*%d'%nh,hl,'Elevation count / plan length')
        nvs=('=2*%d'%nv) if nv else ('=2*(ROUNDUP(%d/150,0)+1)'%L)
        vl=('=(1250+350+%d+%d*%d)/1000'%(H,LAP,dv)) if starter else ('=(%d+%d*%d)/1000'%(H,LAP,dv))
        add(fl,el,ref,'%s %s %s - vertical Y%d@150 NF/FF%s'%(core,name,label,dv,' (starters from raft)' if starter else ''),'V-Y%d'%dv,dv,1,nvs,vl,'Elevation / plan')
    add(fl,el,ref,'%s confinement links Y10@150 (%d positions on plan) %s'%(core,links_pos,label),'LNK-Y10',10,1,'=%d*ROUNDUP(%d/150,0)'%(links_pos,H),'=%d/1000'%LINK_LEN,'Assumed link cut length')
for label,fl,H,nh,dvs,dvl,st in MAIN_ST:
    if dvs: wall_rows('Shear Walls','Main core',MAIN_SHEAR,label,H,nh,dvs,fl,st,26,'STR-015/016')
    wall_rows('Lift Walls','Main core (lift shafts)',MAIN_LIFT,label,H,nh,dvl,fl,st,26,'STR-015/017')
for label,fl,H,nh,dv,st in EM_ST:
    wall_rows('Shear Walls','Emergency stair core',EMERG,label,H,nh,dv,fl,st,33,'STR-013/014')
# ramp wall RAMP-01 (provisional - no reinforcement detail issued)
add('F01','Retaining / Ramp Walls','STR-002','RAMP-01 wall 250 thk x 7400 long x 3500 high (raft top -1000 to M1 +2500) - horizontal Y12@150 NF/FF (PROVISIONAL)','H-Y12',12,1,'=2*ROUNDUP(3500/150,0)','=(7400-2*30+40*12)/1000','Provisional')
add('F01','Retaining / Ramp Walls','STR-002','RAMP-01 wall - vertical Y12@150 NF/FF (PROVISIONAL)','V-Y12',12,1,'=2*(ROUNDUP(7400/150,0)+1)','=(1250+350+3500+40*12)/1000','Provisional')
json.dump({str(k):v for k,v in COLCHECK.items()},open('colcheck.json','w'))
