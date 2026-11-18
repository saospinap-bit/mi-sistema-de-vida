"""Acceso directo al toolkit de EPANET (version 2.0.12 compilada del codigo oficial, y 2.2 de WNTR).

run(inp, version) corre el analisis hidraulico paso a paso (ENrunH / ENnextH) y guarda los
resultados de TODOS los pasos hidraulicos, incluidos los intermedios (p. ej. cuando un tanque
se llena), que no aparecen en los reportes horarios.
"""
import ctypes
import os
import tempfile

import pandas as pd

from modelo import MOTOR

_WNTR_LIB = None
try:
    import wntr
    _WNTR_LIB = os.path.join(os.path.dirname(wntr.__file__), "epanet", "libepanet", "linux-x64", "libepanet22.so")
except ImportError:  # pragma: no cover
    pass

LIBS = {"2.0.12": os.path.join(MOTOR, "libepanet20.so"), "2.2": _WNTR_LIB}

# Codigos del toolkit (iguales en 2.0 y 2.2)
EN_NODECOUNT, EN_LINKCOUNT = 0, 2
EN_ELEVATION, EN_DEMAND, EN_HEAD, EN_PRESSURE = 0, 9, 10, 11
EN_DIAMETER, EN_LENGTH, EN_FLOW, EN_VELOCITY, EN_STATUS, EN_SETTING = 0, 1, 8, 9, 11, 12
NODE_TYPES = {0: "Junction", 1: "Reservoir", 2: "Tank"}
LINK_TYPES = {0: "CVPipe", 1: "Pipe", 2: "Pump", 3: "PRV", 4: "PSV", 5: "PBV", 6: "FCV", 7: "TCV", 8: "GPV"}


class Resultado:
    """Resultados por paso hidraulico. Tablas indexadas por tiempo (s); unidades del .inp (L/s, m)."""

    def __init__(self, version):
        self.version = version
        self.nodes, self.links = [], []
        self.node_type, self.link_type, self.link_nodes = {}, {}, {}
        self.elev = {}
        self.warnings = []
        self._rows = {k: [] for k in ("head", "pressure", "demand", "flow", "velocity", "status", "setting")}
        self.times = []

    def _finish(self):
        for k, rows in self._rows.items():
            cols = self.nodes if k in ("head", "pressure", "demand") else self.links
            setattr(self, k, pd.DataFrame(rows, index=self.times, columns=cols))
        del self._rows


def _check(err, fn):
    if err > 100:
        raise RuntimeError(f"EPANET: error {err} en {fn}")
    return err


def run(inp, version="2.0.12"):
    lib = ctypes.CDLL(LIBS[version])
    r = Resultado(version)
    tmp = tempfile.mkdtemp()
    rpt = os.path.join(tmp, "x.rpt").encode()
    out = os.path.join(tmp, "x.out").encode()
    _check(lib.ENopen(inp.encode(), rpt, out), "ENopen")
    try:
        n, m = ctypes.c_int(), ctypes.c_int()
        lib.ENgetcount(EN_NODECOUNT, ctypes.byref(n))
        lib.ENgetcount(EN_LINKCOUNT, ctypes.byref(m))
        buf = ctypes.create_string_buffer(64)
        typ = ctypes.c_int()
        val = ctypes.c_float()
        for i in range(1, n.value + 1):
            lib.ENgetnodeid(i, buf)
            nid = buf.value.decode()
            r.nodes.append(nid)
            lib.ENgetnodetype(i, ctypes.byref(typ))
            r.node_type[nid] = NODE_TYPES[typ.value]
            lib.ENgetnodevalue(i, EN_ELEVATION, ctypes.byref(val))
            r.elev[nid] = val.value
        a, b = ctypes.c_int(), ctypes.c_int()
        for i in range(1, m.value + 1):
            lib.ENgetlinkid(i, buf)
            lid = buf.value.decode()
            r.links.append(lid)
            lib.ENgetlinktype(i, ctypes.byref(typ))
            r.link_type[lid] = LINK_TYPES[typ.value]
            lib.ENgetlinknodes(i, ctypes.byref(a), ctypes.byref(b))
            r.link_nodes[lid] = (r.nodes[a.value - 1], r.nodes[b.value - 1])

        _check(lib.ENopenH(), "ENopenH")
        _check(lib.ENinitH(0), "ENinitH")
        t, dt = ctypes.c_long(), ctypes.c_long()
        while True:
            w = _check(lib.ENrunH(ctypes.byref(t)), "ENrunH")
            if w:
                r.warnings.append((t.value, w))
            r.times.append(t.value)
            for key, code in (("head", EN_HEAD), ("pressure", EN_PRESSURE), ("demand", EN_DEMAND)):
                row = []
                for i in range(1, n.value + 1):
                    lib.ENgetnodevalue(i, code, ctypes.byref(val))
                    row.append(val.value)
                r._rows[key].append(row)
            for key, code in (("flow", EN_FLOW), ("velocity", EN_VELOCITY), ("status", EN_STATUS),
                              ("setting", EN_SETTING)):
                row = []
                for i in range(1, m.value + 1):
                    lib.ENgetlinkvalue(i, code, ctypes.byref(val))
                    row.append(val.value)
                r._rows[key].append(row)
            _check(lib.ENnextH(ctypes.byref(dt)), "ENnextH")
            if dt.value <= 0:
                break
        lib.ENcloseH()
    finally:
        lib.ENclose()
    r._finish()
    return r


def hhmmss(t):
    t = int(round(t))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"


def hhmm(t):
    t = int(round(t))
    s = t % 60
    return f"{t // 3600}:{t % 3600 // 60:02d}" + (f":{s:02d}" if s else "")
