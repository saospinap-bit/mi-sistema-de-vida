# -*- coding: utf-8 -*-
"""Genera los PDF listos para imprimir: Sobre 1, Sobre 2 (original y copia) y APU."""
import sys
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle, KeepTogether)
import reportlab
import datos as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FD = reportlab.__path__[0] + "/fonts/"
pdfmetrics.registerFont(TTFont("V", FD + "Vera.ttf"))
pdfmetrics.registerFont(TTFont("VB", FD + "VeraBd.ttf"))
pdfmetrics.registerFont(TTFont("VI", FD + "VeraIt.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("V", normal="V", bold="VB", italic="VI", boldItalic="VB")

AZUL = colors.HexColor("#1F4E78")
CAP = colors.HexColor("#D9E1F2")
AMA = colors.HexColor("#FFF2CC")
BAR = colors.HexColor("#2E75B6")


def st(size=9, bold=False, align=None, lead=None, italic=False):
    s = ParagraphStyle("x", fontName="VB" if bold else ("VI" if italic else "V"), fontSize=size,
                       leading=lead or size * 1.25)
    if align:
        s.alignment = align
    return s


P = lambda t, **k: Paragraph(t, st(**k))
pesos = D.pesos


def n0(x):
    return f"{x:,.0f}".replace(",", ".")


def n2(x):
    s = f"{x:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


class Doc(BaseDocTemplate):
    def __init__(self, path, marca="", **kw):
        super().__init__(path, pagesize=letter, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                         topMargin=2.2 * cm, bottomMargin=1.6 * cm, **kw)
        self.marca = marca
        fp = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="p")
        lw, lh = landscape(letter)
        fl = Frame(1.2 * cm, 1.4 * cm, lw - 2.4 * cm, lh - 3.4 * cm, id="l")
        self.addPageTemplates([
            PageTemplate("P", [fp], onPage=self.deco, pagesize=letter),
            PageTemplate("L", [fl], onPage=self.deco, pagesize=landscape(letter)),
        ])

    def deco(self, c, doc):
        w, h = c._pagesize
        c.saveState()
        c.setFont("VB", 8)
        c.drawString(1.2 * cm, h - 1.0 * cm, D.ENTIDAD + "  –  " + D.LICITACION)
        c.setFont("V", 7)
        c.drawString(1.2 * cm, h - 1.4 * cm, "Proponente: " + D.PROPONENTE)
        if self.marca:
            c.setFont("VB", 11)
            c.setFillColor(colors.HexColor("#C00000"))
            c.drawRightString(w - 1.2 * cm, h - 1.2 * cm, self.marca)
            c.setFillColor(colors.black)
        c.setFont("V", 7)
        c.drawRightString(w - 1.2 * cm, 0.8 * cm, f"Folio {doc.page}")
        c.line(1.2 * cm, h - 1.6 * cm, w - 1.2 * cm, h - 1.6 * cm)
        c.restoreState()


def tabla(data, widths, style, repeat=1):
    t = Table(data, colWidths=widths, repeatRows=repeat)
    base = [("FONT", (0, 0), (-1, -1), "V", 7), ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]
    t.setStyle(TableStyle(base + style))
    return t


def hdr_style(row=0):
    return [("BACKGROUND", (0, row), (-1, row), AZUL), ("TEXTCOLOR", (0, row), (-1, row), colors.white),
            ("FONT", (0, row), (-1, row), "VB", 7), ("ALIGN", (0, row), (-1, row), "CENTER")]


def titulo(t, sub=None):
    out = [P(t, size=12, bold=True, align=TA_CENTER), Spacer(1, 3)]
    out.append(P("OBJETO: " + D.OBJETO, size=8, align=TA_CENTER))
    if sub:
        out.append(P(sub, size=8, align=TA_CENTER, bold=True))
    out.append(Spacer(1, 8))
    return out


def bloque_firma():
    return [Spacer(1, 30), P("_________________________________________", size=9),
            P(f"<b>{D.REPRESENTANTE}</b>", size=9),
            P(f"Representante legal – {D.PROPONENTE}", size=9), P(D.CEDULA_REP, size=9)]


def rotulo(sobre):
    s = [Spacer(1, 3 * cm)]
    filas = [["Proponente:", D.PROPONENTE], ["Dirección:", D.DIRECCION], ["Teléfono:", D.TELEFONO],
             ["Correo:", D.CORREO], ["Dirigido a:", "ALCALDÍA MUNICIPAL DE SANDONÁ – Secretaría de "
                                                    "Planeación e Infraestructura"],
             ["Proceso:", D.LICITACION], ["Objeto:", D.OBJETO]]
    t = Table([[P(a, size=12, bold=True), P(b, size=12)] for a, b in filas],
              colWidths=[4 * cm, 13 * cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.5, colors.black),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    s += [P(sobre, size=30, bold=True, align=TA_CENTER), Spacer(1, 1.2 * cm), t]
    return s


# ------------------------------------------------------------------ OFERTA (Anexo 4)
def oferta():
    s = titulo("ANEXO 4 – FORMATO DE CANTIDADES Y PRESUPUESTO OFICIAL DE LA OBRA",
               "OFERTA ECONÓMICA – SOBRE No. 2")
    data = [["COD.", "ITEM", "UNIDAD", "CANTIDAD", "VR. UNITARIO", "VR. TOTAL"]]
    sty = hdr_style()
    for f in D.FORMATO:
        if f[0] == "cap":
            data.append([f[1] + ".", f[2], "", "", "", ""])
            i = len(data) - 1
            sty += [("BACKGROUND", (0, i), (-1, i), CAP), ("FONT", (0, i), (-1, i), "VB", 7)]
        else:
            _, cod, desc, und, q, vu = f
            pu = D.PRECIOS[cod]
            data.append([cod, P(desc, size=7), und, n2(q), n0(pu), n0(D.total_item(cod))])
    sty += [("ALIGN", (3, 1), (-1, -1), "RIGHT"), ("ALIGN", (2, 1), (2, -1), "CENTER")]
    s.append(tabla(data, [1.2 * cm, 8.6 * cm, 1.5 * cm, 1.8 * cm, 2.2 * cm, 2.9 * cm], sty))
    s.append(Spacer(1, 6))
    tot = [["VALOR TOTAL COSTO DIRECTO", "", n0(D.CD)],
           ["COSTOS INDIRECTOS", "PORCENTAJE", "VR. TOTAL"],
           ["A – Administración", "15,00 %", n0(D.VA)],
           ["I – Imprevistos", "7,00 %", n0(D.VI)],
           ["U – Utilidad", "2,00 %", n0(D.VU_)],
           ["VALOR TOTAL COSTO INDIRECTO", "24,00 %", n0(D.VA + D.VI + D.VU_)],
           ["VALOR TOTAL DE LA PROPUESTA", "", pesos(D.TOTAL)]]
    t = tabla(tot, [11.3 * cm, 3 * cm, 3.9 * cm],
              [("FONT", (0, 0), (-1, 0), "VB", 8), ("BACKGROUND", (0, 0), (-1, 0), AMA)]
              + hdr_style(1) + [("FONT", (0, 5), (-1, 5), "VB", 7),
                                ("FONT", (0, 6), (-1, 6), "VB", 10), ("BACKGROUND", (0, 6), (-1, 6), AMA),
                                ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("ALIGN", (1, 1), (1, -1), "CENTER")],
              repeat=0)
    s.append(KeepTogether([t, Spacer(1, 6),
                           P(f"<b>SON: {D.letras(D.TOTAL)} PESOS M/CTE.</b>", size=9),
                           Spacer(1, 4),
                           P("Precios ajustados al peso. Cantidades y unidades del formato oficial sin "
                             "modificación. Los precios unitarios cubren materiales, mano de obra, "
                             "prestaciones sociales, herramienta, equipo y transporte. Impuestos, "
                             "contribuciones, personal directivo, señalización, seguridad y limpieza incluidos "
                             "en el AIU (numerales 3.2.1, 3.2.1.1, 6.1, 6.10, 6.12 y 6.13 de los TR). "
                             "Precios unitarios fijos, sin reajuste durante el plazo de ejecución.",
                             size=7, italic=True, align=TA_JUSTIFY)] + bloque_firma()))
    return s


# ------------------------------------------------------------------ CARTA (Anexo 1)
def carta():
    s = [P("ANEXO 1 – CARTA DE PRESENTACIÓN", size=12, bold=True, align=TA_CENTER), Spacer(1, 14),
         P(D.CIUDAD_FECHA, size=10), Spacer(1, 10),
         P("Señores<br/><b>ALCALDÍA MUNICIPAL DE SANDONÁ</b><br/>Secretaría de Planeación e "
           "Infraestructura<br/>Sandoná – Nariño", size=10), Spacer(1, 10),
         P(f"<b>Referencia:</b> {D.LICITACION}", size=10),
         P(f"<b>Objeto:</b> “{D.OBJETO}” – a todo costo, incluye suministro y transporte de materiales, "
           "mano de obra calificada y no calificada.", size=10, align=TA_JUSTIFY), Spacer(1, 10),
         P("Cordial saludo.", size=10), Spacer(1, 6)]
    j = dict(size=10, align=TA_JUSTIFY, lead=13.5)
    s.append(P(f"El suscrito <b>{D.REPRESENTANTE}</b>, identificado con {D.CEDULA_REP}, obrando en "
               f"nombre y representación de <b>{D.PROPONENTE}</b>, comedida y formalmente me permito "
               "presentar oferta en la Licitación Pública de la referencia, con base en la siguiente "
               "información:", **j))
    s.append(Spacer(1, 6))
    filas = [["Proponente:", D.PROPONENTE + "     Persona natural ___   Jurídica ___   Consorcio / UT ___"],
             ["NIT / C.C.:", D.NIT], ["Representante legal:", D.REPRESENTANTE],
             ["Documento de identificación:", D.CEDULA_REP], ["Dirección y teléfono:", D.DIRECCION + " – " + D.TELEFONO],
             ["Correo electrónico:", D.CORREO],
             ["Integrantes del consorcio o UT (si aplica):", "_______________________________________"]]
    t = Table([[P(a, size=9, bold=True), P(b, size=9)] for a, b in filas], colWidths=[5.5 * cm, 12.3 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    s += [t, Spacer(1, 8)]
    decl = [
        "Como único interesado en la propuesta, declaro que no tengo intereses patrimoniales o relación "
        "jurídico-legal con otra persona participante en esta licitación, que ninguno de los socios o "
        "empleados de mi firma ha tomado parte en la elaboración de la oferta que haya presentado otra "
        "persona, y que el representante legal o los administradores no ostentan igual condición en otra "
        "entidad participante.",
        "Manifiesto que he estudiado y acepto las condiciones, requisitos y especificaciones contenidas en el "
        "pliego de condiciones, sus anexos y adendas, relacionados con el objeto del contrato.",
        "Bajo la gravedad del juramento, que se entiende prestado con la suscripción de esta oferta, declaro "
        "que no me encuentro incurso en las causales de inhabilidad, incompatibilidad o prohibiciones para "
        "contratar con el Municipio de Sandoná señaladas en la Constitución Política, el artículo 8 de la "
        "Ley 80 de 1993 y demás normas aplicables.",
        "Me comprometo a ejecutar la obra en un plazo de <b>CINCO (5) MESES</b> contados a partir del acta de "
        "inicio, a precios unitarios fijos sin reajuste, y a suscribir y legalizar el contrato dentro de los "
        "cinco (5) días hábiles siguientes a la notificación de la adjudicación.",
        "Me comprometo a mantener durante la ejecución el personal exigido en el numeral 4.3 (director de obra, "
        "residente de tiempo completo y maestro de obra) y a contratar la mano de obra no calificada en el "
        "Municipio de Sandoná (numeral 6.1).",
        f"Adjunto garantía de seriedad de la oferta a favor del Municipio de Sandoná: aseguradora "
        f"_______________, póliza No. ________, valor asegurado <b>{pesos(r10())}</b> (10 % del presupuesto "
        "oficial), vigencia de seis (6) meses contados desde la fecha de cierre.",
        "La oferta económica se presenta en sobre independiente (Sobre No. 2), en original y copia, en el "
        "formato de presupuesto suministrado por la entidad. La presente oferta consta de ______ folios "
        "debidamente numerados.",
    ]
    for k, d in enumerate(decl, 1):
        s += [P(f"{k}. {d}", **j), Spacer(1, 4)]
    s += [Spacer(1, 6), P("Atentamente,", size=10)] + bloque_firma()
    return s


def r10():
    return D.r0(Decimal(D.PRESUPUESTO_OFICIAL) * Decimal("0.10"))


# ------------------------------------------------------------------ ANEXO 3
def anexo3():
    smmlv_req = Decimal(D.PRESUPUESTO_OFICIAL) * Decimal("0.5") / D.SMMLV
    s = [P("ANEXO 3 – EXPERIENCIA ESPECÍFICA", size=12, bold=True, align=TA_CENTER), Spacer(1, 6),
         P(f"Proponente: <b>{D.PROPONENTE}</b>", size=9), Spacer(1, 6)]
    head = ["No.", "Contratista", "Contrato No.", "Objeto", "Forma de ejecución (I / C / UT) y %",
            "Entidad contratante", "Fecha inicio", "Fecha terminación", "Valor facturado ($)",
            "Valor facturado (SMMLV)", "m2 cubierta"]
    data = [[P(h, size=6.5, bold=True, align=TA_CENTER) for h in head]]
    for k in range(1, 6):
        data.append([str(k)] + [""] * 10)
    data.append(["", P("<b>TOTALES</b>", size=7), "", "", "", "", "", "", "", "", ""])
    W = [w * cm for w in [0.8, 2.6, 1.8, 4.2, 2.2, 2.6, 1.7, 1.9, 2.4, 2.0, 1.6]]
    t = Table(data, colWidths=W, rowHeights=[None] + [34] * 5 + [None])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "V", 7), ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, 0), CAP),
                           ("ALIGN", (0, 1), (0, -1), "CENTER")]))
    s += [t, Spacer(1, 8)]
    req = [
        "Máximo 5 contratos con entidades estatales, ejecutados y terminados en los últimos 10 años, "
        "en edificaciones clasificables en la especialidad 04 del RUP.",
        f"La suma de los valores, expresada en SMMLV del año de terminación, debe ser igual o superior al "
        f"50 % del presupuesto oficial: 0,5 × {pesos(D.PRESUPUESTO_OFICIAL)} ÷ {pesos(D.SMMLV)} = "
        f"<b>{n2(smmlv_req)} SMMLV</b> (con el SMMLV 2026).",
        "Contratos en consorcio o unión temporal: se informa únicamente el valor correspondiente al "
        "porcentaje de participación y se adjunta el documento de conformación.",
        "Soporte: acta final de obra, acta de liquidación, o contrato con certificación de cumplimiento "
        "de la entidad, donde consten el tipo de obra, las cantidades y las fechas de inicio y terminación.",
    ]
    s += [P("• " + x, size=8, align=TA_JUSTIFY) for x in req]
    smm = [["Año", "SMMLV"], ["2026", "1.750.905"], ["2025", "1.423.500"], ["2024", "1.300.000"],
           ["2023", "1.160.000"], ["2022", "1.000.000"], ["2021", "908.526"], ["2020", "877.803"],
           ["2019", "828.116"], ["2018", "781.242"], ["2017", "737.717"], ["2016", "689.455"]]
    s += [Spacer(1, 6), tabla(smm, [2 * cm, 3 * cm], hdr_style() + [("ALIGN", (0, 0), (-1, -1), "CENTER")])]
    s += bloque_firma()
    return s


