import tk,re,os,shutil,math,zipfile,openpyxl
from xml.sax.saxutils import escape,quoteattr
SRC='user.xlsx'; OUT='/home/user/OnukpaTay/BOQ_KANESHIE_BLOCK_N_WITH_TAKEOFF.xlsx'
W='ux2'
if os.path.exists(W): shutil.rmtree(W)
os.makedirs(W); zipfile.ZipFile(SRC).extractall(W)
# ---------------- styles ----------------
st=open(W+'/xl/styles.xml',encoding='utf-8',newline='').read()
def addlist(tag,items):
    global st
    m=re.search(r'<%s count="(\d+)"[^>]*>'%tag,st); n=int(m.group(1))
    end=st.index('</%s>'%tag,m.end())
    st=st[:end]+''.join(items)+st[end:]
    st=st[:m.start()]+m.group(0).replace('count="%d"'%n,'count="%d"'%(n+len(items)))+st[m.end():]
    return list(range(n,n+len(items)))
def font(sz=11,b=False,i=False,u=False,color=None):
    return '<font>'+('<b/>' if b else '')+('<i/>' if i else '')+('<u/>' if u else '')+'<sz val="%g"/>'%sz+('<color rgb="%s"/>'%color if color else '<color theme="1"/>')+'<name val="Calibri"/><family val="2"/><scheme val="minor"/></font>'
FN=addlist('fonts',[font(),font(b=True),font(14,b=True,color='FF1F3864'),font(10,i=True,color='FF595959'),font(b=True,color='FFFFFFFF'),
                   font(u=True,color='FF0563C1'),font(9,color='FF7F7F7F'),font(12,b=True,color='FF1F3864'),font(i=True,b=True,color='FF1F3864'),font(11,b=True,color='FF1F3864')])
fill=lambda c:'<fill><patternFill patternType="solid"><fgColor rgb="%s"/><bgColor indexed="64"/></patternFill></fill>'%c
PL=addlist('fills',[fill('FF1F3864'),fill('FFD9E1F2'),fill('FFFFF2CC'),fill('FFF2F2F2')])
thin=lambda c='FF808080':'<left style="thin"><color rgb="%s"/></left><right style="thin"><color rgb="%s"/></right><top style="thin"><color rgb="%s"/></top><bottom style="thin"><color rgb="%s"/></bottom><diagonal/>'%(c,c,c,c)
BD=addlist('borders',['<border>%s</border>'%thin(),'<border><left/><right/><top style="thin"><color auto="1"/></top><bottom style="double"><color auto="1"/></bottom><diagonal/></border>',
                      '<border><left/><right/><top/><bottom style="medium"><color rgb="FF1F3864"/></bottom><diagonal/></border>','<border>%s</border>'%thin('FFBFBFBF')])
m=re.search(r'<numFmts count="(\d+)">',st)
st=st.replace(m.group(0),'<numFmts count="%d">'%(int(m.group(1))+2)).replace('</numFmts>','<numFmt numFmtId="190" formatCode="#,##0.000"/><numFmt numFmtId="191" formatCode="#,##0.###"/></numFmts>')
def xf(f,fill=0,b=0,nf=0,h=None,v='center',wrap=False,ind=0):
    al='<alignment'+(' horizontal="%s"'%h if h else '')+(' vertical="%s"'%v if v else '')+(' wrapText="1"' if wrap else '')+(' indent="%d"'%ind if ind else '')+'/>'
    return '<xf numFmtId="%d" fontId="%d" fillId="%d" borderId="%d" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1">%s</xf>'%(nf,f,fill,b,al)
