"""Generador minimo de modelos Vensim (.mdl) + renderizado del diagrama en PNG.

Una sola definicion (variables con ecuaciones y coordenadas) produce:
  * el archivo .mdl (texto) que abre Vensim PLE, con su boceto (sketch)
  * una imagen PNG del diagrama de flujos y niveles, para el informe
"""
import math
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Ellipse, Polygon


class View:
    def __init__(self, name):
        self.name = name
        self.objs = []      # elementos dibujados en orden


class Model:
    def __init__(self, initial=0, final=100, step=1, tunit="Mes", saveper=None):
        self.initial, self.final, self.step, self.tunit = initial, final, step, tunit
        self.saveper = saveper
        self.vars = {}          # nombre -> dict(ecuacion, unidades, comentario, ...)
        self.order = []
        self.views = []
        self.graphs = []        # graficos personalizados (texto :GRAPH)
        self.unit_equivs = []
        self.view("Vista 1")

    # ------------------------------------------------------------------ vistas
    def view(self, name):
        self.cur = View(name)
        self.views.append(self.cur)
        return self.cur

    def _addvar(self, name, **kw):
        if name not in self.vars:
            self.order.append(name)
        self.vars[name] = kw

    # --------------------------------------------------------------- elementos
    def stock(self, name, init, units="", x=0, y=0, comment="", rng=None, w=50, h=24,
              supplementary=False):
        self._addvar(name, kind="stock", init=init, units=units, comment=comment, rng=rng,
                     inflows=[], outflows=[], supplementary=supplementary)
        self.cur.objs.append(dict(t="stock", name=name, x=x, y=y, w=w, h=h))

    def cloud(self, key, x, y):
        self.cur.objs.append(dict(t="cloud", name=key, x=x, y=y, w=12, h=9))

    def flow(self, name, eq, units="", src=None, dst=None, valve=(0, 0), vertical=False,
             src_corner=None, dst_corner=None, comment="", label_off=None, w=40, h=14,
             both_heads=False, supplementary=False):
        """src/dst: nombre de nivel o clave de nube (las nubes se crean con cloud())."""
        self._addvar(name, kind="flow", eq=eq, units=units, comment=comment, rng=None,
                     supplementary=supplementary)
        for s in (src, dst):
            pass
        if src in self.vars and self.vars[src]["kind"] == "stock":
            self.vars[src]["outflows"].append(name)
        if dst in self.vars and self.vars[dst]["kind"] == "stock":
            self.vars[dst]["inflows"].append(name)
        vx, vy = valve
        if label_off is None:
            label_off = (w + 14, 0) if vertical else (0, 22)
        self.cur.objs.append(dict(t="flow", name=name, src=src, dst=dst, x=vx, y=vy,
                                  vertical=vertical, src_corner=src_corner,
                                  dst_corner=dst_corner, lx=vx + label_off[0],
                                  ly=vy + label_off[1], w=w, h=h, both_heads=both_heads))

    def aux(self, name, eq, units="", x=0, y=0, comment="", rng=None, w=45, h=16,
            supplementary=False):
        self._addvar(name, kind="aux", eq=eq, units=units, comment=comment, rng=rng,
                     supplementary=supplementary)
        self.cur.objs.append(dict(t="aux", name=name, x=x, y=y, w=w, h=h))

    def shadow(self, name, x, y, w=45, h=16):
        self.cur.objs.append(dict(t="shadow", name=name, x=x, y=y, w=w, h=h))

    def arrow(self, frm, to, via=None, init_link=False):
        """via: punto (x, y) por donde pasa la flecha curva; None = recta."""
        self.cur.objs.append(dict(t="arrow", frm=frm, to=to, via=via, init_link=init_link))

    def loop(self, letter, x, y, clockwise=True, r=18):
        self.cur.objs.append(dict(t="loop", name=letter, x=x, y=y, cw=clockwise, r=r))

    def comment(self, text, x, y, w=120, h=20, size=10):
        self.cur.objs.append(dict(t="comment", name=text, x=x, y=y, w=w, h=h, size=size))

    def slider(self, var, lo, hi, inc, x, y, w=110, h=18):
        self.cur.objs.append(dict(t="slider", name=var, lo=lo, hi=hi, inc=inc, x=x, y=y, w=w, h=h))

    def graph_obj(self, graph_name, x, y, w=220, h=150):
        self.cur.objs.append(dict(t="graphobj", name=graph_name, x=x, y=y, w=w, h=h))

    def custom_graph(self, name, title, series, xaxis=None, xmin=None, xmax=None, xdiv=None,
                     scale_groups=None):
        """series: lista de (variable, dataset o None, ancho de linea o None).
        scale_groups: lista de indices donde arranca un grupo con escala comun."""
        self.graphs.append(dict(name=name, title=title, series=series, xaxis=xaxis,
                                xmin=xmin, xmax=xmax, xdiv=xdiv, scale_groups=scale_groups))

    # ------------------------------------------------------------ escritura mdl
    def _eq_text(self, name):
        v = self.vars[name]
        if v["kind"] == "stock":
            net = "".join(["+" + f for f in v["inflows"]] + ["-" + f for f in v["outflows"]])
            if net.startswith("+"):
                net = net[1:]
            if not net:
                net = "0"
            return f"{name}= INTEG (\n\t{net},\n\t\t{v['init']})"
        return f"{name}=\n\t{v['eq']}"

    def to_mdl(self):
        out = ["{UTF-8}"]
        for name in self.order:
            v = self.vars[name]
            units = v["units"]
            if v.get("rng"):
                units = (units + " " if units else "") + "[%s,%s]" % v["rng"]
            comment = v.get("comment", "")
            supp = "\t\t:SUPPLEMENTARY " if v.get("supplementary") else ""
            out.append(self._eq_text(name))
            out.append(f"\t~\t{units}")
            out.append(f"\t~\t{comment}{supp}")
            out.append("\t|\n")
        sp = "TIME STEP" if self.saveper is None else str(self.saveper)
        out.append("""********************************************************
\t.Control
********************************************************~
\t\tParametros de control de la simulacion
\t|
""")
        out.append(f"FINAL TIME  = {self.final}\n\t~\t{self.tunit}\n\t~\tEl tiempo final de la simulacion.\n\t|\n")
        out.append(f"INITIAL TIME  = {self.initial}\n\t~\t{self.tunit}\n\t~\tEl tiempo inicial de la simulacion.\n\t|\n")
        out.append(f"SAVEPER  = \n        {sp}\n\t~\t{self.tunit} [0,?]\n\t~\tFrecuencia con la que se guarda la salida.\n\t|\n")
        out.append(f"TIME STEP  = {self.step}\n\t~\t{self.tunit} [0,?]\n\t~\tPaso de tiempo de la simulacion.\n\t|\n")
        out.append("\\\\\\---/// Sketch information - do not modify anything except names")
        out.append("V300  Do not put anything below this section - it will be ignored")
        for view in self.views:
            out.extend(self._sketch(view))
        out.append("///---\\\\\\")
        for g in self.graphs:
            out.append(f":GRAPH {g['name']}")
            out.append(f":TITLE {g['title']}")
            if g["xaxis"]:
                out.append(f":X-AXIS {g['xaxis']}")
                if g["xmin"] is not None:
                    out.append(f":X-MIN {g['xmin']}")
                if g["xmax"] is not None:
                    out.append(f":X-MAX {g['xmax']}")
                if g["xdiv"] is not None:
                    out.append(f":X-DIV {g['xdiv']}")
            groups = g["scale_groups"] or [0]
            for i, (var, ds, lw) in enumerate(g["series"]):
                if i in groups:
                    out.append(":SCALE")
                out.append(f":VAR {var}")
                out.append(f":DATASET {ds or ''}")
                if lw:
                    out.append(f":LINE-WIDTH {lw}")
        out.append(":L<%^E!@")
        out.append("4:Time")
        for eq in self.unit_equivs:
            out.append(f"22:{eq}")
        out.append("")
        return "\n".join(out)

    def _sketch(self, view):
        lines = [f"*{view.name}",
                 "$192-192-192,0,Arial|12||0-0-0|0-0-0|0-0-255|-1--1--1|-1--1--1|96,96,100,0"]
        ids = {}
        n = [0]
        tail = ",0,0,0,0,0,0"

        def nid():
            n[0] += 1
            return n[0]

        # 1) nodos (niveles, nubes, auxiliares, sombras, comentarios)
        for o in view.objs:
            t = o["t"]
            if t == "stock":
                i = nid(); ids[o["name"]] = i
                lines.append(f"10,{i},{o['name']},{o['x']},{o['y']},{o['w']},{o['h']},3,3,0,0,-1,0,0,0{tail}")
            elif t == "cloud":
                i = nid(); ids[o["name"]] = i
                lines.append(f"12,{i},48,{o['x']},{o['y']},10,8,0,3,0,0,-1,0,0,0{tail}")
            elif t == "aux":
                i = nid(); ids[o["name"]] = i
                lines.append(f"10,{i},{o['name']},{o['x']},{o['y']},{o['w']},{o['h']},8,3,0,0,-1,0,0,0{tail}")
            elif t == "shadow":
                i = nid(); ids["<" + o["name"] + ">"] = i
                lines.append(f"10,{i},{o['name']},{o['x']},{o['y']},{o['w']},{o['h']},8,2,0,3,-1,0,0,0,128-128-128,0-0-0,|12||128-128-128{tail}")
        # 2) flujos: valvula + variable de flujo + tuberias
        for o in view.objs:
            if o["t"] != "flow":
                continue
            vi = nid()
            if o["vertical"]:
                lines.append(f"11,{vi},0,{o['x']},{o['y']},8,6,33,3,0,0,4,0,0,0{tail}")
            else:
                lines.append(f"11,{vi},0,{o['x']},{o['y']},6,8,34,3,0,0,1,0,0,0{tail}")
            fi = nid(); ids[o["name"]] = fi
            lines.append(f"10,{fi},{o['name']},{o['lx']},{o['ly']},{o['w']},{o['h']},40,3,0,0,-1,0,0,0{tail}")
            for end, corner, head in ((o["src"], o["src_corner"], 4 if o["both_heads"] else 100),
                                      (o["dst"], o["dst_corner"], 4)):
                pi = nid()
                if corner is None:
                    ex, ey = self._obj(view, end)["x"], self._obj(view, end)["y"]
                    corner = ((o["x"] + ex) // 2, (o["y"] + ey) // 2)
                lines.append(f"1,{pi},{vi},{ids[end]},{head},0,0,22,0,192,0,-1--1--1,,1|({corner[0]},{corner[1]})|")
        def rid(name):
            if name in ids:
                return ids[name]
            return ids["<" + name + ">"]

        # 3) flechas causales, lazos, comentarios, controles
        for o in view.objs:
            t = o["t"]
            if t == "arrow":
                i = nid()
                if o["via"] is None:
                    lines.append(f"1,{i},{rid(o['frm'])},{rid(o['to'])},0,0,0,0,0,192,{1 if o['init_link'] else 0},-1--1--1,,1|(0,0)|")
                else:
                    lines.append(f"1,{i},{rid(o['frm'])},{rid(o['to'])},1,0,0,0,0,192,{1 if o['init_link'] else 0},-1--1--1,,1|({o['via'][0]},{o['via'][1]})|")
            elif t == "loop":
                i = nid()
                shape = 4 if o["cw"] else 5
                lines.append(f"12,{i},0,{o['x']},{o['y']},{o['r']},{o['r']},{shape},7,0,0,-1,0,0,0{tail}")
                lines.append(o["name"])
            elif t == "comment":
                i = nid()
                lines.append(f"12,{i},0,{o['x']},{o['y']},{o['w']},{o['h']},8,7,0,0,-1,0,0,0{tail}")
                lines.append(o["name"])
            elif t == "slider":
                i = nid()
                lines.append(f"12,{i},0,{o['x']},{o['y']},{o['w']},{o['h']},3,188,0,0,0,0,0,0")
                lines.append(f"{o['name']},{o['lo']},{o['hi']},{o['inc']}")
            elif t == "graphobj":
                i = nid()
                lines.append(f"12,{i},0,{o['x']},{o['y']},{o['w']},{o['h']},0,15,0,0,1,0,0,0{tail}")
                lines.append(o["name"])
        return lines

    def _obj(self, view, name):
        for o in view.objs:
            if o.get("name") == name and o["t"] in ("stock", "cloud", "aux", "flow"):
                return o
        raise KeyError(name)

    # ------------------------------------------------------------ dibujo PNG
    def render(self, view_name, path, crop=None, scale=1.0):
        view = [v for v in self.views if v.name == view_name][0]
        xs, ys = [], []
        for o in view.objs:
            if "x" in o:
                xs += [o["x"] - o.get("w", 20) - 10, o["x"] + o.get("w", 20) + 10]
                ys += [o["y"] - o.get("h", 20) - 10, o["y"] + o.get("h", 20) + 10]
            if o["t"] == "flow":
                ys.append(o["ly"] + 20); xs.append(o["lx"] + o["w"] + 10)
            if o["t"] == "arrow" and o["via"] is not None:
                xs += [o["via"][0] - 15, o["via"][0] + 15]; ys += [o["via"][1] - 15, o["via"][1] + 15]
        x0, x1, y0, y1 = (min(xs), max(xs), min(ys), max(ys)) if crop is None else crop
        W, H = (x1 - x0), (y1 - y0)
        fig = plt.figure(figsize=(W / 100 * scale, H / 100 * scale), dpi=150)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis("off")
        fs = 8.5 * scale

        def wrap(name, w):
            return "\n".join(textwrap.wrap(name, max(8, int(2 * w / 6.2))))

        def box(o):
            if o["t"] == "flow":
                return (o["lx"], o["ly"], o["w"], 10)
            if o["t"] in ("aux", "shadow"):
                nlines = wrap(o["name"], o["w"]).count("\n") + 1
                return (o["x"], o["y"], min(o["w"], len(o["name"]) * 3.3 + 4), 7 * nlines)
            return (o["x"], o["y"], o["w"], o["h"])

        objs = {}
        for o in view.objs:
            if o["t"] == "shadow":
                objs["<" + o["name"] + ">"] = o
        for o in view.objs:
            if o["t"] in ("stock", "cloud", "aux", "flow"):
                objs[o["name"]] = o

        def get(name):
            return objs[name] if name in objs else objs["<" + name + ">"]

        def inside(p, b, pad=3):
            return abs(p[0] - b[0]) <= b[2] + pad and abs(p[1] - b[1]) <= b[3] + pad

        # tuberias
        for o in view.objs:
            if o["t"] != "flow":
                continue
            for end, corner, head in ((o["src"], o["src_corner"], o["both_heads"]),
                                      (o["dst"], o["dst_corner"], True)):
                e = objs[end]
                pts = [(o["x"], o["y"])]
                if corner is not None:
                    pts.append(corner)
                last = pts[-1]
                vertical_end = (last[0] == e["x"]) if corner is not None else o["vertical"]
                if vertical_end:
                    ex = e["x"]
                    ey = e["y"] - e["h"] if e["y"] > last[1] else e["y"] + e["h"]
                else:
                    ey = last[1]
                    ex = e["x"] - e["w"] if e["x"] > last[0] else e["x"] + e["w"]
                pts.append((ex, ey))
                X = [p[0] for p in pts]; Y = [p[1] for p in pts]
                ax.plot(X, Y, color="black", lw=4.2 * scale, solid_capstyle="butt", solid_joinstyle="miter", zorder=2)
                ax.plot(X, Y, color="white", lw=2.0 * scale, solid_capstyle="butt", solid_joinstyle="miter", zorder=3)
                if head:
                    dx, dy = X[-1] - X[-2], Y[-1] - Y[-2]
                    L = math.hypot(dx, dy) or 1
                    ux, uy = dx / L, dy / L
                    tip = (X[-1], Y[-1]); base = (X[-1] - 11 * ux, Y[-1] - 11 * uy)
                    tri = [tip, (base[0] - 6 * uy, base[1] + 6 * ux), (base[0] + 6 * uy, base[1] - 6 * ux)]
                    ax.add_patch(Polygon(tri, closed=True, color="black", zorder=4))
            # valvula (reloj de arena)
            vx, vy = o["x"], o["y"]
            if o["vertical"]:
                tri = [(vx - 7, vy - 6), (vx + 7, vy - 6), (vx - 7, vy + 6), (vx + 7, vy + 6)]
                ax.add_patch(Polygon([(vx - 7, vy - 7), (vx - 7, vy + 7), (vx + 7, vy - 7), (vx + 7, vy + 7)], closed=True, fc="white", ec="black", lw=1, zorder=5))
            else:
                ax.add_patch(Polygon([(vx - 7, vy - 8), (vx + 7, vy - 8), (vx - 7, vy + 8), (vx + 7, vy + 8)], closed=True, fc="white", ec="black", lw=1, zorder=5))
            ax.text(o["lx"], o["ly"], wrap(o["name"], o["w"]), ha="center", va="center", fontsize=fs, zorder=6)
        # nodos
        for o in view.objs:
            t = o["t"]
            if t == "stock":
                ax.add_patch(Rectangle((o["x"] - o["w"], o["y"] - o["h"]), 2 * o["w"], 2 * o["h"], fc="white", ec="black", lw=1.2, zorder=6))
                ax.text(o["x"], o["y"], wrap(o["name"], o["w"]), ha="center", va="center", fontsize=fs, zorder=7)
            elif t == "cloud":
                for dx, dy, r in ((-5, 0, 6), (3, -3, 6), (5, 3, 5), (-1, 4, 5)):
                    ax.add_patch(Circle((o["x"] + dx, o["y"] + dy), r, fc="white", ec="black", lw=1, zorder=6))
                for dx, dy, r in ((-5, 0, 5), (3, -3, 5), (5, 3, 4), (-1, 4, 4)):
                    ax.add_patch(Circle((o["x"] + dx, o["y"] + dy), r, fc="white", ec="none", zorder=7))
            elif t == "aux":
                ax.text(o["x"], o["y"], wrap(o["name"], o["w"]), ha="center", va="center", fontsize=fs, zorder=7)
            elif t == "shadow":
                ax.text(o["x"], o["y"], "<" + o["name"] + ">", ha="center", va="center", fontsize=fs, color="#666666", zorder=7)
            elif t == "loop":
                ax.add_patch(Circle((o["x"], o["y"]), o["r"] * 0.8, fc="none", ec="#444444", lw=1, ls="-", zorder=3))
                ax.text(o["x"], o["y"], o["name"], ha="center", va="center", fontsize=fs * 1.2, weight="bold", color="#444444")
            elif t == "comment":
                ax.text(o["x"], o["y"], o["name"], ha="center", va="center", fontsize=o["size"] * scale, style="italic", color="#333355")
            elif t == "slider":
                ax.add_patch(Rectangle((o["x"] - o["w"], o["y"] - o["h"]), 2 * o["w"], 2 * o["h"], fc="#eeeeee", ec="#888888", lw=1, zorder=5))
                ax.plot([o["x"] - o["w"] + 8, o["x"] + o["w"] - 8], [o["y"], o["y"]], color="#555555", lw=2, zorder=6)
                ax.add_patch(Rectangle((o["x"] - 6, o["y"] - 8), 12, 16, fc="#3366aa", ec="black", zorder=7))
                ax.text(o["x"] - o["w"], o["y"] - o["h"] - 6, o["name"], fontsize=fs * 0.9, va="bottom")
            elif t == "graphobj":
                ax.add_patch(Rectangle((o["x"] - o["w"], o["y"] - o["h"]), 2 * o["w"], 2 * o["h"], fc="#f7f7ff", ec="#666699", lw=1, zorder=5))
                ax.text(o["x"], o["y"], "Grafico: " + o["name"], ha="center", va="center", fontsize=fs, color="#333366")
        # flechas causales
        for o in view.objs:
            if o["t"] != "arrow":
                continue
            a, b = get(o["frm"]), get(o["to"])
            ba, bb = box(a), box(b)
            p0 = (ba[0], ba[1]); p2 = (bb[0], bb[1])
            if o["via"] is None:
                pm = ((p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2)
            else:
                pm = o["via"]
            # control de bezier cuadratica que pasa por pm en t=0.5
            c = (2 * pm[0] - (p0[0] + p2[0]) / 2, 2 * pm[1] - (p0[1] + p2[1]) / 2)
            pts = []
            for k in range(201):
                tt = k / 200
                x = (1 - tt) ** 2 * p0[0] + 2 * (1 - tt) * tt * c[0] + tt ** 2 * p2[0]
                y = (1 - tt) ** 2 * p0[1] + 2 * (1 - tt) * tt * c[1] + tt ** 2 * p2[1]
                pts.append((x, y))
            pts = [p for p in pts if not inside(p, ba) and not inside(p, bb)]
            if len(pts) < 2:
                continue
            X = [p[0] for p in pts]; Y = [p[1] for p in pts]
            color = "#8b0000" if o["init_link"] else "#1f3f8f"
            ax.plot(X[:-1], Y[:-1], color=color, lw=0.9, zorder=8)
            ax.add_patch(FancyArrowPatch(pts[-6] if len(pts) > 6 else pts[0], pts[-1], arrowstyle="-|>", mutation_scale=9, color=color, lw=0.9, zorder=8))
        fig.savefig(path, dpi=150)
        plt.close(fig)
