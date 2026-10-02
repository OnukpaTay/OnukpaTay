import json,collections,math
W=json.load(open('walls.json')); FIN=json.load(open('finishes.json')); RBF=json.load(open('rebar_floor.json')); CH=json.load(open('colheights.json'))
SHEETS=['SUB','GF','1ST','2ND','3RD','4TH','5TH','6TH','7TH','8TH','9TH','10TH','11TH','12TH']
FSH={'F00':'SUB','F01':'GF','F02':'GF','F03':'1ST','F04':'1ST','F05':'2ND','F06':'2ND','F07':'3RD','F08':'4TH','F09':'5TH','F10':'6TH','F11':'7TH','F12':'8TH','F13':'9TH','F14':'10TH','F15':'11TH','F16':'12TH','F17':'12TH'}
ASH={'GF':'GF','1F':'1ST','2F':'2ND','MEZZ':'2ND','3F':'3RD','4F':'4TH','5F':'5TH','6F':'6TH','7F':'7TH','8F':'8TH','9F':'9TH','10F':'10TH','RT':'11TH','ROOF':'12TH'}
STF={'FOUNDATION':'F00','GROUND':'F01','M1':'F02','FIRST':'F03','M2':'F04','SECOND':'F05','MEZZ':'F06','THIRD':'F07','FOURTH':'F08','FIFTH':'F09','SIXTH':'F10','SEVENTH':'F11','EIGHT':'F12','NINTH':'F13','TENTH':'F14','ROOF TOP':'F15'}
Q=collections.defaultdict(lambda: collections.defaultdict(list))   # Q[sheet][key] -> list of formula terms
def add(sheet,key,term):
    if term not in (None,'','0'): Q[sheet][key].append(term)
# ---- slabs/beams/edges per F
SL={'F02':(689.1,238.4,67.8,0),'F03':(737.6,185.9,81.1,43.5),'F04':(650.6,224.9,63.6,0),'F05':(737.5,186.5,79.9,43.0),'F06':(554.9,216.4,64.3,0),'F07':(1273.9,232.4,97.4,33.1),
    'F08':(1134.6,294.6,166.8,33.1),'F09':(1134.6,294.6,166.8,33.1),'F10':(1134.6,294.6,166.8,33.1),'F11':(1134.6,294.6,166.8,33.1),'F12':(1134.6,294.6,166.8,33.1),
    'F13':(1134.4,294.5,186.5,33.1),'F14':(868.4,252.6,122.2,14.2),'F15':(868.1,252.9,125.7,14.2)}
for f,(a,e,b3,b2) in SL.items():
    s=FSH[f]; add(s,'slab','%g*0.25'%a); add(s,'fs','%g'%a); add(s,'fe','%g'%e)
    if b3: add(s,'beam','%g*0.3*0.35'%b3); add(s,'fb','%g*(2*0.35+0.3)'%b3)
    if b2: add(s,'beam','%g*0.2*0.35'%b2); add(s,'fb','%g*(2*0.35+0.2)'%b2)
add('12TH','slab150','176.3*0.15'); add('12TH','slab150','16.3*0.15'); add('12TH','fs','176.3'); add('12TH','fs','16.3'); add('12TH','fe','159.3'); add('12TH','fe','17.3')
add('12TH','beam','31.4*0.25*0.45'); add('12TH','beam','34.0*0.2*0.3'); add('12TH','fb','31.4*(2*0.45+0.25)'); add('12TH','fb','34.0*(2*0.3+0.2)')
# ---- columns per storey
AREA={'01':'0.75*0.5','02':'1.2*0.3','SW':'(2.85*0.25+0.825*0.25)'}; PER={'01':'2*(0.75+0.5)','02':'2*(1.2+0.3)','SW':'2*(2.85+1.075)'}
typ=lambda t: 'SW' if t.startswith('SWC') else t[4:6]
for t,(nos,sub,sup,hs) in CH.items():
    for st,h in hs:
        f=STF[st]; s=FSH[f]
        hc=h if st=='FOUNDATION' else round(h-0.25,3)
        add(s,'col','%d*%s*%g'%(nos,AREA[typ(t)],hc)); add(s,'fc','%d*%s*%g'%(nos,PER[typ(t)],hc))
        if st in ('GROUND','M1','FIRST','M2','SECOND','MEZZ'): add(ASH_COL:= 'colpaint_'+s, 'x','%d*%s*%g'%(nos,PER[typ(t)],hc)) if False else add(s,'colpaint','%d*%s*%g'%(nos,PER[typ(t)],hc))
