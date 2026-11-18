"""Figuras del informe (todas salen de los resultados de calculos.py)."""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.lines import Line2D
import numpy as np

import modelo as M
import calculos as C

plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
                     "figure.dpi": 100, "savefig.dpi": 220, "font.family": "DejaVu Sans"})
J = C.J
AZUL, ROJO, VERDE, NARANJA, GRIS = "#1f4e79", "#c0392b", "#1e8449", "#e67e22", "#7f8c8d"
COL_J = dict(zip(J, plt.get_cmap("tab10").colors[:8]))
XY = M.COORDS
PRV_XY = {v: tuple(np.mean([XY[a], XY[b]], axis=0)) for v, (a, b, *_r) in M.PRVS.items()}
PMP_XY = tuple(np.mean([XY["PMP-1-S"], XY["PMP-1-D"]], axis=0))


def _save(fig, nombre):
    os.makedirs(M.FIGURAS, exist_ok=True)
    p = os.path.join(M.FIGURAS, nombre)
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    return p


def _pos(n):
    """Posicion de dibujo: los nudos auxiliares se dibujan en el simbolo de su elemento."""
    if n.startswith("PMP-1"):
        return PMP_XY
    for v in M.PRVS:
        if n.startswith(v):
            return PRV_XY[v]
    return XY[n]


# ------------------------------------------------------------------ simbolos
def _simbolos(ax, prv_color=None):
    x, y = XY["R-1"]
    ax.add_patch(plt.Polygon([[x - 22, y + 14], [x + 22, y + 14], [x, y - 12]], closed=True,
                             fc="#aed6f1", ec="k", lw=1, zorder=5))
    x, y = XY["T-1"]
    ax.add_patch(plt.Rectangle((x - 18, y - 18), 36, 36, fc="#aed6f1", ec="k", lw=1, zorder=5))
    ax.plot([x - 18, x + 18], [y + 4, y + 4], color=AZUL, lw=1, zorder=6)
    x, y = PMP_XY
    ax.add_patch(plt.Circle((x, y), 16, fc="#f9e79f", ec="k", lw=1, zorder=5))
    ax.annotate("", xy=(x + 12, y), xytext=(x - 10, y), arrowprops=dict(arrowstyle="-|>", color="k", lw=1), zorder=6)
    for v, (xv, yv) in PRV_XY.items():
        vert = v != "PRV-1"
        s = 14
        fc = (prv_color or {}).get(v, "#f5b7b1")
        if vert:
            tri1 = [[xv - s, yv + s], [xv + s, yv + s], [xv, yv]]
            tri2 = [[xv - s, yv - s], [xv + s, yv - s], [xv, yv]]
        else:
            tri1 = [[xv - s, yv - s], [xv - s, yv + s], [xv, yv]]
            tri2 = [[xv + s, yv - s], [xv + s, yv + s], [xv, yv]]
        for tri in (tri1, tri2):
            ax.add_patch(plt.Polygon(tri, closed=True, fc=fc, ec="k", lw=1, zorder=5))


def _tuberias(ax, lw=None, color=None):
    for p, (a, b, L, d) in M.PIPES.items():
        (x1, y1), (x2, y2) = _pos(a), _pos(b)
        ax.plot([x1, x2], [y1, y2], color=(color or {}).get(p, AZUL), lw=(lw or {}).get(p, 2.2),
                solid_capstyle="round", zorder=2)