NAMES=['title','proj','note','hdr','bill','head','itemA','itemD','unit','text','in','nr','qty','totl','totn','totu','calc','link','idx','linkb','sub']
XS=[xf(FN[2],v='center'),xf(FN[9]),xf(FN[3]),xf(FN[4],PL[0],BD[0],h='center',wrap=True),xf(FN[7],PL[1],BD[2]),xf(FN[8],ind=1),
    xf(FN[1],h='center',v='top'),xf(FN[1],wrap=True,v='top'),xf(FN[0],h='center'),xf(FN[0],ind=2),xf(FN[0],PL[2],BD[3],nf=190),
    xf(FN[0],PL[2],BD[3],nf=191,h='center'),xf(FN[0],nf=190),xf(FN[1],PL[3],BD[1],ind=1),xf(FN[1],PL[3],BD[1],nf=190),xf(FN[1],PL[3],BD[1],h='center'),
    xf(FN[6]),xf(FN[5]),xf(FN[0]),xf(FN[5],v='top'),xf(FN[0],PL[3],BD[1])]
S=dict(zip(NAMES,addlist('cellXfs',XS)))
open(W+'/xl/styles.xml','w',encoding='utf-8',newline='').write(st)
# ---------------- values ----------------
def ev(s): return eval(s,{'__builtins__':{}})
isnum=lambda s: re.fullmatch(r'-?\d+(\.\d+)?',s) is not None
HDR=5; IDX0=HDR+1
bills=tk.LINKS['_bills']
OFF=IDX0+len(bills)+2-1    # R index i (1-based) -> sheet row i+OFF
rowof=lambda i:i+OFF
rows=[]  # (rownum, [(col,xml)], ht)
def cs(c,r,text,s): return '<c r="%s%d" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'%(c,r,s,escape(text))
def cn(c,r,v,s): return '<c r="%s%d" s="%d"><v>%r</v></c>'%(c,r,s,v)
def cf(c,r,f,v,s,str_=False):
    if str_: return '<c r="%s%d" s="%d" t="str"><f>%s</f><v>%s</v></c>'%(c,r,s,escape(f),escape(v))
    return '<c r="%s%d" s="%d"><f>%s</f><v>%r</v></c>'%(c,r,s,escape(f),v)
HL=[]
wbv=openpyxl.load_workbook(SRC,data_only=True)['GEN SUMMARY']
rows.append((1,[cf('A',1,"'GEN SUMMARY'!A1",wbv['A1'].value,S['proj'],True)],None))
rows.append((2,[cf('A',2,"'GEN SUMMARY'!A2",wbv['A2'].value,S['proj'],True)],None))
rows.append((3,[cs('A',3,'QUANTITY TAKE-OFF  -  DIMENSION SHEETS (FLOOR BY FLOOR, SUBSTRUCTURE TO 12TH FLOOR)',S['title'])],22))
rows.append((4,[cs('A',4,'Yellow cells are dimensions - edit them here and the QTY column of each bill (and all amounts / summaries) updates. Qty = Times x Dim1 x Dim2 x Dim3 (blank cells count as 1); Ddt lines are negative. Dimensions in metres, reinforcement in tonnes from the reinforcement take-off (BBS).',S['note'])],None))
H=['BILL / FLOOR','ITEM','DESCRIPTION / LOCATION OF DIMENSION','TIMES / NR','LENGTH / DIM 1','WIDTH / DIM 2','HEIGHT / DEPTH / DIM 3','QUANTITY','UNIT','ORIGINAL CALCULATION (FOR REFERENCE)','LINK TO BOQ QTY CELL']
rows.append((HDR,[cs(c,HDR,h,S['hdr']) for c,h in zip('ABCDEFGHIJK',H)],32))
# index
ir=IDX0
rows.append((ir,[cs('A',ir,'BILL INDEX (click to jump)',S['itemD'])],None))
for k,(nm,title,bstart) in enumerate(bills):
    r=ir+1+k
    rows.append((r,[cs('A',r,'   '+title,S['link']),cs('K',r,"Open bill: '%s'"%nm.strip(),S['link'])],None))
    HL.append(('A%d'%r,"TAKEOFF!A%d"%rowof(bstart))); HL.append(('K%d'%r,"'%s'!A1"%nm))
