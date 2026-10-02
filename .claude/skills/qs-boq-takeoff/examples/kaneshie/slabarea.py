import pymupdf,numpy as np,cv2,sys
from grid import gridpos
d=pymupdf.open('docs/Documents.pdf')
Z=4
def calib(n):
    X,Y=gridpos(n)
    top=lambda k: min(v[1] for v in X[k])
    x1=[v[0] for v in X['1'] if abs(v[1]-top('1'))<2][0]; x12=[v[0] for v in X['12'] if abs(v[1]-top('12'))<2][0]
    left=min(v[0] for v in Y['A1']); ya1=[v[1] for v in Y['A1'] if abs(v[0]-left)<2][0]; yq=[v[1] for v in Y['Q'] if abs(v[0]-left)<2][0]
    return (36500/(x12-x1)), (34350/(yq-ya1)), (x1,x12,ya1,yq)
def area(n,margin_mm=3500,save=None,grey=None):
    sx,sy,(x1,x12,ya1,yq)=calib(n)
    p=d[n-1]; pix=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),alpha=False)
    a=np.frombuffer(pix.samples,np.uint8).reshape(pix.height,pix.width,3)
    g=a.mean(axis=2)
    m=((g<250) if grey is None else (np.abs(g-grey)<4)).astype(np.uint8)
    # crop to grid box + margin
    mx=margin_mm/sx; my=margin_mm/sy
    X0,X1,Y0,Y1=[int(v*Z) for v in (x1-mx,x12+mx,ya1-my,yq+my)]
    c=np.zeros_like(m); c[Y0:Y1,X0:X1]=m[Y0:Y1,X0:X1]
    k=np.ones((5,5),np.uint8)
    c=cv2.morphologyEx(c,cv2.MORPH_OPEN,k)
    c=cv2.morphologyEx(c,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    nlab,lab,st,_=cv2.connectedComponentsWithStats(c)
    keep=np.zeros_like(c)
    for i in range(1,nlab):
        if st[i,4]>20000: keep[lab==i]=1
    mm2=(sx/Z)*(sy/Z)
    if save: cv2.imwrite(save,(255-keep*200).astype(np.uint8)[::2,::2])
    return keep.sum()*mm2/1e6,(sx,sy)
if __name__=='__main__':
    for n in map(int,sys.argv[1:]):
        A,s=area(n,save='sl_%d.png'%n); print(n,round(A,1),'m2 scale mm/pt',[round(x,2) for x in s])