def _base(figsize=(10.5, 6.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    ax.set_xlim(40, 1720)
    ax.set_ylim(-85, 800)
    ax.axis("off")
    return fig, ax


# Posicion de etiquetas (dx, dy, ha, va) para nudos y tuberias
LBL_N = {"J-1": (-14, 16, "right", "bottom"), "J-6": (0, 16, "center", "bottom"), "J-5": (16, 6, "left", "bottom"),
         "J-7": (14, 14, "left", "bottom"), "J-8": (0, 16, "center", "bottom"), "J-2": (0, -16, "center", "top"),
         "J-3": (0, -16, "center", "top"), "J-4": (0, -16, "center", "top")}
LBL_P = {"P-1": (0, -14, "center", "top"), "P-2": (0, -14, "center", "top"), "P-3": (-12, 0, "right", "center"),
         "P-4": (0, 12, "center", "bottom"), "P-5": (0, 12, "center", "bottom"), "P-6": (0, 12, "center", "bottom"),
         "P-7": (-12, 0, "right", "center"), "P-8": (-12, 0, "right", "center"), "P-9": (0, -14, "center", "top"),
         "P-10": (0, -14, "center", "top"), "P-11": (-26, 0, "right", "center"), "P-12": (0, 12, "center", "bottom"),
         "P-13": (26, 0, "left", "center"), "P-14": (-12, 0, "right", "center"), "P-15": (-12, 0, "right", "center"),
         "P-16": (14, 10, "left", "bottom")}
LBL_PRV = {"PRV-1": (0, -22, "center", "top"), "PRV-2": (22, 0, "left", "center"), "PRV-3": (22, 0, "left", "center")}


def _mid(p):
    a, b, *_r = M.PIPES[p]
    (x1, y1), (x2, y2) = _pos(a), _pos(b)
    return (x1 + x2) / 2, (y1 + y2) / 2, (x2 - x1, y2 - y1)


# ------------------------------------------------------------------ Figura 1: datos
def fig_red_datos():
    fig, ax = _base()
    _tuberias(ax)
    _simbolos(ax)
    for j in J:
        x, y = XY[j]
        z, q, _u = M.JUNCTIONS[j]
        ax.plot(x, y, "o", ms=8, mfc="white", mec="k", zorder=6)
        dx, dy, ha, va = LBL_N[j]
        ax.text(x + dx, y + dy, f"{j}\nz = {z} m\nq = {q} L/s", ha=ha, va=va, fontsize=7.5,
                bbox=dict(fc="white", ec="none", alpha=.85, pad=.5), zorder=7)
    for p, (a, b, L, d) in M.PIPES.items():
        xm, ym, _v = _mid(p)
        dx, dy, ha, va = LBL_P[p]
        ax.text(xm + dx, ym + dy, f"{p}\n{L} m · Ø{d}", ha=ha, va=va, fontsize=6.8, color=AZUL, zorder=7,
                bbox=dict(fc="white", ec="none", alpha=.8, pad=.3))
    for v, (a, b, z, d, hgl) in M.PRVS.items():
        x, y = PRV_XY[v]
        dx, dy, ha, va = LBL_PRV[v]
        ax.text(x + dx, y + dy, f"{v}\nz = {z} m · Ø{d}\nHGL = {hgl:.1f} m", ha=ha, va=va, fontsize=7.2,
                color=ROJO, zorder=7, bbox=dict(fc="white", ec="none", alpha=.85, pad=.4))
    x, y = XY["R-1"]
    ax.text(x, y + 22, "R-1\nnivel 290 m", ha="center", va="bottom", fontsize=7.5)
    x, y = PMP_XY
    ax.text(x, y + 22, "PMP-1\nz = 288 m", ha="center", va="bottom", fontsize=7.5)
    x, y = XY["T-1"]
    ax.text(x + 26, y + 6, "T-1 (D = 15 m)\nbase 308 · mín 314\ninicial 320 · máx 326 m", ha="left", va="bottom",
            fontsize=7.5, bbox=dict(fc="white", ec="none", alpha=.85, pad=.4))
    return _save(fig, "fig01_red_datos.png")


# ------------------------------------------------------------------ Figuras 3 y 4: resultados
def fig_red_resultados(S, r, nombre, titulo):
    t = 0
    Q = r.flow.loc[t]
    qmax = max(abs(Q[p]) for p in M.PIPES)
    lw = {p: 1.2 + 4.5 * abs(Q[p]) / qmax for p in M.PIPES}
    col = {p: (GRIS if abs(Q[p]) < 0.005 else AZUL) for p in M.PIPES}
    est = S["prv"]["estado"].to_dict()
    pc = {v: ("#58d68d" if e == "Activa" else "#ec7063" if e == "Cerrada" else "#f7dc6f") for v, e in est.items()}
    fig, ax = _base()
    _tuberias(ax, lw, col)
    _simbolos(ax, pc)
    norm = colors.Normalize(40, 90)
    cmap = plt.get_cmap("viridis_r")
    for j in J:
        x, y = XY[j]
        p = S["nudos"].loc[j, "p"]
        ax.scatter([x], [y], s=110, c=[cmap(norm(p))], edgecolors="k", zorder=6)
        dx, dy, ha, va = (16, -16, "left", "top") if j == "J-1" else LBL_N[j]
        ax.text(x + dx, y + dy, f"{j}\np = {p:.2f} m", ha=ha, va=va, fontsize=7.8, weight="bold", zorder=7,
                bbox=dict(fc="white", ec="none", alpha=.85, pad=.4))
    for p, (a, b, L, d) in M.PIPES.items():
        xm, ym, (vx, vy) = _mid(p)
        q = Q[p]
        if abs(q) >= 0.005:
            u = np.array([vx, vy]) / np.hypot(vx, vy) * np.sign(q)
            ax.annotate("", xy=(xm + 13 * u[0], ym + 13 * u[1]), xytext=(xm - 13 * u[0], ym - 13 * u[1]),
                        arrowprops=dict(arrowstyle="-|>", color=ROJO, lw=1.4, mutation_scale=13), zorder=8)
        dx, dy, ha, va = LBL_P[p]
        txt = f"{p}\n{abs(q):.2f} L/s" if r.status.loc[t, p] != 0 else f"{p}\ncerrada"
        ax.text(xm + dx, ym + dy, txt, ha=ha, va=va, fontsize=6.9, color=AZUL if abs(q) >= .005 else GRIS,
                zorder=7, bbox=dict(fc="white", ec="none", alpha=.8, pad=.3))
    for v, row in S["prv"].iterrows():
        x, y = PRV_XY[v]
        dx, dy, ha, va = LBL_PRV[v]
        ax.text(x + dx, y + dy, f"{v}: {row['estado']}\nQ = {row['Q']:.2f} L/s\nHGL sal. = {row['Ho']:.2f} m",
                ha=ha, va=va, fontsize=7.2, color=ROJO, zorder=7, bbox=dict(fc="white", ec="none", alpha=.85, pad=.4))
    b = S["bomba"]
    x, y = PMP_XY
    ax.text(x, y + 22, f"PMP-1\nQ = {b['Q']:.2f} L/s\nH = {b['H']:.2f} m", ha="center", va="bottom", fontsize=7.5,
            weight="bold")
    x, y = XY["R-1"]
    ax.text(x, y - 18, "R-1\n290 m", ha="center", va="top", fontsize=7.5)
    x, y = XY["T-1"]
    if S["P16_estado"] == "Cerrada":
        tt = "T-1 fuera de servicio\n(P-16 cerrada)"
    else:
        tt = f"T-1: entran {S['T_Q']:.2f} L/s\nHGL = {S['T_H']:.2f} m"
    ax.text(x + 26, y + 6, tt, ha="left", va="bottom", fontsize=7.5, weight="bold",
            bbox=dict(fc="white", ec="none", alpha=.85, pad=.4))
    sm = cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, fraction=.025, pad=.01)
    cb.set_label("Presión en el nudo (m)")
    leg = [Line2D([0], [0], color=ROJO, marker=">", lw=0, label="sentido del flujo"),
           Line2D([0], [0], color=AZUL, lw=3, label="ancho ∝ caudal"),
           Line2D([0], [0], marker="s", color="w", mfc="#58d68d", mec="k", ms=9, label="PRV activa"),
           Line2D([0], [0], marker="s", color="w", mfc="#ec7063", mec="k", ms=9, label="PRV cerrada")]
    ax.legend(handles=leg, loc="upper center", fontsize=7.5, frameon=False, ncol=4, bbox_to_anchor=(.5, .02))
    if titulo:
        ax.set_title(titulo, fontsize=10)
    return _save(fig, nombre)


# ------------------------------------------------------------------ Figura 2: curvas de consumo
def fig_patrones():
    h = np.arange(25)
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    for vals, lab, c, mk in ((M.RES, "Residencial (J-1, J-2, J-3, J-7)", AZUL, "D"),
                             (M.COM, "Comercial (J-4, J-5, J-8)", ROJO, "s")):
        v = list(vals) + [vals[0]]
        ax.step(h, v, where="post", color=c, lw=1.8, label=lab)
        ax.plot(h, v, mk, color=c, ms=3.5)
    ax.axhline(1, color=GRIS, lw=.8, ls=":")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 2.2)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Multiplicador del caudal medio")
    ax.grid(alpha=.3)
    ax.set_ylim(0, 2.6)
    ax.legend(loc="upper right", ncol=2)
    return _save(fig, "fig02_curvas_consumo.png")


