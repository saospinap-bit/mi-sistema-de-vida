"""Crea la plantilla reference.docx: A4, margenes 2.5 cm, tipografia,
estilos de titulo, pies de pagina numerados y tablas con bordes."""
import os, re, shutil, subprocess, zipfile

BD = '/projects/sandbox/.build'
R = f'{BD}/ref'
if os.path.exists(R):
    shutil.rmtree(R)
shutil.copytree(f'{BD}/ref0', R)

# ----------------------------------------------------------------- styles.xml
p = f'{R}/word/styles.xml'
d = open(p, encoding='utf-8').read()

# tipografia y espaciado base: 10.5 pt, interlineado 1.12, espacio posterior 6 pt
d = d.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />',
              '<w:sz w:val="21" />\n        <w:szCs w:val="21" />')
d = d.replace('<w:pPr>\n        <w:spacing w:after="200" />\n      </w:pPr>',
              '<w:pPr>\n        <w:spacing w:after="120" w:line="268" '
              'w:lineRule="auto" />\n      </w:pPr>')

# cuerpo de texto justificado
d = d.replace("""    <w:pPr>
      <w:spacing w:before="180" w:after="180" />
    </w:pPr>
  </w:style>""",
              """    <w:pPr>
      <w:spacing w:before="60" w:after="120" w:line="268" w:lineRule="auto" />
      <w:jc w:val="both" />
    </w:pPr>
  </w:style>""", 1)


def set_heading(d, sid, sz, color, before, after, pagebreak=False,
                bold=True, border=False):
    m = re.search(r'(<w:style [^>]*w:styleId="' + sid + r'">)(.*?)(</w:style>)',
                  d, re.S)
    body = m.group(2)
    body = re.sub(r'<w:spacing [^/]*/>',
                  f'<w:spacing w:before="{before}" w:after="{after}" />', body)
    body = re.sub(r'<w:sz w:val="\d+" />', f'<w:sz w:val="{sz}" />', body)
    body = re.sub(r'<w:szCs w:val="\d+" />', f'<w:szCs w:val="{sz}" />', body)
    body = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"[^/]*/>',
                  f'<w:color w:val="{color}" />', body)
    extra = ''
    if pagebreak:
        extra += '<w:pageBreakBefore />'
    if border:
        extra += ('<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" '
                  f'w:color="{color}" /></w:pBdr>')
    if extra:
        body = body.replace('<w:keepNext />', '<w:keepNext />' + extra, 1)
    if bold and '<w:b />' not in body:
        body = body.replace('<w:rPr>', '<w:rPr><w:b />', 1)
    return d[:m.start()] + m.group(1) + body + m.group(3) + d[m.end():]


d = set_heading(d, 'Heading1', 34, '1A4E8A', 0, 200, pagebreak=True, border=True)
d = set_heading(d, 'Heading2', 27, '13335C', 320, 120)
d = set_heading(d, 'Heading3', 23, '333333', 240, 100)

# titulo / subtitulo / autor
d = re.sub(r'(w:styleId="Title">.*?)<w:sz w:val="56" />', r'\1<w:sz w:val="48" />',
           d, flags=re.S)
d = re.sub(r'(w:styleId="Title">.*?)<w:szCs w:val="56" />',
           r'\1<w:szCs w:val="48" />', d, flags=re.S)

# pie de figura: centrado, cursiva, 9 pt
m = re.search(r'(<w:style [^>]*w:styleId="ImageCaption">)(.*?)(</w:style>)', d, re.S)
d = (d[:m.start()] + m.group(1) +
     """
    <w:name w:val="Image Caption" />
    <w:basedOn w:val="Normal" />
    <w:next w:val="BodyText" />
    <w:qFormat />
    <w:pPr>
      <w:keepLines />
      <w:spacing w:before="60" w:after="280" />
      <w:jc w:val="center" />
    </w:pPr>
    <w:rPr>
      <w:i />
      <w:color w:val="404040" />
      <w:sz w:val="18" />
      <w:szCs w:val="18" />
    </w:rPr>
  """ + m.group(3) + d[m.end():])

# las imagenes deben quedar centradas (pandoc usa Figure y CaptionedFigure)
for sid in ('Figure', 'CaptionedFigure'):
    body = ('\n    <w:name w:val="' + sid + '" />'
            '\n    <w:basedOn w:val="Normal" />'
            '\n    <w:pPr>\n      <w:keepNext />'
            '\n      <w:spacing w:before="260" w:after="0" />'
            '\n      <w:jc w:val="center" />\n    </w:pPr>\n  ')
    m = re.search(r'(<w:style [^>]*w:styleId="' + sid + r'">)(.*?)(</w:style>)',
                  d, re.S)
    if m:
        d = d[:m.start()] + m.group(1) + body + m.group(3) + d[m.end():]
    else:
        d = d.replace('</w:styles>',
                      '<w:style w:type="paragraph" w:styleId="' + sid + '">'
                      + body + '</w:style></w:styles>')
