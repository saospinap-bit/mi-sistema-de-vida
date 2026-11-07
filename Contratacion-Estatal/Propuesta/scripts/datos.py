# -*- coding: utf-8 -*-
"""Fuente única de datos de la propuesta. Todos los generadores importan de aquí."""
from decimal import Decimal, ROUND_HALF_UP
import xlrd

XLS = "/projects/sandbox/mi-sistema-de-vida/EJERCICIO.xls"

PROPONENTE = "[NOMBRE DEL PROPONENTE]"
REPRESENTANTE = "[NOMBRE DEL REPRESENTANTE LEGAL]"
CEDULA_REP = "[C.C. No.]"
NIT = "[NIT / C.C.]"
DIRECCION = "[DIRECCIÓN]"
TELEFONO = "[TELÉFONO]"
CORREO = "[CORREO ELECTRÓNICO]"
CIUDAD_FECHA = "Bogotá D.C., 7 de noviembre de 2025"

LICITACION = "LICITACIÓN PÚBLICA No. L02-2009 (ejercicio académico 2025)"
ENTIDAD = "MUNICIPIO DE SANDONÁ – NARIÑO"
OBJETO = "CONSTRUCCIÓN POLIDEPORTIVO CUBIERTO CABECERA MUNICIPAL DE SANDONÁ – DEPARTAMENTO DE NARIÑO"

PRESUPUESTO_OFICIAL = 872_826_612
A_PCT, I_PCT, U_PCT = Decimal("0.15"), Decimal("0.07"), Decimal("0.02")
AIU = A_PCT + I_PCT + U_PCT

# Valor objetivo de la oferta: 94,0 % del presupuesto oficial.
OBJETIVO_PCT = Decimal("0.940")


def r0(x):
    """Redondeo al peso igual que ROUND(x;0) de Excel (mitad hacia arriba)."""
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------- formato
def leer_formato():
    s = xlrd.open_workbook(XLS).sheet_by_index(0)
    filas = []  # ('cap', cod, nombre) | ('item', cod, desc, und, cant, vu_oficial)
    for r in range(6, s.nrows):
        c, i, u, q, p, t = [s.cell_value(r, k) for k in range(6)]
        if isinstance(q, str) and q.startswith("VALOR"):
            break
        if isinstance(p, float) and p > 0:
            filas.append(("item", c.strip().rstrip("."), " ".join(i.split()), u.strip(), q, p))
        elif isinstance(c, str) and c.strip() and i:
            filas.append(("cap", c.strip().rstrip("."), i.strip()))
    return filas


FORMATO = leer_formato()
ITEMS = [f for f in FORMATO if f[0] == "item"]
assert len(ITEMS) == 85, len(ITEMS)

# ---------------------------------------------------------------- mano de obra
ANIO = 2025
SMMLV = 1_423_500          # Decreto 1572 de 2024
DEC_SMMLV = "Decreto 1572 de 2024"
AUX_TRANSPORTE = 200_000   # Decreto 1573 de 2024
DEC_AUX = "Decreto 1573 de 2024"
HORAS_SEMANA = 44          # Ley 2101 de 2021: 44 h/semana desde el 15-jul-2025
HORAS_MES = Decimal(HORAS_SEMANA) * 52 / 12  # 190,67 h

# Fechas del proceso (cierre 2025-NOV-07)
CIERRE = "7 de noviembre de 2025"
POLIZA_DESDE = "7 de noviembre de 2025"
POLIZA_HASTA = "7 de mayo de 2026"          # 6 meses desde el cierre
CAMARA_DESDE = "8 de octubre de 2025"       # máximo 30 días antes del cierre
EXP_DESDE = "7 de noviembre de 2015"        # últimos 10 años
DURACION_SOCIEDAD = "7 de abril de 2027"    # cierre + 5 meses de plazo + 1 año
DURACION_CONSORCIO = "7 de abril de 2028"   # cierre + 5 meses de plazo + 2 años
SMMLV_ANIOS = [(2025, 1_423_500), (2024, 1_300_000), (2023, 1_160_000), (2022, 1_000_000),
               (2021, 908_526), (2020, 877_803), (2019, 828_116), (2018, 781_242),
               (2017, 737_717), (2016, 689_455), (2015, 644_350)]