# ---- walls per storey
MAIN={'F01':3.85,'F03':2.7,'F05':4.05,'F07':3.3,'F08':3.3,'F09':3.3,'F10':3.3,'F11':3.3,'F12':3.3,'F13':3.3,'F14':3.3,'F15':3.15}
EMG={'F01':2.5,'F02':2.7,'F04':2.7,'F06':3.0,'F07':3.3,'F08':3.3,'F09':3.3,'F10':3.3,'F11':3.3,'F12':3.3,'F13':3.3,'F14':3.3,'F15':3.15}
for f,h in MAIN.items():
    s=FSH[f]; add(s,'wsh','22.05*%g*0.25'%(h-0.25)); add(s,'wlift','21.825*%g*0.25'%(h-0.25)); add(s,'fw','2*22.05*%g'%(h-0.25)); add(s,'fw','2*21.825*%g'%(h-0.25))
for f,h in EMG.items():
    s=FSH[f]; add(s,'wsh','25.57*%g*0.25'%(h-0.25)); add(s,'fw','2*25.57*%g'%(h-0.25))
add('12TH','wlift','21.825*4.05*0.25'); add('12TH','fw','2*21.825*4.05')
# ---- stairs per storey (main 11, emergency 12)
SMAIN={'F01':3.85,'F03':2.7,'F05':4.05,'F07':3.3,'F08':3.3,'F09':3.3,'F10':3.3,'F11':3.3,'F12':3.3,'F13':3.3,'F14':3.3}
SEMG={'F01':2.5,'F02':2.7,'F04':2.7,'F06':3.0,'F07':3.3,'F08':3.3,'F09':3.3,'F10':3.3,'F11':3.3,'F12':3.3,'F13':3.3,'F14':3.3}
for D in (SMAIN,SEMG):
    for f,h in D.items():
        s=FSH[f]; add(s,'stair','(2.966*%g/3.3+2.625)'%h); add(s,'fst','(2*3.424*1.8+15.0+22*0.15*1.8)'); add(s,'t_stair','(2*1.8*3.0+22*0.15*1.8+2.2*3.75+1.8*3.75)')
# ---- rebar per sheet
RBK={('Columns',10):'r_c10',('Columns',20):'r_c20',('Columns',25):'r_c25',('Beams',10):'r_b10',('Beams',16):'r_b16',('Beams',20):'r_b20',('Beams',25):'r_b25',
     ('Shear Walls',10):'r_w10',('Lift Walls',10):'r_w10',('Shear Walls',12):'r_w12',('Lift Walls',12):'r_w12',('Retaining / Ramp Walls',12):'r_w12',
     ('Shear Walls',20):'r_w20',('Lift Walls',20):'r_w20',('Shear Walls',25):'r_w25',('Lift Walls',25):'r_w25',('Staircases',12):'r_s12',('Staircases',16):'r_s16',
     ('Floor Slabs',12):'r_sl12',('Floor Slabs',16):'r_sl16',('Lift Core Roof Slab',12):'r_sl12',('Raft Foundation',20):'r_raft20',('Raft Foundation',25):'r_raft25'}
for k,v in RBF.items():
    f,e,dd=k.split('|'); 
    if v>0.0005: add(FSH[f],RBK[(e,int(dd))],'%.3f'%v)
# ---- openings & allocations
DOORS=[('D1',1.8,2.4,1),('D2',1.0,2.2,59),('D3',0.9,2.2,126),('D4',0.9,2.35,1),('D5',3.2,2.2,1),('D6',0.75,2.2,172),('D7',0.7,2.2,12),('D8',1.2,2.2,21),('ED1',1.0,2.2,36),('ED2',1.0,2.2,20),('D9',0.9,2.2,13),('MD1',1.8,2.2,3),('FD1',1.5,2.2,7),('M1',0.9,2.2,18),('M2',0.75,2.2,36),('M3',0.45,2.2,8),('M5',0.6,2.2,24),('GD1',1.8,2.2,2),('DW1',2.4,2.2,2),('DW2',5.05,2.2,1),('SD1',3.0,2.2,8),('SD2',1.6,2.2,28),('SD3',1.3,2.2,16),('SD4',1.8,2.2,30),('SD5',1.2,2.2,7),('RD1',4.2,2.157,2)]
WINS=[('W1',3.6,1.9,1),('W2',1.8,1.3,44),('W3',1.8,1.5,1),('W4',0.9,1.3,77),('W5',1.8,1.9,1),('W6',3.5,1.5,1),('W7',1.8,1.6,12),('W8',1.2,1.9,22),('W9',1.2,1.15,61),('W10',1.2,1.2,8),('W11',1.5,1.3,47),('W12',1.5,1.15,27),('W13',2.4,1.3,6),('W14',3.6,2.2,3),('W15',3.0,1.6,8),('W16',2.4,1.9,2),('W17',1.8,1.9,22),('W18',0.75,1.3,7),('W19',2.1,0.9,2),('W20',1.45,1.9,6),('HW1',0.9,0.6,104),('HW2',0.75,0.6,40),('HW3',0.6,0.6,12),('HW4',1.2,0.6,12)]
# finished floor areas per arch floor (with documented corrections)
def fin(f,k): return FIN.get(f,{}).get('res',{}).get(k,0)
K={'wet':'40x40 non-slip porcelain (wet areas)','lob':'60x120 semi-polished porcelain (lobbies)','ns':'60x60 non-slip porcelain R11 (corridors/terraces/service)','semi':'60x60 semi-polished porcelain (habitable rooms)','pu':'PU resin / coating (parking & ramps)','grey':'interlocking/PU (unlabelled grey)'}
AF={}
for f in ['GF','1F','2F','MEZZ','3F','4F','5F','6F','7F','8F','9F','10F','RT']:
    d={k:fin(f,v) for k,v in K.items()}; d['int']=d.pop('grey')
    AF[f]=d
