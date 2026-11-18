"""Genera el informe en Word (markdown -> pandoc -> docx con ecuaciones nativas) y lo formatea.

Todos los numeros salen de calculos.py (motor EPANET 2.0.12). Se arma en dos pasadas para que
las referencias a figuras y tablas ("Figura 6", "Tabla 15") tengan el numero correcto.
"""
import os
import subprocess

import pypandoc
from docx import Document
from docx.enum.section import WD_SECTION  # noqa: F401
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import calculos as C
import figuras as FG
import modelo as M
import motor

SALIDA = os.path.join(M.BASE, "Informe_Taller1_EPANET_WaterGEMS.docx")
PANDOC = pypandoc.get_pandoc_path()
AZUL = RGBColor(0x1F, 0x4E, 0x79)
J = C.J


def f(x, d=2):
    return f"{x:.{d}f}"


def hh(t):
    return motor.hhmm(t)


def hs(t):
    return motor.hhmmss(t)


def lista_horas(hs_):
    """[7, 8, 14] -> '7, 8 y 14 h'."""
    s = [str(h) for h in hs_]
    return (", ".join(s[:-1]) + " y " + s[-1] if len(s) > 1 else s[0]) + " h"


def horas_extremo(serie, valor):
    """Pasos en que la serie vale lo mismo que el extremo (a 2 decimales), agrupando pasos seguidos."""
    idx = list(serie.index)
    pos = [k for k, v in enumerate(serie.values) if round(float(v), 2) == round(float(valor), 2)]
    grupos, g = [], [pos[0]]
    for k in pos[1:]:
        if k == g[-1] + 1:
            g.append(k)
        else:
            grupos.append(g)
            g = [k]
    grupos.append(g)
    partes = []
    for g in grupos:
        if len(g) >= 3:
            partes.append(f"{hh(idx[g[0]])}–{hh(idx[g[-1]])}")
        else:
            partes.extend(hh(idx[k]) for k in g)
    return partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " y " + partes[-1]