PRESTACIONES = [  # % sobre el salario
    ("Cesantías", Decimal("0.0833")),
    ("Intereses sobre cesantías", Decimal("0.0100")),
    ("Prima de servicios", Decimal("0.0833")),
    ("Vacaciones", Decimal("0.0417")),
    ("Salud (empleador)", Decimal("0.0850")),
    ("Pensión (empleador)", Decimal("0.1200")),
    ("ARL riesgo V (construcción)", Decimal("0.0696")),
    ("Caja de compensación", Decimal("0.0400")),
    ("ICBF", Decimal("0.0300")),
    ("SENA", Decimal("0.0200")),
    ("Dotación y EPP", Decimal("0.0400")),
]
PREST_TOTAL = sum(p for _, p in PRESTACIONES)  # 0.6229
# El auxilio de transporte también genera cesantías, intereses y prima
AUX_FACTOR = 1 + Decimal("0.0833") + Decimal("0.0100") + Decimal("0.0833")

CARGOS = [  # nombre, múltiplo del SMMLV
    ("Ayudante (obrero)", Decimal("1.0")),
    ("Oficial", Decimal("1.6")),
]


def costo_hora(mult):
    sal = Decimal(SMMLV) * mult
    mensual = sal * (1 + PREST_TOTAL) + Decimal(AUX_TRANSPORTE) * AUX_FACTOR
    return mensual / HORAS_MES


HORA_AY = costo_hora(Decimal("1.0"))
HORA_OF = costo_hora(Decimal("1.6"))
CUADRILLAS = {
    "C11": ("Cuadrilla 1 oficial + 1 ayudante", HORA_OF + HORA_AY),
    "C12": ("Cuadrilla 1 oficial + 2 ayudantes", HORA_OF + 2 * HORA_AY),
    "C13": ("Cuadrilla 1 oficial + 3 ayudantes", HORA_OF + 3 * HORA_AY),
}

