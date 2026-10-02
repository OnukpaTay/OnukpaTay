import pymupdf,json,sys,re
from PIL import Image,ImageDraw,ImageFont
from parse import parse,DPI
d=pymupdf.open('docs/Documents.pdf')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22) if __import__('os').path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
def good(r):
    return len(r['nums'])>=3 and r['nums'][0]==r['mark'][:2]
def make(n):
    rows=[r for r in parse(n) if good(r)]
    json.dump(rows,open('rows_%d.json'%n,'w'))
    # group by column x
    cols={}
    for r in rows: cols.setdefault(round(r['x']/100),[]).append(r)
    outs=[]
    p=d[n-1]
    for k,rs in sorted(cols.items()):
        x0=min(r['x'] for r in rs)-60; y0=max(0,min(r['y'] for r in rs)-250); y1=max(r['y'] for r in rs)+250
        s=72/DPI
        pix=p.get_pixmap(dpi=DPI,clip=pymupdf.Rect(x0*s,y0*s,(x0+390)*s,y1*s))
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        canvas=Image.new('RGB',(im.width+330,im.height),'white'); canvas.paste(im,(0,0))
        dr=ImageDraw.Draw(canvas)
        for r in rs:
            dr.text((im.width+5,r['y']-y0-12),'%s %s %s %s'%(r['mark'],*r['nums'][:3]),fill='red',font=F)
        outs.append(canvas)
    if not outs: return None
    W=sum(o.width for o in outs); H=max(o.height for o in outs)
    big=Image.new('RGB',(W,H),'white'); x=0
    for o in outs: big.paste(o,(x,0)); x+=o.width
    fn='ov/ov_%d.png'%n; big.save(fn); return fn,len(rows)
if __name__=='__main__':
    for n in map(int,sys.argv[1:]): print(make(n))