class Doc:
    """Acumula markdown y numera figuras y tablas en orden de aparicion."""

    def __init__(self, nums=None):
        self.out, self.nums, self.tabfmt = [], nums or {}, []
        self.orden = []

    def add(self, *bloques):
        """Cada argumento es un bloque (parrafo, ecuacion, titulo) separado por una linea en blanco."""
        for b in bloques:
            self.out.extend([b, ""])

    def lineas(self, *s):
        """Lineas seguidas sin linea en blanco (tablas, listas compactas, bloques especiales)."""
        self.out.extend(s)
        self.out.append("")

    def lista(self, *items):
        self.lineas(*[f"- {x}" for x in items])

    def numerada(self, *items):
        self.lineas(*[f"{i}. {x}" for i, x in enumerate(items, 1)])

    def F(self, k):
        return f"Figura {self.nums.get(('fig', k), '?')}"

    def T(self, k):
        return f"Tabla {self.nums.get(('tab', k), '?')}"

    def fig(self, k, path, cap, w=16):
        self.orden.append(("fig", k))
        n = sum(1 for t, _ in self.orden if t == "fig")
        self.add(f"![**Figura {n}.** {cap}]({path}){{width={w}cm}}")

    def tab(self, k, head, rows, cap, widths, size=9, align=None):
        self.orden.append(("tab", k))
        n = sum(1 for t, _ in self.orden if t == "tab")
        align = align or (["l"] + ["c"] * (len(head) - 1))
        sep = {"l": ":---", "c": ":---:", "r": "---:"}
        esc = lambda x: str(x).replace("|", "\\|")
        lines = ["| " + " | ".join(esc(h) for h in head) + " |",
                 "|" + "|".join(sep[a] for a in align) + "|"]
        lines += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
        self.lineas(*lines)
        self.add(f"Table: **Tabla {n}.** {cap}")
        self.tabfmt.append((widths, size))

    def nota(self, texto, estilo="Nota"):
        self.lineas(f'::: {{custom-style="{estilo}"}}', texto, ":::")

    def xml(self, x):
        self.lineas("```{=openxml}", x, "```")

    def salto(self):
        self.xml('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def md(self):
        return "\n".join(self.out)

    def numeros(self):
        cont, nums = {"fig": 0, "tab": 0}, {}
        for t, k in self.orden:
            cont[t] += 1
            nums[(t, k)] = cont[t]
        return nums


TOC = ('<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>Contenido</w:t></w:r></w:p>'
       '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
       '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
       '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
       '<w:r><w:t>Si no ve la tabla de contenido: clic derecho aquí y elija «Actualizar campo».</w:t></w:r>'
       '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')


def portada(D):
    D.nota("UNIVERSIDAD NACIONAL DE COLOMBIA\\\nFACULTAD DE INGENIERÍA\\\nDEPARTAMENTO DE INGENIERÍA CIVIL",
           "Institucion")
    D.nota("Taller 1: Simulación de sistemas de distribución", "Title")
    D.nota("Modelación de una red con bomba, tanque y válvulas reductoras de presión en EPANET 2.0 y WaterGEMS",
           "Subtitle")
    D.nota("**Profesor:** Ing. Rafael O. Ortiz M.\\\n**Integrantes:** [Nombre 1 – código] · [Nombre 2 – código]",
           "Portada")
    D.nota("Segundo semestre de 2026", "Portada")
    D.salto()
    D.xml(TOC)
    D.salto()


def resumen(D, R):
    e1, e2, e3, X = R["E1"], R["E2"], R["E3"], R["X"]
    caida = (e1["nudos"]["p"].round(2) - e2["nudos"]["p"].round(2))[["J-1", "J-2", "J-5", "J-6", "J-7", "J-8"]]
    ext = e3["ext"]
    nmin, nmax = ext["pmin"].idxmin(), ext["pmax"].idxmax()
    ahorro = 100 * (1 - R["rec"]["R3"]["eps"]["energia"] / e3["energia"])
    D.add("# Resumen")
    D.add("Se modeló la red del taller: reservorio R-1, bomba PMP-1, ocho nudos de demanda, tanque T-1, tres "
          "válvulas reductoras de presión (PRV) y dieciséis tuberías de hierro fundido con $C = 100$. Los tres "
          "escenarios pedidos se calcularon con el motor de EPANET 2.0 (versión 2.00.12) y se repitieron con "
          "EPANET 2.2. Las dos versiones dan los mismos resultados (diferencias menores que 0.0001 m y 0.0001 L/s). "
          "El informe incluye el procedimiento para construir el mismo modelo en WaterGEMS y los valores de control "
          "para comparar los dos programas.")
    b = e1["bomba"]
    D.lista(f"**Escenario 1 (sin P-16).** La bomba entrega {f(b['Q'])} L/s, igual a la demanda total, con una altura "
          f"de {f(b['H'])} m. Las presiones van de {f(e1['nudos']['p'].min())} m (J-3 y J-4) a "
          f"{f(e1['nudos']['p'].max())} m (J-1).",
          f"**Escenario 2 (tanque en servicio).** Con el agua del tanque en 320 m, a T-1 entran {f(e2['T_Q'])} L/s. "
          f"La bomba pasa a {f(e2['bomba']['Q'])} L/s y {f(e2['bomba']['H'])} m, y las presiones de la zona alta "
          f"bajan entre {f(caida.min())} y {f(caida.max())} m.",
          f"**Escenario 3 (periodo extendido de 24 h).** El tanque se llena a las {hs(e3['t_lleno'])} h y queda "
          f"aislado el resto del día. La presión mínima es {f(ext['pmin'].min())} m ({nmin}, "
          f"{hh(ext.loc[nmin, 'tmin'])} h) y la máxima {f(ext['pmax'].max())} m ({nmax}, {hh(ext.loc[nmax, 'tmax'])} h).",
          "En los tres escenarios PRV-2 y PRV-3 están activas y fijan una HGL de 286.50 m en la zona baja "
          "(J-3 y J-4). PRV-1 permanece cerrada porque su consigna (285.0 m) es menor que esa HGL.",
          "Todas las presiones superan el mínimo de 15 m de la Resolución 0330 de 2017, pero la red supera la "
          "presión estática máxima de 50 m del artículo 62.")
    D.add("Las recomendaciones del final se comprobaron con simulaciones adicionales. Con la consigna de PRV-1 en "
          "286.5 m trabajan las tres válvulas; con las tres consignas en 285.0 m la zona baja queda en 50 m; y un "
          "control de la bomba por nivel del tanque hace que el tanque regule el consumo y reduce la energía "
          f"hidráulica de bombeo en {ahorro:.1f} %.")


def objetivo(D):
    D.add("# 1. Objetivo")
    D.add("Utilizar los programas de cálculo de redes para simular la red del enunciado:")
    D.numerada("Simular con EPANET 2.0 los escenarios propuestos.", "Simular con WaterGEMS los escenarios propuestos.")
    D.tab("esc", ["Escenario", "Condición del enunciado", "Tipo de análisis"],
          [["1", "No se tiene en cuenta la tubería P-16 (tanque fuera de servicio)", "Estático"],
           ["2", "El tanque T-1 entra en funcionamiento", "Estático"],
           ["3", "Curvas de consumo residencial y comercial en los nudos de demanda", "Periodo extendido (24 h)"]],
          "Escenarios de simulación.", [2.2, 9.5, 4.3], align=["c", "l", "l"])


def datos(D, P):
    D.add("# 2. Descripción del sistema y datos de entrada")
    D.add("El reservorio R-1 (nivel 290 m) abastece la red. La bomba PMP-1, a cota 288 m, impulsa el agua por la "
          "línea P-2 (1525 m, 300 mm) hasta el nudo J-1. Desde J-1 la red forma dos mallas en la zona alta (J-1, J-6, "
          "J-5, J-8 y J-7). La zona baja (J-3 y J-4, cota 235 m) se alimenta a través de tres válvulas reductoras de "
          "presión (PRV), y J-2 queda entre J-1 y PRV-1. El tanque T-1 se conecta al nudo J-7 por la tubería P-16. "
          "Todas las tuberías son de hierro fundido con coeficiente de Hazen-Williams $C = 100$. "
          f"La {D.F('red')} muestra el esquema y las Tablas {D.T('nudos')[6:]} a {D.T('patrones')[6:]} reúnen los datos.")
    D.fig("red", P["red"], "Esquema de la red con los datos de entrada (topología del enunciado).", 16.5)
    uso = {"RES": "Residencial", "COM": "Comercial", "": "Sin curva asignada"}
    rows = [[j, z, f(q, 1), uso[u]] for j, (z, q, u) in M.JUNCTIONS.items()]
    rows.append(["**Total**", "", f"**{f(sum(q for z, q, u in M.JUNCTIONS.values()), 1)}**", ""])
    D.tab("nudos", ["Nudo", "Elevación (m)", "Demanda base (L/s)", "Uso (Escenario 3)"], rows,
          "Datos de los nudos.", [2.5, 3.2, 3.6, 4.5])
    D.tab("tubos", ["Tubo", "Nudo inicial", "Nudo final", "Longitud (m)", "Diámetro (mm)", "C (H-W)"],
          [[p, C.nom(a), C.nom(b), L, d, M.C_HW] for p, (a, b, L, d) in M.PIPES.items()],
          "Datos de las tuberías. El sentido inicial → final es el de dibujo; el sentido real del flujo sale del cálculo.",
          [2.0, 2.8, 2.8, 2.8, 2.8, 2.2], size=8.5)
    D.tab("prv", ["Válvula", "Elevación (m)", "Diámetro (mm)", "HGL de consigna (m)", "Dirección de flujo"],
          [[v, z, d, f(h, 1), f"{a} → {b}"] for v, (_, _, z, d, h) in M.PRVS.items()
           for a, b in [M.PRV_TUBOS[v]]],
          "Datos de las válvulas reductoras de presión.", [2.4, 2.8, 2.8, 3.6, 3.8])
    D.tab("bomba", ["Punto", "Caudal Q (L/s)", "Carga H (m)"],
          [[n, f(q, 1), f(h, 1)] for n, (q, h) in zip(["Cierre (shutoff)", "Diseño", "Máxima operación"], M.PUMP_CURVE)],
          "Curva característica de la bomba PMP-1 (elevación 288 m).", [5.0, 3.6, 3.6])
    t = M.TANK
    D.tab("tanque", ["Elemento", "Dato", "Valor"],
          [["Reservorio R-1", "Elevación del agua", "290 m"],
           ["Tanque T-1", "Elevación de la base (fondo)", f"{t['base']} m"],
           ["", "Elevación mínima / inicial / máxima", f"{t['base'] + t['min']} / {t['base'] + t['init']} / {t['base'] + t['max']} m"],
           ["", "Diámetro (sección circular)", f"{t['diam']} m"],
           ["", "Área de la sección (calculada)", f"{f(C.A_T)} m²"],
           ["", "Volumen entre 320 y 326 m (calculado)", f"{f(C.A_T * 6, 1)} m³"]],
          "Datos del reservorio y del tanque.", [3.4, 6.4, 4.6], align=["l", "l", "c"])


def datos_patrones(D, R, P):
    X = R["X"]
    h1, h2 = list(range(0, 13)), list(range(13, 25))
    res, com = M.RES + [M.RES[0]], M.COM + [M.COM[0]]
    rows = [["Residencial"] + [f(res[h], 1) for h in h1], ["Comercial"] + [f(com[h], 1) for h in h1],
            ["**Hora**"] + [f"**{h}**" for h in h2] + [""],
            ["Residencial"] + [f(res[h], 1) for h in h2] + [""], ["Comercial"] + [f(com[h], 1) for h in h2] + [""]]
    D.tab("patrones", ["Hora"] + [str(h) for h in h1], rows,
          "Curvas de consumo (multiplicadores del caudal medio). Uso residencial: J-1, J-2, J-3 y J-7. "
          "Uso comercial: J-4, J-5 y J-8. La hora 24 es igual a la hora 0.",
          [2.1] + [1.05] * 13, size=8)
    D.add("Los multiplicadores se leyeron de la gráfica del enunciado midiendo la posición de cada marcador. Todas las "
          f"lecturas quedan a menos de {f(X['graf_dif'])} de un múltiplo de 0.1, así que se usaron con un decimal. "
          f"Los promedios diarios son {f(X['m_res'], 3)} (residencial) y {f(X['m_com'], 3)} (comercial), menores que 1.")
    D.fig("patrones", P["patrones"], "Curvas de consumo tal como entran al modelo (multiplicador constante durante "
          "cada hora).", 14)
    D.add(f"Los nudos residenciales y los comerciales suman la misma demanda base, {f(X['q_res'], 1)} L/s cada grupo, "
          "y J-6 aporta 5.0 L/s constantes. Por eso la demanda total del Escenario 3 depende solo de la suma de los dos "
          "multiplicadores:")
    D.add(f"$$q_{{total}}(t) = {f(X['q_res'], 1)}\\,\\left[M_R(t) + M_C(t)\\right] + 5.0 \\quad \\text{{(L/s)}}$$")


def teoria(D):
    D.add("# 3. Fundamento teórico y criterios de modelación", "## 3.1 Ecuaciones de la red")
    D.add("EPANET y WaterGEMS resuelven la red con el método del gradiente (Todini y Pilati, 1988), que plantea a la vez "
          "la continuidad en los nudos y la conservación de la energía en los tramos. Es el método que exige el "
          "numeral 2 del artículo 57 de la Resolución 0330 de 2017.")
    D.add("Continuidad en cada nudo $i$, con $q_i$ la demanda del nudo:",
          "$$\\sum_{j} Q_{ji} - \\sum_{k} Q_{ik} = q_i$$",
          "Energía en cada tubería entre los nudos $i$ y $j$, con $H$ la altura piezométrica (HGL):",
          "$$H_i - H_j = h_{f,ij}$$",
          "Pérdida por fricción de Hazen-Williams en unidades SI ($h_f$ y $L$ en m, $Q$ en m³/s, $D$ en m):",
          "$$h_f = \\frac{10.67\\, L\\, Q^{1.852}}{C^{1.852}\\, D^{4.871}}$$",
          "La presión en cada nudo es la diferencia entre la HGL y la cota:",
          "$$p_i = H_i - z_i$$",
          "No se consideraron pérdidas menores porque el enunciado no da coeficientes.")


def teoria_2(D):
    q1, h1 = M.PUMP_CURVE[1]
    q2, h2 = M.PUMP_CURVE[2]
    D.add("## 3.2 Curva de la bomba")
    D.add("Con tres puntos, EPANET y WaterGEMS (definición *Standard (3 Point)*) ajustan la curva $H_b = A - B\\,Q^{C}$, "
          "con $A$ igual a la carga de cierre. Los coeficientes salen de los otros dos puntos:",
          f"$$A = H_0 = {f(C.A_P, 1)} \\text{{ m}}$$",
          f"$$C = \\frac{{\\ln\\left(\\dfrac{{A - H_2}}{{A - H_1}}\\right)}}{{\\ln\\left(\\dfrac{{Q_2}}{{Q_1}}\\right)}}"
          f" = \\frac{{\\ln\\left(\\dfrac{{{C.A_P} - {h2}}}{{{C.A_P} - {h1}}}\\right)}}{{\\ln\\left(\\dfrac{{{q2}}}{{{q1}}}\\right)}}"
          f" = {f(C.C_P, 4)}$$",
          f"$$B = \\frac{{A - H_1}}{{Q_1^{{C}}}} = \\frac{{{C.A_P} - {h1}}}{{{q1}^{{{f(C.C_P, 4)}}}}} = {f(C.B_P, 6)}$$",
          f"La curva queda $H_b = {f(C.A_P, 1)} - {f(C.B_P, 6)}\\,Q^{{{f(C.C_P, 4)}}}$, con $Q$ en L/s y $H_b$ en m, y pasa "
          f"exactamente por los tres puntos del enunciado ({D.F('bomba')}). La potencia hidráulica que entrega la bomba es "
          "$P = \\gamma\\,Q\\,H_b$, con $\\gamma = 9.81$ kN/m³.")
    D.add("## 3.3 Válvulas reductoras de presión (PRV)")
    D.add("Una PRV impide que la HGL aguas abajo supere su consigna. Puede estar en tres estados:")
    D.lista("**Activa:** estrangula el flujo y la HGL de salida es igual a la consigna.",
            "**Abierta:** la HGL aguas arriba es menor que la consigna; la válvula no estrangula y actúa como un tramo abierto.",
            "**Cerrada:** la HGL aguas abajo es mayor que la consigna o que la HGL aguas arriba. La válvula no deja pasar "
            "flujo, tampoco en sentido inverso.")
    D.add("En EPANET la consigna de una PRV es una presión. La HGL del enunciado se convierte con la cota de la válvula:",
          "$$p_{set} = H_{set} - z_v$$",
          "$$p_{set,\\,PRV\\text{-}1} = 285.0 - 250 = 35.0 \\text{ m} \\qquad "
          "p_{set,\\,PRV\\text{-}2} = p_{set,\\,PRV\\text{-}3} = 286.5 - 253 = 33.5 \\text{ m}$$",
          "En WaterGEMS se puede ingresar la HGL directamente (*Setting Type = Hydraulic Grade*).")
    D.add("## 3.4 Tanque y periodo extendido")
    D.add("El tanque es cilíndrico, con área",
          f"$$A_T = \\frac{{\\pi D^2}}{{4}} = \\frac{{\\pi\\,(15)^2}}{{4}} = {f(C.A_T)} \\text{{ m}}^2$$",
          "En el periodo extendido el nivel se actualiza con el balance de volumen, donde $Q_T$ es el caudal neto que entra "
          "al tanque:",
          "$$\\frac{dH_T}{dt} = \\frac{Q_T}{A_T}$$",
          f"El volumen entre el nivel inicial (320 m) y el máximo (326 m) es $A_T \\cdot 6 = {f(C.A_T * 6, 1)}$ m³. Cuando el "
          "tanque llega al nivel máximo, el programa cierra la tubería de entrada para que no se desborde. La demanda de "
          "cada nudo en el instante $t$ es",
          "$$q_i(t) = q_{i,base} \\cdot M(t)$$",
          "con $M(t)$ el multiplicador de la curva de consumo, constante durante cada hora.")


def supuestos(D):
    D.add("## 3.5 Supuestos adoptados")
    D.lista("**Escenario 1:** la tubería P-16 se deja cerrada. Equivale a desactivar P-16 y T-1 en WaterGEMS; el tanque "
            "queda aislado.",
            "**Escenario 2:** el estado estático es la condición en $t = 0$, con el agua del tanque en su elevación inicial "
            "(320 m).",
            "**Escenario 3:** parte del Escenario 2 (tanque en servicio, 320 m). Dura 24 h, con paso hidráulico y de "
            "patrón de 1 h. El valor de la gráfica en la hora $h$ se aplica durante el intervalo $[h,\\ h+1)$, y la hora 24 "
            "coincide con la hora 0.",
            "EPANET 2.0 solo admite curvas de consumo escalonadas. En WaterGEMS se usa el mismo formato (*Stepwise*) para "
            "que los dos programas resuelvan el mismo problema.",
            "El enunciado no asigna curva de consumo al nudo J-6 (5.0 L/s), así que se modeló con demanda constante. La "
            "sección 7.4 evalúa la alternativa de asignarle uso residencial.",
            "La bomba es de velocidad fija y opera las 24 h, porque el enunciado no da reglas de control.",
            "Unidades SI con caudal en L/s y fórmula de Hazen-Williams. Precisión de cálculo 0.0001 con hasta 200 "
            "iteraciones.")


def construccion(D):
    D.add("# 4. Construcción de los modelos", "## 4.1 EPANET 2.0")
    D.numerada("*Project → Defaults → Hydraulics:* Flow Units = LPS y Headloss Formula = H-W.",
               "En EPANET la bomba y las válvulas son enlaces, así que cada una necesita un nudo a cada lado. Se crearon "
               "nudos auxiliares sin demanda: PMP-1-S y PMP-1-D (succión y descarga, cota 288 m) y PRV-x-A y PRV-x-B "
               "(entrada y salida, a la cota de cada válvula). Las tuberías conservan las longitudes de la "
               f"{D.T('tubos')}, así que la hidráulica es la misma del esquema.",
               f"**Bomba:** curva BOMBA-1 de tres puntos ({D.T('bomba')}). El editor de curvas muestra la ecuación "
               f"ajustada, $H = 48.80 - 0.02191\\,Q^{{1.46}}$.",
               "**PRV:** Setting = 35.0 m (PRV-1), 33.5 m (PRV-2) y 33.5 m (PRV-3), con *Start Node* aguas arriba "
               f"según la {D.T('prv')}.",
               "**Tanque:** Elevation = 308 m, Initial Level = 12 m, Minimum Level = 6 m, Maximum Level = 18 m "
               "(niveles medidos desde el fondo) y Diameter = 15 m.",
               "**Escenario 1:** P-16 con Initial Status = Closed. **Escenarios 2 y 3:** Open.",
               "**Escenario 3:** *Times* con Total Duration = 24 h y Hydraulic y Pattern Time Step = 1:00. Patrones "
               "RESIDENCIAL y COMERCIAL de 24 multiplicadores, asignados en el campo *Demand Pattern* de cada nudo.")
    D.nota("No llame «1» a ningún patrón. EPANET aplica el patrón «1» por defecto a todo nudo que no tenga patrón "
           "(*Options → Hydraulics → Default Pattern*), y J-6 tomaría esa curva sin que se la asigne.")
    D.add("Los archivos listos para abrir en EPANET 2.0 están en la carpeta `modelos/` (Anexo A).")
    D.add("## 4.2 WaterGEMS")
    D.add("El procedimiento detallado está en el Anexo B. Las diferencias con EPANET son:")
    D.lista("La bomba y las PRV son nodos. Las tuberías P-1 a P-16 se conectan directamente a ellos y no hacen falta "
            "nudos auxiliares. El sentido se define con la propiedad *Downstream Pipe*: P-2 para la bomba, y P-5, P-7 y "
            "P-15 para las válvulas.",
            "La consigna de la PRV se ingresa como HGL (*Hydraulic Grade Setting*): 285.0, 286.5 y 286.5 m.",
            "La bomba se define como *Standard (3 Point)*, que usa la misma ecuación $H = A - BQ^C$.",
            "Los tres escenarios caben en un solo archivo, con alternativas de topología activa (P-16 y T-1 activos o "
            "no) y de demanda (con o sin curvas) y dos opciones de cálculo (Steady State y EPS).",
            "Las curvas de consumo deben usar el formato *Stepwise* para que los resultados coincidan con EPANET.")


def tablas_estatico(D, S, n):
    """Tablas de nudos, tuberias, bomba y PRV de un escenario estatico (n = '1' o '2')."""
    nd = S["nudos"]
    rows = [[j, f"{r['z']:.0f}", f(r["q"]), f(r["H"]), f(r["p"])] for j, r in nd.iterrows()]
    rows.append(["R-1 (reservorio)", "—", f"{f(S['R_Q'])} (sale)", "290.00", "—"])
    t1 = "fuera de servicio" if S["P16_estado"] == "Cerrada" else f"{f(S['T_Q'])} (entra)"
    rows.append(["T-1 (tanque)", "308", t1, f(S["T_H"]), f"{f(S['T_nivel'])} (nivel)"])
    D.tab(f"n{n}", ["Nudo", "Cota z (m)", "Demanda (L/s)", "HGL (m)", "Presión (m)"], rows,
          f"Escenario {n}: resultados en nudos.", [3.6, 2.6, 3.4, 2.8, 3.2])
    tb = S["tub"]
    rows = [[p, r["sentido"], r["L"], r["D"], f(r["Q"]), f(r["V"], 3), f(r["hf"], 3), f(r["S"], 3), r["estado"]]
            for p, r in tb.iterrows()]
    D.tab(f"t{n}", ["Tubo", "Sentido del flujo", "L (m)", "D (mm)", "Q (L/s)", "V (m/s)", "h~f~ (m)", "S (m/km)",
                    "Estado"], rows,
          f"Escenario {n}: resultados en tuberías ($h_f$ = pérdida por fricción, $S$ = pérdida unitaria).",
          [1.3, 3.0, 1.3, 1.3, 1.6, 1.6, 1.6, 1.7, 1.7], size=8.5)
    b = S["bomba"]
    D.tab(f"b{n}", ["Q (L/s)", "Altura H~b~ (m)", "HGL succión (m)", "HGL descarga (m)", "p succión (m)",
                    "p descarga (m)", "Potencia hidráulica (kW)"],
          [[f(b["Q"]), f(b["H"]), f(b["Hs"]), f(b["Hd"]), f(b["ps"]), f(b["pd"]), f(b["Pot"])]],
          f"Escenario {n}: punto de operación de la bomba.", [2.0, 2.2, 2.3, 2.4, 2.2, 2.3, 2.6], size=8.5)
    rows = [[v, f(r["hgl"], 1), f(r["pset"], 1), r["estado"], f(r["Q"]), f(r["Hi"]), f(r["Ho"]), f(r["pi"]),
             f(r["po"]), f(r["dH"])] for v, r in S["prv"].iterrows()]
    D.tab(f"v{n}", ["Válvula", "Consigna HGL (m)", "Consigna p (m)", "Estado", "Q (L/s)", "HGL entrada (m)",
                    "HGL salida (m)", "p entrada (m)", "p salida (m)", "ΔH (m)"], rows,
          f"Escenario {n}: válvulas reductoras de presión.", [1.5, 1.7, 1.6, 1.6, 1.4, 1.8, 1.8, 1.6, 1.6, 1.4],
          size=8)


def escenario1(D, R, P):
    S, X = R["E1"], R["X"]
    nd, tb, b, pv = S["nudos"], S["tub"], S["bomba"], S["prv"]
    alta = ["J-1", "J-2", "J-5", "J-6", "J-7", "J-8"]
    smax, vmax = tb["S"].idxmax(), tb["V"].idxmax()
    q2, q3 = round(pv.loc["PRV-2", "Q"], 2), round(pv.loc["PRV-3", "Q"], 2)
    D.add("# 5. Escenario 1: estado estático sin la tubería P-16")
    D.fig("e1", P["e1"], "Escenario 1: presiones, caudales y estado de las válvulas. El ancho de cada tubería es "
          "proporcional al caudal.", 16.5)
    tablas_estatico(D, S, "1")
    D.add("### Análisis")
    D.lista(f"**Bomba.** Con el tanque aislado, la bomba entrega exactamente la demanda total, {f(b['Q'])} L/s, con una "
            f"altura de {f(b['H'])} m. El punto de operación está a la izquierda del punto de diseño (63.2 L/s), en la zona "
            f"de alta carga de la curva ({D.F('bomba')}). La HGL sube de {f(b['Hs'])} m en la succión a {f(b['Hd'])} m en la "
            f"descarga; la línea P-2 pierde {f(tb.loc['P-2', 'hf'])} m y la HGL llega a J-1 con {f(nd.loc['J-1', 'H'])} m.",
            f"**Zona alta (J-1, J-2, J-5, J-6, J-7 y J-8).** La HGL varía poco, entre {f(nd.loc[alta, 'H'].min())} y "
            f"{f(nd.loc[alta, 'H'].max())} m, porque los caudales son bajos. La mayor pérdida unitaria es "
            f"{f(tb.loc[smax, 'S'])} m/km en {smax} y la mayor velocidad {f(tb.loc[vmax, 'V'], 3)} m/s en P-1 y P-2. Las "
            f"presiones dependen sobre todo de la cota: van de {f(nd.loc['J-7', 'p'])} m en J-7 (cota 277 m) a "
            f"{f(nd.loc['J-1', 'p'])} m en J-1 (cota 250 m).",
            f"**Zona baja (J-3 y J-4).** PRV-2 y PRV-3 están activas: disipan {f(pv.loc['PRV-2', 'dH'])} y "
            f"{f(pv.loc['PRV-3', 'dH'])} m y fijan una HGL de 286.50 m a la salida. Entre las dos entregan {f(q2)} + "
            f"{f(q3)} = {f(q2 + q3)} L/s, que es la demanda de J-3 y J-4 (4.7 + 3.2 = 7.9 L/s). La presión en J-3 y J-4 es "
            f"{f(nd.loc['J-3', 'p'])} m. Por P-6 pasan {f(tb.loc['P-6', 'Q'])} L/s de J-4 a J-3.",
            f"**PRV-1 cerrada.** Su consigna (285.0 m) es menor que la HGL que PRV-2 y PRV-3 mantienen en J-3 "
            f"({f(nd.loc['J-3', 'H'])} m). Para entregar caudal, PRV-1 tendría que bajar la HGL a 285.0 m, y eso no es "
            "posible porque aguas abajo ya hay más carga. Por eso se cierra y funciona como una válvula de retención. P-4 y "
            f"P-5 no conducen agua y J-2 queda como un ramal ciego alimentado solo por P-3 ({f(tb.loc['P-3', 'Q'])} L/s).",
            "**Presiones frente a la norma.** Todas las presiones superan el mínimo de 15 m del artículo 61 de la "
            f"Resolución 0330 de 2017, y todas superan también 50 m. Sin consumo, la HGL de la zona alta subiría a "
            f"290 + 48.8 = {f(X['h_estatica_alta'], 1)} m, lo que daría {f(X['p_estatica']['J-1'], 1)} m en J-1. La "
            "sección 9 compara estos valores con la presión estática máxima del artículo 62.")


def escenario2(D, R, P):
    S, S1 = R["E2"], R["E1"]
    nd, tb, b, nd1, tb1 = S["nudos"], S["tub"], S["bomba"], S1["nudos"], S1["tub"]
    alta = ["J-1", "J-2", "J-5", "J-6", "J-7", "J-8"]
    caida = (nd1["p"].round(2) - nd["p"].round(2))[alta]
    smax, vmax = tb["S"].idxmax(), tb["V"].idxmax()
    vel = S["T_Q"] / 1000 / C.A_T
    D.add("# 6. Escenario 2: estado estático con el tanque T-1 en funcionamiento")
    D.fig("e2", P["e2"], "Escenario 2: presiones, caudales y estado de las válvulas.", 16.5)
    tablas_estatico(D, S, "2")
    D.add("### Análisis")
    D.lista(f"**El tanque se está llenando.** En el Escenario 1 la HGL en J-7 era {f(nd1.loc['J-7', 'H'])} m, mayor que el "
            f"nivel del tanque (320 m). Al abrir P-16 el agua fluye hacia T-1 con {f(S['T_Q'])} L/s. El tanque se comporta "
            f"como una demanda adicional y fija la HGL de su entorno: J-7 queda en {f(nd.loc['J-7', 'H'])} m, apenas "
            f"{f(tb.loc['P-16', 'hf'])} m por encima del agua del tanque.",
            f"**Bomba.** Para atender la demanda y el llenado, el caudal sube a {f(b['Q'])} L/s y la altura baja a "
            f"{f(b['H'])} m ({f(round(S1['bomba']['H'], 2) - round(b['H'], 2))} m menos que en el Escenario 1). La pérdida "
            f"en P-2 pasa de {f(tb1.loc['P-2', 'hf'])} a {f(tb.loc['P-2', 'hf'])} m y la HGL en J-1 cae "
            f"{f(round(nd1.loc['J-1', 'H'], 2) - round(nd.loc['J-1', 'H'], 2))} m, hasta {f(nd.loc['J-1', 'H'])} m.",
            f"**Cambia la distribución de caudales.** {smax} lleva {f(tb.loc[smax, 'Q'])} L/s hacia J-7 y tiene la mayor "
            f"pérdida unitaria ({f(tb.loc[smax, 'S'])} m/km) y la mayor velocidad de la red "
            f"({f(tb.loc[vmax, 'V'], 3)} m/s). P-12 y P-13 invierten su sentido ({tb.loc['P-13', 'sentido'].split(' → ')[0]} → J-8 → J-7) "
            "porque el tanque también atrae agua por la malla oriental.",
            f"**Presiones.** En la zona alta bajan entre {f(caida.min())} y {f(caida.max())} m. La mínima de la red es "
            f"{f(nd['p'].min())} m en {nd['p'].idxmin()}, todavía muy por encima del mínimo de 15 m.",
            f"**Zona baja sin cambios.** J-3 y J-4 mantienen {f(nd.loc['J-3', 'p'])} m, igual que en el Escenario 1, porque "
            "PRV-2 y PRV-3 siguen fijando la HGL en 286.50 m. Las válvulas aíslan la zona baja de lo que pasa en la zona "
            "alta. PRV-1 sigue cerrada por la misma razón del Escenario 1.",
            f"**Velocidad de llenado.** Con este caudal el agua sube $dH_T/dt = {S['T_Q'] / 1000:.5f} / {f(C.A_T)} = "
            f"{vel * 1000:.3f}$ mm/s, o sea {f(vel * 3600, 3)} m/h. A ese ritmo el tanque llegaría a 326 m en unas "
            f"{f(6 / (vel * 3600), 1)} h. El periodo extendido (sección 7) da un tiempo menor porque en la madrugada la "
            "demanda es baja y entra más caudal al tanque.")


def escenario3_tablas(D, R, P):
    e = R["E3"]
    s = e["serie"]
    D.add("# 7. Escenario 3: periodo extendido de 24 horas")
    D.add(f"La {D.T('eps')} resume cada paso de cálculo. EPANET agrega el instante {hs(e['t_lleno'])} h, cuando el tanque "
          f"llega al nivel máximo. Las presiones de cada nudo en cada paso están en el Anexo C ({D.T('anexoC')}).")
    rows = [[r["hora"], f(r["dem"]), f(r["Qb"]), f(r["Hb"]), f(r["Q16"]), f(r["HT"]), r["P16"], f(r["Q2"]), f(r["Q3"]),
             f"{f(r['pmin'])} ({r['nmin']})", f"{f(r['pmax'])} ({r['nmax']})"] for _, r in s.iterrows()]
    D.tab("eps", ["Hora", "Demanda (L/s)", "Q bomba (L/s)", "H bomba (m)", "Q a T-1 (L/s)", "HGL T-1 (m)", "P-16",
                  "Q PRV-2 (L/s)", "Q PRV-3 (L/s)", "p mín (m)", "p máx (m)"], rows,
          "Escenario 3: resultados en cada paso de cálculo. PRV-1 permanece cerrada todo el día (caudal 0.00 L/s).",
          [1.35, 1.4, 1.4, 1.4, 1.4, 1.5, 1.45, 1.3, 1.3, 1.95, 1.95], size=7.5)
    D.fig("caudales", P["caudales"], "Escenario 3: caudal de la bomba, demanda de la red y caudal que entra al tanque.", 14.5)
    D.fig("bomba", P["bomba"], "Curva de la bomba y puntos de operación de los tres escenarios.", 13)
    D.fig("tanque", P["tanque"], "Escenario 3: elevación del agua en el tanque T-1 y altura de bombeo.", 14.5)
    D.fig("presiones", P["presiones"], "Escenario 3: presión en los nudos de demanda. J-3 y J-4 casi coinciden.", 14.5)
    D.fig("prv", P["prv"], "Escenario 3: caudal a través de las válvulas reductoras de presión.", 14.5)
    uso = {"RES": "Residencial", "COM": "Comercial", "": "Constante"}
    ext = e["ext"]
    rows = []
    for j in J:
        r = ext.loc[j]
        rows.append([j, uso[M.JUNCTIONS[j][2]], f(r["pmin"]), horas_extremo(e["P"][j], r["pmin"]), f(r["pmax"]),
                     horas_extremo(e["P"][j], r["pmax"]), f(r["pmed"])])
    D.tab("ext", ["Nudo", "Uso", "p mín (m)", "Hora", "p máx (m)", "Hora", "p media (m)"], rows,
          "Escenario 3: presiones extremas y promedio del día (promedio ponderado por la duración de cada paso).",
          [1.4, 2.2, 1.8, 3.2, 1.8, 3.2, 1.9], size=8.5)


def escenario3_analisis(D, R, P):
    e, e3b, X = R["E3"], R["E3b"], R["X"]
    s = e["serie"]
    t7 = s.index[s.index < e["t_lleno"]][-1]
    base = X["q_base"] * 86.4
    D.add("## 7.1 Demanda y bomba")
    D.lista(f"La demanda total va de {f(e['dem_min'])} L/s (de 0 a 4 h) a {f(e['dem_max'])} L/s (a las "
            f"{lista_horas(X['h_dem_max'])}). Esas tres horas tienen la misma demanda porque $M_R + M_C = 2.6$ en las "
            f"tres (sección 2). El promedio diario es {f(e['Q_med'])} L/s y el volumen consumido en el día, "
            f"{f(e['V_dem'], 1)} m³.",
            f"Como los promedios de las curvas son menores que 1, el consumo del día es el "
            f"{100 * e['V_dem'] / base:.1f} % de la demanda base sostenida 24 h ({f(base, 1)} m³).",
            f"La bomba trabaja entre {f(e['Qb_min'])} y {f(e['Qb_max'])} L/s, con alturas de {f(e['Hb_min'])} a "
            f"{f(e['Hb_max'])} m. Todos los puntos están sobre la curva y dentro del rango de los datos (0 a 88.4 L/s), "
            f"como muestra la {D.F('bomba')}. En el día bombea {f(e['V_bomba'], 1)} m³: {f(e['V_dem'], 1)} m³ para el "
            f"consumo y {f(e['V_tanque'], 1)} m³ para llenar el tanque. La energía hidráulica entregada es "
            f"{f(e['energia'], 1)} kWh.")
    D.add("## 7.2 Tanque T-1")
    D.lista(f"El agua sube de 320 a 326 m entre las 0:00 y las {hs(e['t_lleno'])} h ({D.F('tanque')}). El caudal de "
            f"entrada baja de {f(s.loc[0, 'Q16'])} L/s a {f(s.loc[t7, 'Q16'])} L/s ({hh(t7)} h) a medida que crece la "
            f"demanda de la mañana. El volumen almacenado es {f(e['V_tanque'], 1)} m³, igual al volumen útil calculado "
            f"($A_T \\cdot 6 = {f(C.A_T * 6, 1)}$ m³).",
            f"Al llegar al máximo, EPANET cierra P-16 («Tank T-1 is closed at 18.00 m»). En ese instante la bomba pierde "
            f"el caudal de llenado y pasa de {f(s.loc[t7, 'Qb'])} a {f(s.loc[e['t_lleno'], 'Qb'])} L/s. Su altura sube y "
            f"todas las presiones de la zona alta aumentan: J-1 pasa de {f(e['P'].loc[t7, 'J-1'])} a "
            f"{f(e['P'].loc[e['t_lleno'], 'J-1'])} m ({D.F('presiones')}).",
            f"Después, la HGL en J-7 se mantiene entre {f(e['hj7_min'])} y {f(e['hj7_max'])} m, siempre por encima de "
            "326 m, así que el tanque no vuelve a entregar agua: queda lleno y aislado el resto del día. Con la bomba "
            "operando 24 h sin controles, el tanque solo almacena durante la madrugada y no regula los picos de consumo.")
    ext = e["ext"]
    nmin, nmax = ext["pmin"].idxmin(), ext["pmax"].idxmax()
    v = X["v_sobre_05"]
    partes_v = [f"{p} ({f(d['vmax'], 2)} m/s)" for p, d in v.items()]
    lista_v = ", ".join(partes_v[:-1]) + " y " + partes_v[-1]
    D.add("## 7.3 Presiones y válvulas")
    D.lista(f"La presión mínima del día es {f(ext.loc[nmin, 'pmin'])} m en {nmin} ({hh(ext.loc[nmin, 'tmin'])} h, cuando el "
            f"tanque todavía se llena). La máxima es {f(ext.loc[nmax, 'pmax'])} m en {nmax} ({hh(ext.loc[nmax, 'tmax'])} h, "
            "con demanda mínima y el tanque aislado). Siempre se cumple el mínimo de 15 m.",
            f"PRV-2 y PRV-3 están activas las 24 h. Juntas entregan entre {f(e['q23_min'])} y {f(e['q23_max'])} L/s, según "
            f"la demanda de J-3 y J-4, y la presión en la zona baja solo varía entre {f(e['zb_min'])} y {f(e['zb_max'])} m "
            f"({D.F('prv')}). PRV-1 permanece cerrada todo el día.",
            f"La velocidad máxima es {f(e['vmax'], 3)} m/s en {e['vmax_tubo']} ({hh(e['vmax_t'])} h, llenado del tanque). "
            f"Las tuberías que superan 0.5 m/s son {lista_v}, y solo lo hacen mientras el tanque se llena, antes de "
            f"las {hs(e['t_lleno'])} h. Las demás nunca pasan de 0.5 m/s, lo que favorece tiempos de residencia largos.")


def sensibilidad(D, R, P):
    e, e3b, X = R["E3"], R["E3b"], R["X"]
    adelanto = (e["t_lleno"] - e3b["t_lleno"]) / 60
    D.add("## 7.4 Sensibilidad: J-6 con uso residencial")
    D.add(f"Si a J-6 se le asigna la curva residencial, el tanque se llena a las {hs(e3b['t_lleno'])} h "
          f"({adelanto:.0f} min antes) y el volumen consumido en el día baja de {f(e['V_dem'], 1)} a "
          f"{f(e3b['V_dem'], 1)} m³. Las presiones mínimas y máximas cambian como máximo {f(X['sens_dif_ext'])} m y, "
          f"comparando hora por hora, la mayor diferencia es {f(X['sens_dif_horaria'])} m, ambas en "
          f"{X['sens_nudo_horaria']} ({D.F('sens')}). J-3 y J-4 no cambian porque las PRV fijan su presión. Las "
          "conclusiones no dependen de este supuesto. El modelo de esta variante se entrega como "
          "`Escenario3b_Sensibilidad_J6_residencial.inp`.")
    D.fig("sens", P["sensibilidad"], "Escenario 3 con J-6 a demanda constante y con uso residencial.", 15)


def comparacion(D, R, P):
    e1, e2, e3 = R["E1"], R["E2"], R["E3"]
    ext = e3["ext"]
    D.add("# 8. Comparación entre escenarios")
    D.fig("comp", P["comparacion"], "Presiones en los tres escenarios (en el Escenario 3 se muestra el rango del día y "
          "la media). Líneas rojas: 15 m y 50 m.", 14.5)
    rows = [[j, f(e1["nudos"].loc[j, "p"]), f(e2["nudos"].loc[j, "p"]), f(ext.loc[j, "pmin"]), f(ext.loc[j, "pmax"])]
            for j in J]
    rows += [["Q bomba (L/s)", f(e1["bomba"]["Q"]), f(e2["bomba"]["Q"]), f(e3["Qb_min"]), f(e3["Qb_max"])],
             ["H bomba (m)", f(e1["bomba"]["H"]), f(e2["bomba"]["H"]), f(e3["Hb_min"]), f(e3["Hb_max"])]]
    D.tab("resumen", ["Nudo / variable", "Escenario 1", "Escenario 2", "Escenario 3 (mín)", "Escenario 3 (máx)"], rows,
          "Resumen comparativo (presiones en m).", [3.6, 3.0, 3.0, 3.2, 3.2])
    D.lista(f"Conectar el tanque cuando está por debajo de la HGL de la red le agrega demanda a la bomba. El punto de "
            "operación se desplaza a mayor caudal y menor carga, y las presiones de la zona alta bajan. El Escenario 2 es la "
            f"condición más desfavorable de presión ({e2['nudos']['p'].idxmin()} con {f(e2['nudos']['p'].min())} m).",
            f"En el periodo extendido el sistema pasa por dos regímenes. Mientras el tanque se llena (0:00 a "
            f"{hh(e3['t_lleno'])} h) las presiones se parecen a las del Escenario 2. Después el tanque queda aislado y la "
            "red se comporta como en el Escenario 1, con presiones aún más altas en las horas de bajo consumo.",
            f"La zona baja (J-3 y J-4) tiene prácticamente la misma presión en todos los escenarios, entre "
            f"{f(min(e3['zb_min'], e1['nudos'].loc['J-3', 'p']))} y {f(e3['zb_max'])} m, gracias a PRV-2 y PRV-3.")


def norma(D, R):
    e1, e2, e3, X = R["E1"], R["E2"], R["E3"], R["X"]
    D.add("# 9. Evaluación frente a la Resolución 0330 de 2017")
    D.add("El artículo 61 fija una presión dinámica mínima de 15 m para poblaciones de diseño de más de 12 500 habitantes "
          "(10 m para poblaciones menores). Como el enunciado no da la población, se usa el valor más exigente. El "
          "artículo 62, modificado por la Resolución 799 de 2021, fija una presión estática máxima de 50 m para sistemas "
          "nuevos u optimizaciones.")
    D.add("La presión estática es la que hay sin consumo. Sin caudal no hay pérdidas, así que la HGL de la zona alta es la "
          f"de la bomba a caudal cero, 290 + 48.8 = {f(X['h_estatica_alta'], 1)} m, o la del tanque lleno "
          f"({f(X['h_estatica_tanque'], 0)} m) si la bomba está apagada. En la zona baja la HGL estática es la consigna "
          f"de PRV-2 y PRV-3 ({f(X['h_estatica_baja'], 1)} m).")
    rows = []
    for j in J:
        pd_min = min(e1["nudos"].loc[j, "p"], e2["nudos"].loc[j, "p"], e3["ext"].loc[j, "pmin"])
        pb, pt = X["p_estatica"][j], X["p_estatica_tanque"][j]
        rows.append([j, f(pd_min), "Sí" if pd_min >= 15 else "No", f(pb, 1), f(pt, 1), "Sí" if pb <= 50 else "No"])
    D.tab("norma", ["Nudo", "p dinámica mínima (m)", "Art. 61: ≥ 15 m", "p estática con la bomba a Q = 0 (m)",
                    "p estática con T-1 lleno y bomba apagada (m)", "Art. 62: ≤ 50 m"], rows,
          "Presiones del modelo frente a los artículos 61 y 62. La presión dinámica mínima es la menor de los tres "
          "escenarios.", [1.6, 2.7, 2.2, 3.4, 3.8, 2.2], size=8.5)
    D.lista("**Artículo 61:** se cumple en todos los nudos y escenarios. La menor presión es "
            f"{f(e2['nudos']['p'].min())} m en {e2['nudos']['p'].idxmin()} (Escenario 2).",
            "**Artículo 62:** no se cumple. Con la bomba operando a caudal cero la zona alta llega a "
            f"{f(max(X['p_estatica'].values()), 1)} m (J-1), y la zona baja queda en "
            f"{f(X['p_estatica']['J-3'], 1)} m. El parágrafo del artículo permite presiones mayores solo en el 10 % del área "
            "de cada zona (hasta 55 m) y en el 5 % (hasta 60 m), lo que no alcanza para la zona alta.",
            "**Artículo 63:** los diámetros (200 a 300 mm) superan el mínimo de 75 mm para redes urbanas.",
            "**Artículo 57:** el Escenario 3 cumple el requisito de modelar en periodo extendido con frecuencia horaria y "
            "con patrones de consumo, y los dos programas usan el método del gradiente.")


def watergems(D, R):
    e1, e2, e3 = R["E1"], R["E2"], R["E3"]
    D.add("# 10. Comparación EPANET 2.0 – WaterGEMS", "## 10.1 Diferencias de modelación")
    D.add("EPANET y WaterGEMS usan el mismo método de solución (gradiente), la misma fórmula de Hazen-Williams y la misma "
          "forma de la curva de bomba de tres puntos. Las diferencias son de representación y de manejo:")
    D.tab("dif", ["Aspecto", "EPANET 2.0", "WaterGEMS"], [
        ["Bomba y válvulas", "Enlaces (requieren nudos auxiliares)", "Nodos (se conectan a las tuberías)"],
        ["Consigna de la PRV", "Presión: 35.0 / 33.5 / 33.5 m", "HGL: 285.0 / 286.5 / 286.5 m (Hydraulic Grade)"],
        ["Escenarios", "Un archivo .inp por escenario", "Un solo modelo con alternativas y escenarios"],
        ["Curva de bomba", "Curva de 3 puntos → H = A − B·Q^C^", "Standard (3 Point) → H = A − B·Q^C^"],
        ["Tanque", "Niveles desde el fondo (6 / 12 / 18 m)", "Elevaciones absolutas (314 / 320 / 326 m)"],
        ["Curvas de consumo", "Siempre escalonadas", "Stepwise o Continuous; se usa Stepwise"],
        ["Solucionador", "EPANET 2.00.12", "Versión mejorada por Bentley; puede fijarse EPANET 2.00.12 (Engine Compatibility)"],
    ], "Diferencias de modelación entre los dos programas.", [3.3, 5.6, 7.4], size=8.5, align=["l", "l", "l"])
    D.add("Bentley indica que su solucionador incluye mejoras sobre EPANET, por lo que pueden aparecer diferencias "
          "pequeñas, y que la opción *Engine Compatibility* de las opciones de cálculo permite resolver con el mismo motor "
          "de EPANET 2.00.12 (Bentley, KB0016932 y KB0014547). Con esa opción y los mismos datos, los resultados deben "
          "coincidir con los de la sección siguiente a la segunda cifra decimal.")
    D.add("## 10.2 Valores de control")
    p16 = "J-7 → T-1"
    rows = [["E1 – Q bomba (L/s)", f(e1["bomba"]["Q"])], ["E1 – H bomba (m)", f(e1["bomba"]["H"])],
            ["E1 – p J-1 / J-3 / J-7 (m)", " / ".join(f(e1["nudos"].loc[j, "p"]) for j in ("J-1", "J-3", "J-7"))],
            ["E1 – Q PRV-2 / PRV-3 (L/s)", f"{f(e1['prv'].loc['PRV-2', 'Q'])} / {f(e1['prv'].loc['PRV-3', 'Q'])}"],
            ["E1 – estado de PRV-1", e1["prv"].loc["PRV-1", "estado"]],
            ["E2 – Q bomba (L/s)", f(e2["bomba"]["Q"])], ["E2 – H bomba (m)", f(e2["bomba"]["H"])],
            [f"E2 – Q en P-16 ({p16}) (L/s)", f(e2["T_Q"])],
            ["E2 – p J-1 / J-7 (m)", f"{f(e2['nudos'].loc['J-1', 'p'])} / {f(e2['nudos'].loc['J-7', 'p'])}"],
            ["E2 – Q en P-11 (L/s)", f(e2["tub"].loc["P-11", "Q"])],
            ["E3 – hora en que T-1 se llena", hs(e3["t_lleno"])],
            ["E3 – Q bomba a las 0:00 / 12:00 (L/s)", f"{f(e3['serie'].loc[0, 'Qb'])} / {f(e3['serie'].loc[43200, 'Qb'])}"],
            ["E3 – p mínima (m)", f"{f(e3['ext']['pmin'].min())} ({e3['ext']['pmin'].idxmin()}, "
                                  f"{hh(e3['ext'].loc[e3['ext']['pmin'].idxmin(), 'tmin'])} h)"],
            ["E3 – p máxima (m)", f"{f(e3['ext']['pmax'].max())} ({e3['ext']['pmax'].idxmax()}, "
                                  f"{hh(e3['ext'].loc[e3['ext']['pmax'].idxmax(), 'tmax'])} h)"]]
    D.tab("control", ["Valor de control", "EPANET 2.0", "WaterGEMS", "Diferencia"], [r + ["", ""] for r in rows],
          "Valores de control para verificar el modelo de WaterGEMS (completar con los resultados propios).",
          [6.4, 3.8, 3.2, 2.6], size=8.5, align=["l", "c", "c", "c"])
    D.add("Una diferencia mayor que 0.05 m o 0.05 L/s indica casi siempre un error de datos. Las causas más frecuentes "
          "son la consigna o el sentido de una PRV, el coeficiente C (que cambia al escoger el material), las unidades de "
          "presión (WaterGEMS usa kPa por defecto) y el formato de las curvas de consumo. El Anexo B trae la lista "
          "completa de revisiones.")
    D.add("## 10.3 Resultados obtenidos en WaterGEMS")
    for t in ("Captura de la red de WaterGEMS del Escenario 1 con presiones en nudos y caudales en tuberías.",
              "Captura del Escenario 2 con los mismos datos.",
              "Gráficas de WaterGEMS del Escenario 3: nivel de T-1, caudal de PMP-1 y presión en J-1, J-3 y J-7.",
              f"Completar la {D.T('control')} y comentar las diferencias encontradas."):
        D.nota(f"[Pendiente: {t}]", "Pendiente")


def sci(x):
    """4.5e-05 -> '4.5 × 10^−5^' (superindice real de Word, no caracteres Unicode)."""
    if x == 0:
        return "0"
    e = int(f"{x:e}".split("e")[1])
    return f"{x / 10 ** e:.1f} × 10^{str(e).replace('-', '−')}^"


def verificacion(D, R):
    e1, X = R["E1"], R["X"]
    Q = e1["bomba"]["Q"] / 1000
    hf2 = 10.67 * 1525 * Q ** 1.852 / (100 ** 1.852 * 0.3 ** 4.871)
    hf1 = e1["tub"].loc["P-1", "hf"]
    hb = C.h_bomba(e1["bomba"]["Q"])
    D.add("# 11. Verificación de los resultados", "## 11.1 Verificación manual (Escenario 1)")
    D.add(f"Pérdida en P-2 con $Q = {Q:.4f}$ m³/s:",
          f"$$h_{{f,P\\text{{-}}2}} = \\frac{{10.67 \\cdot 1525 \\cdot ({Q:.4f})^{{1.852}}}}{{100^{{1.852}} \\cdot "
          f"(0.300)^{{4.871}}}} = {f(hf2, 3)} \\text{{ m}} \\quad (\\text{{EPANET: }} {f(e1['tub'].loc['P-2', 'hf'], 3)} "
          "\\text{ m})$$",
          f"Altura de la bomba con $Q = {f(e1['bomba']['Q'])}$ L/s:",
          f"$$H_b = {C.A_P} - {f(C.B_P, 6)} \\cdot ({f(e1['bomba']['Q'])})^{{{f(C.C_P, 4)}}} = {f(hb, 3)} \\text{{ m}} "
          f"\\quad (\\text{{EPANET: }} {f(e1['bomba']['H'], 3)} \\text{{ m}})$$",
          "HGL en J-1:",
          f"$$H_{{J\\text{{-}}1}} = 290 - {f(hf1, 3)} + {f(hb, 3)} - {f(hf2, 3)} = {f(290 - hf1 + hb - hf2)} \\text{{ m}} "
          f"\\quad (\\text{{EPANET: }} {f(e1['nudos'].loc['J-1', 'H'])} \\text{{ m}})$$")
    tb, pv = e1["tub"], e1["prv"]
    D.add(f"Continuidad en J-3: entran {f(tb.loc['P-15', 'Q'])} L/s por P-15 y {f(tb.loc['P-6', 'Q'])} L/s por P-6, en "
          f"total {f(round(tb.loc['P-15', 'Q'], 2) + round(tb.loc['P-6', 'Q'], 2))} L/s, igual a la demanda de J-3 (4.70 L/s). "
          f"En J-4: PRV-2 entrega {f(pv.loc['PRV-2', 'Q'])} L/s = 3.20 L/s de demanda + {f(tb.loc['P-6', 'Q'])} L/s que "
          "siguen hacia J-3.")
    D.add("## 11.2 Verificación sistemática")
    D.add("Un script independiente (`scripts/verificacion.py`) compara cada archivo .inp con una segunda transcripción "
          "de las tablas del enunciado y revisa que la solución cumpla todas las ecuaciones en cada paso de cálculo:")
    V, dv = X["ver"], R["dif_versiones"]
    esc = ["E1", "E2", "E3", "E3b"]
    ok = lambda k: "sin diferencias" if not V[k]["datos"] else f"{len(V[k]['datos'])} diferencias"
    rows = [["Datos del .inp frente al enunciado"] + [ok(k) for k in esc],
            ["Continuidad en nudos, error máx. (L/s)"] + [sci(V[k]["continuidad"]) for k in esc],
            ["Energía (Hazen-Williams), error máx. (m)"] + [sci(V[k]["hw"]) for k in esc],
            ["Bomba sobre su curva, error máx. (m)"] + [sci(V[k]["bomba"]) for k in esc],
            ["HGL de salida de PRV activas − consigna (m)"] + [sci(V[k]["prv"]) for k in esc],
            ["Estados de las PRV coherentes"] + ["sí" if not V[k]["fallas"] else "no" for k in esc],
            ["Volumen del tanque: integrado / por nivel (m³)", "—", "—"]
            + [f"{f(V[k]['tanque']['v_int'], 1)} / {f(V[k]['tanque']['v_niv'], 1)}" for k in ("E3", "E3b")],
            ["EPANET 2.00.12 vs. 2.2: dif. máx. HGL (m)"] + [sci(dv[k]["H"]) for k in esc],
            ["EPANET 2.00.12 vs. 2.2: dif. máx. Q (L/s)"] + [sci(dv[k]["Q"]) for k in esc]]
    D.tab("verif", ["Comprobación", "Esc. 1", "Esc. 2", "Esc. 3", "Esc. 3b"], rows,
          "Comprobaciones de datos, continuidad, energía, bomba, válvulas y tanque en todos los pasos de cálculo.",
          [6.2, 2.5, 2.5, 2.6, 2.6], size=8.5, align=["l", "c", "c", "c", "c"])
    D.add("Los errores son del orden de la precisión de cálculo (0.0001) y de la precisión numérica con que el motor "
          "entrega los resultados. Las corridas con EPANET 2.00.12 y 2.2 tienen los mismos pasos de cálculo, incluido el "
          f"instante {hs(R['E3']['t_lleno'])} h en que se llena el tanque.")


def conclusiones(D, R, P):
    e1, e2, e3, rec = R["E1"], R["E2"], R["E3"], R["rec"]
    r1, r1b, r2, r3 = (rec[k] for k in ("R1", "R1b", "R2", "R3"))
    q = lambda d, v: f(d["prv"].loc[v, "Q"])
    c3 = r3["eps"]
    off, on = (hs(t) for t, _ in r3["cambios"][:2])
    ahorro = 100 * (1 - c3["energia"] / e3["energia"])
    caida_max = (e1["nudos"]["p"].round(2) - e2["nudos"]["p"].round(2)).max()
    D.add("# 12. Conclusiones y recomendaciones")
    D.numerada(
        f"En los tres escenarios la red cumple la presión mínima de servicio (15 m). La menor presión es "
        f"{f(e2['nudos']['p'].min())} m en {e2['nudos']['p'].idxmin()}, en el Escenario 2.",
        f"Conectar el tanque T-1 cuando su nivel está por debajo de la HGL de la red le agrega {f(e2['T_Q'])} L/s de demanda "
        f"a la bomba. La bomba pasa de {f(e1['bomba']['Q'])} a {f(e2['bomba']['Q'])} L/s, su altura baja "
        f"{f(round(e1['bomba']['H'], 2) - round(e2['bomba']['H'], 2))} m, las presiones de la zona alta caen hasta "
        f"{f(caida_max)} m y se invierte el flujo en P-12 y P-13.",
        "PRV-2 y PRV-3 controlan la zona baja en todos los casos: la presión en J-3 y J-4 queda alrededor de 51.4 m, "
        "independiente de lo que pase aguas arriba.",
        "PRV-1 nunca opera, porque su consigna (285.0 m) es menor que la de PRV-2 y PRV-3 (286.5 m). Para que las tres "
        f"compartan el abastecimiento, la consigna de PRV-1 debe ser igual a 286.5 m ({D.T('rec')}, caso 1). Una consigna "
        "mayor no sirve para repartir: con 287.0 m PRV-1 toma todo el caudal y PRV-2 y PRV-3 se cierran (caso 2).",
        f"En el periodo extendido el tanque se llena a las {hh(e3['t_lleno'])} h y queda aislado el resto del día, así que "
        f"no regula el consumo. Con un control de nivel (caso 4) la bomba se apaga a las {off} h, el tanque abastece la "
        f"red hasta bajar a 320 m y la bomba vuelve a encender a las {on} h. La energía hidráulica de bombeo baja "
        f"{ahorro:.1f} % y la presión máxima pasa de {f(e3['ext']['pmax'].max())} a {f(c3['ext']['pmax'].max())} m, con "
        f"una mínima de {f(c3['ext']['pmin'].min())} m.",
        "Las presiones superan los 50 m de presión estática máxima del artículo 62. En la zona baja basta con bajar las "
        f"consignas a 285.0 m: J-3 y J-4 quedan en {f(r2['p']['J-3'])} m (caso 3). La zona alta necesitaría otra zona de "
        "presión o menos altura de bombeo; esa alternativa no se simuló.",
        f"Las velocidades son bajas (máximo {f(e3['vmax'], 2)} m/s), así que las tuberías tienen capacidad de sobra para "
        "estas demandas.")
    rows = [["1", "Consigna de PRV-1 = 286.5 m (Escenario 2)",
             f"Las tres PRV activas: {q(r1, 'PRV-1')} / {q(r1, 'PRV-2')} / {q(r1, 'PRV-3')} L/s. J-3 y J-4 con "
             f"{f(r1['p']['J-3'])} m."],
            ["2", "Consigna de PRV-1 = 287.0 m (Escenario 2)",
             f"PRV-1 activa con {q(r1b, 'PRV-1')} L/s; PRV-2 y PRV-3 cerradas. J-3 con {f(r1b['p']['J-3'])} m."],
            ["3", "Consigna de las tres PRV = 285.0 m (Escenario 2)",
             f"Las tres activas: {q(r2, 'PRV-1')} / {q(r2, 'PRV-2')} / {q(r2, 'PRV-3')} L/s. J-3 y J-4 con "
             f"{f(r2['p']['J-3'])} m (50.0 m sin consumo)."],
            ["4", "Control de PMP-1: se apaga con T-1 en 326 m y se enciende con T-1 en 320 m (Escenario 3)",
             f"Bomba apagada de {off} a {on} h (encendida {f(r3['horas_bomba'], 1)} h). Energía hidráulica "
             f"{f(c3['energia'], 1)} kWh frente a {f(e3['energia'], 1)} kWh. Presiones entre {f(c3['ext']['pmin'].min())} y "
             f"{f(c3['ext']['pmax'].max())} m."]]
    D.tab("rec", ["Caso", "Cambio simulado", "Resultado"], rows,
          "Simulaciones de las recomendaciones (modelos en la carpeta modelos/recomendaciones).", [1.2, 6.0, 9.2], size=8.5,
          align=["c", "l", "l"])
    D.fig("control", P["control"], "Caso 4: Escenario 3 sin control y con control de la bomba por nivel del tanque.", 15)


def referencias(D):
    D.add("# Referencias")
    D.lista(
        "Bentley Systems. *Engine Compatibility Mode and related Calculation options* (KB0014547). "
        "https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0014547",
        "Bentley Systems. *Should the EPANET solver and the WaterGEMS/CAD solver give the same results for a model?* "
        "(KB0016932). https://bentleysystems.service-now.com/community?id=kb_article_view&sysparm_article=KB0016932",
        "Bentley Systems. *What are the limitations of importing/exporting EPANET files?* (KB0057434). "
        "https://bentleysystems.service-now.com/community?id=kb_article&sysparm_article=KB0057434",
        "Ministerio de Vivienda, Ciudad y Territorio (2017). Resolución 0330 de 2017, Reglamento Técnico del Sector de "
        "Agua Potable y Saneamiento Básico (RAS), artículos 57, 61, 62 y 63 (art. 62 modificado por la Resolución 799 de "
        "2021). https://normas.cra.gov.co/gestor/docs/resolucion_minviviendact_0330_2017.htm",
        "OpenWaterAnalytics. Código fuente de EPANET, versiones 2.0.12 y 2.2. https://github.com/OpenWaterAnalytics/EPANET",
        "Rossman, L. A. (2000). *EPANET 2 Users Manual*. U.S. EPA, EPA/600/R-00/057.",
        "Rossman, L. A., Woo, H., Tryby, M., Shang, F., Janke, R. y Haxton, T. (2020). *EPANET 2.2 User Manual*. "
        "U.S. EPA, EPA/600/R-20/133.",
        "Todini, E. y Pilati, S. (1988). A gradient algorithm for the analysis of pipe networks. En *Computer "
        "Applications in Water Supply*, Vol. 1. Research Studies Press.")


def anexo_a(D):
    D.salto()
    D.add("# Anexo A. Archivos entregados")
    D.tab("archivos", ["Archivo", "Contenido"], [
        ["`modelos/Escenario1_Estatico_sin_P16.inp`", "Modelo EPANET del Escenario 1"],
        ["`modelos/Escenario2_Estatico_con_tanque.inp`", "Modelo EPANET del Escenario 2"],
        ["`modelos/Escenario3_Periodo_extendido_24h.inp`", "Modelo EPANET del Escenario 3"],
        ["`modelos/Escenario3b_Sensibilidad_J6_residencial.inp`", "Variante del Escenario 3 con J-6 residencial"],
        ["`modelos/recomendaciones/*.inp`", "Modelos de los casos 1 a 4 de la sección 12"],
        ["`resultados/*_EPANET2.0.12.rpt`, `*_EPANET2.2.rpt`", "Reportes completos de las dos versiones de EPANET"],
        ["`resultados/Resultados_Taller1.xlsx`", "Tablas de resultados de todos los escenarios, una hoja por tabla"],
        ["`figuras/*.png`", "Figuras del informe"],
        ["`scripts/*.py`", "Datos, generación de modelos, simulación, verificación, figuras e informe"],
    ], "Archivos del taller.", [8.6, 7.8], size=8.5, align=["l", "l"])
    D.add("Para abrir un modelo: EPANET 2.0 → *File → Open* → seleccionar el .inp → *Project → Run Analysis*. En la "
          "versión en español los comandos son *Archivo → Abrir* y *Proyecto → Calcular*. Los .inp también se pueden "
          "importar en WaterGEMS (*File → Import → EPANET*), pero el modelo importado conserva los nudos auxiliares de "
          "EPANET y solo trae los datos que existen en los dos formatos (Bentley, KB0057434). Por eso se recomienda "
          "construir el modelo según el Anexo B.")


def anexo_b1(D):
    D.salto()
    D.add("# Anexo B. Guía paso a paso en WaterGEMS")
    D.add("Las rutas de menú son las de WaterGEMS CONNECT Edition. En versiones anteriores (V8i) los mismos comandos están "
          "en los menús *Tools*, *Components*, *Analysis* y *View*.")
    D.add("## B.1 Proyecto, unidades y opciones de cálculo")
    D.numerada("*File → New* y guardar de una vez como `Taller1.wtg`.",
               "*Tools → Options*, pestaña *Units*: restablecer las unidades al Sistema Internacional (*Reset Defaults – "
               "SI*). Revisar Flow = L/s, Pressure = m H2O (por defecto aparece en kPa), Length y Elevation = m, "
               "Diameter = mm y Velocity = m/s.",
               "*Tools → Options*, pestaña *Drawing*: Drawing Mode = Schematic, para que la longitud de cada tubería sea la "
               "que se escribe y no la del dibujo.",
               "*Analysis → Calculation Options → Base Calculation Options*: Friction Method = Hazen-Williams y Time "
               "Analysis Type = Steady State. Si la versión tiene la opción *Engine Compatibility*, elegir EPANET 2.00.12.")
    D.add("## B.2 Definición de la bomba")
    D.numerada("*Components → Pump Definitions → New*, con el nombre «Definicion Bomba 1».",
               "Pump Definition Type = Standard (3 Point). Shutoff: 0 L/s y 48.8 m. Design: 63.2 L/s y 39.6 m. "
               "Max Operating: 88.4 L/s y 33.8 m.",
               "Pestaña *Efficiency*: eficiencia constante (por ejemplo 75 %). La eficiencia no cambia los resultados "
               "hidráulicos.")
    D.add("## B.3 Trazado de la red")
    D.numerada("Con la herramienta de trazado, dibujar en el sentido del flujo: R-1 → P-1 → PMP-1 → P-2 → J-1.",
               "Seguir con J-1 → P-3 → J-2 → P-4 → PRV-1 → P-5 → J-3; J-5 → P-8 → PRV-2 → P-7 → J-4; y J-6 → P-14 → "
               "PRV-3 → P-15 → J-3.",
               "Completar P-6, P-9, P-10, P-11, P-12 y P-13, y por último T-1 con P-16 desde J-7.",
               "Renombrar cada elemento (*Label*) como en la Figura 1.",
               "Revisar *Downstream Pipe*: PMP-1 → P-2, PRV-1 → P-5, PRV-2 → P-7 y PRV-3 → P-15. Si alguno quedó al revés, "
               "corregirlo en ese mismo campo.")
    D.add("## B.4 Datos de los elementos")
    D.tab("wg_datos", ["Elemento", "Campo en WaterGEMS", "Valor"], [
        ["J-1 a J-8", "Elevation", f"{D.T('nudos')}"],
        ["J-1 a J-8", "Demand Collection → Flow (Base); Pattern", f"{D.T('nudos')}; Pattern = Fixed"],
        ["P-1 a P-16", "Has User Defined Length? / Length (User Defined) / Diameter", f"True / {D.T('tubos')}"],
        ["P-1 a P-16", "Material, y después Hazen-Williams C", "Cast iron; C = 100 en las 16 tuberías"],
        ["R-1", "Elevation", "290 m"],
        ["PMP-1", "Elevation / Pump Definition / Status (Initial)", "288 m / Definicion Bomba 1 / On"],
        ["PRV-1, PRV-2, PRV-3", "Elevation / Diameter (Valve)", "250, 253, 253 m / 200 mm"],
        ["PRV-1, PRV-2, PRV-3", "Setting Type / Hydraulic Grade Setting (Initial)", "Hydraulic Grade / 285.0, 286.5, 286.5 m"],
        ["PRV-1, PRV-2, PRV-3", "Status (Initial)", "Active"],
        ["T-1", "Operating Range Type", "Elevation"],
        ["T-1", "Elevation (Base / Minimum / Initial / Maximum)", "308 / 314 / 320 / 326 m"],
        ["T-1", "Section / Diameter", "Circular / 15 m"],
    ], "Datos que se ingresan en WaterGEMS.", [3.4, 7.2, 5.8], size=8.5, align=["l", "l", "l"])
    D.add("Para poner C = 100 en todas las tuberías a la vez: en la FlexTable de tuberías, clic derecho en el encabezado de "
          "la columna → *Global Edit* → *Set* 100. Hágalo después de escoger el material, porque al escogerlo WaterGEMS "
          "le pone a la tubería el C de su librería. Al terminar, *Analysis → Validate* no debe mostrar errores.")


def anexo_b2(D):
    D.add("## B.5 Curvas de consumo")
    D.numerada("*Components → Patterns*, carpeta *Hydraulic* → *New*, con el nombre «Residencial».",
               "Start Time = 12:00:00 AM, Starting Multiplier = 0.1 y Pattern Format = Stepwise.",
               f"En la tabla, escribir una fila por hora (*Time from Start* de 1 a 24 h) con los valores de la "
               f"{D.T('wg_patrones')}. La fila de 24 h repite el multiplicador inicial y cierra el ciclo de 24 h.",
               "Repetir con «Comercial» (Starting Multiplier = 0.0).")
    rows = [[f"{h} (Starting Multiplier)" if h == 0 else str(h), f(M.RES[h % 24], 1), f(M.COM[h % 24], 1)]
            for h in range(25)]
    D.tab("wg_patrones", ["Time from Start (h)", "Residencial", "Comercial"], rows,
          "Curvas de consumo en el formato de WaterGEMS (Stepwise: cada valor rige desde esa hora hasta la siguiente).",
          [5.0, 3.2, 3.2], size=8.5)
    D.nota("Use *Stepwise*. Con *Continuous* WaterGEMS interpola entre horas y los resultados no coinciden con EPANET.")
    D.add("## B.6 Escenarios y alternativas")
    D.add("El escenario base es la red completa en estado estático (Escenario 2). Los otros dos se crean como hijos, de "
          "modo que solo guardan lo que cambia:")
    D.numerada("*Analysis → Scenarios*: renombrar «Base» como «Escenario 2 – Con tanque».",
               "*Analysis → Alternatives → Active Topology*: clic derecho sobre la alternativa base → *New → Child "
               "Alternative*, con el nombre «Sin P-16».",
               "*Alternatives → Demand*: crear la alternativa hija «Con curvas».",
               "*Analysis → Calculation Options → New*, con el nombre «EPS 24 h»: Time Analysis Type = EPS, Start Time = "
               "12:00 AM, Duration = 24 h y Hydraulic Time Step = 1 h (y la misma *Engine Compatibility* de B.1).",
               "En *Scenarios*, clic derecho sobre «Escenario 2» → *New → Child Scenario*: «Escenario 1 – Sin P-16», con "
               "Active Topology = «Sin P-16».",
               "Otro escenario hijo de «Escenario 2»: «Escenario 3 – EPS», con Demand = «Con curvas» y "
               "*Steady State/EPS Solver Calculation Options* = «EPS 24 h».",
               "Hacer actual el Escenario 1 (*Make Current*), seleccionar P-16 y T-1 y poner *Is Active?* = False. El cambio "
               "queda guardado solo en la alternativa «Sin P-16».",
               "Hacer actual el Escenario 3 y, en *Tools → Demand Control Center*, asignar Residencial a J-1, J-2, J-3 y "
               "J-7, y Comercial a J-4, J-5 y J-8. J-6 queda en Fixed.")
    D.nota("Antes de editar cualquier dato, revise cuál escenario está activo. Lo que se edita queda en las alternativas "
           "de ese escenario.")
    D.add("## B.7 Cálculo y resultados")
    D.numerada("Para cada escenario: *Make Current* → *Analysis → Compute* (F9). También se puede usar *Batch Run* en "
               "*Scenarios* y marcar los tres.",
               "En el *Calculation Summary* todos los pasos deben aparecer como balanceados. Revisar *User Notifications*.",
               "*View → FlexTables*: tablas de nudos (Hydraulic Grade, Pressure), tuberías (Flow, Velocity, Headloss "
               "Gradient), bombas, válvulas (Status) y tanques. Cada tabla se puede exportar a Excel.",
               "Escenario 3: graficar el nivel de T-1, el caudal de PMP-1 y la presión en J-1, J-3 y J-7 (clic derecho → "
               "*Graph*), y usar el *EPS Results Browser* para recorrer las horas.",
               "*Element Symbology*: colorear nudos por presión y tuberías por velocidad, y tomar las capturas de la "
               "sección 10.3.",
               "Guardar el proyecto. El archivo .wtg y las capturas son el soporte de la simulación en WaterGEMS.")


def anexo_b3_c(D, R):
    D.add("## B.8 Qué revisar si los resultados no coinciden")
    D.lista("**Unidades de presión:** WaterGEMS usa kPa por defecto; 1 m H2O = 9.81 kPa.",
            "**Coeficiente C:** si se escogió el material después de escribir C = 100, el C queda en el valor de la librería.",
            "**Sentido de las PRV:** si *Downstream Pipe* está al revés, la válvula regula hacia el lado equivocado.",
            "**Consigna de las PRV:** con *Setting Type = Pressure* los valores son 35.0 / 33.5 / 33.5 m, no 285.0 / 286.5.",
            "**Tanque:** con *Operating Range Type = Level* los valores se miden desde el fondo (6 / 12 / 18 m).",
            "**Curvas de consumo:** deben estar en *Stepwise*.",
            "**Escenario 1:** desactivar P-16 y también T-1; si solo se desactiva P-16, T-1 queda como un nodo aislado.",
            "**Solucionador:** si quedan diferencias pequeñas, revisar *Engine Compatibility* (sección 10.1).")
    D.salto()
    e = R["E3"]
    D.add("# Anexo C. Escenario 3: presión por nudo en cada paso de cálculo")
    rows = [[hh(t)] + [f(e["P"].loc[t, j]) for j in J] for t in e["P"].index]
    D.tab("anexoC", ["Hora"] + J, rows, "Escenario 3: presión en cada nudo de demanda (m).", [1.7] + [1.65] * 8, size=8)


def construir(R, P, nums=None):
    D = Doc(nums)
    portada(D)
    resumen(D, R)
    objetivo(D)
    datos(D, P)
    datos_patrones(D, R, P)
    teoria(D)
    teoria_2(D)
    supuestos(D)
    construccion(D)
    escenario1(D, R, P)
    escenario2(D, R, P)
    escenario3_tablas(D, R, P)
    escenario3_analisis(D, R, P)
    sensibilidad(D, R, P)
    comparacion(D, R, P)
    norma(D, R)
    watergems(D, R)
    verificacion(D, R)
    conclusiones(D, R, P)
    referencias(D)
    anexo_a(D)
    anexo_b1(D)
    anexo_b2(D)
    anexo_b3_c(D, R)
    return D


# ---------------------------------------------------------------- documento de referencia (estilos, pagina)
PPR_DESPUES_SHD = ["w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct", "w:topLinePunct",
                   "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
                   "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection",
                   "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr",
                   "w:sectPr", "w:pPrChange"]


def _estilo(doc, nombre, size=None, bold=None, italic=None, color=None, align=None, before=None, after=None,
            keep=None, line=None, indent=None, fill=None, font="Calibri", base="Normal"):
    from docx.enum.style import WD_STYLE_TYPE
    try:
        st = doc.styles[nombre]
    except KeyError:
        st = doc.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles[base]
        st.quick_style = True
    fnt, pf = st.font, st.paragraph_format
    if font:
        fnt.name = font
        rpr = st.element.get_or_add_rPr()
        rpr.get_or_add_rFonts().set(qn("w:eastAsia"), font)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            rpr.rFonts.attrib.pop(qn(a), None)
    for attr, val in (("size", Pt(size) if size else None), ("bold", bold), ("italic", italic)):
        if val is not None:
            setattr(fnt, attr, val)
    if color:
        fnt.color.rgb = color
    for attr, val in (("alignment", align), ("space_before", Pt(before) if before is not None else None),
                      ("space_after", Pt(after) if after is not None else None), ("keep_with_next", keep),
                      ("line_spacing", line), ("left_indent", Cm(indent) if indent else None)):
        if val is not None:
            setattr(pf, attr, val)
    if fill:
        ppr = st.element.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill)
        ppr.insert_element_before(shd, *PPR_DESPUES_SHD)
    return st


