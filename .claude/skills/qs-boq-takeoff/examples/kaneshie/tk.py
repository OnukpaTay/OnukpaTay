import openpyxl,re,ast,collections,math,lab
from xml.sax.saxutils import escape
U='user.xlsx'
wb=openpyxl.load_workbook(U)
BILLS=[('SUBSTRUCTURE','SUB'),('GROUND FLR ','GF'),('1ST FLR ','1ST'),('2ND FLR','2ND'),('3RD FLR','3RD'),('4TH FLR ','4TH'),('5TH FLR ','5TH'),('6TH FLR  ','6TH'),
('7TH FLR   ','7TH'),('8TH FLR   ','8TH'),('9TH FLR    ','9TH'),('10TH FLR   ','10TH'),('11TH FLR','11TH'),('12TH FLR ','12TH'),('LIFTS & PS',None)]
def norm(e): return re.sub(r'\s','',re.sub(r'\d+\.?\d*(?:[eE][-+]?\d+)?',lambda m:repr(float(m.group())),e.lstrip('=')))
# ---------- expression expansion ----------
ADDS=(ast.Add,ast.Sub)
def terms_of(n,s=1):
    if isinstance(n,ast.BinOp) and isinstance(n.op,ADDS):
        return terms_of(n.left,s)+terms_of(n.right,s if isinstance(n.op,ast.Add) else -s)
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub): return terms_of(n.operand,-s)
    return [(s,n)]
def facs(n):
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mult): return facs(n.left)+facs(n.right)
    return [n]
def is_coll(n):
    if not(isinstance(n,ast.BinOp) and isinstance(n.op,ADDS)): return False
    T=terms_of(n)
    if len(T)>=3: return True
    for s,t in T:
        f=facs(t)
        if len(f)>=3 or any(isinstance(x,ast.BinOp) and isinstance(x.op,ADDS) for x in f) or (isinstance(t,ast.BinOp) and isinstance(t.op,ast.Div)): return True
    return False
def expand(n,top=False):
    """-> list of (sign,[factor nodes])"""
    if isinstance(n,ast.BinOp) and isinstance(n.op,ADDS) and (top or is_coll(n)):
        out=[]
        for s,t in terms_of(n):
            for s2,f in expand(t): out.append((s*s2,f))
        return out
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):
        return [(-s,f) for s,f in expand(n.operand)]
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Mult):
        L=expand(n.left); R=expand(n.right)
        return [(a*b,f+g) for a,f in L for b,g in R]
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):
        L=expand(n.left); out=[]
        for s,f in L:
            out.append((s,f[:-1]+[ast.BinOp(left=f[-1],op=ast.Div(),right=n.right)]))
        return out
    return [(1,[n])]
def txt(n):
    if isinstance(n,ast.Constant): return SRC_NUM(n)
    if isinstance(n,ast.BinOp):
        l=txt(n.left); r=txt(n.right)
        if isinstance(n.op,ADDS):
            return l+('+' if isinstance(n.op,ast.Add) else '-')+(('('+r+')') if isinstance(n.right,ast.BinOp) and isinstance(n.right.op,ADDS) else r)
        wl=lambda x,s: '('+s+')' if isinstance(x,ast.BinOp) and isinstance(x.op,ADDS) else s
        if isinstance(n.op,ast.Mult): return wl(n.left,l)+'*'+wl(n.right,r)
        if isinstance(n.op,ast.Div): return wl(n.left,l)+'/'+(('('+r+')') if isinstance(n.right,ast.BinOp) else r)
    if isinstance(n,ast.UnaryOp): return '-'+txt(n.operand)
    return ast.unparse(n)
def SRC_NUM(n):
    v=n.value
    return getattr(n,'_s',None) or (repr(v) if isinstance(v,float) else str(v))
def parse(e):
    t=ast.parse(e.lstrip('=').strip(),mode='eval').body
    # keep original number spelling
    toks=iter(re.findall(r'\d+\.?\d*(?:[eE][-+]?\d+)?',e.lstrip('=')))
    nodes=sorted([x for x in ast.walk(t) if isinstance(x,ast.Constant)],key=lambda x:(x.lineno,x.col_offset))
    for x in nodes: x._s=next(toks)
    return t
