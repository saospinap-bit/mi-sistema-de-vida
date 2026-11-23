"""Simula todos los modelos con PySD (integracion de Euler, igual que Vensim)
y genera las graficas y las cifras clave que se usan en el informe."""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import pysd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1]
CLASE = sys.argv[2]           # ruta al Epidemia8 (1).mdl del curso
MOD = os.path.join(OUT, "modelos")
FIG = os.path.join(OUT, "figuras")
plt.rcParams.update({"figure.dpi": 130, "font.size": 9, "axes.grid": True, "grid.alpha": .35,
                     "axes.spines.top": False, "axes.spines.right": False})
K = {}


def run(fname, params=None, ret=None):
    m = pysd.read_vensim(os.path.join(MOD, fname))
    return m.run(params=params or {}, return_columns=ret)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, name))
    plt.close(fig)


def peak(s):
    return float(s.idxmax()), float(s.max())

# ---------------------------------------------------------------- Capitulo 9
cols = ["Clientes Potenciales", "Clientes", "nuevos clientes", "demanda boca a boca",
        "mercado total"]
c1 = run("Cap09_difusion1_clientes.mdl")
c2 = run("Cap09_difusion2_capacidad.mdl")
c3 = run("Cap09-10_difusion3_capacidad_detallada.mdl")
c4 = run("Cap09-10_difusion3_capacidad_detallada.mdl", {"tiempo para ajustar la capacidad": 4})
runs = {"clientes1": c1, "clientes2": c2, "clientes3": c3, "clientes4": c4}
colors = {"clientes1": "#1f77b4", "clientes2": "#d62728", "clientes3": "#2ca02c", "clientes4": "#9467bd"}
for k, r in runs.items():
    t, v = peak(r["nuevos clientes"])
    K[k] = dict(pico_t=t, pico_nuevos=v,
                clientes_t100=float(r["Clientes"].iloc[-1]),
                cp_t100=float(r["Clientes Potenciales"].iloc[-1]),
                t_50=float(r.index[(r["Clientes"] >= 0.5 * 1.001e6).values.argmax()]),
                t_90=float(r.index[(r["Clientes"] >= 0.9 * 1.001e6).values.argmax()]))
    if "Ingresos Acumulados" in r:
        K[k]["ingresos_t100"] = float(r["Ingresos Acumulados"].iloc[-1])
    if "Capacidad" in r:
        K[k]["cap_max"] = float(r["Capacidad"].max())
        K[k]["cap_max_t"] = float(r["Capacidad"].idxmax())
K["clientes1"]["nuevos_t0"] = float(c1["nuevos clientes"].iloc[0])

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(c1.index, c1["Clientes Potenciales"] / 1e6, label="Clientes Potenciales")
ax[0].plot(c1.index, c1["Clientes"] / 1e6, label="Clientes")
ax[0].set(title="Niveles (corrida clientes1)", xlabel="Tiempo (Mes)", ylabel="millones de personas")
ax[0].legend()
ax[1].plot(c1.index, c1["nuevos clientes"] / 1e3, color="#d62728")
ax[1].set(title="nuevos clientes (clientes1)", xlabel="Tiempo (Mes)", ylabel="miles de personas/Mes")
save(fig, "c09_clientes1.png")

fig, ax = plt.subplots(figsize=(6.5, 3.2))
for k in ["clientes1", "clientes2"]:
    ax.plot(runs[k].index, runs[k]["nuevos clientes"] / 1e3, label=k, color=colors[k], lw=1.6)
ax.set(title="nuevos clientes: sin y con restricción de capacidad", xlabel="Tiempo (Mes)",
       ylabel="miles de personas/Mes"); ax.legend()
save(fig, "c09_nuevos_clientes_1vs2.png")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(c2.index, c2["demanda boca a boca"] / 1e3, label="demanda boca a boca", ls="--")
ax[0].plot(c2.index, c2["Capacidad"] / 1e3, label="Capacidad")
ax[0].plot(c2.index, c2["nuevos clientes"] / 1e3, label="nuevos clientes", lw=2)
ax[0].set(title="clientes2: la capacidad limita las ventas", xlabel="Tiempo (Mes)",
          ylabel="miles por Mes"); ax[0].legend(fontsize=7.5)