def _campo(par, instr, size=8.5):
    for tipo in ("begin", None, "separate", "1", "end"):
        r = par.add_run()
        r.font.size = Pt(size)
        if tipo in ("begin", "separate", "end"):
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), tipo)
            r._r.append(fc)
        elif tipo is None:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f" {instr} "
            r._r.append(it)
        else:
            r.text = tipo


def referencia(path):
    subprocess.run([PANDOC, "-o", path, "--print-default-data-file", "reference.docx"], check=True)
    doc = Document(path)
    J_, C_, L_ = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
    gris = RGBColor(0x40, 0x40, 0x40)
    _estilo(doc, "Normal", size=11, after=4)
    for n in ("Body Text", "First Paragraph"):
        _estilo(doc, n, align=J_, before=0, after=6, line=1.15)
    _estilo(doc, "Compact", align=L_, before=0, after=2, line=1.1)
    _estilo(doc, "Heading 1", size=14, bold=True, color=AZUL, before=18, after=8, keep=True)
    _estilo(doc, "Heading 2", size=12, bold=True, color=AZUL, before=12, after=6, keep=True)
    _estilo(doc, "Heading 3", size=11, bold=True, italic=False, color=AZUL, before=10, after=4, keep=True)
    _estilo(doc, "Title", size=22, bold=True, color=AZUL, align=C_, before=36, after=12)
    _estilo(doc, "Subtitle", size=13, italic=True, color=gris, align=C_, before=0, after=48)
    _estilo(doc, "Table Caption", size=9.5, align=C_, before=10, after=4, keep=True)
    _estilo(doc, "Image Caption", size=9.5, align=C_, before=2, after=12)
    for n in ("Captioned Figure", "Figure"):
        _estilo(doc, n, align=C_, before=6, after=0, keep=True)
    _estilo(doc, "TOC Heading", size=14, bold=True, color=AZUL, before=0, after=12)
    _estilo(doc, "Nota", size=9.5, italic=True, color=gris, align=L_, before=4, after=8, indent=0.4, fill="F2F2F2")
    _estilo(doc, "Pendiente", size=10, bold=True, color=RGBColor(0x7F, 0x60, 0x00), align=L_, before=4, after=6,
            fill="FFF2CC")
    _estilo(doc, "Institucion", size=13, bold=True, color=AZUL, align=C_, before=60, after=36, line=1.3)
    _estilo(doc, "Portada", size=12, align=C_, before=6, after=18, line=1.4)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(2.5))
    sec.header_distance = sec.footer_distance = Cm(1.2)
    sec.different_first_page_header_footer = True
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run("Taller 1 – Simulación de sistemas de distribución · EPANET 2.0 y WaterGEMS")
    r.font.size, r.font.color.rgb = Pt(8.5), RGBColor(0x7F, 0x7F, 0x7F)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.add_run("Página ").font.size = Pt(8.5)
    _campo(fp, "PAGE")
    fp.add_run(" de ").font.size = Pt(8.5)
    _campo(fp, "NUMPAGES")
    doc.save(path)
    return path


