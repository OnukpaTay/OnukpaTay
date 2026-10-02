import pymupdf,os,re,collections,math
d=pymupdf.open('arch/'+os.listdir('arch')[0])
def scale(n):
    # grid 1->12 = 36500 using top bubble labels
    ws=d[n-1].get_text('words')
    xs={w[4]:[] for w in ws}
    for w in ws:
        if w[4] in('1','12') and w[1]<200: xs[w[4]].append((w[0]+w[2])/2)
    return 36500/(min(xs['12'])-min(xs['1'])) if xs.get('1') and xs.get('12') else None
def arcs(n):
    p=d[n-1]; s=scale(n); out=[]
    for dr in p.get_drawings():
        for it in dr['items']:
            if it[0]=='c':
                a,c1,c2,b=it[1:5]
                chord=math.hypot(a.x-b.x,a.y-b.y)
                # quarter-circle bezier: radius = chord/sqrt2
                out.append((round(chord/math.sqrt(2)*s/50)*50, dr.get('color'), round(dr.get('width') or 0,2)))
    return out,s
if __name__=='__main__':
    import sys
    for n in map(int,sys.argv[1:]):
        o,s=arcs(n); print(n,'mm/pt',round(s,2) if s else s, sorted(collections.Counter((r) for r,c,w in o if 500<=r<=2000).items()))
