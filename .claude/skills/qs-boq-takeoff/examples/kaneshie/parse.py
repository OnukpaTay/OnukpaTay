import json,re,sys
DPI=230
def norm(t):
    return t.replace('O','0').replace('o','0').replace('S','5').replace('s','5').replace('l','1').replace('I','1').replace('B','8').replace('Z','2').replace('D','0').replace(',','').replace('.','')
def parse(n):
    toks=json.load(open('ocrp_%d.json'%n))
    # split multi-number tokens into pseudo tokens
    T=[]
    for cx,cy,x0,x1,h,t,sc in toks:
        parts=t.split()
        if len(parts)>1:
            w=(x1-x0)/max(1,len(t))
            pos=0
            for p in parts:
                i=t.find(p,pos); pos=i+len(p)
                T.append(((x0+w*(i+len(p)/2)),cy,x0+w*i,x0+w*(i+len(p)),h,p,sc))
        else: T.append((cx,cy,x0,x1,h,t,sc))
    marks=[]
    for tk in T:
        s=norm(tk[5])
        if re.fullmatch(r'(10|12|16|20|25|32)\d{2}[A-Z]?',s) or re.fullmatch(r'Y?(10|12|16|20|25|32)\d{2}',s):
            marks.append(tk)
    rows=[]
    for m in marks:
        mx,my,mx0,mx1,mh=m[0],m[1],m[2],m[3],m[4]
        cand=[t for t in T if t is not m and abs(t[1]-my)<max(12,mh*0.7) and mx1-5<t[2] and t[0]<mx1+260]
        cand.sort()
        vals=[norm(t[5]) for t in cand]
        nums=[v for v in vals if re.fullmatch(r'\d+',v)]
        mk=norm(m[5]).lstrip('Y')
        nums=nums[:3]
        for i in (1,2):
            if len(nums)==3 and nums[i].startswith('0'):
                nums[i]=nums[i][::-1].translate(str.maketrans('69','96'))
        rows.append(dict(mark=mk,y=round(my),x=round(mx),raw=[t[5] for t in cand],nums=nums[:3]))
    # drop marks that are just inside another row's numbers (e.g. lengths like 1200)
    rows.sort(key=lambda r:(r['x']//150,r['y']))
    return rows
if __name__=='__main__':
    for r in parse(int(sys.argv[1])): print(r['mark'],r['x'],r['y'],r['nums'],r['raw'])
