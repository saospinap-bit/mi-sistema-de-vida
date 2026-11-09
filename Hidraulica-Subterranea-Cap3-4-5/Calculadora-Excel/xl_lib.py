"""Utilidades comunes para construir la calculadora de Hidráulica Subterránea."""
import math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.formatting.rule import FormulaRule

# ------------------------------------------------------------------ formatos
SCI, F0, F1, F2, F3, F4 = '0.00E+00', '#,##0', '0.0', '0.00', '0.000', '0.0000'
PCT, GEN = '0.0%', 'General'

# ------------------------------------------------------------------ estilos
FILL_T = PatternFill('solid', fgColor='1F3864')
F_T = Font(size=16, bold=True, color='FFFFFF')
F_S = Font(size=10, italic=True, color='DDEBF7')
FILL_SEC = PatternFill('solid', fgColor='D9E1F2')
F_SEC = Font(size=12, bold=True, color='1F3864')
FILL_IN = PatternFill('solid', fgColor='FFF2CC')
F_IN = Font(bold=True, color='1F4E79')
FILL_OUT = PatternFill('solid', fgColor='E2EFDA')
F_OUT = Font(bold=True, color='375623')
FILL_MAIN = PatternFill('solid', fgColor='A9D08E')
F_MAIN = Font(bold=True, size=12, color='1E3D10')
FILL_HEAD = PatternFill('solid', fgColor='305496')
F_HEAD = Font(bold=True, color='FFFFFF', size=10)
F_NOTE = Font(italic=True, color='595959', size=9)
_thin = Side(style='thin', color='BFBFBF')
BOX = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
FILL_OK = PatternFill('solid', fgColor='C6EFCE')
FILL_BAD = PatternFill('solid', fgColor='FFC7CE')
FILL_WARN = PatternFill('solid', fgColor='FFEB9C')

wb = Workbook()
INI = wb.active
INI.title = 'INICIO'
INDEX = []          # (hoja, titulo, subtitulo)
CHECKS = []         # (worksheet, fila, columna_inicial, columna_final)


def W(u):
    """W(u) de Theis como fórmula de Excel (Abramowitz y Stegun 5.1.53 y 5.1.56).
    Error relativo máximo 5e-5. `u` debe ser una referencia o una expresión
    entre paréntesis."""
    return (f"IF({u}<1,-LN({u})-0.57721566+0.99999193*{u}-0.24991055*{u}^2"
            f"+0.05519968*{u}^3-0.00976004*{u}^4+0.00107857*{u}^5,"
            f"EXP(-{u})/{u}*({u}^2+2.334733*{u}+0.250621)"
            f"/({u}^2+3.330657*{u}+1.681534))")


def link(cell, sheet, text=None):
    if text is not None:
        cell.value = text
    cell.hyperlink = Hyperlink(ref=cell.coordinate, location=f"'{sheet}'!A1")
    cell.font = Font(color='0563C1', underline='single', bold=True)


