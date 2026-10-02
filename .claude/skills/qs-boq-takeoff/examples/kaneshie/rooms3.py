import numpy as np,cv2,sys,json,collections,re
from rooms2 import gridref,classify
from walls import wallband,d,DPI
KW=[('40x40 non-slip porcelain (wet areas)',['WASH','WASHR','WC','TOILET','MALE','FEMALE','SHOWER','BATH']),
    ('50x50 matte porcelain R11 (stairs)',['STAIRS','STAIR','EMERGENCY']),
    ('60x120 semi-polished porcelain (lobbies)',['LOBBY','RECEPTION']),
    ('60x60 non-slip porcelain R11 (corridors/terraces/service)',['CORRIDOR','TERRACE','K.TERRACE','VERANDAH','UTILITY','TRASH','CHUTE','ELECTRICAL','ATRIUM','SECURITY','GARBAGE','STORE','PUMP','POWER','BALCONY','ENTRANCE']),
    ('PU resin / coating (parking & ramps)',['PARKING','RAMP','LEVEL']),
    ('60x60 semi-polished porcelain (habitable rooms)',['BEDROOM','MASTER','LIVING','DINING','KITCHEN','KITCHENETTE','STUDIO','WIC','SHOP','OFFICE','GYM','SITTING','LOUNGE','PLAY','STUDY','HALL','BAR','RESTAURANT']),
    ('no finish (lifts/voids/shafts)',['LIFT','VOID','DUCT','OPEN','SHAFT'])]
def kwclass(t):
    t=t.upper().strip('.,')
    for c,ks in KW:
        if t in ks: return c
    return None