# ---------------------------------------------------------------- APU
# (grupo, descripción, unidad, cantidad, desperdicio, valor unitario | 'C12'...)
# grupo: M materiales, E equipo, H herramienta menor (% MO), O mano de obra, T transporte
APUS = {
    "3.06": {
        "titulo": "Concreto de 3000 psi (21 MPa) para zapatas",
        "und": "M3",
        "nota": "Incluye formaleta lateral, colocación, vibrado y curado. El concreto de limpieza "
                "y el acero de refuerzo se pagan en los ítems 3.02 y 3.13.",
        "rec": [
            ("M", "Concreto premezclado 3000 psi (21 MPa), puesto en obra", "m3", 1.00, 0.03, 470000),
            ("M", "Formaleta lateral en madera (tabla 1x10\" + repisa, 4 usos)", "m2", 2.00, 0.00, 9000),
            ("M", "Puntilla 2\" a 3\"", "lb", 0.30, 0.00, 6000),
            ("M", "Desmoldante para formaleta", "gal", 0.03, 0.00, 38000),
            ("M", "Curador de concreto (membrana)", "kg", 0.40, 0.05, 9500),
            ("E", "Vibrador de concreto a gasolina (8 m3/día)", "día", 0.125, 0.00, 55000),
            ("E", "Carretillas, canaletas y elementos de vaciado (8 m3/día)", "día", 0.125, 0.00, 30000),
            ("H", "Herramienta menor", "%MO", 0.05, 0.00, None),
            ("O", "Cuadrilla 1 oficial + 3 ayudantes (rendimiento 8 m3/día = 1,0 hc/m3)", "hc", 1.00, 0.00, "C13"),
        ],
    },
    "4.05": {
        "titulo": "Cubierta en teja termoacústica instalada",
        "und": "M2",
        "nota": "Teja trapezoidal en lámina de acero cal. 0,27 mm con aislamiento termoacústico, "
                "fijada con tornillo autoperforante 14x3/4\" sobre correas cada 2,40 m como máximo. "
                "Incluye trabajo seguro en alturas (Res. 4272/2021).",
        "rec": [
            ("M", "Teja termoacústica trapezoidal acero cal. 0,27 mm", "m2", 1.00, 0.08, 48000),
            ("M", "Tornillo autoperforante 14x3/4\" con arandela de neopreno", "und", 6.00, 0.05, 450),
            ("M", "Cinta butílica de sello para traslapos", "ml", 0.50, 0.05, 3200),
            ("E", "Andamio tubular certificado (alquiler)", "módulo-día", 0.08, 0.00, 6000),
            ("E", "Kit de trabajo en alturas por persona (3 personas, 40 m2/día)", "día", 0.075, 0.00, 25000),
            ("E", "Atornillador eléctrico (40 m2/día)", "día", 0.025, 0.00, 25000),
            ("H", "Herramienta menor", "%MO", 0.05, 0.00, None),
            ("O", "Cuadrilla 1 oficial + 2 ayudantes certificados en alturas (rendimiento 40 m2/día = 0,20 hc/m2)", "hc", 0.20, 0.00, "C12"),
            ("T", "Izaje de tejas a cubierta (equipo y elementos de izaje)", "m2", 1.00, 0.00, 1200),
        ],
    },
    "7.01": {
        "titulo": "Enchape en porcelanato para baños públicos",
        "und": "M2",
        "nota": "Porcelanato antideslizante de alto tráfico sobre superficie pañetada. "
                "El pañete se paga en el ítem 6.02.",
        "rec": [
            ("M", "Porcelanato antideslizante 60x60 alto tráfico (PEI IV)", "m2", 1.00, 0.08, 46000),
            ("M", "Pegante para porcelanato (bulto 25 kg)", "bulto", 0.25, 0.00, 38000),
            ("M", "Boquilla para porcelanato", "kg", 0.40, 0.00, 6500),
            ("M", "Separadores / crucetas plásticas", "und", 8.00, 0.10, 60),
            ("E", "Cortadora de porcelanato (alquiler, 11,4 m2/día)", "día", 0.088, 0.00, 45000),
            ("H", "Herramienta menor", "%MO", 0.05, 0.00, None),
            ("O", "Cuadrilla 1 oficial enchapador + 1 ayudante (rendimiento 11,4 m2/día = 0,70 hc/m2)", "hc", 0.70, 0.00, "C11"),
        ],
    },
    "12.02": {
        "titulo": "Orinales",
        "und": "UND",
        "nota": "Orinal institucional en porcelana sanitaria con grifería push antivandálica, "
                "instalado y probado. Los puntos hidráulico y sanitario se pagan en los capítulos 5.",
        "rec": [
            ("M", "Orinal institucional en porcelana sanitaria, blanco", "und", 1.00, 0.00, 240000),
            ("M", "Llave push temporizada antivandálica para orinal", "und", 1.00, 0.00, 92000),
            ("M", "Kit de instalación (spud, acoples, tubo de abasto, chazos y tornillos)", "und", 1.00, 0.00, 32000),
            ("M", "Silicona antihongos", "und", 0.25, 0.00, 18000),
            ("M", "Soldadura y limpiador PVC", "und", 0.05, 0.00, 40000),
            ("H", "Herramienta menor", "%MO", 0.05, 0.00, None),
            ("O", "Cuadrilla 1 oficial plomero + 1 ayudante (rendimiento 4 und/día = 2,0 hc/und)", "hc", 2.00, 0.00, "C11"),
        ],
    },
}
GRUPOS = [("M", "I. MATERIALES"), ("E", "II. EQUIPO Y HERRAMIENTA"),
          ("O", "III. MANO DE OBRA"), ("T", "IV. TRANSPORTE")]


