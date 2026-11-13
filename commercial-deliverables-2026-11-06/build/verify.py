import json, re, subprocess, sys
from collections import OrderedDict
rows = json.load(open('rows.json'))

# ---- route 1: computed from the structured extraction -------------------
n = len(rows)
sp = sum(r['planned'] for r in rows); sa = sum(r['actual'] for r in rows)
done   = [r for r in rows if r['actual'] >= 1]
onplan = [r for r in rows if r['actual'] < 1 and abs(r['actual'] - r['planned']) < 1e-9]
behind = [r for r in rows if r['actual'] < r['planned'] - 1e-9]
print(f"rows                 {n}")
print(f"projects             {len(OrderedDict((r['project'],1) for r in rows))}")
print(f"delivered            {len(done)}   {len(done)}/{n} = {len(done)/n*100:.1f}%")
print(f"incomplete, on plan  {len(onplan)}   {len(onplan)/n*100:.1f}%")
print(f"behind plan          {len(behind)}   {len(behind)/n*100:.1f}%")
print(f"check 16+2+2         {len(done)+len(onplan)+len(behind)} == {n}  -> {len(done)+len(onplan)+len(behind)==n}")
print(f"planned sum          {' + '.join(f'{r[chr(112)+chr(108)+chr(97)+chr(110)+chr(110)+chr(101)+chr(100)]:g}' for r in rows)} = {sp:g}")
print(f"actual  sum          {sa:g}")
print(f"planned pct          {sp}/{n} = {sp/n*100:.2f}%")
print(f"actual  pct          {sa}/{n} = {sa/n*100:.2f}%")
print(f"variance             {sa/n*100:.2f} - {sp/n*100:.2f} = {(sa-sp)/n*100:.2f} points")
print(f"variance in items    {sa:g} - {sp:g} = {sa-sp:.1f} deliverables")
gap = sum(r['planned']-r['actual'] for r in behind)
print(f"gap from behind rows {' + '.join(f'{r[chr(112)+chr(108)+chr(97)+chr(110)+chr(110)+chr(101)+chr(100)]-r[chr(97)+chr(99)+chr(116)+chr(117)+chr(97)+chr(108)]:.1f}' for r in behind)} = {gap:.1f}  -> matches: {abs(gap-(sp-sa))<1e-9}")

print("\nBEHIND PLAN")
for r in behind:
    print(f"  {r['project'][:34]:34s} {r['deliverable'][:40]:40s} P{r['planned']*100:4.0f}% A{r['actual']*100:4.0f}% due {r['due']} {'/'.join(r['owners'])}")
print("INCOMPLETE BUT ON PLAN")
for r in onplan:
    print(f"  {r['project'][:34]:34s} {r['deliverable'][:40]:40s} P{r['planned']*100:4.0f}% A{r['actual']*100:4.0f}% due {r['due']} {'/'.join(r['owners'])}")

byp = OrderedDict()
for r in rows:
    d = byp.setdefault(r['project'], {'n':0,'p':0.0,'a':0.0,'done':0})
    d['n']+=1; d['p']+=r['planned']; d['a']+=r['actual']
    if r['actual']>=1: d['done']+=1
print(f"\nBY PROJECT  ({sum(1 for v in byp.values() if v['a']==v['n'])} of {len(byp)} fully delivered)")
for k,v in byp.items():
    print(f"  {'OK ' if v['a']==v['n'] else '** '}{k[:34]:34s} n={v['n']} planned {v['p']/v['n']*100:5.1f}% actual {v['a']/v['n']*100:5.1f}% delivered {v['done']}")
print(f"  sum of project n = {sum(v['n'] for v in byp.values())} == {n} -> {sum(v['n'] for v in byp.values())==n}")
print(f"  sum of delivered = {sum(v['done'] for v in byp.values())} == {len(done)} -> {sum(v['done'] for v in byp.values())==len(done)}")

byo = {}
for r in rows:
    for o in r['owners']:
        d = byo.setdefault(o, {'n':0,'d':0,'open':[]})
        d['n']+=1
        if r['actual']>=1: d['d']+=1
        else: d['open'].append(f"{r['project'][:18]}/{r['deliverable'][:22]}")
print("\nBY OWNER")
for k,v in sorted(byo.items(), key=lambda t:-t[1]['n']):
    print(f"  {k:8s} total {v['n']:2d}  delivered {v['d']:2d}  open {v['n']-v['d']:2d}   {'; '.join(v['open'])}")
print(f"  sum of owner totals = {sum(v['n'] for v in byo.values())}  (vs {n} deliverables; shared items counted per owner)")
print(f"  sum of owner open   = {sum(v['n']-v['d'] for v in byo.values())}  (vs {len(onplan)+len(behind)} incomplete rows; shared counted per owner)")

print("\nREMARKS")
rem = {}
for r in rows:
    if r['remark']: rem.setdefault(r['remark'], []).append(r)
for t, items in rem.items():
    print(f"  [{len(items)}] {t[:76]}")
    for r in items: print(f"        {r['project'][:30]:30s} {r['deliverable'][:34]}")

print("\nDUE DATES")
dd = {}
for r in rows: dd.setdefault(r['due'], []).append(r)
for d, items in sorted(dd.items()):
    print(f"  {d}: {len(items)} item(s)  incomplete: {sum(1 for r in items if r['actual']<1)}")
