import pymupdf,collections,sys
from beams import merge,d
from slabarea import calib
def lines2(n,col=(0.39,0.39,0.4),w=0.72):
    p=d[n-1]; Hd=collections.defaultdict(list);Vd=collections.defaultdict(list);Hs=collections.defaultdict(list);Vs=collections.defaultdict(list)
    for dr in p.get_drawings():
        if round(dr.get('width') or 0,2)!=w or tuple(round(c,2) for c in (dr.get('color') or ()))!=col: continue
        for it in dr['items']:
            if it[0]!='l': continue
            a,b=it[1],it[2]; L=abs(a-b); dash=L<=3.2
            if abs(a.y-b.y)<0.05: (Hd if dash else Hs)[round(a.y*4)/4].append((min(a.x,b.x),max(a.x,b.x)))
            elif abs(a.x-b.x)<0.05: (Vd if dash else Vs)[round(a.x*4)/4].append((min(a.y,b.y),max(a.y,b.y)))
    f=lambda D,g:{k:merge(v,g) for k,v in D.items()}
    return f(Hd,3.0),f(Vd,3.0),f(Hs,0.5),f(Vs,0.5)
def pairs2(Dd,Ds,width_pt,tol=0.3,minlen=8):
    segs=[]
    allk=sorted(set(Dd)|set(Ds))
    for k in sorted(Dd):
        for k2 in allk:
            if abs(abs(k2-k)-width_pt)>tol: continue
            if k2 in Dd and k2<k: continue   # dashed-dashed counted once
            other=(Dd.get(k2,[]) if k2>k else [])+Ds.get(k2,[])
            for a,b in Dd[k]:
                for c,e in other:
                    o=min(b,e)-max(a,c)
                    if o>minlen: segs.append((min(k,k2),max(a,c),min(b,e)))
    # remove duplicates/overlaps on same line
    by=collections.defaultdict(list)
    for k,a,b in segs: by[round(k*4)/4].append((a,b))
    out=[];tot=0
    for k,v in by.items():
        for a,b in merge(v,0.5): out.append((k,a,b)); tot+=b-a
    return tot,out
def measure(n,draw=None,widths=((300,(1,0,0)),(200,(0,0,1)))):
    sx,sy,_=calib(n); Hd,Vd,Hs,Vs=lines2(n)
    res={}; p=d[n-1]; sh=p.new_shape() if draw else None
    for wmm,col in widths:
        th,s1=pairs2(Hd,Hs,wmm/sy); tv,s2=pairs2(Vd,Vs,wmm/sx)
        res[wmm]=round((th*sx+tv*sy)/1000,1)
        if draw:
            for k,a,b in s1: sh.draw_line((a,k+wmm/sy/2),(b,k+wmm/sy/2))
            for k,a,b in s2: sh.draw_line((k+wmm/sx/2,a),(k+wmm/sx/2,b))
            sh.finish(color=col,width=2.5)
    if draw: sh.commit(); p.get_pixmap(dpi=90,clip=pymupdf.Rect(*draw)).save('bm%d.png'%n)
    return res
if __name__=='__main__':
    for n in map(int,sys.argv[1:]): print(n,measure(n,draw=(150,100,900,760)))
