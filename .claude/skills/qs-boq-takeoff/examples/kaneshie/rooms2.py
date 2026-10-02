import pymupdf,os,numpy as np,cv2,collections,sys,json
from walls import wallband,d,DPI
from rooms import LK,LC
from arcs import scale
def gridref(n):
    ws=d[n-1].get_text('words')
    def first(lbl,axis):
        c=[w for w in ws if w[4]==lbl and w[0]<1000]
        if axis=='x':  # top-most occurrence
            w=min(c,key=lambda w:w[1]); return (w[0]+w[2])/2
        w=min(c,key=lambda w:w[0]); return (w[1]+w[3])/2
    return first('1','x'),first('12','x'),first('A1','y'),first('Q','y')
def classify(cp,N):
    if N==0 or len(cp)<0.008*N or len(cp)<12: return 'untiled'
    r,g,b=cp.mean(0); fr=len(cp)/N
    if b>r+15 and b>g: return '40x40 non-slip porcelain'
    if g>r+15 and b>r+15: return '50x50 matte porcelain R11'
    if g>r+15 and g>=b: return '60x120 semi-polished porcelain' if fr<0.5 else 'grass/landscape'
    if r>g+20: return '60x60 non-slip porcelain R11' if fr>=0.10 else '60x60 semi-polished porcelain'
    return 'grey: interlocking/PU'
def rooms(n,tn,clip=(60,90,1000,800),save=None,sn=None):
    L,k,sk,mmpx,_=wallband(n,clip)
    z=DPI/72
    br=k.copy()
    br=br|cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((1,79),np.uint8))|cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((79,1),np.uint8))
    big=cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((121,121),np.uint8))
    cs,_=cv2.findContours(big,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    foot=np.zeros_like(k); cv2.drawContours(foot,[c for c in cs if cv2.contourArea(c)>200000],-1,1,-1)
    if sn:
        from grid import gridpos
        import grid as G
        X,Y=G.gridpos(sn)
        top=lambda k: min(v[1] for v in X[k]); left=min(v[0] for v in Y['A1'])
        s1=[v[0] for v in X['1'] if abs(v[1]-top('1'))<2][0]; s12=[v[0] for v in X['12'] if abs(v[1]-top('12'))<2][0]
        sa=[v[1] for v in Y['A1'] if abs(v[0]-left)<2][0]; sq=[v[1] for v in Y['Q'] if abs(v[0]-left)<2][0]
        g=gridref(n)
        axs=(s12-s1)/(g[1]-g[0]); bxs=s1-axs*g[0]; ays=(sq-sa)/(g[3]-g[2]); bys=sa-ays*g[2]
        sm=(cv2.imread('sl_%d.png'%sn,0)<128).astype(np.uint8)
        H,W=k.shape; yy,xx=np.mgrid[0:H,0:W]
        mx=((xx/z+clip[0])*axs+bxs)*2; my=((yy/z+clip[1])*ays+bys)*2
        foot=cv2.remap(sm,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_NEAREST,borderValue=0)
        foot=cv2.erode(foot,np.ones((25,25),np.uint8))
    br=br|(1-foot)
    free=(br==0).astype(np.uint8)
    nl,lab,st,cen=cv2.connectedComponentsWithStats(free,connectivity=4)
    # tiling sheet raster
    g1=gridref(n); g2=gridref(tn)
    ax=(g2[1]-g2[0])/(g1[1]-g1[0]); bx=g2[0]-ax*g1[0]
    ay=(g2[3]-g2[2])/(g1[3]-g1[2]); by=g2[2]-ay*g1[2]
    tz=150/72
    tp=d[tn-1].get_pixmap(dpi=150,alpha=False); ta=np.frombuffer(tp.samples,np.uint8).reshape(tp.height,tp.width,3).astype(int)
    tsat=(ta.max(2)-ta.min(2))>25
    words=d[n-1].get_text('words')
    out=[]
    for i in range(1,nl):
        A=st[i,4]*mmpx*mmpx/1e6
        x,y,w_,h_=st[i,:4]
        if A<0.8 or x==0 or y==0 or x+w_>=lab.shape[1]-1 or y+h_>=lab.shape[0]-1: continue
        m=(lab[y:y+h_,x:x+w_]==i)
        ys,xs=np.nonzero(m); ys=ys+y; xs=xs+x
        sel=np.arange(len(xs)); 
        if len(sel)>4000: sel=np.random.RandomState(0).choice(len(xs),4000,replace=False)
        px=(xs[sel]/z+clip[0]); py=(ys[sel]/z+clip[1])
        tx=((ax*px+bx)*tz).astype(int); ty=((ay*py+by)*tz).astype(int)
        ok=(tx>=0)&(ty>=0)&(tx<ta.shape[1])&(ty<ta.shape[0]); tx,ty=tx[ok],ty[ok]
        s=tsat[ty,tx]; cp=ta[ty[s],tx[s]]
        mc=cp.mean(0).round().tolist() if len(cp) else None
        cp=cp[~((cp[:,0]>200)&(cp[:,2]>200)&(cp[:,1]<90))]
        cp2=cp[(cp.max(1)-cp.min(1))>40]; mc2=cp2.mean(0).round().tolist() if len(cp2) else None
        frac=s.mean() if len(s) else 0
        cls=classify(cp,len(s))
        cnt,_=cv2.findContours(m.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        per=sum(cv2.arcLength(c,True) for c in cnt)*mmpx/1000
        nm=[ww[4] for ww in words if clip[0]<ww[0]<clip[2] and clip[1]<ww[1]<clip[3] and ww[4].isalpha() and ww[4].isupper() and len(ww[4])>1
            and 0<=int(((ww[1]+ww[3])/2-clip[1])*z)-y<h_ and 0<=int(((ww[0]+ww[2])/2-clip[0])*z)-x<w_ and m[int(((ww[1]+ww[3])/2-clip[1])*z)-y,int(((ww[0]+ww[2])/2-clip[0])*z)-x]]
        out.append(dict(area=round(A,2),perim=round(per,2),cls=cls,name=' '.join(nm),frac=round(float(frac),3),mc=mc,mc2=mc2,n2=int(len(cp2)),cx=float(cen[i,0]),cy=float(cen[i,1]),i=i))
    if save:
        v=np.full(k.shape+(3,),255,np.uint8); v[br>0]=(0,0,0)
        col={'40x40 non-slip porcelain':(200,120,120),'50x50 matte porcelain R11':(200,200,120),'60x120 semi-polished porcelain':(140,200,140),'grass/landscape':(100,230,100),
             '60x60 non-slip porcelain R11':(120,120,230),'60x60 semi-polished porcelain':(200,170,240),'grey: interlocking/PU':(170,170,170),'untiled':(240,240,240)}
        for r in out: v[lab==r['i']]=col[r['cls']]
        for r in out: cv2.putText(v,'%s %.0f'%(r['name'][:10],r['area']),(int(r['cx'])-30,int(r['cy'])),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),1)
        cv2.imwrite(save,v)
    return out
if __name__=='__main__':
    n,tn=int(sys.argv[1]),int(sys.argv[2]); sn=int(sys.argv[3]) if len(sys.argv)>3 else None; o=rooms(n,tn,save='rmA%d.png'%n,sn=sn)
    c=collections.defaultdict(float)
    for r in o: c[r['cls']]+=r['area']
    print(n,len(o),{k:round(v,1) for k,v in sorted(c.items())},'total',round(sum(c.values()),1))
    json.dump(o,open('rooms_%d.json'%n,'w'))