# ------------------------------------------------------------------ ANEXO 6
def anexo6():
    s = titulo("ANEXO 6 – FORMATO PROGRAMACIÓN DE OBRA")
    data = [["Ítem", "Actividad", "Und", "Cantidad", "Duración (días)", "Costo actividad ($)",
             "Inicio (día)", "Fin (día)", "Personal y equipo"]]
    sty = hdr_style()
    for f in D.FORMATO:
        if f[0] == "cap":
            data.append([f[1] + ".", f[2]] + [""] * 7)
            i = len(data) - 1
            sty += [("BACKGROUND", (0, i), (-1, i), CAP), ("FONT", (0, i), (-1, i), "VB", 6.5),
                    ("SPAN", (1, i), (-1, i))]
        else:
            _, cod, desc, und, q, vu = f
            ini, dur, pers = D.PROG[cod]
            data.append([cod, P(desc, size=6.5), und, n2(q), str(dur), n0(D.total_item(cod)),
                         str(ini), str(ini + dur - 1), P(pers, size=6.5)])
    data.append(["", "COSTO DIRECTO TOTAL", "", "", "", n0(D.CD), "1", str(D.DIAS), ""])
    i = len(data) - 1
    sty += [("FONT", (0, i), (-1, i), "VB", 7), ("BACKGROUND", (0, i), (-1, i), AMA),
            ("ALIGN", (2, 1), (-2, -1), "CENTER"), ("ALIGN", (3, 1), (3, -1), "RIGHT"),
            ("ALIGN", (5, 1), (5, -1), "RIGHT"), ("FONT", (0, 1), (-1, -1), "V", 6.5)]
    sty += [("FONT", (0, j), (-1, j), "VB", 6.5) for j, r in enumerate(data) if r[2] == "" and j > 0]
    s.append(tabla(data, [1.0 * cm, 7.6 * cm, 1.1 * cm, 1.6 * cm, 1.5 * cm, 2.4 * cm, 1.3 * cm, 1.2 * cm,
                          7.4 * cm], sty))
    s.append(Spacer(1, 8))
    for t in [
        "<b>a. Secuencia y duración:</b> columnas Inicio, Duración y Fin de cada una de las actividades del "
        "presupuesto oficial.",
        "<b>b. Inicio y final:</b> en días calendario contados desde el día 1 = fecha del acta de inicio.",
        "<b>c. Duración del proyecto: CINCO (5) MESES.</b> Cronograma de 21 semanas = 147 días calendario; los 3 "
        "días restantes del plazo (150 días) se destinan a la entrega de la obra (Anexo 7 de los TR).",
        "<b>d. Jornada de trabajo:</b> " + D.JORNADA,
    ]:
        s += [P(t, size=8, align=TA_JUSTIFY), Spacer(1, 2)]
    s += bloque_firma()
    return s