def calc_apu(cod):
    a = APUS[cod]
    filas = []
    mo = sum(Decimal(str(q)) * CUADRILLAS[vu][1] for g, d, u, q, w, vu in a["rec"] if g == "O")
    for g, d, u, q, w, vu in a["rec"]:
        if g == "O":
            v = CUADRILLAS[vu][1]
        elif g == "H":
            v = mo
        else:
            v = Decimal(vu)
        parcial = Decimal(str(q)) * (1 + Decimal(str(w))) * v
        filas.append((g, d, u, q, w, v, parcial))
    total = sum(f[6] for f in filas)
    return filas, total, r0(total)


APU_PRECIO = {c: calc_apu(c)[2] for c in APUS}

# ---------------------------------------------------------------- oferta
def total_con_factor(k):
    cd = 0
    precios = {}
    for _, cod, desc, und, q, vu in ITEMS:
        pu = APU_PRECIO.get(cod, None)
        if pu is None:
            pu = r0(Decimal(str(vu)) * k)
        precios[cod] = pu
        cd += r0(Decimal(str(q)) * pu)
    a, i, u = r0(cd * A_PCT), r0(cd * I_PCT), r0(cd * U_PCT)
    return precios, cd, a, i, u, cd + a + i + u


def buscar_factor():
    objetivo = Decimal(PRESUPUESTO_OFICIAL) * OBJETIVO_PCT
    mejor = None
    for n in range(8000, 10001):           # factor con 4 decimales
        k = Decimal(n) / 10000
        tot = total_con_factor(k)[-1]
        d = abs(tot - objetivo)
        if mejor is None or d < mejor[0]:
            mejor = (d, k)
    return mejor[1]


FACTOR = buscar_factor()
PRECIOS, CD, VA, VI, VU_, TOTAL = total_con_factor(FACTOR)


def total_item(cod):
    for _, c, desc, und, q, vu in ITEMS:
        if c == cod:
            return r0(Decimal(str(q)) * PRECIOS[c])