# ---------------------------------------------------------------- formato de tablas (orden de elementos segun OOXML)
ORD_TBLPR = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize", "tblW",
             "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption",
             "tblDescription"]
ORD_TCPR = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar", "textDirection",
            "tcFitText", "vAlign", "hideMark"]
ORD_TRPR = ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter", "cantSplit", "trHeight", "tblHeader",
            "tblCellSpacing", "jc", "hidden"]


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(f"w:{k}"), str(v))
    return e


def _ordenar(parent, nuevos, orden):
    """Reemplaza/agrega hijos y los deja en el orden del esquema (Word es estricto con el orden)."""
    hijos = {c.tag.split("}")[1]: c for c in parent}
    hijos.update(nuevos)
    for c in list(parent):
        parent.remove(c)
    for k in orden:
        if k in hijos:
            parent.append(hijos[k])


def formatear_tabla(tbl, widths, size):
    dxa = [int(round(w * 567)) for w in widths]
    t = tbl._tbl
    bordes = _el("w:tblBorders")
    for lado, sz, color in (("top", 12, "1F4E79"), ("left", 0, "auto"), ("bottom", 12, "1F4E79"), ("right", 0, "auto"),
                            ("insideH", 4, "BFBFBF"), ("insideV", 4, "D9D9D9")):
        bordes.append(_el(f"w:{lado}", val="single" if sz else "nil", sz=sz, space=0, color=color))
    mar = _el("w:tblCellMar")
    for lado, v in (("top", 15), ("left", 60), ("bottom", 15), ("right", 60)):
        mar.append(_el(f"w:{lado}", w=v, type="dxa"))
    _ordenar(t.tblPr, {"tblW": _el("w:tblW", w=sum(dxa), type="dxa"), "jc": _el("w:jc", val="center"),
                       "tblBorders": bordes, "tblLayout": _el("w:tblLayout", type="fixed"), "tblCellMar": mar}, ORD_TBLPR)
    grid = t.tblGrid
    for g in list(grid):
        grid.remove(g)
    for w in dxa:
        grid.append(_el("w:gridCol", w=w))
    for i, row in enumerate(tbl.rows):
        trpr = row._tr.get_or_add_trPr()
        _ordenar(trpr, {"cantSplit": _el("w:cantSplit")}, ORD_TRPR)
        for j, cell in enumerate(row.cells):
            nuevos = {"tcW": _el("w:tcW", w=dxa[j], type="dxa"), "vAlign": _el("w:vAlign", val="center")}
            if i == 0:
                nuevos["shd"] = _el("w:shd", val="clear", color="auto", fill="D9E2F3")
            _ordenar(cell._tc.get_or_add_tcPr(), nuevos, ORD_TCPR)
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.space_before, pf.space_after, pf.line_spacing = Pt(1), Pt(1), 1.0
                for r in p.runs:
                    r.font.size = Pt(size)
                    if i == 0:
                        r.font.bold = True


