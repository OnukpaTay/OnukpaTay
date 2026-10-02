import pymupdf, re, json, collections
d=pymupdf.open('docs/Documents.pdf')
def dec(s): return ''.join(chr(ord(c)-0xF000) if 0xF000<=ord(c)<0xF100 else c for c in s)
LV=[('FOUNDATION',-1000),('GROUND',300),('M1',2500),('FIRST',4150),('M2',5200),('SECOND',6850),('MEZZ',7900),('THIRD',10900),('FOURTH',14200),('FIFTH',17500),('SIXTH',20800),('SEVENTH',24100),('EIGHT',27400),('NINTH',30700),('TENTH',34000),('ROOF TOP',37300),('ROOF LEVEL',40450)]
def lvl(t):
    t=t.upper()
    for k,v in LV:
        if k=='GROUND' and 'N.G.L /GROUND' in t: return 'GROUND'
        if k in t: return k
    return None
res={}
for n in [8,9,11,12,13]:
    bl=[(b[0],b[1],dec(b[4]).strip().replace('\n',' / ')) for b in d[n-1].get_text('blocks')]
    levels=[];calls=[];titles=[];nos=[]
    for x,y,t in bl:
        if t.startswith('COLUMN TYPE'): titles.append((x,y,t.split('_')[1].split('/')[0].strip()))
        elif re.match(r'\d+-NOS',t): nos.append((x,y,int(t.split('-')[0])))
        elif re.search(r'Y\d{3,5}',t) and 'x' not in t.split('-')[0][:0]:
            calls.append((x,y,t))
        else:
            L=lvl(t)
            if L and ('S.S.L' in t or 'FLOOR' in t or 'LEVEL' in t or 'TERRACE' in t) and 'N.G.L' != t.split('/')[0].strip():
                if t.startswith('N.G.L') and 'GROUND' not in t: continue
                levels.append((x,y+12,L))
    # cluster levels by x
    groups=collections.defaultdict(list); gi=0; lastx=None
    for x,y,L in sorted(levels):
        if lastx is not None and x-lastx>40: gi+=1
        groups[gi].append((x,y,L)); lastx=x
    gx=sorted(groups)
    for g in gx:
        lv=sorted(groups[g],key=lambda a:-a[1])  # bottom first
        x0=min(a[0] for a in lv)
        # title: nearest title to the right within 250
        tt=[t for t in titles if 0<t[0]-x0<260]
        tt=min(tt,key=lambda t:t[0]-x0)
        nn=min([q for q in nos if abs(q[1]-tt[1])<25],key=lambda q:abs(q[0]-tt[0]))
        allx0=sorted(min(a[0] for a in groups[h]) for h in groups)
        cs=[c for c in calls if 60<c[0]-x0<320 and max([q for q in allx0 if q<c[0]-60])==x0]
        key=tt[2]
        R=res.setdefault(key,{'nos':nn[2],'page':n,'items':[]})
        names=[a[2] for a in lv]; ys=[a[1] for a in lv]
        for x,y,t in cs:
            for part in t.split(' / '):
                m=re.match(r'(?:(\d)x)?(\d+)-Y(\d+)',part.strip())
                if not m: continue
                mult=int(m.group(1) or 1); cnt=int(m.group(2)); mark=m.group(3).replace('25003','2503')
                if '@' in part:  # links: interval containing y
                    st=None
                    for i in range(len(ys)-1):
                        if ys[i+1]<=y+4<=ys[i]: st=names[i]
                    if st is None: st='??'
                else:  # main: nearest level line; storey below it
                    i=min(range(len(ys)),key=lambda i:abs(ys[i]-(y+8)))
                    st=names[i-1] if i>0 else 'BELOW_'+names[0]
                R['items'].append((st,mark,mult*cnt,part.strip(),round(y)))
json.dump(res,open('cols.json','w'),indent=0)
ORDER=[k for k,v in LV]
for k,v in res.items():
    print(k,v['nos'],'P',v['page'])
    agg=collections.defaultdict(lambda: collections.defaultdict(list))
    for st,mark,c,p,y in v['items']: agg[st][mark].append(c)
    for st in sorted(agg,key=lambda s: ORDER.index(s.replace('BELOW_','')) if s.replace('BELOW_','') in ORDER else 99):
        print('   %-12s'%st, '  '.join('%s:%s'%(m,'+'.join(map(str,c))) for m,c in sorted(agg[st].items())))

# dedupe BELOW_
import copy
out={}
for k,v in res.items():
    agg=collections.defaultdict(lambda: collections.defaultdict(int))
    below=[]
    for st,mark,c,p,y in v['items']:
        if st.startswith('BELOW_'): below.append((st[6:],mark,c)); continue
        agg[st][mark]+=c
    for L,mark,c in below:
        i=ORDER.index(L); prev=[s for s in ORDER[:i] if s in agg][-1]
        if mark not in agg[prev]: agg[prev][mark]+=c; print('  moved',k,L,mark,'->',prev)
    out[k]={'nos':v['nos'],'page':v['page'],'st':{s:dict(m) for s,m in agg.items()}}
json.dump(out,open('cols_final.json','w'),indent=1)
tot=collections.defaultdict(int)
for k,v in out.items():
    pg=v['page']
    for s,m in v['st'].items():
        for mk,c in m.items(): tot[(pg,mk)]+=c*v['nos']
for kk in sorted(tot): print(kk,tot[kk])