# titulo de la tabla de contenido
m = re.search(r'(<w:style [^>]*w:styleId="TOCHeading">)(.*?)(</w:style>)', d, re.S)
if m:
    d = (d[:m.start()] + m.group(1) +
         '\n    <w:name w:val="TOC Heading" />'
         '\n    <w:basedOn w:val="Heading1" />'
         '\n    <w:pPr><w:pageBreakBefore w:val="false" /></w:pPr>\n  '
         + m.group(3) + d[m.end():])

# tabla con bordes y encabezado sombreado
d = d.replace('</w:styles>', """<w:style w:type="table" w:styleId="Table">
    <w:name w:val="Table" />
    <w:basedOn w:val="TableNormal" />
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="8FA8BF" />
        <w:left w:val="single" w:sz="6" w:space="0" w:color="8FA8BF" />
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="8FA8BF" />
        <w:right w:val="single" w:sz="6" w:space="0" w:color="8FA8BF" />
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFD0DE" />
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFD0DE" />
      </w:tblBorders>
      <w:tblCellMar>
        <w:top w:w="60" w:type="dxa" /><w:left w:w="90" w:type="dxa" />
        <w:bottom w:w="60" w:type="dxa" /><w:right w:w="90" w:type="dxa" />
      </w:tblCellMar>
    </w:tblPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Compact2">
    <w:name w:val="Compact2" /><w:basedOn w:val="Normal" />
    <w:pPr><w:spacing w:after="0" /></w:pPr>
  </w:style>
</w:styles>""")
open(p, 'w', encoding='utf-8').write(d)

# ------------------------------------------------- tamano de pagina y pie
foot = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:p>
    <w:pPr><w:jc w:val="center" />
      <w:rPr><w:color w:val="666666" /><w:sz w:val="18" /></w:rPr></w:pPr>
    <w:r><w:rPr><w:color w:val="666666" /><w:sz w:val="18" /></w:rPr>
      <w:t xml:space="preserve">- </w:t></w:r>
    <w:r><w:fldChar w:fldCharType="begin" /></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate" /></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end" /></w:r>
    <w:r><w:rPr><w:color w:val="666666" /><w:sz w:val="18" /></w:rPr>
      <w:t xml:space="preserve"> -</w:t></w:r>
  </w:p>
</w:ftr>
"""
open(f'{R}/word/footer1.xml', 'w', encoding='utf-8').write(foot)

p = f'{R}/word/_rels/document.xml.rels'
d = open(p, encoding='utf-8').read()
d = d.replace('</Relationships>',
              '<Relationship Id="rIdFtr1" Type="http://schemas.openxmlformats.org/'
              'officeDocument/2006/relationships/footer" Target="footer1.xml" />'
              '</Relationships>')
open(p, 'w', encoding='utf-8').write(d)

p = f'{R}/[Content_Types].xml'
d = open(p, encoding='utf-8').read()
if 'footer1.xml' not in d:
    d = d.replace('</Types>',
                  '<Override PartName="/word/footer1.xml" ContentType='
                  '"application/vnd.openxmlformats-officedocument.'
                  'wordprocessingml.footer+xml" /></Types>')
open(p, 'w', encoding='utf-8').write(d)

p = f'{R}/word/document.xml'
d = open(p, encoding='utf-8').read()
d = d.replace("""    <w:sectPr>
      <w:footnotePr>
        <w:numRestart w:val="eachSect" />
      </w:footnotePr>
    </w:sectPr>""",
              """    <w:sectPr>
      <w:footerReference w:type="default" r:id="rIdFtr1" />
      <w:footnotePr>
        <w:numRestart w:val="eachSect" />
      </w:footnotePr>
      <w:pgSz w:w="11906" w:h="16838" />
      <w:pgMar w:top="1417" w:right="1417" w:bottom="1417" w:left="1417"
               w:header="708" w:footer="708" w:gutter="0" />
    </w:sectPr>""")
open(p, 'w', encoding='utf-8').write(d)

# ----------------------------------------------------------------- empacar
out = f'{BD}/reference.docx'
if os.path.exists(out):
    os.remove(out)
zf = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
for root, _dirs, files in os.walk(R):
    for fn in files:
        full = os.path.join(root, fn)
        zf.write(full, os.path.relpath(full, R))
zf.close()
print('reference.docx ->', out, os.path.getsize(out), 'bytes')