def run(n,tn,sn=None,clip=(60,90,1000,800),save=None,bridge=79):
    L,k,sk,mmpx,_=wallband(n,clip); z=DPI/72; H,W=k.shape
    br=k|cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((1,bridge),np.uint8))|cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((bridge,1),np.uint8))
    yy,xx=np.mgrid[0:H,0:W]
    if sn:
        import grid as G
        X,Y=G.gridpos(sn); top=lambda q: min(v[1] for v in X[q]); left=min(v[0] for v in Y['A1'])
        s1=[v[0] for v in X['1'] if abs(v[1]-top('1'))<2][0]; s12=[v[0] for v in X['12'] if abs(v[1]-top('12'))<2][0]
        sa=[v[1] for v in Y['A1'] if abs(v[0]-left)<2][0]; sq=[v[1] for v in Y['Q'] if abs(v[0]-left)<2][0]
        g=gridref(n); axs=(s12-s1)/(g[1]-g[0]); bxs=s1-axs*g[0]; ays=(sq-sa)/(g[3]-g[2]); bys=sa-ays*g[2]
        sm=(cv2.imread('sl_%d.png'%sn,0)<128).astype(np.uint8)
        foot=cv2.remap(sm,(((xx/z+clip[0])*axs+bxs)*2).astype(np.float32),(((yy/z+clip[1])*ays+bys)*2).astype(np.float32),cv2.INTER_NEAREST,borderValue=0)
        foot=cv2.erode(foot,np.ones((25,25),np.uint8))
    else:
        big=cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((121,121),np.uint8)); cs,_=cv2.findContours(big,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        foot=np.zeros_like(k); cv2.drawContours(foot,[c for c in cs if cv2.contourArea(c)>200000],-1,1,-1)
    free=((br==0)&(foot>0)).astype(np.uint8)
    nl,lab,st,cen=cv2.connectedComponentsWithStats(free,connectivity=4)
    # tiling raster for fallback
    g1=gridref(n); g2=gridref(tn)
    ax=(g2[1]-g2[0])/(g1[1]-g1[0]); bx=g2[0]-ax*g1[0]; ay=(g2[3]-g2[2])/(g1[3]-g1[2]); by=g2[2]-ay*g1[2]
    tz=150/72; tp=d[tn-1].get_pixmap(dpi=150,alpha=False); ta=np.frombuffer(tp.samples,np.uint8).reshape(tp.height,tp.width,3).astype(int)
    tsat=(ta.max(2)-ta.min(2))>25
    seeds=[]
    for w in d[n-1].get_text('words'):
        c=kwclass(w[4])
        if not c: continue
        px=int(((w[0]+w[2])/2-clip[0])*z); py=int(((w[1]+w[3])/2-clip[1])*z)
        if 0<=px<W and 0<=py<H: seeds.append((px,py,c,w[4]))
    res=collections.defaultdict(float); rooms=[]
    cmap=np.full((H,W),-1,int); CN=[c for c,_ in KW]+['fallback']
    for i in range(1,nl):
        x,y,w_,h_=st[i,:4]; A=st[i,4]*mmpx*mmpx/1e6
        if A<0.5: continue
        m=(lab[y:y+h_,x:x+w_]==i)
        ss=[s for s in seeds if x<=s[0]<x+w_ and y<=s[1]<y+h_ and m[s[1]-y,s[0]-x]]
        if ss:
            ry,rx=np.nonzero(m)
            P=np.array([(s[0]-x,s[1]-y) for s in ss],float)
            dd=((rx[:,None]-P[None,:,0])**2+(ry[:,None]-P[None,:,1])**2).argmin(1)
            for j,s in enumerate(ss):
                a=(dd==j).sum()*mmpx*mmpx/1e6; res[s[2]]+=a
                cmap[ry[dd==j]+y,rx[dd==j]+x]=CN.index(s[2])
            rooms.append(dict(area=A,names=' '.join(s[3] for s in ss)))
        else:
            ys,xs=np.nonzero(m); ys=ys+y; xs=xs+x
            sel=np.random.RandomState(0).choice(len(xs),min(3000,len(xs)),replace=False)
            tx=(((xs[sel]/z+clip[0])*ax+bx)*tz).astype(int); ty=(((ys[sel]/z+clip[1])*ay+by)*tz).astype(int)
            ok=(tx>=0)&(ty>=0)&(tx<ta.shape[1])&(ty<ta.shape[0]); tx,ty=tx[ok],ty[ok]
            s=tsat[ty,tx]; cp=ta[ty[s],tx[s]]; cp=cp[~((cp[:,0]>200)&(cp[:,2]>200)&(cp[:,1]<90))] if len(cp) else cp
            c0=classify(cp,len(s))
            c={'40x40 non-slip porcelain':KW[0][0],'50x50 matte porcelain R11':KW[1][0],'60x120 semi-polished porcelain':KW[2][0],
               '60x60 non-slip porcelain R11':KW[3][0],'60x60 semi-polished porcelain':KW[5][0],'grey: interlocking/PU':'interlocking/PU (unlabelled grey)',
               'grass/landscape':'landscape (grass)','untiled':'no finish (lifts/voids/shafts)'}[c0]
            if A<1.2 and c==KW[6][0]: pass
            res[c]+=A; cmap[ys,xs]=CN.index(c) if c in CN else len(CN)-1
            rooms.append(dict(area=A,names='(unlabelled:%s)'%c0))
    if save:
        cols=[(200,120,120),(200,200,120),(140,200,140),(120,120,230),(170,170,170),(200,170,240),(235,235,235),(90,90,90)]
        v=np.full((H,W,3),255,np.uint8); v[br>0]=0
        for j,c in enumerate(cols): v[cmap==j]=c
        for s in seeds: cv2.circle(v,(s[0],s[1]),6,(0,0,0),-1)
        cv2.imwrite(save,cv2.resize(v,(W//3,H//3),interpolation=cv2.INTER_AREA))
    return dict(res),rooms
if __name__=='__main__':
    n,tn=int(sys.argv[1]),int(sys.argv[2]); sn=int(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3]!='0' else None
    r,rm=run(n,tn,sn,save='f3_%d.png'%n)
    print(n,{k:round(v,1) for k,v in sorted(r.items())},'total',round(sum(r.values()),1))