DESPUES_UPDATEFIELDS = {"hdrShapeDefaults", "footnotePr", "endnotePr", "compat", "docVars", "rsids", "mathPr",
                        "attachedSchema", "themeFontLang", "clrSchemeMapping", "doNotIncludeSubdocsInStats",
                        "doNotAutoCompressPictures", "forceUpgrade", "captions", "readModeInkLockDown", "smartTagType",
                        "schemaLibrary", "shapeDefaults", "doNotEmbedSmartTags", "decimalSymbol", "listSeparator"}


def chequeos(R):
    """Afirmaciones del texto que dependen de los resultados: si alguna deja de cumplirse, el informe no se genera."""
    e1, e2, e3, X, rec = R["E1"], R["E2"], R["E3"], R["X"], R["rec"]
    ok = []
    ok.append(all(e1["prv"]["estado"] == ["Cerrada", "Activa", "Activa"]))
    ok.append(all(e2["prv"]["estado"] == ["Cerrada", "Activa", "Activa"]))
    ok.append(e3["prv1_siempre_cerrada"] and e3["prv23_siempre_activas"])
    ok.append(e1["nudos"]["p"].min() > 50 and e1["nudos"]["p"].idxmin() in ("J-3", "J-4"))
    ok.append(round(e1["nudos"].loc["J-3", "p"], 2) == round(e1["nudos"].loc["J-4", "p"], 2))
    ok.append(e1["tub"]["V"].idxmax() in ("P-1", "P-2") and e1["tub"].loc["P-6", "sentido"] == "J-4 → J-3")
    ok.append(e1["nudos"].loc["J-7", "H"] > 320 and e2["T_Q"] > 0)
    ok.append(e2["tub"]["S"].idxmax() == "P-11" and e2["tub"]["V"].idxmax() == "P-11")
    ok.append(e2["tub"].loc["P-12", "sentido"] == "J-8 → J-7" and e2["tub"].loc["P-13", "sentido"] == "J-5 → J-8")
    ok.append(e1["tub"].loc["P-12", "sentido"] == "J-7 → J-8" and e1["tub"].loc["P-13", "sentido"] == "J-8 → J-5")
    ok.append(e2["nudos"]["p"].min() <= min(e1["nudos"]["p"].min(), e3["ext"]["pmin"].min()))
    ext = e3["ext"]
    ok.append(ext.loc[ext["pmin"].idxmin(), "tmin"] < e3["t_lleno"] <= ext.loc[ext["pmax"].idxmax(), "tmax"])
    ok.append(X["h_dem_max"] == [7, 8, 14] and all(abs(M.RES[h] + M.COM[h] - 2.6) < 1e-9 for h in X["h_dem_max"]))
    ok.append(X["h_dem_min"] == [0, 1, 2, 3])
    ok.append(all(_seg(d["fin"]) < e3["t_lleno"] for d in X["v_sobre_05"].values()))
    ok.append(X["sens_nudo_horaria"] == X["sens_nudo_ext"])
    ok.append(all(rec["R1"]["prv"]["estado"] == "Activa") and all(rec["R2"]["prv"]["estado"] == "Activa"))
    r1b = rec["R1b"]["prv"]
    ok.append(r1b.loc["PRV-1", "estado"] == "Activa" and all(r1b.loc[["PRV-2", "PRV-3"], "estado"] == "Cerrada"))
    ok.append(len(rec["R3"]["cambios"]) == 2 and rec["R3"]["eps"]["ext"]["pmin"].min() >= 15)
    ok.append(all(not v["datos"] and not v["fallas"] for v in X["ver"].values()))
    malos = [i for i, x in enumerate(ok) if not x]
    if malos:
        raise AssertionError(f"Afirmaciones del texto que no se cumplen: {malos}")