class Hoja:
    """Hoja con columna B = etiqueta, C = valor, D = unidad, E = nota."""

    def __init__(self, name, title, sub, widths=None, cols=None):
        ws = wb.create_sheet(name)
        self.ws, self.name, self.v, self.r = ws, name, {}, 5
        w = {'A': 2, 'B': 50, 'C': 17, 'D': 14, 'E': 58, 'F': 3}
        if widths:
            w.update(widths)
        for k, val in w.items():
            ws.column_dimensions[k].width = val
        for k, val in (cols or {}).items():
            ws.column_dimensions[k].width = val
        ws.sheet_view.showGridLines = False
        ws.sheet_view.zoomScale = 90
        for col in 'BCDE':
            ws[f'{col}1'].fill = FILL_T
            ws[f'{col}2'].fill = FILL_T
        ws['B1'] = title
        ws['B1'].font = F_T
        ws['B2'] = sub
        ws['B2'].font = F_S
        ws.row_dimensions[1].height = 30
        ws.row_dimensions[2].height = 18
        link(ws['B3'], 'INICIO', '← volver al INICIO')
        ws['B3'].font = Font(color='0563C1', underline='single', size=9)
        INDEX.append((name, title, sub))

    # --------------------------------------------------------------- basico
    def ext(self, key):
        return f"'{self.name}'!{self.v[key]}"

    def f(self, s, mapping=None):
        return '=' + s.format(**(mapping or self.v))

    def to(self, row):
        self.r = max(self.r, row)

    def blank(self, n=1):
        self.r += n

    def sec(self, text):
        self.r += 1
        r = self.r
        for col in 'BCDE':
            self.ws[f'{col}{r}'].fill = FILL_SEC
        self.ws[f'B{r}'] = text
        self.ws[f'B{r}'].font = F_SEC
        self.ws.row_dimensions[r].height = 20
        self.r += 1

    def note(self, text):
        r = self.r
        self.ws.merge_cells(f'B{r}:E{r}')
        c = self.ws[f'B{r}']
        c.value = text
        c.font = F_NOTE
        c.alignment = Alignment(wrap_text=True, vertical='top')
        lines = max(1, math.ceil(len(text) / 135)) + text.count('\n')
        self.ws.row_dimensions[r].height = 13 * lines + 3
        self.r += 1

    def _row(self, label, unit, note):
        r = self.r
        c = self.ws[f'B{r}']
        c.value = label
        c.alignment = Alignment(wrap_text=True, vertical='center')
        if unit:
            self.ws[f'D{r}'] = unit
            self.ws[f'D{r}'].font = Font(color='595959')
        if note:
            n = self.ws[f'E{r}']
            n.value = note
            n.font = F_NOTE
            n.alignment = Alignment(wrap_text=True, vertical='center')
            if len(note) > 70:
                self.ws.row_dimensions[r].height = 13 * math.ceil(len(note) / 70) + 3
        return r

    # --------------------------------------------------------------- celdas
    def inp(self, key, label, value, unit='', note='', fmt=None):
        r = self._row(label, unit, note)
        c = self.ws[f'C{r}']
        c.value = value
        c.fill, c.font, c.border = FILL_IN, F_IN, BOX
        c.alignment = Alignment(horizontal='right')
        if fmt:
            c.number_format = fmt
        if key:
            self.v[key] = f'$C${r}'
        self.r += 1
        return f'$C${r}'

    def out(self, key, label, formula, unit='', note='', fmt=F3, main=False):
        r = self._row(label, unit, note)
        c = self.ws[f'C{r}']
        c.value = self.f(formula)
        c.fill = FILL_MAIN if main else FILL_OUT
        c.font = F_MAIN if main else F_OUT
        c.border = BOX
        c.alignment = Alignment(horizontal='right')
        if fmt:
            c.number_format = fmt
        if key:
            self.v[key] = f'$C${r}'
        self.r += 1
        return f'$C${r}'

    def chk(self, label, formula, key=None):
        r = self._row(label, '', '')
        self.ws.merge_cells(f'C{r}:E{r}')
        c = self.ws[f'C{r}']
        c.value = self.f(formula)
        c.font = Font(bold=True)
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical='center')
        CHECKS.append((self.ws, r, 'C', 'E'))
        if key:
            self.v[key] = f'$C${r}'
        self.r += 1

    # ------------------------------------------------- dos columnas (casos)
    def head2(self, a, b):
        r = self.r
        for col, txt in (('C', a), ('D', b)):
            c = self.ws[f'{col}{r}']
            c.value = txt
            c.fill, c.font, c.border = FILL_HEAD, F_HEAD, BOX
            c.alignment = Alignment(horizontal='center')
        self.r += 1

    def inp2(self, key, label, va, vb, note='', fmt=None):
        r = self._row(label, '', note)
        for col, val, case in (('C', va, 'A'), ('D', vb, 'B')):
            c = self.ws[f'{col}{r}']
            c.value = val
            c.fill, c.font, c.border = FILL_IN, F_IN, BOX
            if fmt:
                c.number_format = fmt
            self.v[f'{key}_{case}'] = f'${col}${r}'
        self.r += 1

    def out2(self, key, label, tmpl, case_keys=(), note='', fmt=F3, main=False):
        r = self._row(label, '', note)
        for col, case in (('C', 'A'), ('D', 'B')):
            m = dict(self.v)
            for k in case_keys:
                m[k] = self.v[f'{k}_{case}']
            t = tmpl[0 if case == 'A' else 1] if isinstance(tmpl, tuple) else tmpl
            c = self.ws[f'{col}{r}']
            c.value = '=' + t.format(**m)
            c.fill = FILL_MAIN if main else FILL_OUT
            c.font = F_MAIN if main else F_OUT
            c.border = BOX
            c.alignment = Alignment(horizontal='right', wrap_text=True)
            if fmt:
                c.number_format = fmt
            if key:
                self.v[f'{key}_{case}'] = f'${col}${r}'
        self.r += 1

    def chk2(self, label, tmpl, case_keys=()):
        r = self._row(label, '', '')
        for col, case in (('C', 'A'), ('D', 'B')):
            m = dict(self.v)
            for k in case_keys:
                m[k] = self.v[f'{k}_{case}']
            c = self.ws[f'{col}{r}']
            c.value = '=' + tmpl.format(**m)
            c.font = Font(bold=True, size=9)
            c.border = BOX
            c.alignment = Alignment(wrap_text=True, vertical='center')
            CHECKS.append((self.ws, r, col, col))
        self.ws.row_dimensions[r].height = 42
        self.r += 1


