from walls import wallband
import cv2,numpy as np,json
import sys
plans={7:'GF',9:'1F',11:'2F',13:'MEZZ',15:'3F',17:'4F',18:'5F',19:'6F',20:'7F',21:'8F',23:'9F',25:'10F',27:'RT',29:'ROOF'}
sel=[int(x) for x in sys.argv[1:]]
old=json.load(open('walls.json')) if sel else {}
out=old
for n,f in plans.items():
    if sel and n not in sel: continue
    L,k,sk,m,t=wallband(n,save='wb%d.png'%n)
    dt=cv2.distanceTransform(k,cv2.DIST_L2,3); th=2*dt[sk]*m
    px=m/1000*1.06
    r={'w150':float((th<=210).sum()*px),'w200':float(((th>210)&(th<=245)).sum()*px),'rc':float((th>245).sum()*px)}
    out[f]=r; print(f,{k:round(v,1) for k,v in r.items()},flush=True)
json.dump(out,open('walls.json','w'),indent=1)