def _seg(hora):
    p = [int(x) for x in hora.split(":")]
    return p[0] * 3600 + p[1] * 60 + (p[2] if len(p) > 2 else 0)


def generar():
    R = C.calcular(salidas=True)
    chequeos(R)
    P = FG.todas(R)
    D = construir(R, P, construir(R, P).numeros())
    md = D.md()
    if "Figura ?" in md or "Tabla ?" in md:
        raise AssertionError("Hay referencias a figuras o tablas sin numero")
    tmp = os.path.join("/projects/sandbox", ".tmp_pandoc")
    os.makedirs(tmp, exist_ok=True)
    fuente = os.path.join(tmp, "informe.md")
    with open(fuente, "w", encoding="utf-8") as fh:
        fh.write(md)
    ref = referencia(os.path.join(tmp, "referencia.docx"))
    subprocess.run([PANDOC, fuente, "-f", "markdown", "-t", "docx", "--reference-doc", ref, "-M", "lang=es-CO",
                    "-o", SALIDA], check=True)
    doc = Document(SALIDA)
    if len(doc.tables) != len(D.tabfmt):
        raise AssertionError(f"{len(doc.tables)} tablas en el docx y {len(D.tabfmt)} esperadas")
    for tbl, (widths, size) in zip(doc.tables, D.tabfmt):
        if len(tbl.columns) != len(widths):
            raise AssertionError("Numero de columnas distinto en una tabla")
        formatear_tabla(tbl, widths, size)
    st = doc.settings.element
    uf = _el("w:updateFields", val="true")
    for c in st:
        if c.tag.split("}")[1] in DESPUES_UPDATEFIELDS:
            c.addprevious(uf)
            break
    else:
        st.append(uf)
    cp = doc.core_properties
    cp.title = "Taller 1: Simulación de sistemas de distribución"
    cp.subject = "Modelación de una red con bomba, tanque y PRV en EPANET 2.0 y WaterGEMS"
    cp.author, cp.last_modified_by, cp.language = "", "", "es-CO"
    cp.keywords = "EPANET, WaterGEMS, redes de distribución, PRV, periodo extendido"
    doc.save(SALIDA)
    return SALIDA, D, R


if __name__ == "__main__":
    out, D, R = generar()
    nums = D.numeros()
    print(out, "|", sum(1 for k in nums if k[0] == "fig"), "figuras |", sum(1 for k in nums if k[0] == "tab"), "tablas")