def _horas(e):
    return np.array(e["serie"].index, dtype=float) / 3600


# ------------------------------------------------------------------ Figura 5: caudales EPS
def fig_eps_caudales(e):
    s, h = e["serie"], _horas(e)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.step(h, s["Qb"], where="post", color=NARANJA, lw=2, label="Caudal de la bomba PMP-1")
    ax.step(h, s["dem"], where="post", color=VERDE, lw=1.6, label="Demanda total de la red")
    ax.step(h, s["Q16"], where="post", color=AZUL, lw=1.6, ls="--", label="Caudal que entra a T-1 (P-16)")
    tl = e["t_lleno"] / 3600
    ax.axvline(tl, color=GRIS, ls=":", lw=1)
    ax.text(tl + .2, s["Qb"].max() * .97, f"T-1 lleno\n{C.motor.hhmmss(e['t_lleno'])} h", fontsize=7.5, va="top")
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel("Hora")
    ax.set_ylabel("Caudal (L/s)")
    ax.grid(alpha=.3)
    ax.legend(loc="upper right")
    return _save(fig, "fig05_eps_caudales.png")


# ------------------------------------------------------------------ Figura 6: curva de la bomba
def fig_bomba(R):
    q = np.linspace(0, 95, 300)
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.plot(q, C.h_bomba(q), color="k", lw=1.6, label=f"$H = {C.A_P:.1f} - {C.B_P:.6f}\\,Q^{{{C.C_P:.4f}}}$")
    pts = np.array(M.PUMP_CURVE)
    ax.plot(pts[:, 0], pts[:, 1], "ks", mfc="white", ms=7, label="Puntos del enunciado")
    s = R["E3"]["serie"]
    ax.plot(s["Qb"], s["Hb"], "o", color=AZUL, ms=4, alpha=.7, label="Escenario 3 (cada paso)")
    for esc, c, mk in (("E1", VERDE, "D"), ("E2", ROJO, "^")):
        b = R[esc]["bomba"]
        ax.plot(b["Q"], b["H"], mk, color=c, ms=9, mec="k", label=f"Escenario {esc[1]}: {b['Q']:.2f} L/s; {b['H']:.2f} m")
    ax.set_xlim(0, 95)
    ax.set_ylim(30, 50)
    ax.set_xlabel("Caudal Q (L/s)")
    ax.set_ylabel("Altura de bombeo H (m)")
    ax.grid(alpha=.3)
    ax.legend(loc="lower left", fontsize=7.5)
    return _save(fig, "fig06_curva_bomba.png")


