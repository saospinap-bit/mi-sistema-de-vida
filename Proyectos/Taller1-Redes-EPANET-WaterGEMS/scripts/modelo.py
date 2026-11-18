"""Taller 1 - Simulacion de redes de distribucion (UNAL 2026-2).

Datos del enunciado y generacion de los archivos .inp de EPANET para los
escenarios del taller. Todos los datos salen del documento del taller.
"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # carpeta taller1/
MODELOS = os.path.join(BASE, "modelos")
RESULTADOS = os.path.join(BASE, "resultados")
FIGURAS = os.path.join(BASE, "figuras")
MOTOR = os.path.join(os.path.dirname(BASE), "motor")                  # EPANET 2.0.12 compilado

C_HW = 100  # hierro fundido, Hazen-Williams

# ---------------- Datos del taller ----------------
# Nudos: elevacion (m), demanda base (L/s), uso (curva del escenario 3)
JUNCTIONS = {
    "J-1": (250, 3.2, "RES"), "J-2": (265, 3.2, "RES"), "J-3": (235, 4.7, "RES"),
    "J-4": (235, 3.2, "COM"), "J-5": (270, 4.7, "COM"), "J-6": (270, 5.0, ""),
    "J-7": (277, 0.0, "RES"), "J-8": (276, 3.2, "COM"),
}
PATTERN_ID = {"RES": "RESIDENCIAL", "COM": "COMERCIAL"}
# Nudos auxiliares (en EPANET bombas y valvulas son tramos entre dos nudos)
AUX = {
    "PMP-1-S": 288, "PMP-1-D": 288,          # succion / descarga de la bomba
    "PRV-1-A": 250, "PRV-1-B": 250,          # aguas arriba / abajo de cada PRV
    "PRV-2-A": 253, "PRV-2-B": 253,
    "PRV-3-A": 253, "PRV-3-B": 253,
}
RESERVOIR = ("R-1", 290)
# Tanque: base 308, min 314, inicial 320, max 326 (elevaciones), D = 15 m
TANK = dict(id="T-1", base=308, init=320 - 308, min=314 - 308, max=326 - 308, diam=15)
# Tuberias: (nudo inicial, nudo final, longitud m, diametro mm)
PIPES = {
    "P-1": ("R-1", "PMP-1-S", 3, 300),
    "P-2": ("PMP-1-D", "J-1", 1525, 300),
    "P-3": ("J-1", "J-2", 300, 200),
    "P-4": ("J-2", "PRV-1-A", 30, 200),
    "P-5": ("PRV-1-B", "J-3", 460, 200),
    "P-6": ("J-3", "J-4", 460, 200),
    "P-7": ("PRV-2-B", "J-4", 300, 200),
    "P-8": ("J-5", "PRV-2-A", 30, 200),
    "P-9": ("J-6", "J-5", 460, 200),
    "P-10": ("J-1", "J-6", 460, 200),
    "P-11": ("J-1", "J-7", 550, 200),
    "P-12": ("J-7", "J-8", 460, 250),
    "P-13": ("J-8", "J-5", 300, 250),
    "P-14": ("J-6", "PRV-3-A", 30, 200),
    "P-15": ("PRV-3-B", "J-3", 300, 200),
    "P-16": ("J-7", "T-1", 460, 300),        # dibujada de J-7 hacia el tanque: Q > 0 = entra a T-1
}
# PRV: nudo entrada, nudo salida, elevacion, diametro mm, HGL de consigna (m)
PRVS = {
    "PRV-1": ("PRV-1-A", "PRV-1-B", 250, 200, 285.0),
    "PRV-2": ("PRV-2-A", "PRV-2-B", 253, 200, 286.5),
    "PRV-3": ("PRV-3-A", "PRV-3-B", 253, 200, 286.5),
}
PRV_TUBOS = {"PRV-1": ("P-4", "P-5"), "PRV-2": ("P-8", "P-7"), "PRV-3": ("P-14", "P-15")}
# Curva de la bomba (Q L/s, H m) y elevacion
PUMP_CURVE = [(0.0, 48.8), (63.2, 39.6), (88.4, 33.8)]
PUMP_Z = 288
# Curvas de consumo leidas de la grafica (horas 0..23; la hora 24 = hora 0)
RES = [0.1, 0.1, 0.1, 0.1, 0.3, 0.8, 1.8, 2.0, 1.4, 1.0, 0.9, 0.8,
       0.7, 1.2, 1.4, 0.8, 0.7, 0.9, 1.0, 1.2, 1.4, 1.1, 0.7, 0.5]
COM = [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.4, 0.6, 1.2, 1.4, 1.5, 1.2,
       1.5, 1.1, 1.2, 1.0, 0.9, 1.2, 1.1, 0.7, 0.5, 0.2, 0.2, 0.1]

# Coordenadas tomadas de la figura del taller (solo para dibujo)
COORDS = {
    "R-1": (115, 335), "PMP-1-S": (300, 335), "PMP-1-D": (320, 335),
    "J-1": (505, 335), "J-6": (965, 335), "J-5": (1398, 335),
    "J-7": (648, 567), "J-8": (1235, 567), "T-1": (398, 710),
    "J-2": (505, 32), "J-3": (965, 32), "J-4": (1398, 32),
    "PRV-1-A": (708, 32), "PRV-1-B": (728, 32),
    "PRV-3-A": (965, 192), "PRV-3-B": (965, 172),
    "PRV-2-A": (1398, 197), "PRV-2-B": (1398, 177),
}

# Escenarios: titulo, tanque conectado, periodo extendido, curva de J-6
ESCENARIOS = {
    "E1": ("Escenario1_Estatico_sin_P16.inp",
           "Taller 1 - Escenario 1: estado estatico, sin tuberia P-16 (P-16 cerrada)", False, False, ""),
    "E2": ("Escenario2_Estatico_con_tanque.inp",
           "Taller 1 - Escenario 2: estado estatico, tanque T-1 en funcionamiento", True, False, ""),
    "E3": ("Escenario3_Periodo_extendido_24h.inp",
           "Taller 1 - Escenario 3: periodo extendido 24 h con curvas de consumo", True, True, ""),
    "E3b": ("Escenario3b_Sensibilidad_J6_residencial.inp",
            "Taller 1 - Escenario 3b: periodo extendido 24 h, J-6 con uso residencial (sensibilidad)", True, True, "RES"),
}


def ruta(esc):
    return os.path.join(MODELOS, ESCENARIOS[esc][0])


def write_inp(path, title, with_tank, eps, j6="", prv_hgl=None, controls=()):
    """Escribe un .inp. prv_hgl permite cambiar consignas (HGL) y controls agrega [CONTROLS]."""
    L = []
    a = L.append
    a("[TITLE]")
    a(title)
    a("UNAL - Facultad de Ingenieria - Depto. Ingenieria Civil - 2026-2")
    a("\n[JUNCTIONS]\n;ID\tElev\tDemand\tPattern")
    for j, (z, q, uso) in JUNCTIONS.items():
        if j == "J-6":
            uso = j6
        pat = PATTERN_ID[uso] if (eps and uso) else ""
        a(f"{j}\t{z}\t{q}\t{pat}")
    for j, z in AUX.items():
        a(f"{j}\t{z}\t0\t")
    a("\n[RESERVOIRS]\n;ID\tHead\tPattern")
    a(f"{RESERVOIR[0]}\t{RESERVOIR[1]}\t")
    a("\n[TANKS]\n;ID\tElev\tInitLvl\tMinLvl\tMaxLvl\tDiam\tMinVol\tVolCurve")
    t = TANK
    a(f"{t['id']}\t{t['base']}\t{t['init']}\t{t['min']}\t{t['max']}\t{t['diam']}\t0\t")
    a("\n[PIPES]\n;ID\tNode1\tNode2\tLength\tDiam\tRough\tMLoss\tStatus")
    for p, (n1, n2, l, d) in PIPES.items():
        status = "Open" if (p != "P-16" or with_tank) else "Closed"
        a(f"{p}\t{n1}\t{n2}\t{l}\t{d}\t{C_HW}\t0\t{status}")
    a("\n[PUMPS]\n;ID\tNode1\tNode2\tParameters")
    a("PMP-1\tPMP-1-S\tPMP-1-D\tHEAD BOMBA-1")
    a("\n[VALVES]\n;ID\tNode1\tNode2\tDiam\tType\tSetting\tMLoss")
    for v, (n1, n2, z, d, hgl) in PRVS.items():
        if prv_hgl and v in prv_hgl:
            hgl = prv_hgl[v]
        a(f"{v}\t{n1}\t{n2}\t{d}\tPRV\t{hgl - z:.2f}\t0")
    a("\n[PATTERNS]\n;ID\tMultipliers")
    if eps:
        for uso, vals in (("RES", RES), ("COM", COM)):
            a(f";Curva de consumo uso {PATTERN_ID[uso].lower()} (horas 0 a 23; la hora 24 = hora 0)")
            for i in range(0, 24, 6):
                a(PATTERN_ID[uso] + "\t" + "\t".join(f"{v:.2f}" for v in vals[i:i + 6]))
    a("\n[CURVES]\n;ID\tX-Value(L/s)\tY-Value(m)\n;PUMP: Curva caracteristica PMP-1 (Q en L/s, H en m)")
    for q, h in PUMP_CURVE:
        a(f"BOMBA-1\t{q}\t{h}")
    a("\n[CONTROLS]")
    for c in controls:
        a(c)
    a("\n[TIMES]")
    if eps:
        a("Duration\t24:00\nHydraulic Timestep\t1:00\nPattern Timestep\t1:00\n"
          "Pattern Start\t0:00\nReport Timestep\t1:00\nReport Start\t0:00\nStart ClockTime\t12 am")
    else:
        a("Duration\t0:00")
    a("\n[REPORT]\nStatus\tFull\nSummary\tYes\nNodes\tAll\nLinks\tAll")
    a("\n[OPTIONS]\nUnits\tLPS\nHeadloss\tH-W\nSpecific Gravity\t1.0\nViscosity\t1.0\n"
      "Trials\t200\nAccuracy\t0.0001\nUnbalanced\tContinue 10\n"
      "Demand Multiplier\t1.0\nEmitter Exponent\t0.5")
    a("\n[COORDINATES]\n;Node\tX\tY")
    for n, (x, y) in COORDS.items():
        a(f"{n}\t{x}\t{y}")
    a("\n[END]")
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(L) + "\n")


def generar():
    os.makedirs(MODELOS, exist_ok=True)
    for esc, (fn, title, tank, eps, j6) in ESCENARIOS.items():
        write_inp(os.path.join(MODELOS, fn), title, tank, eps, j6)
    return [ruta(e) for e in ESCENARIOS]


if __name__ == "__main__":
    for p in generar():
        print("escrito", p)
