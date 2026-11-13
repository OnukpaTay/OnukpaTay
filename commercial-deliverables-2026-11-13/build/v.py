import sys, json, datetime, re
sys.path.insert(0, '/home/user/OnukpaTay/skill/commercial-status-deck/scripts')
from read_register import load
rows, df, sheet = load(sys.argv[1])
n=len(rows); sp=sum(r['planned'] for r in rows); sa=sum(r['actual'] for r in rows)
print(f"\nrows {n}  planned {sp:g} ({sp/n*100:.2f}%)  actual {sa:g} ({sa/n*100:.2f}%)  variance {(sa-sp)/n*100:.2f} pts = {sa-sp:+.2f} items")

# duplicate detection
seen={}
dups=[]
for r in rows:
    k=(r['project'].lower().strip(), r['deliverable'].lower().strip(), str(r['due']), r['planned'], r['actual'])
    if k in seen: dups.append((seen[k], r))
    else: seen[k]=r
print(f"\nEXACT DUPLICATE ROWS: {len(dups)}")
for a,b in dups:
    print(f"  rows {a['row']} and {b['row']}: {a['project']} / {a['deliverable']} / {a['due']} / P{a['planned']} A{a['actual']}")

behind=[r for r in rows if r['actual']<r['planned']-1e-9]
gap=sum(r['planned']-r['actual'] for r in behind)
print(f"\nbehind-plan rows {len(behind)}, gap total {gap:.2f}  -> matches column totals: {abs(gap-(sp-sa))<1e-9}")
print("  " + "\n  ".join(f"{r['project'][:30]:30s} {r['deliverable'][:34]:34s} P{r['planned']*100:4.0f}% A{r['actual']*100:4.0f}% gap {r['planned']-r['actual']:.2f} due {r['due']} {'/'.join(r['owners'])}" for r in behind))
onplan=[r for r in rows if r['actual']<1 and abs(r['actual']-r['planned'])<1e-9]
print(f"\nincomplete but 'on plan' {len(onplan)}")
for r in onplan:
    print(f"  {r['project'][:30]:30s} {r['deliverable'][:34]:34s} P{r['planned']*100:4.0f}% A{r['actual']*100:4.0f}% due {r['due']}")
print(f"\ndelivered {sum(1 for r in rows if r['actual']>=1)}   check {sum(1 for r in rows if r['actual']>=1)}+{len(onplan)}+{len(behind)} = {sum(1 for r in rows if r['actual']>=1)+len(onplan)+len(behind)} == {n}")
import collections
dd=collections.Counter(str(r['due']) for r in rows)
print("\ndue dates:", dict(dd))
print("\nincomplete items and their due dates:")
for r in rows:
    if r['actual']<1: print(f"  {r['due']}  {r['project'][:28]:28s} {r['deliverable'][:36]:36s} A{r['actual']*100:4.0f}%")
json.dump([{k:(str(v) if isinstance(v,(datetime.date,datetime.datetime)) else v) for k,v in r.items()} for r in rows], open('rows13.json','w'), indent=1)