# ------------------------------------------------------------------ Figura 7: tanque y bomba
def fig_eps_tanque(e):
    s, h = e["serie"], _horas(e)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True)
    a1.plot(h, s["HT"], "-", color=AZUL, lw=2, marker="o", ms=3)
    a1.axhline(C.H_MAX, color=ROJO, ls="--", lw=.9)
    a1.axhline(M.TANK["base"] + M.TANK["min"], color=ROJO, ls="--", lw=.9)
    a1.text(24.2, C.H_MAX, "máx. 326", va="center", fontsize=7.5, color=ROJO)
    a1.text(24.2, 314, "mín. 314", va="center", fontsize=7.5, color=ROJO)
    a1.set_ylabel("Agua en T-1 (m)")
    a1.set_ylim(312, 328)
    a1.grid(alpha=.3)
    a2.step(h, s["Hb"], where="post", color=NARANJA, lw=2)
    a2.set_ylabel("Altura bomba (m)")
    a2.set_xlabel("Hora")
    a2.grid(alpha=.3)
    a2.set_xlim(0, 24)
    a2.set_xticks(range(0, 25, 2))
    for a in (a1, a2):
        a.axvline(e["t_lleno"] / 3600, color=GRIS, ls=":", lw=1)
    return _save(fig, "fig07_eps_tanque_bomba.png")