def ev(s): return eval(s.replace('^','**'),{'__builtins__':{}})
def jf(fs): return '*'.join(('('+txt(f)+')') if isinstance(f,ast.BinOp) and isinstance(f.op,ADDS) else txt(f) for f in fs)
def isint(n): return isinstance(n,ast.Constant) and isinstance(n.value,int)
def layout(sign,fs):
    """-> dict nr,dims(list of (text,isconst)),qty"""
    fs=list(fs); nr=[]
    if len(fs)>=2 and isint(fs[0]):
        nr.append(fs.pop(0))
        if len(fs)==3 and isint(fs[0]) and all(isinstance(x,ast.Constant) for x in fs[1:]): nr.append(fs.pop(0))
    dims=[]
    i=0
    while i<len(fs):
        if isint(fs[i]) and fs[i].value==2 and i+1<len(fs) and isinstance(fs[i+1],ast.BinOp) and isinstance(fs[i+1].op,ADDS):
            dims.append(ast.BinOp(left=fs[i],op=ast.Mult(),right=fs[i+1])); i+=2
        else: dims.append(fs[i]); i+=1
    while len(dims)>3:
        dims=[ast.BinOp(left=dims[0],op=ast.Mult(),right=dims[1])]+dims[2:]
    nrt=None
    if nr: nrt='*'.join(txt(x) for x in nr)
    return nrt,[txt(d) for d in dims]
# ---------- opening matcher ----------
AFS=collections.defaultdict(list)
for af,s in lab.ASH.items(): AFS[s].append(af)
def opening(af,fs,used):
    if not af: return None
    vals=[]
    for f in fs:
        try: vals.append(ev(txt(f)))
        except Exception: vals.append(None)
    texts=[txt(f) for f in fs]
    best=None
    for n,c in lab.OPEN.get(af,{}).items():
        if n in used: continue
        w,h=lab.DIM[n]
        for i in range(len(fs)-1):
            if vals[i]==c and re.match(r'%s(?![\d.])'%re.escape('%g'%w),texts[i+1]):
                rest=' '.join(texts[i+2:]); sc=1+(1 if re.search(r'(?<![\d.])%s(?![\d.])'%re.escape('%g'%h),rest) else 0)
                if not best or sc>best[0]: best=(sc,n,c)
    if not best: return None
    used.add(best[1])
    return '%s (%d nr, %gx%g)'%(best[1],best[2],lab.DIM[best[1]][0],lab.DIM[best[1]][1])
SUBL={'stair':['flights: 2.966 m3 per 3.3 m storey x (storey ht / 3.3)','landings'],
'fst':['flight soffits: 2 x 3.424 x 1.8','landing soffits','risers: 22 x 0.15 x 1.8'],
't_stair':['flights: 2 x 1.8 x 3.0','risers: 22 x 0.15 x 1.8','floor landing 2.2 x 3.75','half landing 1.8 x 3.75']}
SUBL['bed']=SUBL['t_stair']
def sublabels(code,key,parent,rows):
    out=[]; used=set()
    if len(rows)==1: return [parent]
    for i,(s,fs) in enumerate(rows):
        t=jf(fs); o=opening(code,fs,used); ddt='Ddt ' if s<0 else ''
        lb=None
        if key in SUBL and len(rows)==len(SUBL[key]): lb=parent+' - '+SUBL[key][i]
        elif key=='rint':
            lb={0:'block wall faces: 2 x (150 + 200 block runs) x ht',1:'RC wall faces: 2 x RC wall run x ht',2:'Ddt lift/stair shaft inner faces 16.8 m x ht',3:'Ddt external face of perimeter wall (rendered externally)'}.get(i)
            if lb is None: lb='Ddt washroom walls (measured separately)' if '/3.8' in t else ('Ddt opening %s%s'%(o or '',' - both faces' if fs and isint(fs[0]) and fs[0].value==2 and len(fs)>=4 else ''))
        elif key in ('rwet','wtile','pwet'):
            lb=(ddt+'washroom doors: nr x 0.75 x 2.2') if '0.75*2.2' in t else (ddt+'washroom walls: (wet area / 3.8 m2 per WC) x 8.0 m girth x ht')
        elif key=='rext': lb='External perimeter x storey ht' if i==0 else 'Ddt window %s'%(o or '')
        elif key in ('lintel','fl'): lb=('Lintel over ' if key=='lintel' else 'Lintel formwork over ')+(o or t)+(': nr x (width + 2 x 150 bearing) x '+('150 x 225' if key=='lintel' else 'girth 0.60'))
        elif key in ('blk150','blk200'): lb='Walling over opening %s: nr x width x (3.05 - opening ht) x thickness share'%(o or '')
        elif key=='burglar': lb='Window %s: nr x w x h'%(o or '')
        elif key=='pwood': lb=('Door frame %s: girth x 0.25 m'%o if '0.25' in t[-5:] else 'Door leaf %s: nr x w x h x 2 faces'%o) if o else t
        elif key in ('frame','stop'): lb='Door %s: nr x (2 x ht + width)'%(o or '')
        if lb is None: lb=(ddt if s<0 else '')+(o or ('%s (%d)'%(parent,i+1) if i==0 else '  "  (cont.)'))
        out.append(lb if i==0 or key not in SUBL else lb)
    if key not in SUBL and key not in ('rint','rwet','wtile','pwet','rext'):
        out=[parent+' - '+out[0]]+out[1:] if out and not out[0].startswith(parent) and key not in('lintel','fl','blk150','blk200','burglar','pwood','frame','stop') else out
        if key in('lintel','fl','blk150','blk200','burglar','pwood','frame','stop'): pass
    return out
