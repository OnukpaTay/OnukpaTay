import openpyxl, datetime
from collections import OrderedDict

def load(path, sheet=None):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    rows=[]; proj=owner=rem=None
    r=5
    while r <= ws.max_row:
        b = ws.cell(r,2).value
        if b in (None,""): break
        p = ws.cell(r,1).value or proj; proj=p
        o = ws.cell(r,6).value or owner; owner=o
        g = ws.cell(r,7).value or rem;   rem=g
        rows.append({'row':r,'project':str(p).strip(),'deliv':str(b).strip(),
                     'due':ws.cell(r,3).value,
                     'p':float(ws.cell(r,4).value or 0),'a':float(ws.cell(r,5).value or 0),
                     'own':[x.strip() for x in str(o or '').split('\n') if x.strip()],
                     'rem':str(g or '').strip()})
        r+=1
    return rows

def summarise(rows, label):
    n=len(rows); sp=sum(x['p'] for x in rows); sa=sum(x['a'] for x in rows)
    done=[x for x in rows if x['a']>=1]; prog=[x for x in rows if 0<x['a']<1]; ns=[x for x in rows if x['a']==0]
    print(f"\n===== {label} =====")
    print(f"deliverables {n}   projects {len(set(x['project'] for x in rows))}")
    print(f"delivered {len(done)} ({len(done)/n*100:.1f}%)  in-progress {len(prog)} ({len(prog)/n*100:.1f}%)  not-started {len(ns)} ({len(ns)/n*100:.1f}%)")
    print(f"actual {sa}/{n} = {sa/n*100:.2f}%   planned {sp}/{n} = {sp/n*100:.2f}%   gap {(sp-sa)/n*100:.2f} pts = {sp-sa:.1f} deliverables")
    return rows

w1 = summarise(load('source_v2.xlsx','18-09-2025'), "WEEK 1  18 Sep 2026")
w2 = summarise(load('source_w2.xlsx'), "WEEK 2  25 Sep 2026")

print("\n--- WEEK 2 rows ---")
for x in w2:
    d = x['due']
    ds = d.strftime('%d %b %Y') if isinstance(d,datetime.datetime) else str(d)
    print(f"  {x['project']:28s} | {x['deliv']:28s} | {ds:12s} | P{x['p']*100:4.0f}% A{x['a']*100:4.0f}% | {'/'.join(x['own']):22s} | {x['rem']}")

print("\n--- WEEK 2 by project ---")
byp=OrderedDict()
for x in w2:
    d=byp.setdefault(x['project'],{'n':0,'p':0.0,'a':0.0,'own':set()})
    d['n']+=1; d['p']+=x['p']; d['a']+=x['a']; d['own'].update(x['own'])
for k,v in byp.items():
    print(f"  {k:28s} n={v['n']} planned {v['p']/v['n']*100:5.1f}%  actual {v['a']/v['n']*100:5.1f}%  {','.join(sorted(v['own']))}")
print(f"  fully delivered projects: {sum(1 for v in byp.values() if v['a']==v['n'])} / {len(byp)}")

print("\n--- WEEK 2 owners (shared counted per person) ---")
byo={}
for x in w2:
    for o in x['own']:
        d=byo.setdefault(o,{'n':0,'d':0}); d['n']+=1
        if x['a']>=1: d['d']+=1
for k,v in sorted(byo.items(), key=lambda t:-t[1]['n']):
    print(f"  {k:8s} total {v['n']}  delivered {v['d']}  outstanding {v['n']-v['d']}")
print(f"  sum of owner totals = {sum(v['n'] for v in byo.values())}")

print("\n--- AWAITING REVIEW ---")
ar=[x for x in w2 if 'review' in x['rem'].lower()]
for x in ar: print(f"  {x['project']:28s} {x['deliv']}")
print(f"  {len(ar)} of {len(w2)} deliverables; {len([x for x in ar if x['a']>=1])} of {len([x for x in w2 if x['a']>=1])} delivered items")

print("\n--- CARRY-OVER: week1 -> week2 (same project + deliverable) ---")
k1={(x['project'].lower(),x['deliv'].lower()):x for x in w1}
for x in w2:
    m=k1.get((x['project'].lower(),x['deliv'].lower()))
    if m: print(f"  CARRIED  {x['project']:28s} {x['deliv']:28s} {m['a']*100:5.0f}% -> {x['a']*100:5.0f}%  ({(x['a']-m['a'])*100:+.0f})")
    else: print(f"  NEW      {x['project']:28s} {x['deliv']:28s}   -> {x['a']*100:5.0f}%")
print("\n--- DROPPED from week 1 ---")
k2={(x['project'].lower(),x['deliv'].lower()) for x in w2}
drop=[x for x in w1 if (x['project'].lower(),x['deliv'].lower()) not in k2]
print(f"  {len(drop)} rows dropped")
for x in drop: print(f"     {x['project']:28s} {x['deliv']:34s} was {x['a']*100:.0f}%")