VAL={}
for i,x in enumerate(tk.R,1):
    r=rowof(i); c=x['c']; k=x['kind']; out=[]; ht=None
    if k=='bill':
        out=[cs('A',r,c['A'][0],S['bill'])]+[cs(col,r,'',S['bill']) for col in 'BCDEFGHIJK']; ht=21
    elif k=='head':
        out=[cs('C',r,c['C'][0],S['head'])]
    elif k=='item':
        d=c['C'][0]; ln=max(1,math.ceil(len(d)/78)); ht=15.6*ln+1 if ln>1 else None
        out=[cs('A',r,c['A'][0],S['itemA']),cs('B',r,c['B'][0],S['itemA']),cs('C',r,d,S['itemD']),cs('I',r,c['I'][0],S['unit'])]
        out.append(cs('K',r,c['K'][0][5:],S['linkb'])); HL.append(('K%d'%r,c['K'][2]))
    elif k=='dim':
        out=[cs('C',r,c['C'][0],S['text'])]
        prod=1.0
        for col in 'DEFG':
            if col in c:
                t=c[col][0]; v=ev(t); prod*=v
                out.append(cn(col,r,v if not float(v).is_integer() or '.' in t else int(v),S['nr' if col=='D' else 'in']) if isnum(t) else cf(col,r,t,v,S['nr' if col=='D' else 'in']))
        h,typ=c['H']
        if typ=='prod':
            v=-prod if h=='-' else prod
            out.append(cf('H',r,('-' if h=='-' else '')+'PRODUCT(D%d:G%d)'%(r,r),v,S['qty']))
        else:
            v=ev(h)
            out.append(cn('H',r,v,S['in']) if isnum(h) else cf('H',r,h,v,S['in']))
        VAL[i]=v
        out.append(cs('J',r,c['J'][0],S['calc']))
    elif k=='total':
        a,b=c['H'][0]; v=sum(VAL.get(j,0) for j in range(a,b+1)); VAL[i]=v
        out=[cs('C',r,c['C'][0],S['totl'])]+[cs(col,r,'',S['totl']) for col in 'DEFG']+[cf('H',r,'SUM(H%d:H%d)'%(rowof(a),rowof(b)),v,S['totn']),cs('I',r,c['I'][0],S['totu'])]
    rows.append((r,out,ht))
last=max(r for r,_,_ in rows)
# ---------------- check against original quantities ----------------
wbval=openpyxl.load_workbook(SRC,data_only=True)
bad=0
for nm,r,f,t,a,b in tk.CHECK:
    orig=wbval[nm].cell(r,3).value
    if orig is None or abs(orig-VAL[t])>1e-6*max(1,abs(orig)): bad+=1; print('MISMATCH',nm,r,orig,VAL[t])
print('items',len(tk.CHECK),'mismatch',bad)
# ---------------- sheet xml ----------------
colw={'A':13,'B':6,'C':78,'D':10,'E':12,'F':12,'G':13,'H':15,'I':7,'J':48,'K':24}
xml=['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
'<sheetPr><tabColor rgb="FF1F3864"/><pageSetUpPr fitToPage="1"/></sheetPr><dimension ref="A1:K%d"/>'%last,
'<sheetViews><sheetView workbookViewId="0" zoomScale="85" zoomScaleNormal="85"><pane ySplit="%d" topLeftCell="A%d" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A%d" sqref="A%d"/></sheetView></sheetViews>'%(HDR,HDR+1,HDR+1,HDR+1),
'<sheetFormatPr defaultRowHeight="15"/><cols>'+''.join('<col min="%d" max="%d" width="%g" customWidth="1"/>'%(i,i,colw[c]) for i,c in enumerate('ABCDEFGHIJK',1))+'</cols><sheetData>']
for r,cells,ht in sorted(rows):
    xml.append('<row r="%d"%s>'%(r,' ht="%g" customHeight="1"'%ht if ht else '')+''.join(cells)+'</row>')
