import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from models import MODELOS

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "modelos"), exist_ok=True)
os.makedirs(os.path.join(OUT, "figuras"), exist_ok=True)
for fname, fn in MODELOS.items():
    m = fn()
    with open(os.path.join(OUT, "modelos", fname), "w", encoding="utf-8") as f:
        f.write(m.to_mdl())
    for v in m.views:
        png = os.path.join(OUT, "figuras", f"diagrama_{fname[:-4]}_{v.name.replace(' ', '_')}.png")
        m.render(v.name, png)
    print("ok", fname, [v.name for v in m.views])
