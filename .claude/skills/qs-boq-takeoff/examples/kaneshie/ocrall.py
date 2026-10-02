import pymupdf, json, sys
from rapidocr_onnxruntime import RapidOCR
eng=RapidOCR()
d=pymupdf.open('docs/Documents.pdf')
DPI=230; T=1500; OV=200
out={}
pages=[int(x) for x in sys.argv[1:]]
import os
for n in pages:
    if os.path.exists('ocrp_%d.json'%n): continue
    p=d[n-1]; s=DPI/72
    W,H=p.rect.x1*s,p.rect.y1*s
    toks=[]
    y=0
    while y<H:
        x=0
        while x<W:
            c=pymupdf.Rect(x/s,y/s,min(W,x+T+OV)/s,min(H,y+T+OV)/s)
            pix=p.get_pixmap(dpi=DPI,clip=c); pix.save('tile_%s.png'%sys.argv[1])
            res,_=eng('tile_%s.png'%sys.argv[1])
            for b,t,sc in (res or []):
                cx=(b[0][0]+b[2][0])/2+x; cy=(b[0][1]+b[2][1])/2+y
                h=abs(b[2][1]-b[0][1])
                toks.append((cx,cy,b[0][0]+x,b[2][0]+x,h,t,float(sc)))
            x+=T
        y+=T
    # dedupe
    ded=[]
    for t in sorted(toks,key=lambda t:-t[6]):
        if any(abs(t[0]-u[0])<15 and abs(t[1]-u[1])<8 for u in ded): continue
        ded.append(t)
    out[n]=ded
    json.dump(ded,open('ocrp_%d.json'%n,'w'))
    print(n,len(ded),file=sys.stderr)
json.dump(out,open('ocr_%s.json'%sys.argv[1],'w'))