AF['GF']['semi']+=86.2; AF['GF']['ns']+=47.0
AF['9F']['lob']-=337.4; AF['9F']['int']+=337.4
AF['RT']['ns']-=412.1; AF['RT']['int']+=412.1
AF['MEZZ']['ns']-=176.8; AF['MEZZ']['pu']+=176.8
AFL=list(AF)
def alloc(total,weights):
    keys=[k for k in weights if weights[k]>0]; s=sum(weights[k] for k in keys)
    raw={k:total*weights[k]/s for k in keys}; base={k:int(math.floor(raw[k])) for k in keys}
    rem=total-sum(base.values())
    for k in sorted(keys,key=lambda k:-(raw[k]-base[k]))[:rem]: base[k]+=1
    return {k:v for k,v in base.items() if v}
RES=['3F','4F','5F','6F','7F','8F','9F','10F']
semiW={f:AF[f]['semi'] for f in AFL}; resW={f:AF[f]['semi'] for f in RES}; wetW={f:AF[f]['wet'] for f in AFL}
even=lambda fl:{f:1 for f in fl}
RULE={'D1':{'GF':1},'D4':{'GF':1},'D5':{'GF':1},'GD1':{'GF':1},'DW1':{'GF':1},'DW2':{'GF':1},'RD1':{'GF':1},'MD1':{'GF':1},
      'D2':resW,'D3':{f:AF[f]['semi'] for f in ['GF']+RES+['RT']},'D6':wetW,'D7':even(['GF']+RES+['RT']),'D8':even(RES),'ED1':even(['GF','1F','2F','MEZZ']+RES+['RT']),
      'ED2':even(RES),'D9':even(['GF']+RES+['RT']),'FD1':resW,'M1':even(RES),'M2':even(RES),'M3':even(RES),'M5':even(RES),
      'SD1':resW,'SD2':resW,'SD3':resW,'SD4':resW,'SD5':resW}
OPEN={}   # OPEN[archfloor][name]=n
for n,w,h,q in DOORS:
    for f,c in alloc(q,RULE[n]).items(): OPEN.setdefault(f,{})[n]=c
for n,w,h,q in WINS:
    if q<=3: rule={'GF':1}
    elif n.startswith('HW'): rule=wetW
    else: rule=resW
    for f,c in alloc(q,rule).items(): OPEN.setdefault(f,{})[n]=c
DIM={n:(w,h) for n,w,h,q in DOORS+WINS}
for f,o in OPEN.items():
    s=ASH[f]
    for n,c in o.items(): add(s,'n_'+n,'%d'%c)
    lint='+'.join('%d*(%g+0.3)'%(c,DIM[n][0]) for n,c in o.items())
    add(s,'lintel','(%s)*0.15*0.225'%lint); add(s,'fl','(%s)*(2*0.225+0.15)'%lint)