# ------------------------------------------------------------------ ANEXO 7
def semanal():
    sem = [0] * D.SEMANAS
    filas = {}
    for _, cod, *_ in D.ITEMS:
        ini, dur, _p = D.PROG[cod]
        fin = ini + dur - 1
        cost = D.total_item(cod)
        v = []
        for w in range(D.SEMANAS):
            d0, d1 = 7 * w + 1, 7 * w + 7
            n = max(0, min(fin, d1) - max(ini, d0) + 1)
            x = D.r0(Decimal(cost) * n / dur) if n else 0
            v.append(x)
            sem[w] += x
        filas[cod] = v
    return filas, sem


def anexo7():
    s = titulo("ANEXO 7 – CRONOGRAMA DE ACTIVIDADES E INVERSIÓN",
               "21 semanas = 147 días calendario + 3 días de entrega = 5 meses (150 días)")
    filas, sem = semanal()
    head = ["Ítem", "Actividad", "Ini", "Fin"] + [f"S{w}" for w in range(1, 22)]
    data = [head]
    sty = hdr_style() + [("FONT", (0, 0), (-1, -1), "V", 6), ("FONT", (0, 0), (-1, 0), "VB", 6),
                         ("ALIGN", (2, 0), (-1, -1), "CENTER")]
    for f in D.FORMATO:
        if f[0] == "cap":
            data.append([f[1] + ".", f[2]] + [""] * 23)
            i = len(data) - 1
            sty += [("BACKGROUND", (0, i), (-1, i), CAP), ("FONT", (0, i), (-1, i), "VB", 6)]
        else:
            _, cod, desc, *_ = f
            ini, dur, _p = D.PROG[cod]
            data.append([cod, desc[:52], str(ini), str(ini + dur - 1)] + [""] * 21)
            i = len(data) - 1
            for w, x in enumerate(filas[cod]):
                if x:
                    sty.append(("BACKGROUND", (4 + w, i), (4 + w, i), BAR))
    acum, tot = 0, sum(sem)
    r1 = ["", "INVERSIÓN SEMANAL (millones $)", "", ""]
    r2 = ["", "% ACUMULADO", "", ""]
    for x in sem:
        acum += x
        r1.append(n2(x / 1e6).replace(",00", ",0") if x else "")
        r2.append(f"{acum / tot * 100:.0f}%")
    data += [r1, r2]
    sty += [("FONT", (0, -2), (-1, -1), "VB", 5.5), ("BACKGROUND", (0, -2), (-1, -1), AMA)]
    s.append(tabla(data, [0.9 * cm, 6.1 * cm, 0.75 * cm, 0.75 * cm] + [0.9 * cm] * 21, sty))
    s.append(Spacer(1, 6))
    s.append(P("Semanas de 7 días calendario: S1 = días 1 a 7 desde el acta de inicio; S21 = días 141 a 147. "
               "La celda azul indica que la actividad se ejecuta en esa semana. Los días 148 a 150 son para la "
               "entrega de la obra al Municipio y no hacen parte del cronograma evaluado. Jornada: "
               + D.JORNADA, size=7, align=TA_JUSTIFY))
    s += bloque_firma()
    return s