# ------------------------------------------------------------------ Figura 8: presiones
def fig_eps_presiones(e):
    h = _horas(e)
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for j in J:
        ls = (0, (4, 3)) if j == "J-4" else "-"
        ax.step(h, e["P"][j].values, where="post", color=COL_J[j], lw=1.5, ls=ls,
                label="J-4 (sobre J-3)" if j == "J-4" else j, zorder=3 if j == "J-4" else 2)
    ax.axhline(15, color=ROJO, ls="--", lw=.9)
    ax.axhline(50, color=ROJO, ls=":", lw=.9)
    ax.text(.2, 16, "mínima RAS 15 m (Art. 61)", fontsize=7.2, color=ROJO)
    ax.text(8.4, 49.2, "50 m: máxima estática RAS (Art. 62)", fontsize=7.2, color=ROJO, va="top")
    ax.axvline(e["t_lleno"] / 3600, color=GRIS, ls=":", lw=1)
    ax.set_xlim(0, 24)
    ax.set_ylim(10, 95)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel("Hora")
    ax.set_ylabel("Presión (m)")
    ax.grid(alpha=.3)
    ax.legend(ncol=8, loc="upper center", bbox_to_anchor=(.5, -.14), frameon=False)
    return _save(fig, "fig08_eps_presiones.png")


# ------------------------------------------------------------------ Figura 9: PRV
def fig_eps_prv(e):
    s, h = e["serie"], _horas(e)
    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    ax.step(h, s["Q2"], where="post", color=AZUL, lw=1.8, label="PRV-2 (activa)")
    ax.step(h, s["Q3"], where="post", color=VERDE, lw=1.8, label="PRV-3 (activa)")
    ax.step(h, s["Q1"], where="post", color=ROJO, lw=1.8, ls="--", label="PRV-1 (cerrada)")
    ax.step(h, s["Q2"] + s["Q3"], where="post", color="k", lw=1, ls=":", label="PRV-2 + PRV-3")
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel("Hora")
    ax.set_ylabel("Caudal (L/s)")
    ax.set_ylim(-.5, 15)
    ax.grid(alpha=.3)
    ax.legend(loc="upper right", ncol=4, fontsize=7.5)
    return _save(fig, "fig09_eps_prv.png")


# ------------------------------------------------------------------ Figura 10: comparacion
def fig_comparacion(R):
    x = np.arange(len(J))
    w = .26
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    p1, p2 = R["E1"]["nudos"]["p"], R["E2"]["nudos"]["p"]
    ext = R["E3"]["ext"]
    ax.bar(x - w, p1, w, color=VERDE, label="Escenario 1")
    ax.bar(x, p2, w, color=ROJO, label="Escenario 2")
    ax.bar(x + w, ext["pmax"] - ext["pmin"], w, bottom=ext["pmin"], color=AZUL, alpha=.75,
           label="Escenario 3 (rango del día)")
    ax.plot(x + w, ext["pmed"], "k_", ms=10, mew=1.5, label="Escenario 3 (media)")
    ax.axhline(15, color=ROJO, ls="--", lw=.9)
    ax.axhline(50, color=ROJO, ls=":", lw=.9)
    ax.set_xticks(x)
    ax.set_xticklabels(J)
    ax.set_ylabel("Presión (m)")
    ax.set_ylim(0, 95)
    ax.grid(axis="y", alpha=.3)
    hs, ls_ = ax.get_legend_handles_labels()
    orden = [ls_.index(x) for x in ("Escenario 1", "Escenario 2", "Escenario 3 (rango del día)", "Escenario 3 (media)")]
    ax.legend([hs[i] for i in orden], [ls_[i] for i in orden], ncol=4, loc="upper center",
              bbox_to_anchor=(.5, -.1), frameon=False)
    return _save(fig, "fig10_comparacion_presiones.png")


