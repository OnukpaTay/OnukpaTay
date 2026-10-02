import json
from rooms3 import run
M=[('GF',7,43,None),('1F',9,44,47),('2F',11,45,59),('MEZZ',13,46,65),('3F',15,47,71),('4F',17,48,77),('5F',18,48,77),('6F',19,48,77),('7F',20,48,77),('8F',21,48,77),('9F',23,49,84),('10F',25,50,92),('RT',27,51,98)]
out={}
for f,n,tn,sn in M:
    r,rm=run(n,tn,sn,save='f3_%d.png'%n); out[f]={'res':r,'rooms':rm}
    print(f,{k[:22]:round(v,1) for k,v in sorted(r.items())},'total',round(sum(r.values()),1),flush=True)
json.dump(out,open('finishes.json','w'),indent=1,default=float)