# ------------------------------------------------------------------ tablas
def thead(ws, row, col, labels, height=34):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=lab)
        c.fill, c.font, c.border = FILL_HEAD, F_HEAD, BOX
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[row].height = height


def tin(ws, row, col, value, fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    c.fill, c.font, c.border = FILL_IN, F_IN, BOX
    if fmt:
        c.number_format = fmt
    return c


def tout(ws, row, col, formula, fmt=None, main=False):
    c = ws.cell(row=row, column=col, value=formula)
    c.fill = FILL_MAIN if main else FILL_OUT
    c.font = Font(bold=main, color='1E3D10' if main else '375623', size=10)
    c.border = BOX
    if fmt:
        c.number_format = fmt
    return c


def tlabel(ws, row, col, text, bold=False, italic=False):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(bold=bold, italic=italic, color='1F3864' if bold else '595959',
                  size=11 if bold else 9)
    return c


# ------------------------------------------------------------------ gráficas
def chart(title, xt, yt, logx=False, logy=False, w=22, h=11, ymin=None, ymax=None,
          xmin=None, xmax=None):
    ch = ScatterChart()
    ch.title = title
    ch.style = 2
    ch.scatterStyle = 'lineMarker'
    ch.x_axis.title = xt
    ch.y_axis.title = yt
    ch.width, ch.height = w, h
    if logx:
        ch.x_axis.scaling.logBase = 10
    if logy:
        ch.y_axis.scaling.logBase = 10
    for ax, lo, hi in ((ch.y_axis, ymin, ymax), (ch.x_axis, xmin, xmax)):
        if lo is not None:
            ax.scaling.min = lo
        if hi is not None:
            ax.scaling.max = hi
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.x_axis.number_format = 'General'
    ch.y_axis.number_format = 'General'
    ch.legend.position = 'b'
    return ch


def serie(ch, ws, xc, yc, r0, r1, title, kind='pts', color='1F4E79', hollow=False,
          dash=None, size=7):
    x = Reference(ws, min_col=xc, min_row=r0, max_row=r1)
    y = Reference(ws, min_col=yc, min_row=r0, max_row=r1)
    s = Series(y, x, title=title)
    if kind == 'pts':
        s.marker = Marker(symbol='circle', size=size)
        s.marker.graphicalProperties = GraphicalProperties(
            solidFill='FFFFFF' if hollow else color,
            ln=LineProperties(solidFill=color, w=15875))
        s.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))
    else:
        s.marker = Marker(symbol='none')
        s.graphicalProperties = GraphicalProperties(
            ln=LineProperties(solidFill=color, w=28575, prstDash=dash))
    s.smooth = False
    ch.series.append(s)
    return s


def apply_checks():
    for ws, r, c0, c1 in CHECKS:
        rng = f'{c0}{r}:{c1}{r}'
        cell = f'${c0}${r}'
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'LEFT({cell},1)="✔"'], fill=FILL_OK, font=Font(bold=True, color='006100')))
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'LEFT({cell},1)="✘"'], fill=FILL_BAD, font=Font(bold=True, color='9C0006')))
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'LEFT({cell},1)="⚠"'], fill=FILL_WARN, font=Font(bold=True, color='9C5700')))