# ---------- manual items (substructure & lump items) ----------
M={('SUBSTRUCTURE',27):[(1,'40.85*38.27','Block N plot'),(1,'35.2*20.9','Parking-22 forecourt')],
('SUBSTRUCTURE',29):[(1,'(41.0+2*2)*(36.0+2*2)','Raft 41.0 x 36.0 plus 2.0 m working space all round: L x W')],
('SUBSTRUCTURE',31):[(1,'45.0*40.0*4.0','Excavation footprint 45 x 40 (raft + working space) x 4.00 deep (formation -4.000)')],
('SUBSTRUCTURE',33):[(1,'41.0*36.0*1.0','Fill over raft: raft area x 1.00 average'),(-1,'69.445*0.25*1.0','Ddt RC walls: run 69.445 x 0.25 x 1.00'),(-1,'13.294*1.0','Ddt columns: plan area 13.294 m2 x 1.00')],
('SUBSTRUCTURE',35):[(1,'45.0*40.0*1.7','Fill below raft: 45 x 40 x 1.70 (STR-001; RFI - 2700 v 1700)')],
('SUBSTRUCTURE',37):[(1,'45.0*40.0*(4.0-1.7)','Excavation footprint x (4.00 - 1.70)'),(-1,'41.0*36.0*(4.0-1.7)','Ddt raft footprint x (4.00 - 1.70)')],
('SUBSTRUCTURE',39):[(1,'45.0*40.0*4.0','Total excavation'),(-1,'45.0*40.0*(4.0-1.7)','Ddt backfill: excavation footprint x (4.00 - 1.70)'),(1,'41.0*36.0*(4.0-1.7)','Add back raft footprint (backfill is footprint less raft)')],
('SUBSTRUCTURE',41):[(1,'41.0*36.0*0.15','Hardcore under raft: 41.0 x 36.0 x 0.15')],
('SUBSTRUCTURE',50):[(1,'41.0*36.0*0.1','Blinding under raft: 41.0 x 36.0 x 0.10')],
('SUBSTRUCTURE',52):[(1,'41.0*36.0*0.15','Bed: 41.0 x 36.0 x 0.15')],
('SUBSTRUCTURE',55):[(1,'22.05*0.25*1.3','Main stair core walls: run x 250 thk x 1.30 (raft to GF)'),(1,'21.825*0.25*1.3','Lift core walls: run x 250 thk x 1.30'),(1,'25.57*0.25*1.3','Emergency stair core walls: run x 250 thk x 1.30')],
('SUBSTRUCTURE',57):[(1,'41.0*36.0*1.3','Raft: 41.0 x 36.0 x 1.30 (STR-001/002)')],
('SUBSTRUCTURE',75):[(1,'2*22.05*1.3','Main stair core walls: 2 faces x run x 1.30'),(1,'2*21.825*1.3','Lift core walls: 2 faces x run x 1.30'),(1,'2*25.57*1.3','Emergency stair core walls: 2 faces x run x 1.30')],
('SUBSTRUCTURE',77):[(1,'2*(41.0+36.0)','Bed perimeter: 2 x (41.0 + 36.0)')],
('SUBSTRUCTURE',79):[(1,'2*(41.0+36.0)*1.3','Raft perimeter: 2 x (41.0 + 36.0) x 1.30')],
('SUBSTRUCTURE',90):[(1,'2*(41.0+36.0)*1.3','Plinth wall perimeter: 2 x (41.0 + 36.0) x 1.30 high')],
('LIFTS & PS',26):[(1,'2','Passenger lifts in lift core (ARCH lift shaft details)')]}
OVR12={'176.3':'Roof level slab (measured area)','16.3':'Top of lift core slab (measured area)','105.0':'Roof level perimeter (measured)','17.3':'Lift core roof perimeter (measured)'}
# ---------- build row model ----------
R=[]   # each: dict(kind, cells{col:(value,typ)}, ...)  typ: s=str, n=number, f=formula
def row(kind,**c): R.append(dict(kind=kind,c=c)); return len(R)
LINKS={}   # (sheet,row)-> takeoff total row index (1-based in R)
CHECK=[]
for nm,code in BILLS:
    ws=wb[nm]
    title=None
    for r in range(1,40):
        v=ws.cell(r,2).value
        if isinstance(v,str) and v.strip().upper().startswith('BILL NR'): title=v.strip(); break
    if not title: title=nm.strip()
    sub=ws.cell(9,2).value or ''
    bstart=row('bill',A=(title+('  -  '+sub.strip() if sub and not sub.startswith('=') else ''),'s'))
    BILLROW=bstart
    LINKS.setdefault('_bills',[]).append((nm,title,bstart))
    keys=collections.defaultdict(list)
    if code:
        for k,t,l,af in lab.CAP[code]: keys[k].append((t,l,af))
    KN={norm('+'.join(x[0] for x in v)):k for k,v in keys.items()}
    TN=collections.defaultdict(list)
    if code:
        for k,t,l,af in lab.CAP[code]: TN[norm(t)].append(l)
    started=False; lasthead=None
    for r in range(6,ws.max_row+1):
        a=ws.cell(r,1).value; b=ws.cell(r,2).value; v=ws.cell(r,3).value; u=ws.cell(r,4).value
        if isinstance(b,str) and b.upper().startswith('BILL NR'): started=True; continue
        if not started: continue
        if isinstance(v,str) and v.startswith('='):
            # item
            row('item',A=(nm.strip(),'s'),B=(a or '','s'),C=(b.strip() if isinstance(b,str) else '','s'),I=(u or '','s'),K=("BOQ: '%s'!C%d"%(nm,r),'link',"'%s'!C%d"%(nm,r)))
            first=len(R)+1
            n=norm(v)
            if (nm,r) in M:
                src=[(s,e,l,None,None) for s,e,l in M[(nm,r)]]
            elif n in KN:
                k=KN[n]; src=[(1,t,l,k,af) for t,l,af in keys[k]]
            else:
                src=[]
                for s,t in terms_of(parse(v)):
                    tt=txt(t); lb=TN.get(norm(tt))
                    src.append((s,tt,lb[0] if lb else ('Item / provisional sum' if (u or '').lower() in ('item','sum') else 'As measured'),None,None))
            for s,e,l,k,af in src:
                tree=parse(e)
                rows=expand(tree,top=True)
                rows=[(s*s2,f) for s2,f in rows]
                labs=sublabels(af,k,l,rows) if k else ([l] if len(rows)==1 else [l+(' (%d)'%(i+1)) for i in range(len(rows))])
                for (s2,fs),lb in zip(rows,labs):
                    nrt,dims=layout(s2,fs)
                    if nm=='12TH FLR ' and jf(fs) in OVR12: lb=OVR12[jf(fs)]
                    cells=dict(C=(('Ddt  ' if s2<0 and not lb.startswith('Ddt') else '')+lb,'s'),J=(('-' if s2<0 else '')+jf(fs),'s'))
                    allv=([nrt] if nrt else [])+dims
                    if len(allv)==1 and not nrt:
                        cells['H']=(('-' if s2<0 else '')+dims[0],'q1')
                    else:
                        if nrt: cells['D']=(nrt,'in')
                        for col,d in zip('EFG',dims): cells[col]=(d,'in')
                        cells['H']=('-' if s2<0 else '','prod')
                    row('dim',**cells)
            last=len(R)
            t=row('total',C=('Total carried to BOQ  %s item %s'%(nm.strip(),a or ''),'s'),H=((first,last),'sum'),I=(u or '','s'))
            LINKS[(nm,r)]=t
            CHECK.append((nm,r,v,t,first,last))
        elif isinstance(b,str) and a is None and not b.startswith('=') and not re.match(r'(Carried|To Bill|CF|BF|BILL SUMMARY)',b.strip()) and r>20 and len(b)<400:
            row('head',C=(b.strip(),'s'))
    row('blank')