# ---------------------------------------------------------------- programación
# cod: (día de inicio, duración en días calendario, personal y equipo)
PROG = {
    "1.01": (1, 6, "Comisión de topografía (topógrafo + 2 cadeneros), estación total, nivel"),
    "1.02": (3, 6, "Retroexcavadora, operador, 2 ayudantes"),
    "1.03": (5, 22, "Volqueta 6 m3, 3 ayudantes"),
    "1.04": (1, 3, "1 oficial, 1 ayudante"),
    "1.05": (1, 4, "1 oficial, 2 ayudantes"),
    "2.01": (9, 14, "8 ayudantes, herramienta menor"),
    "2.02": (32, 14, "1 oficial, 3 ayudantes, vibrocompactador (canguro)"),
    "2.03": (42, 12, "1 oficial, 3 ayudantes, vibrocompactador, volqueta"),
    "3.01": (18, 10, "1 oficial, 4 ayudantes, mezcladora"),
    "3.02": (16, 8, "1 oficial, 3 ayudantes, mezcladora"),
    "3.03": (28, 10, "1 oficial, 3 ayudantes, vibrador, formaleta"),
    "3.04": (32, 16, "2 oficiales, 4 ayudantes, vibrador, formaleta"),
    "3.05": (58, 14, "2 oficiales, 4 ayudantes, andamio, vibrador, formaleta"),
    "3.06": (20, 14, "1 oficial, 3 ayudantes, vibrador, concreto premezclado"),
    "3.07": (66, 24, "2 oficiales, 6 ayudantes, vibrador, formaleta"),
    "3.08": (70, 14, "1 oficial, 2 ayudantes, formaleta"),
    "3.09": (45, 14, "2 oficiales, 4 ayudantes, andamio, vibrador, formaleta"),
    "3.10": (100, 26, "2 oficiales, 8 ayudantes, regla vibratoria, allanadora, cortadora de juntas"),
    "3.11": (62, 14, "2 oficiales, 6 ayudantes, casetón, andamio, vibrador"),
    "3.12": (70, 10, "1 oficial, 4 ayudantes, andamio, vibrador"),
    "3.13": (16, 70, "2 armadores, 4 ayudantes, cizalla, dobladora"),
    "4.01": (40, 49, "Taller: 2 soldadores, 2 ayudantes; montaje: grúa, 4 montadores, equipo de alturas"),
    "4.02": (70, 25, "2 montadores, 2 ayudantes, equipo de alturas, soldador"),
    "4.03": (86, 8, "2 montadores, tensores, equipo de alturas"),
    "4.04": (36, 7, "1 soldador, 1 ayudante"),
    "4.05": (88, 18, "1 oficial, 2 ayudantes certificados en alturas, andamio, atornillador"),
    "4.06": (80, 14, "2 montadores, equipo de alturas"),
    "4.07": (82, 12, "2 montadores, equipo de alturas"),
    "4.08": (30, 7, "1 soldador, 1 ayudante, equipo de corte"),
    "4.09": (30, 10, "1 oficial, 1 ayudante, plantilla de anclaje"),
    "4.10": (50, 30, "Taller: 1 soldador, 1 ayudante"),
    "5.01": (46, 10, "1 plomero, 2 ayudantes"),
    "5.02": (50, 8, "1 oficial, 1 ayudante"),
    "5.03": (104, 10, "1 oficial, 1 ayudante, equipo de alturas"),
    "5.04": (60, 4, "1 plomero, 1 ayudante"),
    "5.05": (74, 10, "1 plomero, 1 ayudante"),
    "5.06": (80, 7, "1 plomero, 1 ayudante"),
    "5.07": (84, 4, "1 plomero"),
    "5.08": (52, 8, "1 plomero, 1 ayudante"),
    "5.09": (52, 8, "1 plomero, 1 ayudante"),
    "5.10": (46, 12, "1 plomero, 2 ayudantes"),
    "5.11": (56, 10, "1 plomero, 1 ayudante"),
    "5.12": (56, 10, "1 plomero, 1 ayudante"),
    "5.13": (56, 10, "1 plomero, 1 ayudante"),
    "5.14": (120, 3, "1 plomero"),
    "6.01": (60, 28, "3 oficiales, 3 ayudantes, andamio"),
    "6.02": (84, 24, "3 oficiales, 3 ayudantes, andamio"),
    "7.01": (112, 14, "2 enchapadores, 2 ayudantes, cortadora"),
    "7.02": (122, 5, "1 enchapador"),
    "7.03": (118, 7, "1 marmolero, 1 ayudante"),
    "8.01": (90, 5, "1 electricista, 1 ayudante"),
    "8.02": (95, 3, "1 electricista"),
    "8.03": (96, 3, "1 electricista"),
    "8.04": (24, 5, "1 electricista, 1 ayudante, telurómetro"),
    "8.05": (98, 14, "2 electricistas, 1 ayudante"),
    "8.06": (98, 14, "2 electricistas, 1 ayudante"),
    "8.07": (106, 10, "2 electricistas, equipo de alturas"),
    "8.08": (98, 14, "2 electricistas, 1 ayudante"),
    "8.09": (98, 14, "2 electricistas, 1 ayudante"),
    "8.10": (96, 3, "1 electricista"),
    "8.11": (97, 2, "1 electricista"),
    "8.12": (106, 10, "2 electricistas, equipo de alturas"),
    "8.13": (108, 8, "2 electricistas, equipo de alturas"),
    "8.14": (112, 4, "1 electricista, 1 ayudante"),
    "9.01": (112, 8, "1 instalador, 1 ayudante"),
    "9.02": (116, 8, "1 oficial, 1 ayudante"),
    "9.03": (110, 10, "1 instalador, 1 ayudante, andamio"),
    "9.04": (126, 6, "1 instalador, 1 ayudante"),
    "9.05": (124, 5, "1 soldador, 1 ayudante"),
    "10.01": (115, 10, "1 oficial, 1 ayudante, cortadora de juntas"),
    "10.02": (84, 6, "1 oficial"),
    "10.03": (140, 8, "4 ayudantes"),
    "11.01": (92, 4, "1 oficial, 1 ayudante"),
    "11.02": (95, 2, "1 oficial"),
    "11.03": (88, 5, "1 soldador, 1 ayudante"),
    "12.01": (128, 8, "1 plomero, 1 ayudante"),
    "12.02": (128, 4, "1 plomero, 1 ayudante"),
    "12.03": (130, 6, "1 plomero, 1 ayudante"),
    "12.04": (134, 4, "1 plomero"),
    "12.05": (132, 4, "1 plomero"),
    "13.01": (112, 10, "2 pintores, andamio"),
    "13.02": (122, 10, "2 pintores, andamio"),
    "13.03": (134, 7, "2 pintores, equipo de demarcación"),
    "14.01": (130, 6, "1 soldador, 2 ayudantes, equipo de izaje"),
    "14.02": (132, 5, "1 oficial, 2 ayudantes"),
}
DIAS = 147
SEMANAS = 21
JORNADA = ("Lunes a viernes de 7:00 a.m. a 12:00 m. y de 1:00 p.m. a 4:00 p.m. (8 horas diarias); "
           "sábados de 7:00 a.m. a 11:00 a.m. (4 horas). Total 44 horas semanales (Ley 2101 de 2021). "
           "Domingos y festivos no se trabaja, "
           "salvo autorización de la interventoría.")