ax[1].plot(c2.index, c2["Ingresos Acumulados"] / 1e6, color="#2ca02c")
ax[1].set(title="Ingresos Acumulados (clientes2)", xlabel="Tiempo (Mes)", ylabel="millones de dólares")
save(fig, "c09_clientes2_capacidad.png")

fig, ax = plt.subplots(figsize=(6.5, 3.2))
for k in runs:
    ax.plot(runs[k].index, runs[k]["nuevos clientes"] / 1e3, label=k, color=colors[k], lw=1.6)
ax.set(title="nuevos clientes en las cuatro corridas", xlabel="Tiempo (Mes)",
       ylabel="miles de personas/Mes"); ax.legend()
save(fig, "c09_nuevos_clientes_4corridas.png")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
for k in ["clientes2", "clientes3", "clientes4"]:
    ax[0].plot(runs[k].index, runs[k]["Capacidad"] / 1e3, label=k, color=colors[k])
ax[0].set(title="Capacidad", xlabel="Tiempo (Mes)", ylabel="miles de unidades/Mes"); ax[0].legend()
for k in ["clientes3", "clientes4"]:
    ax[1].plot(runs[k].index, runs[k]["demanda boca a boca"] / 1e3, ls="--", color=colors[k], label=f"demanda boca a boca ({k})")
    ax[1].plot(runs[k].index, runs[k]["producción"] / 1e3, color=colors[k], label=f"producción ({k})")
ax[1].set(title="Demanda vs. producción (modelo detallado)", xlabel="Tiempo (Mes)", ylabel="miles por Mes")
ax[1].legend(fontsize=7)
save(fig, "c09_capacidad_detallada.png")

fig, ax = plt.subplots(figsize=(6.5, 3.2))
for k in runs:
    ax.plot(runs[k].index, runs[k]["Clientes"] / 1e6, label=k, color=colors[k])
ax.set(title="Clientes en las cuatro corridas", xlabel="Tiempo (Mes)", ylabel="millones de personas")
ax.legend()
save(fig, "c09_clientes_4corridas.png")

# ---------------------------------------------------------------- Capitulo 10
def base_graph(ax, style):
    marks = {"clientes1": "1", "clientes2": "2", "clientes3": "3", "clientes4": "4"}
    for i, k in enumerate(runs):
        y = runs[k]["nuevos clientes"] / 1e3
        x = runs[k].index
        if style == "fina":
            ax.plot(x, y, color=colors[k], lw=0.8, label=k)
        elif style == "gruesa":
            ax.plot(x, y, color=colors[k], lw=2.6, label=k)
        elif style == "patron":
            ax.plot(x, y, color=colors[k], lw=1.2, ls=["-", "--", "-.", ":"][i], label=k)
        elif style == "puntos":
            ax.plot(x, y, color=colors[k], ls="none", marker=".", ms=3, label=k)
        elif style == "marcas":
            ax.plot(x, y, color=colors[k], lw=1, label=k)
            for xx in x[5 + 3 * i::12]:
                ax.text(xx, y.loc[xx], marks[k], color=colors[k], fontsize=8, ha="center", va="center",
                        bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))
    ax.set(xlabel="Tiempo (Mes)", ylabel="miles de personas/Mes")

fig, axs = plt.subplots(2, 3, figsize=(10, 5.6))
titles = {"fina": "1) Líneas finas de color (por defecto)", "gruesa": "2) Líneas gruesas (Thick Lines)",
          "patron": "3) Líneas con patrón (Patterned)", "puntos": "4) Solo puntos (Dots Only)",
          "marcas": "5) Marcadores de línea (Line Markers)"}
for ax, st in zip(axs.flat, titles):
    base_graph(ax, st); ax.set_title(titles[st], fontsize=9)
axs[0, 0].legend(fontsize=7)
axs.flat[-1].axis("off")
axs.flat[-1].text(0.02, 0.5, "Todas las gráficas muestran\n'nuevos clientes' para las corridas\n"
                  "clientes1 a clientes4.\nSolo cambia la presentación;\nlos datos son los mismos.",
                  fontsize=9, va="center")