xml.append('</sheetData><hyperlinks>'+''.join('<hyperlink ref="%s" location=%s display=%s/>'%(ref,quoteattr(loc),quoteattr(loc)) for ref,loc in HL)+'</hyperlinks>')
xml.append('<pageMargins left="0.4" right="0.4" top="0.6" bottom="0.6" header="0.3" footer="0.3"/><pageSetup paperSize="9" orientation="landscape" fitToHeight="0"/><headerFooter><oddFooter>&amp;LTake-off&amp;RPage &amp;P of &amp;N</oddFooter></headerFooter></worksheet>')
open(W+'/xl/worksheets/sheet20.xml','w',encoding='utf-8',newline='').write(''.join(xml))
# ---------------- link bill QTY cells ----------------
wbx=open(W+'/xl/workbook.xml',encoding='utf-8',newline='').read()
rels=open(W+'/xl/_rels/workbook.xml.rels',encoding='utf-8',newline='').read()
sheetfile={}
for m in re.finditer(r'<sheet name="([^"]*)" sheetId="\d+" r:id="(rId\d+)"/>',wbx):
    nm=m.group(1).replace('&amp;','&'); tgt=re.search(r'Id="%s" Type="[^"]*" Target="([^"]*)"'%m.group(2),rels).group(1); sheetfile[nm]=tgt
n=0
by=collections=__import__('collections').defaultdict(list)
for key,t in tk.LINKS.items():
    if key=='_bills': continue
    by[key[0]].append((key[1],t))
for nm,lst in by.items():
    p=W+'/xl/'+sheetfile[nm]; x=open(p,encoding='utf-8',newline='').read()
    for r,t in lst:
        pat=re.compile(r'(<c r="C%d"[^>]*>)<f>[^<]*</f>'%r)
        x,k=pat.subn(lambda m:m.group(1)+'<f>TAKEOFF!$H$%d</f>'%rowof(t),x); assert k==1,(nm,r,k); n+=1
    open(p,'w',encoding='utf-8',newline='').write(x)
print('linked',n)
# ---------------- workbook / rels / content types ----------------
wbx=wbx.replace('</sheets>','<sheet name="TAKEOFF" sheetId="20" r:id="rId30"/></sheets>')
wbx=wbx.replace('<calcPr calcId="191029"/>','<calcPr calcId="191029" fullCalcOnLoad="1"/>')
wbx=wbx.replace('</definedNames>','<definedName name="_xlnm.Print_Titles" localSheetId="19">TAKEOFF!$%d:$%d</definedName></definedNames>'%(HDR,HDR))
open(W+'/xl/workbook.xml','w',encoding='utf-8',newline='').write(wbx)
rels=re.sub(r'<Relationship Id="rId23" Type="[^"]*calcChain" Target="calcChain.xml"/>','',rels)
rels=rels.replace('</Relationships>','<Relationship Id="rId30" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet20.xml"/></Relationships>')
open(W+'/xl/_rels/workbook.xml.rels','w',encoding='utf-8',newline='').write(rels)
os.remove(W+'/xl/calcChain.xml')
ct=open(W+'/[Content_Types].xml',encoding='utf-8',newline='').read()
ct=re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>','',ct)
ct=ct.replace('</Types>','<Override PartName="/xl/worksheets/sheet20.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
open(W+'/[Content_Types].xml','w',encoding='utf-8',newline='').write(ct)
# ---------------- zip (keep original order) ----------------
names=[i.filename for i in zipfile.ZipFile(SRC).infolist() if i.filename!='xl/calcChain.xml']
names.insert(names.index('xl/worksheets/sheet19.xml')+1,'xl/worksheets/sheet20.xml')
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for nmf in names: z.write(os.path.join(W,nmf),nmf)
print('written',OUT,last)
