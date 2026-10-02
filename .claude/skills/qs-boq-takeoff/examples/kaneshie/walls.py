import pymupdf,os,numpy as np,cv2,sys
from arcs import scale
d=pymupdf.open('arch/'+os.listdir('arch')[0])
DPI=300
def render(n,clip=(60,90,1000,800)):
    p=d[n-1]; pix=p.get_pixmap(dpi=DPI,clip=pymupdf.Rect(*clip),alpha=False)
    a=np.frombuffer(pix.samples,np.uint8).reshape(pix.height,pix.width,3).astype(int)
    return a
def blackmask(a):
    mx=a.max(2); mn=a.min(2)
    return ((mx<110)&(mx-mn<40)).astype(np.uint8)
if __name__=='__main__':
    n=int(sys.argv[1]); s=scale(n); mmpx=s*72/DPI
    a=render(n); b=blackmask(a)
    cv2.imwrite('bk%d.png'%n,(255-b*255).astype(np.uint8))
    print('mm per px',mmpx, b.shape)

from skimage.morphology import skeletonize
MASKS={7:[(285,255,538,382),(255,578,552,652)]}
def wallband(n,clip=(60,90,1000,800),close=13,open_=7,save=None,maxhalf=9):
    a=render(n,clip); b=blackmask(a)
    z0=DPI/72
    for (x0,y0,x1,y1) in MASKS.get(n,[]): b[int((y0-clip[1])*z0):int((y1-clip[1])*z0),int((x0-clip[0])*z0):int((x1-clip[0])*z0)]=0
    p=d[n-1]; z=DPI/72
    for w in p.get_text('words'):
        if (w[2]-w[0])>60 or (w[3]-w[1])>60: continue
        if w[2]<clip[0] or w[0]>clip[2] or w[3]<clip[1] or w[1]>clip[3]: continue
        x0,y0,x1,y1=[(w[0]-clip[0])*z,(w[1]-clip[1])*z,(w[2]-clip[0])*z,(w[3]-clip[1])*z]
        b[max(0,int(y0)-1):int(y1)+2,max(0,int(x0)-1):int(x1)+2]=0
    c=cv2.morphologyEx(b,cv2.MORPH_CLOSE,np.ones((close,close),np.uint8))
    c=cv2.morphologyEx(c,cv2.MORPH_CLOSE,np.ones((1,15),np.uint8)); c=cv2.morphologyEx(c,cv2.MORPH_CLOSE,np.ones((15,1),np.uint8))
    o=cv2.morphologyEx(c,cv2.MORPH_OPEN,np.ones((open_,open_),np.uint8))
    nl,lab,st,_=cv2.connectedComponentsWithStats(o)
    k=np.zeros_like(o)
    for i in range(1,nl):
        if st[i,4]>400: k[lab==i]=1
    dt=cv2.distanceTransform(k,cv2.DIST_L2,3)
    sk=skeletonize(k.astype(bool)) & (dt<=maxhalf) & (dt>=2.5)
    self_thick=np.median(dt[sk])*2 if sk.any() else 0
    s=scale(n); mmpx=s/z
    L=sk.sum()*mmpx/1000*1.06   # skeleton px count undercounts diagonal/ends slightly
    if save:
        v=np.full(b.shape+(3,),255,np.uint8); v[b>0]=(180,180,180); v[k>0]=(60,60,230); v[sk]=(0,0,0)
        cv2.imwrite(save,v)
    return L,k,sk,mmpx,self_thick*mmpx