assert set(PROG) == {c for _, c, *_ in ITEMS}
for c, (ini, dur, _) in PROG.items():
    assert ini >= 1 and ini + dur - 1 <= DIAS, c


# ---------------------------------------------------------------- utilidades
def pesos(n):
    return "$ " + f"{n:,.0f}".replace(",", ".")


_U = ["", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE", "DIEZ",
      "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISÉIS", "DIECISIETE", "DIECIOCHO",
      "DIECINUEVE", "VEINTE", "VEINTIÚN", "VEINTIDÓS", "VEINTITRÉS", "VEINTICUATRO",
      "VEINTICINCO", "VEINTISÉIS", "VEINTISIETE", "VEINTIOCHO", "VEINTINUEVE"]
_D = ["", "", "", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
_C = ["", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS",
      "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]


def _cien(n):
    if n == 100:
        return "CIEN"
    c, r = divmod(n, 100)
    out = _C[c]
    if r:
        if r < 30:
            t = _U[r]
        else:
            d, u = divmod(r, 10)
            t = _D[d] + (" Y " + _U[u] if u else "")
        out = (out + " " + t).strip()
    return out


def letras(n):
    if n == 0:
        return "CERO"
    mill, resto = divmod(n, 1_000_000)
    miles, unid = divmod(resto, 1000)
    partes = []
    if mill:
        partes.append("UN MILLÓN" if mill == 1 else letras(mill) + " MILLONES")
    if miles:
        partes.append("MIL" if miles == 1 else _cien(miles) + " MIL")
    if unid:
        partes.append(_cien(unid))
    s = " ".join(partes)
    if mill and not resto:
        s += " DE"
    return s


if __name__ == "__main__":
    print("Hora ayudante", round(HORA_AY), "oficial", round(HORA_OF))
    for c in APUS:
        f, t, p = calc_apu(c)
        of = [x for x in ITEMS if x[1] == c][0][5]
        print(c, APUS[c]["titulo"][:40], p, "oficial", of, f"{p/of:.3f}")
    print("factor", FACTOR, "CD", CD, "A", VA, "I", VI, "U", VU_, "TOTAL", TOTAL,
          f"{TOTAL/PRESUPUESTO_OFICIAL:.4%}")
    print(letras(TOTAL))


EXP_PESOS = r0(Decimal(PRESUPUESTO_OFICIAL) * Decimal("0.5"))
EXP_SMMLV = Decimal(EXP_PESOS) / SMMLV
POLIZA_VALOR = r0(Decimal(PRESUPUESTO_OFICIAL) * Decimal("0.10"))


def capitulos():
    """[(cod, nombre, [códigos de ítems])] en el orden del formato."""
    out = []
    for f in FORMATO:
        if f[0] == "cap":
            out.append((f[1], f[2], []))
        else:
            out[-1][2].append(f[1])
    return out


CAPITULOS = capitulos()
SUBTOTAL = {c: sum(total_item(i) for i in its) for c, n, its in CAPITULOS}
assert sum(SUBTOTAL.values()) == CD