add('11TH','coping','182.5*0.3*0.15'); add('12TH','coping','(105.0+17.3)*0.3*0.15'); add('11TH','fl','182.5*2*0.15'); add('12TH','fl','(105.0+17.3)*2*0.15')
# ---- architectural per floor
HH={'GF':3.85,'1F':2.7,'2F':2.7,'MEZZ':2.7,'3F':3.3,'4F':3.3,'5F':3.3,'6F':3.3,'7F':3.3,'8F':3.3,'9F':3.3,'10F':3.3,'RT':3.15,'ROOF':1.2}
LEXT={'GF':142.2,'1F':134.3,'2F':134.0,'MEZZ':191.5,'3F':148.0,'4F':224.2,'5F':224.2,'6F':224.2,'7F':224.2,'8F':224.2,'9F':224.1,'10F':181.8,'RT':182.5}
for f in W:
    s=ASH[f]; hc=HH[f]-(0.25 if f!='ROOF' else 0); o=OPEN.get(f,{})
    l150=W[f]['w150']; l200=W[f]['w200']; sh=l150/(l150+l200) if l150+l200 else 1
    dadd='+'.join('%d*%g*(3.05-%g)'%(c,DIM[n][0],DIM[n][1]) for n,c in o.items())
    add(s,'blk150','%.1f*%g'%(l150,hc)); add(s,'blk200','%.1f*%g'%(l200,hc))
    if dadd: add(s,'blk150','(%s)*%.3f'%(dadd,sh)); add(s,'blk200','(%s)*%.3f'%(dadd,1-sh))
    if f=='ROOF': continue
    win='+'.join('%d*%g*%g'%(c,DIM[n][0],DIM[n][1]) for n,c in o.items() if n.startswith(('W','HW'))) or '0'
    dor='+'.join('%d*%g*%g'%(c,DIM[n][0],DIM[n][1]) for n,c in o.items() if not n.startswith(('W','HW'))) or '0'
    wet=AF[f]['wet']
    wetw='%.1f/3.8*8.0*%g'%(wet,hc) if wet else '0'
    add(s,'rint','(2*(%.1f+%.1f)+2*%.1f-16.8-%.1f)*%g-%s-2*(%s)-(%s)'%(l150,l200,W[f]['rc'],LEXT[f],hc,wetw,dor,win))
    if wet:
        add(s,'rwet','%.1f/3.8*8.0*%g-%.1f/3.8*0.75*2.2'%(wet,hc,wet))
        add(s,'wtile','%.1f/3.8*8.0*2.4-%.1f/3.8*0.75*2.2'%(wet,wet))
        add(s,'pwet','(%.1f/3.8*8.0*%g-%.1f/3.8*0.75*2.2)-(%.1f/3.8*8.0*2.4-%.1f/3.8*0.75*2.2)'%(wet,hc,wet,wet,wet))
    add(s,'rext','%.1f*%g-(%s)'%(LEXT[f],HH[f],win))
    if win!='0': add(s,'burglar',win)
    d=AF[f]
    for k,key in (('wet','t_wet'),('lob','t_lob'),('ns','t_ns'),('semi','t_semi'),('int','t_int'),('pu','t_pu')):
        if d[k]>0.05: add(s,key,'%.1f'%d[k])
    tiled=d['wet']+d['lob']+d['ns']+d['semi']
    add(s,'screed','%.1f'%tiled); add(s,'bed','%.1f'%tiled)
    ceil=d['semi']+d['lob']+(0 if f in ('1F','MEZZ') else d['ns'])
    if ceil>0.05: add(s,'ceil','%.1f'%ceil)
    if wet: add(s,'ceilwet','%.1f'%wet)
    td='+'.join('%d*%g*%g*2'%(o[n],DIM[n][0],DIM[n][1]) for n in ('D3','D4','D6','FD1') if n in o)
    fr='+'.join('%d*(2*%g+%g)'%(o[n],DIM[n][1],DIM[n][0]) for n in ('D3','D4','D6','FD1') if n in o)
    if fr:
        add(s,'pwood','%s+(%s)*0.25'%(td,fr)); add(s,'frame',fr); add(s,'stop',fr)
        lv=sum(o.get(n,0) for n in ('D3','D4','D6'))
        add(s,'hinge','%d'%math.ceil(lv*1.5))
        if o.get('D3',0)+o.get('D4',0): add(s,'lock','%d'%(o.get('D3',0)+o.get('D4',0)))
        if o.get('D6',0): add(s,'ilock','%d'%o['D6'])
# bed also over stair finishes
for s in SHEETS:
    for t in Q[s].get('t_stair',[]): add(s,'bed',t)
# waterproofing
add('9TH','wp','337.4'); add('11TH','wp','412.1'); add('12TH','wp','176.3+16.3')
add('9TH','wps','337.4'); add('11TH','wps','412.1'); add('12TH','wps','176.3+16.3')
add('11TH','flash','182.5'); add('12TH','flash','105.0+17.3'); add('11TH','gutter','182.5'); add('12TH','gutter','105.0+17.3')
# colpaint -> arch painting H
if __name__=='__main__':
    import pprint
    for s in SHEETS: print(s,{k:len(v) for k,v in Q[s].items()})
    print({f:o for f,o in OPEN.items()})
