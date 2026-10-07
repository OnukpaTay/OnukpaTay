"""Re-attach the header logo (&G) VML drawings from the template to the rebuilt workbook."""
import sys, zipfile, re
ref, src, out = sys.argv[1:4]
R = zipfile.ZipFile(ref); Z = zipfile.ZipFile(src)
files = {n: Z.read(n) for n in Z.namelist()}
# template sheetN -> vmlDrawingM used for its header
hf = {}
for n in R.namelist():
    m = re.match(r'xl/worksheets/_rels/(sheet\d+)\.xml\.rels$', n)
    if m:
        t = re.search(rb'Type="[^"]*/vmlDrawing" Target="\.\./drawings/(vmlDrawing\d+)\.vml"', R.read(n))
        if t: hf[m.group(1)] = t.group(1).decode()
files['xl/media/hdr_logo.jpeg'] = R.read('xl/media/image3.jpeg')
for sheet, vml in hf.items():
    files[f'xl/drawings/{vml}.vml'] = R.read(f'xl/drawings/{vml}.vml')
    files[f'xl/drawings/_rels/{vml}.vml.rels'] = re.sub(rb'Target="\.\./media/[^"]+"', b'Target="../media/hdr_logo.jpeg"',
                                                         R.read(f'xl/drawings/_rels/{vml}.vml.rels'))
    relp = f'xl/worksheets/_rels/{sheet}.xml.rels'
    rel = files.get(relp, b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>')
    rel = rel.replace(b'</Relationships>', f'<Relationship Id="rIdHF1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/vmlDrawing" Target="../drawings/{vml}.vml"/></Relationships>'.encode())
    files[relp] = rel
    sp = f'xl/worksheets/{sheet}.xml'; x = files[sp]
    if b'xmlns:r=' not in x[:1000]:
        x = x.replace(b'<worksheet ', b'<worksheet xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    tag = b'<legacyDrawingHF r:id="rIdHF1"/>'
    m = re.search(rb'<drawing [^>]*/>', x)
    if m: x = x[:m.end()] + tag + x[m.end():]
    else:
        m = re.search(rb'</headerFooter>', x); x = x[:m.end()] + tag + x[m.end():]
    files[sp] = x
ct = files['[Content_Types].xml']
for ext, typ in ((b'vml', b'application/vnd.openxmlformats-officedocument.vmlDrawing'), (b'jpeg', b'image/jpeg')):
    if f'Extension="{ext.decode()}"'.encode() not in ct:
        ct = ct.replace(b'<Override', b'<Default Extension="' + ext + b'" ContentType="' + typ + b'"/><Override', 1)
files['[Content_Types].xml'] = ct
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as o:
    for n, d in files.items(): o.writestr(n, d)
print('header logos attached to', hf)
