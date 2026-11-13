import sys, re, json, xml.etree.ElementTree as ET
from collections import defaultdict

html = open(sys.argv[1], encoding='utf-8').read()
html = re.sub(r'<!DOCTYPE[^>]*>', '', html).replace('xmlns="http://www.w3.org/1999/xhtml"', '')
root = ET.fromstring(html)
words = []
for w in root.iter('word'):
    t = (w.text or '').strip()
    if t:
        words.append({'x0': float(w.get('xMin')), 'x1': float(w.get('xMax')),
                      'y0': float(w.get('yMin')), 'y1': float(w.get('yMax')), 't': t})

BOUNDS = [0, 145, 260, 330, 378, 415, 460, 9999]
NAMES  = ['project', 'deliverable', 'due', 'planned', 'actual', 'owner', 'remark']
def col(w):
    cx = (w['x0'] + w['x1']) / 2
    for i in range(len(NAMES)):
        if BOUNDS[i] <= cx < BOUNDS[i+1]:
            return NAMES[i]

body = [w for w in words if w['y0'] > 125 and w['t'] != '1']
cells = defaultdict(list)
for w in body:
    c = col(w)
    if c: cells[c].append(w)

def blocks(ws, gap=6.0):
    ws = sorted(ws, key=lambda w: (round(w['y0'], 1), w['x0']))
    out, cur = [], []
    for w in ws:
        if cur and w['y0'] - cur[-1]['y1'] > gap:
            out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    res = []
    for b in out:
        lines = defaultdict(list)
        for w in b:
            lines[round(w['y0'], 1)].append(w)
        txt = ' '.join(' '.join(x['t'] for x in sorted(lines[k], key=lambda w: w['x0']))
                       for k in sorted(lines))
        res.append({'t': re.sub(r'\s+', ' ', txt).strip(),
                    'c': (min(w['y0'] for w in b) + max(w['y1'] for w in b)) / 2,
                    'y0': min(w['y0'] for w in b), 'y1': max(w['y1'] for w in b)})
    return res

rows = blocks(cells['deliverable'])
R = [r['c'] for r in rows]
M = len(R)

def tile(label_blocks):
    """Assign each row to a label block. A merged cell's text sits at the centre
    of its span, so recover the boundaries that best explain the observed centres
    rather than assigning each row to its nearest label."""
    C = [b['c'] for b in label_blocks]
    N = len(C)
    INF = float('inf')
    best = [[INF]*(N+1) for _ in range(M+1)]
    back = [[None]*(N+1) for _ in range(M+1)]
    best[0][0] = 0.0
    for i in range(1, N+1):
        for e in range(i, M - (N - i) + 1):
            for s in range(i-1, e):
                if best[s][i-1] == INF: continue
                cost = best[s][i-1] + ((R[s] + R[e-1])/2 - C[i-1])**2
                if cost < best[e][i]:
                    best[e][i] = cost; back[e][i] = s
    span, e = [None]*M, M
    for i in range(N, 0, -1):
        s = back[e][i]
        for k in range(s, e): span[k] = i-1
        e = s
    return span

proj_b, own_b = blocks(cells['project']), blocks(cells['owner'], gap=2.0)
pspan, ospan = tile(proj_b), tile(own_b)

pcts = blocks(cells['planned']), blocks(cells['actual'])
dues = blocks(cells['due'])
rem_b = blocks(cells['remark'], gap=10.0)

def nearest(bs, y):
    return min(bs, key=lambda b: abs(b['c'] - y)) if bs else None

out = []
for i, r in enumerate(rows):
    p = nearest(pcts[0], r['c']); a = nearest(pcts[1], r['c']); d = nearest(dues, r['c'])
    rem = ''
    for b in rem_b:
        # a remark merged over several rows is centred on that span, and in this
        # register those merges line up with the owner merges -- so borrow the span
        lo = min(k for k in range(M) if ospan[k] == ospan[i])
        hi = max(k for k in range(M) if ospan[k] == ospan[i])
        if abs((R[lo] + R[hi]) / 2 - b['c']) < 4:
            rem = b['t']
    out.append({
        'project': proj_b[pspan[i]]['t'],
        'deliverable': r['t'],
        'due': d['t'] if d and abs(d['c']-r['c']) < 10 else '',
        'planned': int(p['t'].rstrip('%'))/100 if p and abs(p['c']-r['c']) < 10 else None,
        'actual':  int(a['t'].rstrip('%'))/100 if a and abs(a['c']-r['c']) < 10 else None,
        'owners': own_b[ospan[i]]['t'].split(),
        'remark': rem,
    })

print(f"{M} deliverable rows, {len(proj_b)} projects, {len(own_b)} owner blocks, {len(rem_b)} remark blocks\n")
for i, x in enumerate(out, 1):
    print(f"{i:2d}. {x['project'][:30]:30s} | {x['deliverable'][:38]:38s} | {x['due']:10s} | "
          f"P{(x['planned'] or 0)*100:4.0f}% A{(x['actual'] or 0)*100:4.0f}% | {'/'.join(x['owners']):22s} | {x['remark'][:40]}")
json.dump(out, open('rows.json','w'), indent=1)