# ------------------------------------------------------------------ APU
def apus():
    s = []
    # Mano de obra
    s += titulo("CÁLCULO DEL COSTO DE MANO DE OBRA – 2026")
    rows = [["Concepto", "% sobre salario"]] + [[n, f"{float(p)*100:.2f} %"] for n, p in D.PRESTACIONES]
    rows.append(["FACTOR PRESTACIONAL TOTAL", f"{float(D.PREST_TOTAL)*100:.2f} %"])
    s.append(tabla(rows, [9 * cm, 4 * cm], hdr_style() + [("FONT", (0, -1), (-1, -1), "VB", 7),
                                                           ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
    s.append(Spacer(1, 6))
    s.append(P(f"SMMLV 2026 = {pesos(D.SMMLV)} (Decreto 1469/2025). Auxilio de transporte = "
               f"{pesos(D.AUX_TRANSPORTE)} (Decreto 1470/2025), con cesantías, intereses y prima "
               f"(factor {float(D.AUX_FACTOR):.4f}). Horas por mes = 42 × 52 / 12 = {float(D.HORAS_MES):.2f} h "
               "(Ley 2101 de 2021).", size=8, align=TA_JUSTIFY))
    s.append(Spacer(1, 4))
    s.append(P("Costo mensual = salario × (1 + factor prestacional) + auxilio de transporte × 1,1766. "
               "Costo hora = costo mensual ÷ horas por mes.", size=8))
    s.append(Spacer(1, 6))
    rows = [["Cargo / cuadrilla", "× SMMLV", "Costo mensual", "Costo hora"]]
    for n, m in D.CARGOS:
        h = D.costo_hora(m)
        rows.append([n, n2(m), n0(h * D.HORAS_MES), n0(h)])
    for k, (n, v) in D.CUADRILLAS.items():
        rows.append([n, "", "", n0(v)])
    s.append(tabla(rows, [8 * cm, 2 * cm, 3.5 * cm, 3 * cm], hdr_style() + [("ALIGN", (1, 0), (-1, -1), "RIGHT")]))
    s += bloque_firma()
    for cod, a in D.APUS.items():
        s.append(PageBreak())
        s += [P("ANÁLISIS DE PRECIO UNITARIO (APU)", size=12, bold=True, align=TA_CENTER), Spacer(1, 6)]
        head = tabla([["ÍTEM", "DESCRIPCIÓN", "UNIDAD"], [cod, P(f"<b>{a['titulo']}</b>", size=9), a["und"]]],
                     [2 * cm, 12.5 * cm, 3.3 * cm], hdr_style() + [("FONT", (0, 1), (-1, 1), "VB", 9),
                                                                    ("ALIGN", (0, 0), (-1, -1), "CENTER")])
        s += [head, Spacer(1, 8)]
        filas, total, precio = D.calc_apu(cod)
        for g, gname in D.GRUPOS:
            sel = [f for f in filas if f[0] == g or (g == "E" and f[0] == "H")]
            if not sel:
                continue
            data = [[gname, "", "", "", "", ""],
                    ["Descripción", "Unidad", "Cantidad", "Desperdicio", "V. Unitario", "V. Parcial"]]
            for gg, d, u, q, w, v, parc in sel:
                data.append([P(d, size=7.5), u, f"{q:.3f}".replace(".", ","), f"{w*100:.0f} %",
                             n2(v), n2(parc)])
            sub = sum(f[6] for f in sel)
            data.append(["", "", "", "", "Subtotal", n2(sub)])
            sty = [("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), CAP),
                   ("FONT", (0, 0), (-1, 0), "VB", 8)] + hdr_style(1) + [
                ("ALIGN", (1, 2), (-1, -1), "RIGHT"), ("ALIGN", (1, 2), (1, -1), "CENTER"),
                ("FONT", (0, 2), (-1, -1), "V", 7.5), ("FONT", (0, -1), (-1, -1), "VB", 7.5)]
            s += [tabla(data, [7.2 * cm, 1.9 * cm, 1.7 * cm, 1.9 * cm, 2.4 * cm, 2.7 * cm], sty, repeat=0),
                  Spacer(1, 6)]
        tot = tabla([["COSTO DIRECTO TOTAL DEL APU", n2(total)],
                     ["PRECIO UNITARIO ADOPTADO (ajustado al peso)", pesos(precio)]],
                    [15.1 * cm, 2.7 * cm],
                    [("FONT", (0, 0), (-1, -1), "VB", 9), ("BACKGROUND", (0, 0), (-1, -1), AMA),
                     ("ALIGN", (1, 0), (1, -1), "RIGHT")], repeat=0)
        s += [tot, Spacer(1, 6),
              P("<b>Notas:</b> " + a["nota"] + " Herramienta menor = 5 % del costo de la mano de obra. "
                "El precio unitario no incluye AIU: Administración (15 %), Imprevistos (7 %) y Utilidad "
                "(2 %) se aplican sobre el costo directo total de la oferta. Costo de mano de obra según "
                "hoja de cálculo de prestaciones 2026.", size=7.5, align=TA_JUSTIFY)]
        s += bloque_firma()
    return s


# ------------------------------------------------------------------ índice sobre 1
def indice():
    items = [
        ("Carta de presentación (Anexo 1)", "3.1.1", "Incluida"),
        ("Documento de conformación de consorcio o UT (Anexo 2) – solo si aplica; NO subsanable", "3.1.3", "Adjuntar si aplica"),
        ("Garantía de seriedad: 10 % del presupuesto = " + pesos(r10()) + ", vigencia 6 meses", "3.1.4", "Adjuntar"),
        ("Idoneidad: matrícula profesional y certificado de vigencia (COPNIA)", "3.1.5", "Adjuntar"),
        ("Certificado de existencia y representación (máximo 30 días) o cédula", "3.1.6", "Adjuntar"),
        ("Experiencia específica (Anexo 3) con certificaciones", "3.1.7", "Incluido formato"),
        ("Capacidad financiera: patrimonio líquido mínimo 20 % = " + pesos(D.r0(Decimal(D.PRESUPUESTO_OFICIAL) * Decimal('0.2'))), "3.1.8", "Adjuntar"),
        ("RUP: Constructor, especialidad 04, grupo 08", "3.1.9", "Adjuntar"),
        ("RUT (DIAN), firmado", "3.1.11", "Adjuntar"),
        ("Antecedentes disciplinarios (Procuraduría)", "3.1.12", "Adjuntar"),
        ("Antecedentes fiscales (Contraloría)", "3.1.13", "Adjuntar"),
        ("Antecedentes judiciales (Policía Nacional; el TR dice DAS)", "3.1.14", "Adjuntar"),
        ("Programa de ejecución de los trabajos (Anexo 6)", "3.2.2 / 4.1.1.2", "Incluido"),
        ("Cronograma de actividades (Anexo 7)", "3.2.2 / 4.1.1.2", "Incluido"),
    ]
    data = [["No.", "Documento", "Numeral TR", "Estado", "Folios"]]
    for k, (a, b, c) in enumerate(items, 1):
        data.append([str(k), P(a, size=8), b, c, ""])
    s = [P("SOBRE No. 1 – ÍNDICE DE DOCUMENTOS", size=12, bold=True, align=TA_CENTER), Spacer(1, 8),
         tabla(data, [0.9 * cm, 10.2 * cm, 2.4 * cm, 2.8 * cm, 1.5 * cm],
               hdr_style() + [("FONT", (0, 1), (-1, -1), "V", 8), ("ALIGN", (2, 1), (-1, -1), "CENTER")]),
         Spacer(1, 8),
         P("La oferta económica (Anexo 4) va en el Sobre No. 2, en original y copia. Los APU y las hojas de vida "
           "del personal se entregan si el proponente queda en primer orden de elegibilidad (numeral 4.3).",
           size=8, italic=True)]
    return s


def build(path, story, marca=""):
    doc = Doc(path, marca=marca)
    doc.build(story)


s1 = rotulo("SOBRE No. 1") + [PageBreak()] + indice() + [PageBreak()] + carta() + \
     [NextPageTemplate("L"), PageBreak()] + anexo3() + [PageBreak()] + anexo6() + [PageBreak()] + anexo7()
build(f"{OUT}/SOBRE_1_Habilitantes_y_Programa.pdf", s1)
for m in ("ORIGINAL", "COPIA"):
    build(f"{OUT}/SOBRE_2_Oferta_Economica_{m}.pdf",
          rotulo(f"SOBRE No. 2 – {m}") + [PageBreak()] + oferta(), marca=m)
build(f"{OUT}/APU_3.06_4.05_7.01_12.02.pdf", apus())
print("pdf ok")