save(fig, "c10_opciones_graficas.png")

fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(c2.index, c2["Clientes"] / 1e6, color="#1f77b4", lw=2.2, label="Clientes : clientes2")
ax.plot(c4.index, c4["Clientes"] / 1e6, color="#d62728", lw=2.2, label="Clientes : clientes4")
ax.set_ylabel("Clientes (millones de personas)")
ax2 = ax.twinx()
ax2.plot(c2.index, c2["Capacidad"] / 1e3, color="#2ca02c", lw=1, label="Capacidad : clientes2")
ax2.plot(c4.index, c4["Capacidad"] / 1e3, color="#9467bd", lw=1, label="Capacidad : clientes4")
ax2.set_ylabel("Capacidad (miles de unidades/Mes)"); ax2.grid(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="center right")
ax.set(title="Gráfico personalizado 'Difusión de clientes'", xlabel="Tiempo (Mes)")
save(fig, "c10_grafico_personalizado.png")

# ---------------------------------------------------------------- Capitulo 12
w = {}
w["base"] = run("Cap12_boca_a_boca_2_controles.mdl")
for gasto in [0, 1e8, 2e8]:
    w[f"pub_{gasto:.0e}"] = run("Cap12_boca_a_boca_2_controles.mdl", {"c gasto en publicidad": gasto})
for vida in [0.5, 10]:
    w[f"vida_{vida}"] = run("Cap12_boca_a_boca_2_controles.mdl", {"tiempo de obsolescencia": vida})
for k, r in w.items():
    t, v = peak(r["ventas"])
    K["wom_" + k] = dict(pico_t=t, pico_ventas=v, clientes_t5=float(r["Clientes"].iloc[-1]),
                          ventas_t5=float(r["ventas"].iloc[-1]), ventas_t0=float(r["ventas"].iloc[0]))
# juego: el jugador cambia el gasto en publicidad cada 0.5 anos (GAME INTERVAL)
t_game = np.arange(0, 5.0001, 0.0625)
plan = {0: 1e8, 0.5: 1e8, 1.0: 5e7, 1.5: 0, 2.0: 0, 2.5: 0, 3.0: 2e7, 3.5: 2e7, 4.0: 2e7, 4.5: 2e7}
serie = pd.Series([plan[max(k for k in plan if k <= tt + 1e-9)] for tt in t_game], index=t_game)
w["juego"] = run("Cap12_boca_a_boca_2_controles.mdl", {"gasto en publicidad": serie})
t, v = peak(w["juego"]["ventas"])
K["wom_juego"] = dict(pico_t=t, pico_ventas=v, clientes_t5=float(w["juego"]["Clientes"].iloc[-1]))

r = w["base"]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(r.index, r["Clientes Potenciales"] / 1e6, label="Clientes Potenciales")
ax[0].plot(r.index, r["Clientes"] / 1e6, label="Clientes")
ax[0].set(title="Niveles (corrida base)", xlabel="Tiempo (Año)", ylabel="millones de personas"); ax[0].legend()
ax[1].plot(r.index, r["ventas"] / 1e6, color="#d62728", label="ventas")
ax[1].plot(r.index, r["clientes que abandonan"] / 1e6, color="#7f7f7f", ls="--", label="clientes que abandonan")
ax[1].set(title="ventas (salida del control gráfico)", xlabel="Tiempo (Año)", ylabel="millones / Año"); ax[1].legend()
save(fig, "c12_base.png")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
for k, lab in [("pub_0e+00", "gasto = 0"), ("base", "gasto = 20 M$/año (base)"),
               ("pub_1e+08", "gasto = 100 M$/año"), ("pub_2e+08", "gasto = 200 M$/año")]:
    ax[0].plot(w[k].index, w[k]["ventas"] / 1e6, label=lab)
ax[0].set(title="Deslizador: gasto en publicidad", xlabel="Tiempo (Año)", ylabel="ventas (millones/Año)")
ax[0].legend(fontsize=7.5)
for k, lab in [("vida_0.5", "vida = 0.5 años"), ("base", "vida = 2 años (base)"), ("vida_10", "vida = 10 años")]:
    ax[1].plot(w[k].index, w[k]["ventas"] / 1e6, label=lab)
