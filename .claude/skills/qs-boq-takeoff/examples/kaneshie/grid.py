import pymupdf,collections,re
d=pymupdf.open('docs/Documents.pdf')
def dec(s): return ''.join(chr(ord(c)-0xF000) if 0xF000<=ord(c)<0xF100 else c for c in s)
def gridpos(n):
    """x of grid labels 1..12 (top row) and y of A1..Q (left column) from bubble text"""
    p=d[n-1]; ws=p.get_text('words')
    X=collections.defaultdict(list); Y=collections.defaultdict(list)
    for w in ws:
        t=dec(w[4]); cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
        if t in ('1','12','2','6'): X[t].append((cx,cy))
        if t in ('A1','Q','A','E'): Y[t].append((cx,cy))
    return X,Y
if __name__=='__main__':
    import sys
    for n in map(int,sys.argv[1:]):
        X,Y=gridpos(n); print(n,{k:sorted(set((round(a),round(b)) for a,b in v)) for k,v in X.items()},{k:sorted(set((round(a),round(b)) for a,b in v)) for k,v in Y.items()})
