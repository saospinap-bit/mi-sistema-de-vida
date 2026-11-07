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
AMA = colors.HexColor("#BDD7EE")
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
    def __init__(self, path, marca="", first="P", **kw):
        super().__init__(path, pagesize=letter, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                         topMargin=2.2 * cm, bottomMargin=1.6 * cm, **kw)
        self.marca = marca
        fp = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="p")
        lw, lh = landscape(letter)
        fl = Frame(1.2 * cm, 1.4 * cm, lw - 2.4 * cm, lh - 3.4 * cm, id="l")
        tp = [PageTemplate("P", [fp], onPage=self.deco, pagesize=letter),
              PageTemplate("L", [fl], onPage=self.deco, pagesize=landscape(letter))]
        if first == "L":
            tp.reverse()
            self.pagesize = landscape(letter)
        self.addPageTemplates(tp)

    def deco(self, c, doc):
        w, h = c._pagesize
        c.saveState()
        c.setFont("VB", 8)
        c.drawString(1.2 * cm, h - 1.0 * cm, D.ENTIDAD + "  –  " + D.LICITACION)
        c.setFont("V", 7)
        c.drawString(1.2 * cm, h - 1.4 * cm, "Proponente: " + D.PROPONENTE)
        if self.marca:
            c.setFont("VB", 11)
            c.setFillColor(colors.HexColor("#1F4E78"))
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
    for cc, nombre, its in D.CAPITULOS:
        data.append([cc + ".", nombre, "", "", "", ""])
        i = len(data) - 1
        sty += [("BACKGROUND", (0, i), (-1, i), CAP), ("FONT", (0, i), (-1, i), "VB", 7),
                ("SPAN", (1, i), (-1, i))]
        for cod in its:
            _, _, desc, und, q, vu = next(x for x in D.ITEMS if x[1] == cod)
            data.append([cod, P(desc, size=7), und, n2(q), n0(D.PRECIOS[cod]), n0(D.total_item(cod))])
        data.append([f"SUBTOTAL {cc}. {nombre}", "", "", "", "", n0(D.SUBTOTAL[cc])])
        i = len(data) - 1
        sty += [("SPAN", (0, i), (4, i)), ("ALIGN", (0, i), (4, i), "RIGHT"), ("FONT", (0, i), (-1, i), "VB", 7),
                ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#DEEAF6"))]
    sty = [("ALIGN", (3, 1), (-1, -1), "RIGHT"), ("ALIGN", (2, 1), (2, -1), "CENTER")] + sty
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
        f"_______________, póliza No. ________, valor asegurado <b>{pesos(D.POLIZA_VALOR)}</b> (10 % del "
        f"presupuesto oficial de {pesos(D.PRESUPUESTO_OFICIAL)}), vigencia de seis (6) meses: desde el "
        f"<b>{D.POLIZA_DESDE}</b> (fecha de cierre) hasta el <b>{D.POLIZA_HASTA}</b>.",
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
    smmlv_req = D.EXP_SMMLV
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
        f"Máximo 5 contratos con entidades estatales, ejecutados y terminados en los últimos 10 años "
        f"(entre el <b>{D.EXP_DESDE}</b> y el <b>{D.CIERRE}</b>, fecha de cierre), en edificaciones "
        "clasificables en la especialidad 04 del RUP.",
        f"Valor mínimo: 50 % del presupuesto oficial = 0,5 × {pesos(D.PRESUPUESTO_OFICIAL)} = "
        f"<b>{pesos(D.EXP_PESOS)}</b>.",
        f"En SMMLV 2025: {pesos(D.EXP_PESOS)} ÷ {pesos(D.SMMLV)} = <b>{n2(smmlv_req)} SMMLV</b>. La suma de "
        "los contratos, cada uno convertido con el SMMLV del año en que terminó, debe ser igual o mayor.",
        "Contratos en consorcio o unión temporal: se informa únicamente el valor correspondiente al "
        "porcentaje de participación y se adjunta el documento de conformación.",
        "Soporte: acta final de obra, acta de liquidación, o contrato con certificación de cumplimiento "
        "de la entidad, donde consten el tipo de obra, las cantidades y las fechas de inicio y terminación.",
    ]
    s += [P("• " + x, size=8, align=TA_JUSTIFY) for x in req]
    smm = [["Año", "SMMLV"]] + [[str(y), n0(v)] for y, v in D.SMMLV_ANIOS]
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
    s += titulo(f"CÁLCULO DEL COSTO DE MANO DE OBRA – {D.ANIO}")
    rows = [["Concepto", "% sobre salario"]] + [[n, f"{float(p)*100:.2f} %"] for n, p in D.PRESTACIONES]
    rows.append(["FACTOR PRESTACIONAL TOTAL", f"{float(D.PREST_TOTAL)*100:.2f} %"])
    s.append(tabla(rows, [9 * cm, 4 * cm], hdr_style() + [("FONT", (0, -1), (-1, -1), "VB", 7),
                                                           ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
    s.append(Spacer(1, 6))
    s.append(P(f"SMMLV {D.ANIO} = {pesos(D.SMMLV)} ({D.DEC_SMMLV}). Auxilio de transporte = "
               f"{pesos(D.AUX_TRANSPORTE)} ({D.DEC_AUX}), con cesantías, intereses y prima "
               f"(factor {float(D.AUX_FACTOR):.4f}). Horas por mes = {D.HORAS_SEMANA} × 52 / 12 = "
               f"{float(D.HORAS_MES):.2f} h "
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
                f"hoja de cálculo de prestaciones {D.ANIO}.", size=7.5, align=TA_JUSTIFY)]
        s += bloque_firma()
    return s


# ------------------------------------------------------------------ SOBRE 1
SECCIONES = [
    ("1", "Carta de presentación (Anexo 1)", "3.1.1"),
    ("2", "Carta de conformación de consorcio o unión temporal (Anexo 2)", "3.1.3"),
    ("3", "Garantía de seriedad de la oferta", "3.1.4"),
    ("4", "Cédulas de ciudadanía", "3.1.6"),
    ("5", "Certificado de Cámara de Comercio (existencia y representación legal)", "3.1.6"),
    ("6", "Experiencia específica (Anexo 3) y certificaciones", "3.1.7"),
    ("7", "Antecedentes disciplinarios (Procuraduría) y fiscales (Contraloría)", "3.1.12 y 3.1.13"),
    ("8", "Programa de ejecución de los trabajos (Anexo 6) y cronograma (Anexo 7)", "3.2.2 y 4.1.1.2"),
]


def indice():
    data = [["No.", "Documento", "Numeral TR", "Folios"]]
    for n, d, t in SECCIONES:
        data.append([n, P(d, size=9), t, ""])
    s = [P("SOBRE No. 1 – ÍNDICE DE DOCUMENTOS", size=12, bold=True, align=TA_CENTER), Spacer(1, 4),
         P(f"Fecha de cierre: <b>{D.CIERRE}</b>", size=9, align=TA_CENTER), Spacer(1, 10),
         tabla(data, [1 * cm, 11.3 * cm, 3 * cm, 2.5 * cm],
               hdr_style() + [("FONT", (0, 1), (-1, -1), "V", 9), ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                              ("ALIGN", (0, 1), (0, -1), "CENTER"), ("TOPPADDING", (0, 1), (-1, -1), 6),
                              ("BOTTOMPADDING", (0, 1), (-1, -1), 6)]),
         Spacer(1, 10),
         P("La oferta económica (Anexo 4) va en el Sobre No. 2, en original y copia. Los APU y las hojas de vida "
           "del personal se entregan si el proponente queda en primer orden de elegibilidad (numeral 4.3).",
           size=8, italic=True)]
    return s


def separador(num, titulo_, filas, nota=None):
    s = [Spacer(1, 1.5 * cm), P(f"SECCIÓN {num}", size=14, bold=True, align=TA_CENTER), Spacer(1, 4),
         P(titulo_.upper(), size=16, bold=True, align=TA_CENTER), Spacer(1, 1 * cm)]
    t = Table([[P(a, size=9, bold=True), P(b, size=9)] for a, b in filas], colWidths=[5 * cm, 12.8 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BACKGROUND", (0, 0), (0, -1), CAP), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    s.append(t)
    if nota:
        s += [Spacer(1, 10), P(nota, size=8, italic=True, align=TA_JUSTIFY)]
    s += [Spacer(1, 1 * cm), P("A continuación se adjuntan los documentos de esta sección.", size=9,
                                align=TA_CENTER, italic=True)]
    return s


def anexo2():
    j = dict(size=9.5, align=TA_JUSTIFY, lead=13)
    s = [P("ANEXO 2 – CARTA DE CONFORMACIÓN DE CONSORCIO O UNIÓN TEMPORAL", size=12, bold=True,
           align=TA_CENTER), Spacer(1, 4),
         P("Diligenciar solo si el proponente es plural. Si es persona natural o jurídica individual, "
           "escribir NO APLICA y firmar. Su falta o sus errores NO son subsanables (numeral 3.1.3).",
           size=8, italic=True, align=TA_CENTER), Spacer(1, 10),
         P(D.CIUDAD_FECHA, size=9.5), Spacer(1, 6),
         P("Señores<br/><b>ALCALDÍA DE SANDONÁ</b><br/>Sandoná – Nariño", size=9.5), Spacer(1, 6),
         P(f"<b>REFERENCIA:</b> {D.LICITACION}", size=9.5), Spacer(1, 6),
         P("Los suscritos, ______________________ identificado con C.C. No. __________ de __________, en nombre "
           "propio / en representación de ______________________, y ______________________ identificado con "
           "C.C. No. __________ de __________, en nombre propio / en representación de ______________________, "
           "manifestamos que hemos convenido asociarnos en (CONSORCIO / UNIÓN TEMPORAL) para participar en la "
           f"licitación de la referencia, cuyo objeto es “{D.OBJETO}”, y expresamos lo siguiente:", **j),
         Spacer(1, 6),
         P(f"1. La duración del (CONSORCIO / UNIÓN TEMPORAL) será igual al plazo de ejecución del contrato "
           f"(5 meses) y dos (2) años más, es decir, como mínimo hasta el <b>{D.DURACION_CONSORCIO}</b>.", **j),
         P("2. Está integrado por:", **j), Spacer(1, 4)]
    t = tabla([["Nombre del integrante", "NIT / C.C.", "Participación (%)", "Actividades a cargo (solo UT)"],
               ["", "", "", ""], ["", "", "", ""], ["TOTAL", "", "100 %", ""]],
              [5.5 * cm, 3.2 * cm, 3 * cm, 6.1 * cm], hdr_style())
    t.setStyle(TableStyle([("ROWHEIGHT", (0, 1), (-1, 2), 22), ("FONT", (0, 3), (-1, 3), "VB", 8)]))
    s += [t, Spacer(1, 6)]
    for x in [
        "3. Se denomina: ______________________________________.",
        "4. La responsabilidad de los integrantes es solidaria (artículo 7 de la Ley 80 de 1993). En la unión "
        "temporal, las sanciones por incumplimiento se impondrán según la participación de cada integrante en la "
        "ejecución; los términos y la extensión de la participación no podrán modificarse sin el consentimiento "
        "previo de la entidad.",
        "5. El representante es ______________________, identificado con C.C. No. __________ de __________, "
        "expresamente facultado para firmar y presentar la oferta y, en caso de adjudicación, firmar el contrato "
        "y tomar todas las determinaciones necesarias para su ejecución y liquidación.",
        "6. Sede: dirección ____________________, correo ____________________, teléfono ______________.",
        "En constancia se firma en ______________, a los ___ días del mes de noviembre de 2025.",
    ]:
        s += [P(x, **j), Spacer(1, 3)]
    f = Table([["______________________", "______________________", "______________________"],
               ["Integrante 1", "Integrante 2", "Representante"]], colWidths=[5.9 * cm] * 3)
    f.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "V", 9), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    s += [Spacer(1, 26), f]
    return s


def garantia():
    s = [P("SECCIÓN 3 – GARANTÍA DE SERIEDAD DE LA OFERTA", size=12, bold=True, align=TA_CENTER), Spacer(1, 4),
         P("Numeral 3.1.4 de los TR", size=9, align=TA_CENTER), Spacer(1, 10)]
    filas = [
        ("Tipo", "Póliza de seriedad de la oferta (compañía de seguros vigilada por la Superintendencia "
                 "Financiera) o garantía bancaria"),
        ("Tomador / afianzado", f"{D.PROPONENTE} – {D.NIT}. Si es consorcio o UT: a nombre del consorcio o UT "
                                "con la indicación de todos sus integrantes y su porcentaje"),
        ("Asegurado / beneficiario", "MUNICIPIO DE SANDONÁ – NARIÑO"),
        ("Proceso y objeto", f"{D.LICITACION} – {D.OBJETO}"),
        ("Base de cálculo", f"Presupuesto oficial (formulario Excel): {pesos(D.PRESUPUESTO_OFICIAL)}"),
        ("VALOR ASEGURADO", f"<b>10 % × {pesos(D.PRESUPUESTO_OFICIAL)} = {pesos(D.POLIZA_VALOR)}</b>"),
        ("VIGENCIA", f"<b>Seis (6) meses: desde el {D.POLIZA_DESDE} (fecha de cierre) hasta el "
                     f"{D.POLIZA_HASTA}</b>"),
        ("Riesgos amparados", "Retiro de la oferta después del cierre; no firma del contrato dentro de los 5 días "
                              "hábiles siguientes a la adjudicación; documentos falsos u ocultamiento de "
                              "información o de inhabilidades"),
        ("Cláusula de indemnidad", "Artículo 6 del Decreto 4828 de 2008 (el pliego dice 4820 de 2004), "
                                   "modificado por el Decreto 931 de 2009"),
        ("Aseguradora", "______________________________"),
        ("Póliza No.", "______________________________"),
        ("Fecha de expedición", "______________________________ (no posterior al cierre)"),
    ]
    t = Table([[P(a, size=9, bold=True), P(b, size=9)] for a, b in filas], colWidths=[4.5 * cm, 13.3 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.black), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("BACKGROUND", (0, 0), (0, -1), CAP), ("BACKGROUND", (0, 5), (-1, 6), AMA),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    s += [t, Spacer(1, 10),
          P("Adjuntar a continuación: póliza original firmada por el tomador, sus condiciones generales y el "
            "recibo o certificado de pago de la prima. Revisar que el valor, la vigencia, el beneficiario y el "
            "número del proceso coincidan exactamente con este cuadro.", size=8.5, align=TA_JUSTIFY)]
    return s


def sobre1():
    st_ = rotulo("SOBRE No. 1") + [PageBreak()] + indice() + [PageBreak()]
    st_ += separador("1", "Carta de presentación", [("Numeral TR", "3.1.1 – Anexo 1"),
                                                     ("Firma", "Representante legal del proponente")])
    st_ += [PageBreak()] + carta() + [PageBreak()]
    st_ += separador("2", "Carta de consorcio / unión temporal",
                     [("Numeral TR", "3.1.3 – Anexo 2"),
                      ("Duración mínima", f"Plazo del contrato + 2 años: hasta el {D.DURACION_CONSORCIO}"),
                      ("Ojo", "No es subsanable. Si el proponente es individual, se marca NO APLICA")])
    st_ += [PageBreak()] + anexo2() + [PageBreak()] + garantia() + [PageBreak()]
    st_ += separador("4", "Cédulas de ciudadanía", [
        ("Numeral TR", "3.1.6"),
        ("De quién", "Persona natural: el proponente. Persona jurídica: el representante legal. "
                     "Consorcio o UT: cada integrante persona natural y cada representante legal, y el "
                     "representante del consorcio o UT"),
        ("Cómo", "Fotocopia ampliada al 150 %, por ambas caras, legible"),
    ])
    st_ += [PageBreak()] + separador("5", "Certificado de Cámara de Comercio", [
        ("Numeral TR", "3.1.6"),
        ("Fecha de expedición", f"No mayor a 30 días antes del cierre: expedido entre el {D.CAMARA_DESDE} y "
                                f"el {D.CIERRE}"),
        ("Objeto social", "Debe incluir la construcción de obras civiles / edificaciones"),
        ("Duración de la sociedad", f"Como mínimo el plazo del contrato + 1 año: hasta el {D.DURACION_SOCIEDAD} "
                                    "o después"),
        ("Representante legal", "Si tiene límites para contratar, adjuntar la autorización de la junta o asamblea"),
        ("Consorcio o UT", "Un certificado por cada integrante que sea persona jurídica"),
    ], "Si el proponente es persona natural no aplica el certificado de existencia y representación; basta la "
       "cédula (sección 4).")
    st_ += [NextPageTemplate("L"), PageBreak()] + anexo3()
    st_ += [NextPageTemplate("P"), PageBreak()] + separador("6", "Certificaciones de experiencia", [
        ("Qué adjuntar", "Por cada contrato del Anexo 3: acta final de obra, acta de liquidación, o copia del "
                         "contrato con certificación de cumplimiento de la entidad contratante"),
        ("Deben decir", "Tipo de obra, cantidades de obra, fechas de inicio y terminación y valor"),
        ("Periodo", f"Contratos terminados entre el {D.EXP_DESDE} y el {D.CIERRE}"),
        ("Valor mínimo", f"{pesos(D.EXP_PESOS)} = {n2(D.EXP_SMMLV)} SMMLV de 2025"),
        ("Consorcio o UT", "Adjuntar el documento de conformación para acreditar el porcentaje de participación"),
    ])
    st_ += [PageBreak()] + separador("7", "Antecedentes disciplinarios y fiscales", [
        ("Disciplinarios", "Certificado de la Procuraduría General de la Nación (www.procuraduria.gov.co), "
                           "numeral 3.1.12"),
        ("Fiscales", "Certificado de la Contraloría General de la República de no figurar en el Boletín de "
                     "Responsables Fiscales (www.contraloria.gov.co), numeral 3.1.13"),
        ("De quién", "Persona natural: el proponente. Persona jurídica: la empresa (NIT) y su representante "
                     "legal. Consorcio o UT: cada integrante"),
        ("Vigencia", f"Vigentes a la fecha de cierre ({D.CIERRE}). Se recomienda descargarlos en la semana "
                     "del cierre"),
    ], "Ambos certificados son gratuitos y se descargan en línea con el número de cédula o NIT.")
    st_ += [PageBreak()] + separador("8", "Programa de ejecución de los trabajos", [
        ("Numeral TR", "3.2.2 y 4.1.1.2 – evaluación de calidad, hasta 200 puntos"),
        ("a. Secuencia y duración", "Las 85 actividades del presupuesto oficial con su duración"),
        ("b. Inicio y fin", "Día de inicio y día de terminación de cada actividad"),
        ("c. Duración total", "5 meses: 21 semanas = 147 días + 3 días para la entrega"),
        ("d. Jornada de trabajo", D.JORNADA),
        ("Formatos", "Anexo 6 (programación de obra) y Anexo 7 (cronograma)"),
    ])
    st_ += [NextPageTemplate("L"), PageBreak()] + anexo6() + [PageBreak()] + anexo7()
    return st_


def build(path, story, marca="", first="P"):
    doc = Doc(path, marca=marca, first=first)
    doc.build(story)


build(f"{OUT}/SOBRE_1_Documentos_Habilitantes.pdf", sobre1())
build(f"{OUT}/PROGRAMA_DE_OBRA_Anexos_6_y_7.pdf", anexo6() + [PageBreak()] + anexo7(), first="L")
for m in ("ORIGINAL", "COPIA"):
    build(f"{OUT}/SOBRE_2_Oferta_Economica_{m}.pdf",
          rotulo(f"SOBRE No. 2 – {m}") + [PageBreak()] + oferta(), marca=m)
build(f"{OUT}/APU_3.06_4.05_7.01_12.02.pdf", apus())
print("pdf ok")