# ------------------------------------------------------------------ Figura 11: sensibilidad J-6
def fig_sensibilidad(R):
    e3, e3b = R["E3"], R["E3b"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    a1.plot(_horas(e3), e3["serie"]["HT"], color=AZUL, lw=1.8, label="J-6 constante")
    a1.plot(_horas(e3b), e3b["serie"]["HT"], color=NARANJA, lw=1.8, ls="--", label="J-6 residencial")
    a1.set_title("Agua en T-1 (m)")
    a2.step(_horas(e3), e3["P"]["J-6"], where="post", color=AZUL, lw=1.6, label="J-6 constante")
    a2.step(_horas(e3b), e3b["P"]["J-6"], where="post", color=NARANJA, lw=1.6, ls="--", label="J-6 residencial")
    a2.set_title("Presión en J-6 (m)")
    for a in (a1, a2):
        a.set_xlim(0, 24)
        a.set_xticks(range(0, 25, 4))
        a.set_xlabel("Hora")
        a.grid(alpha=.3)
    a1.legend(loc="lower right")
    fig.tight_layout()
    return _save(fig, "fig11_sensibilidad_J6.png")


# ------------------------------------------------------------------ Figura 12: control de la bomba
def fig_control(R):
    e3, ec = R["E3"], R["rec"]["R3"]["eps"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    a1.plot(_horas(e3), e3["serie"]["HT"], color=AZUL, lw=1.8, label="Sin control (Esc. 3)")
    a1.plot(_horas(ec), ec["serie"]["HT"], color=VERDE, lw=1.8, ls="--", label="Con control de nivel")
    a1.set_title("Agua en T-1 (m)")
    a2.step(_horas(e3), e3["serie"]["Qb"], where="post", color=AZUL, lw=1.6, label="Sin control (Esc. 3)")
    a2.step(_horas(ec), ec["serie"]["Qb"], where="post", color=VERDE, lw=1.6, ls="--", label="Con control de nivel")
    a2.set_title("Caudal de la bomba (L/s)")
    for a in (a1, a2):
        a.set_xlim(0, 24)
        a.set_xticks(range(0, 25, 4))
        a.set_xlabel("Hora")
        a.grid(alpha=.3)
    fig.tight_layout()
    hs, ls_ = a2.get_legend_handles_labels()
    fig.legend(hs, ls_, loc="upper center", bbox_to_anchor=(.5, .0), ncol=2, frameon=False)
    return _save(fig, "fig12_control_bomba.png")


def todas(R):
    return {
        "red": fig_red_datos(),
        "patrones": fig_patrones(),
        "e1": fig_red_resultados(R["E1"], R["run"]["E1"], "fig03_escenario1_red.png", None),
        "e2": fig_red_resultados(R["E2"], R["run"]["E2"], "fig04_escenario2_red.png", None),
        "caudales": fig_eps_caudales(R["E3"]),
        "bomba": fig_bomba(R),
        "tanque": fig_eps_tanque(R["E3"]),
        "presiones": fig_eps_presiones(R["E3"]),
        "prv": fig_eps_prv(R["E3"]),
        "comparacion": fig_comparacion(R),
        "sensibilidad": fig_sensibilidad(R),
        "control": fig_control(R),
    }


if __name__ == "__main__":
    R = C.calcular(salidas=False)
    for k, v in todas(R).items():
        print(k, v)
