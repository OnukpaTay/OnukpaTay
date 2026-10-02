import pymupdf,collections,sys
from slabarea import calib
d=pymupdf.open('docs/Documents.pdf')
def merge(iv,gap):
    iv=sorted(iv); out=[]
    for a,b in iv:
        if out and a<=out[-1][1]+gap: out[-1][1]=max(out[-1][1],b)
        else: out.append([a,b])
    return out
def lines(n,col=(0.39,0.39,0.4),w=0.72,gap=4.0,maxseg=None):
    p=d[n-1]; H=collections.defaultdict(list); V=collections.defaultdict(list)
    for dr in p.get_drawings():
        if round(dr.get('width') or 0,2)!=w or tuple(round(c,2) for c in (dr.get('color') or ()))!=col: continue
        for it in dr['items']:
            if it[0]!='l': continue
            a,b=it[1],it[2]
            if maxseg and abs(a-b)>maxseg: continue
            if abs(a.y-b.y)<0.05: H[round(a.y*4)/4].append((min(a.x,b.x),max(a.x,b.x)))
            elif abs(a.x-b.x)<0.05: V[round(a.x*4)/4].append((min(a.y,b.y),max(a.y,b.y)))
    H={k:merge(v,gap) for k,v in H.items()}; V={k:merge(v,gap) for k,v in V.items()}
    return H,V
def pairs(D,width_pt,tol=0.6,minlen=5):
    keys=sorted(D); tot=0; segs=[]; used=set()
    for i,k in enumerate(keys):
        for k2 in keys[i+1:]:
            dd=k2-k
            if dd>width_pt+tol: break
            if abs(dd-width_pt)>tol: continue
            for a,b in D[k]:
                for c,e in D[k2]:
                    o=min(b,e)-max(a,c)
                    if o>minlen: tot+=o; segs.append((k,max(a,c),min(b,e)))
    return tot,segs
if __name__=='__main__':
    for n in map(int,sys.argv[1:]):
        sx,sy,_=calib(n); H,V=lines(n)
        res={}
        for wmm in (200,250,300):
            th,_=pairs(H,wmm/sy); tv,_=pairs(V,wmm/sx)
            res[wmm]=round((th*sx+tv*sy)/1000,1)
        print(n,res)