ax[1].set(title="Deslizador: vida del producto", xlabel="Tiempo (Año)", ylabel="ventas (millones/Año)")
ax[1].legend(fontsize=7.5)
save(fig, "c12_deslizadores.png")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].step(serie.index, serie / 1e6, where="post", color="#9467bd")
ax[0].set(title="Decisiones del jugador (cada 0.5 años)", xlabel="Tiempo (Año)", ylabel="gasto en publicidad (M$/Año)")
ax[1].plot(w["base"].index, w["base"]["ventas"] / 1e6, label="simulación base", color="#1f77b4")
ax[1].plot(w["juego"].index, w["juego"]["ventas"] / 1e6, label="juego", color="#9467bd")
ax[1].set(title="ventas: juego vs. simulación", xlabel="Tiempo (Año)", ylabel="millones/Año"); ax[1].legend()
save(fig, "c12_juego.png")

# ---------------------------------------------------------------- Libro JMG 2.1
e = run("JMG_2.1_desarrollo_epidemia.mdl")
K["jmg"] = dict(
    I_pico_t=peak(e["Infectados"])[0], I_pico=peak(e["Infectados"])[1],
    S_min_t=float(e["Susceptibles"].idxmin()), S_min=float(e["Susceptibles"].min()),
    S_t20=float(e["Susceptibles"].iloc[-1]), I_t20=float(e["Infectados"].iloc[-1]),
    R_t20=float(e["Recuperados"].iloc[-1]), P_t20=float(e["Total poblacion"].iloc[-1]),
    enferman_t0=float(e["enferman"].iloc[0]), enferman_pico=peak(e["enferman"])[1],
    enferman_pico_t=peak(e["enferman"])[0], muertes_pico=peak(e["muertes"])[1],
    muertes_pico_t=peak(e["muertes"])[0], muertes_total=float(1000 - e["Total poblacion"].iloc[-1]),
    R_max=float(e["Recuperados"].max()), R_max_t=float(e["Recuperados"].idxmax()),
)
I = e["Infectados"]
above = [float(t) for t in I.index[(I > 150) & (I.shift(1) <= 150)]]
inn = [float(t) for t in I.index[(I <= 150) & (I.shift(1) > 150)]]
below = [float(t) for t in I.index[(I < 50) & (I.shift(1) >= 50)]]
K["jmg"]["warnings"] = dict(above=above, back_in=inn, below=below)
K["jmg"]["tabla"] = {c: [round(float(x), 1) for x in e[c].values] for c in
                     ["Susceptibles", "Infectados", "Recuperados", "enferman", "vacunados", "muertes", "Total poblacion"]}

fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(e.index, e["Infectados"], marker="+", color="#1f3f8f")
ax[0].axhline(150, color="gray", ls=":", lw=1); ax[0].axhline(50, color="gray", ls=":", lw=1)
ax[0].set(title="Infectados", xlabel="Tiempo (Mes)", xticks=range(0, 21, 2))
ax[1].plot(e.index, e["Susceptibles"], marker="+", color="#1f3f8f")
ax[1].set(title="Susceptibles", xlabel="Tiempo (Mes)", ylim=(0, 1000), xticks=range(0, 21, 2))
save(fig, "jmg_infectados_susceptibles.png")

fig, ax = plt.subplots(figsize=(6.5, 3.4))
for c in ["Susceptibles", "Infectados", "Recuperados", "Total poblacion"]:
    ax.plot(e.index, e[c], label=c, lw=1.6 if c != "Total poblacion" else 1, ls="-" if c != "Total poblacion" else "--")
ax.set(title="Estados del modelo SIR con vacunación", xlabel="Tiempo (Mes)", xticks=range(0, 21, 2))
ax.legend(fontsize=7.5)
save(fig, "jmg_estados.png")

