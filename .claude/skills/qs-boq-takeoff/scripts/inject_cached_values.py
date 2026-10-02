#!/usr/bin/env python3
"""Write cached values (from recalc_check.py -> vals.pkl) into formula cells of an xlsx built with
openpyxl, so viewers that do not recalculate (previews, phone apps, openpyxl data_only) show numbers.
usage: inject_cached_values.py BOOK.xlsx   (run recalc_check.py BOOK.xlsx first, same folder)"""
import zipfile, re, pickle, shutil, sys
src=sys.argv[1]; v=pickle.load(open('vals.pkl','rb'))
book=re.search(r"\[(.*?)\]",next(iter(v))).group(1)
z=zipfile.ZipFile(src)
wbx=z.read('xl/workbook.xml').decode(); rels=z.read('xl/_rels/workbook.xml.rels').decode()
rid2t={m.group(1):m.group(2) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="/?(?:xl/)?([^"]+)"',rels)}
rid2t.update({m.group(2):m.group(1) for m in re.finditer(r'Target="/?(?:xl/)?([^"]+)"[^>]*Id="(rId\d+)"',rels)})
f2name={}
for m in re.finditer(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"',wbx):
    f2name['xl/'+rid2t[m.group(2)]]=m.group(1).replace('&amp;','&')
out=src+'.tmp'; zo=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED); n=0
for it in z.infolist():
    data=z.read(it.filename)
    if it.filename in f2name:
        nm=f2name[it.filename].upper()
        x=data.decode()
        def rep(m):
            global n
            ref=m.group(1); key="'[%s]%s'!%s"%(book,nm,ref)
            val=v.get(key)
            if val is None: return m.group(0)
            n+=1
            if isinstance(val,float): return '<c r="%s"%s><f>%s</f><v>%r</v></c>'%(ref,m.group(2),m.group(3),val)
            return '<c r="%s"%s t="str"><f>%s</f><v>%s</v></c>'%(ref,m.group(2),m.group(3),val.replace('&','&amp;').replace('<','&lt;'))
        x=re.sub(r'<c r="([A-Z]+\d+)"([^>]*)><f>(.*?)</f><v\s*/?>(?:</v>)?</c>|<c r="([A-Z]+\d+)"([^>]*)><f>(.*?)</f></c>',
                 lambda m: rep(m) if m.group(1) else rep(type('M',(),{'group':lambda s,i:[None,m.group(4),m.group(5),m.group(6)][i]})()),x)
        data=x.encode()
    zo.writestr(it,data)
zo.close(); shutil.move(out,src); print('injected',n)