fig, ax = plt.subplots(1, 2, figsize=(9, 3.3))
ax[0].plot(e["enferman"], e["muertes"], color="#1f3f8f", lw=2.5)
ax[0].set(title="Gráfico XY: muertes (Y) vs. enferman (X)", xlabel="enferman", ylabel="muertes", xlim=(0, 110), xticks=range(0, 111, 10))
ax[1].plot(e.index, e["muertes"], marker="+", label="muertes", color="#1f3f8f")
ax[1].plot(e.index, e["enferman"] / 10, marker="$2$", ms=5, label="enferman (÷10)", color="#d62728")
ax[1].set(title="muertes y enferman en el tiempo", xlabel="Tiempo (Mes)", xticks=range(0, 21, 2)); ax[1].legend(fontsize=7.5)
save(fig, "jmg_xy.png")

fig, ax = plt.subplots(figsize=(6.5, 3.2))
for c in ["enferman", "vacunados", "curan", "muertes", "expuestos"]:
    ax.plot(e.index, e[c], label=c)
ax.set(title="Flujos del modelo", xlabel="Tiempo (Mes)", ylabel="personas/Mes", xticks=range(0, 21, 2)); ax.legend(fontsize=7.5)
save(fig, "jmg_flujos.png")

# ---------------------------------------------------------------- Epidemia de clase
cl = pysd.read_vensim(CLASE).run()
inf = cl["Infectados"]
K["clase"] = dict(I_t20=float(inf.iloc[-1]), N_t20=float(cl["No infectados"].iloc[-1]),
                  inf_pico_t=peak(cl["Infecciones por mes"])[0], inf_pico=peak(cl["Infecciones por mes"])[1],
                  t_50=float(inf.index[(inf >= 33).values.argmax()]))
cl40 = pysd.read_vensim(CLASE).run(final_time=40)
K["clase"]["I_t40"] = float(cl40["Infectados"].iloc[-1])
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(cl40.index, cl40["Infectados"], label="Infectados"); ax[0].plot(cl40.index, cl40["No infectados"], label="No infectados")
ax[0].axvline(20, color="gray", ls=":", lw=1); ax[0].text(20.5, 5, "FINAL TIME = 20", fontsize=7, color="gray")
ax[0].set(title="Epidemia de clase (Epidemia8.mdl), extendida a 40 meses", xlabel="Tiempo (Mes)", ylabel="persona"); ax[0].legend(fontsize=7.5)
ax[1].plot(cl40.index, cl40["Infecciones por mes"], color="#d62728")
ax[1].axvline(20, color="gray", ls=":", lw=1)
ax[1].set(title="Infecciones por mes", xlabel="Tiempo (Mes)", ylabel="persona/Mes")
save(fig, "clase_epidemia8.png")

# comparacion normalizada
fig, ax = plt.subplots(1, 2, figsize=(9, 3.3))
ax[0].plot(c1.index, c1["Clientes"] / c1["mercado total"], label="Difusión: Clientes / mercado total")
ax[0].plot(cl40.index, cl40["Infectados"] / 66, label="Epidemia de clase: Infectados / 66")
ax[0].plot(e.index, e["Infectados"] / e["Total poblacion"], label="Epidemia JMG: Infectados / población")
ax[0].set(title="Fracción de la población 'adoptante/infectada'", xlabel="Tiempo (Mes)", xlim=(0, 100)); ax[0].legend(fontsize=7)
ax[1].plot(c1.index, c1["nuevos clientes"] / c1["nuevos clientes"].max(), label="nuevos clientes (difusión)")
ax[1].plot(cl40.index, cl40["Infecciones por mes"] / cl40["Infecciones por mes"].max(), label="Infecciones por mes (clase)")
ax[1].plot(e.index, e["enferman"] / e["enferman"].max(), label="enferman (JMG)")
ax[1].set(title="Flujo de contagio/adopción normalizado (máx = 1)", xlabel="Tiempo (Mes)", xlim=(0, 100)); ax[1].legend(fontsize=7)
save(fig, "comparacion_modelos.png")

with open(os.path.join(OUT, "cifras.json"), "w") as f:
    json.dump(K, f, indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in K.items() if k != "jmg"}, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in K["jmg"].items() if k != "tabla"}, indent=1))
print(K["jmg"]["tabla"]["Infectados"])
