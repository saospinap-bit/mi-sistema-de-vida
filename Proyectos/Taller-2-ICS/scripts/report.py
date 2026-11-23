"""Genera el informe del Taller 2 (HTML para imprimir a PDF + DOCX editable)."""
import base64, html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from models import difusion1, difusion2, difusion3, boca_a_boca, epidemia_jmg

OUT = sys.argv[1]
FIG = os.path.join(OUT, "figuras")
K = json.load(open(os.path.join(OUT, "cifras.json")))
B = []          # bloques del documento
nfig = [0]
ntab = [0]


def h1(t): B.append(("h1", t))
def h2(t): B.append(("h2", t))
def h3(t): B.append(("h3", t))
def p(t): B.append(("p", t))
def ul(items): B.append(("ul", items))
def ol(items): B.append(("ol", items))
def code(t): B.append(("code", t))
def pagebreak(): B.append(("pb", None))


def fig(name, caption, width=16):
    nfig[0] += 1
    B.append(("img", (name, f"Figura {nfig[0]}. {caption}", width)))


def table(header, rows, caption=None, widths=None):
    if caption:
        ntab[0] += 1
        caption = f"Tabla {ntab[0]}. {caption}"
    B.append(("table", (header, rows, caption, widths)))


def n(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def eqs(model, only_view=None):
    """Listado de ecuaciones del modelo (como en Vensim: Model > Document)."""
    lines = []
    names = model.order
    if only_view:
        vw = [v for v in model.views if v.name == only_view][0]
        own = [o["name"] for o in vw.objs if o["t"] in ("stock", "aux", "flow")]
        names = [x for x in names if x in own]
    for nm in names:
        v = model.vars[nm]
        if v["kind"] == "stock":
            net = "".join(["+" + f for f in v["inflows"]] + ["-" + f for f in v["outflows"]]).lstrip("+")
            lines.append(f"{nm} = INTEG({net}, {v['init']})")
        else:
            lines.append(f"{nm} = {v['eq']}")
        u = v["units"] + (f"  [{v['rng'][0]},{v['rng'][1]}]" if v.get("rng") else "")
        extra = "   (suplementaria)" if v.get("supplementary") else ""
        if u or extra:
            lines.append(f"    Unidades: {u}{extra}")
    return "\n".join(lines)


c1, c2, c3, c4 = K["clientes1"], K["clientes2"], K["clientes3"], K["clientes4"]
j, cl = K["jmg"], K["clase"]
w = {k[4:]: v for k, v in K.items() if k.startswith("wom_")}

# =====================================================================  PORTADA
B.append(("cover", None))

# =====================================================================  INTRO
h1("Contenido de la entrega")
p("Este documento desarrolla los puntos 1 a 6 del Taller 2 de Ingeniería Civil Sostenible (2026-2S). "
  "Con él se entregan los modelos de Vensim (archivos .mdl) que se listan en la Tabla 1. Todos los nombres de "
  "variables, vistas, unidades y corridas se tradujeron al español.")
table(["Archivo", "Punto", "Contenido"], [
    ["Cap09_difusion1_clientes.mdl", "2", "Modelo de difusión por boca a boca (cust1 de la guía). Corrida clientes1."],
    ["Cap09_difusion2_capacidad.mdl", "2", "Difusión + vista Capacidad + vista Ingresos por Ventas (cust2). Corrida clientes2."],
    ["Cap09-10_difusion3_capacidad_detallada.mdl", "2 y 3", "Difusión con capacidad detallada (cust3, estructura cap1 pegada). "
     "Corridas clientes3 y clientes4. Incluye los gráficos personalizados del capítulo 10."],
    ["Cap12_boca_a_boca_1_estructura.mdl", "4", "Modelo de ventas por boca a boca y publicidad (wom1)."],
    ["Cap12_boca_a_boca_2_controles.mdl", "4", "El mismo modelo con vistas Inicio, Estructura, Simular y Juego, "
     "deslizadores, gráfico de salida y GAME INTERVAL (wom2 a wom4)."],
    ["JMG_2.1_desarrollo_epidemia.mdl", "6", "Caso 2.1 del libro de Juan Martín García: epidemia SIR con vacunación."],
], "Modelos entregados.", widths=[6.2, 1.3, 9])
p("Nota sobre la numeración de la guía. En la versión actual de la guía en línea de Vensim, el capítulo 9 "
  "(Multiple Views) construye el modelo de difusión de un producto, el capítulo 10 (Customizing Output) trabaja "
  "las salidas gráficas y los controles de entrada y salida están en el capítulo 12 (Input Output Controls, "
  "usr12.html). El punto 4 del enunciado cita el capítulo 10, pero por su título corresponde al capítulo 12, "
  "que es el que se desarrolló.")
p("Las simulaciones usan integración de Euler con el TIME STEP de cada modelo, que es el método por defecto de "
  "Vensim. Las cifras citadas en el texto salen de esas corridas.")

# =====================================================================  1
h1("1. Instalación de Vensim PLE")
ol(["Se ingresó a https://vensim.com/free-downloads/ y se diligenció el formulario de descarga de Vensim PLE "
    "(Personal Learning Edition, uso académico gratuito) con el correo institucional.",
    "Se recibió en el correo el enlace de descarga, se descargó el instalador para Windows y se ejecutó.",
    "Se aceptó la licencia, se escogió la carpeta de instalación y se terminó el asistente. Al abrir Vensim PLE "
    "aparecen la barra de herramientas de boceto (Box Variable, Rate, Arrow, Shadow Variable, etc.) y la barra "
    "de simulación (Runname, Simulate, Set Up a Simulation, SyntheSim)."])

# =====================================================================  2
pagebreak()
h1("2. Tutorial del modelo de difusión (capítulo 9, Multiple Views)")
h2("2.a-b. Reproducción del modelo en español")
p("El tutorial construye en tres etapas un modelo en el que los Clientes Potenciales de un producto lo compran "
  "por la recomendación (boca a boca) de quienes ya lo tienen. Luego se agrega una restricción de capacidad de "
  "producción y una vista de ingresos. La Tabla 2 muestra la traducción usada.")
table(["Guía (inglés)", "Modelo (español)", "Guía (inglés)", "Modelo (español)"], [
    ["Potential Customers", "Clientes Potenciales", "Capacity", "Capacidad"],
    ["Customers", "Clientes", "capacity adjustment", "ajuste de capacidad"],
    ["new customers", "nuevos clientes", "target capacity", "capacidad objetivo"],
    ["word of mouth demand", "demanda boca a boca", "time to adjust capacity", "tiempo para ajustar la capacidad"],
    ["contacts of noncustomers with customers", "contactos de no clientes con clientes", "widgets per person", "unidades por persona"],
    ["contacts with customers", "contactos con clientes", "investment / reductions", "inversión / reducciones"],
    ["sociability", "sociabilidad", "capacity life", "vida de la capacidad"],
    ["fruitfulness", "fructuosidad", "desired / potential production", "producción deseada / potencial"],
    ["potential customer concentration", "concentración de clientes potenciales", "production", "producción"],
    ["total market", "mercado total", "sales, price", "ventas, precio"],
    ["Widget / Gadget", "Unidad / Aparato", "sales revenue / Cumulative Revenue", "ingresos por ventas / Ingresos Acumulados"],
    ["runs cust1 … cust4", "corridas clientes1 … clientes4", "views Customer / Capacity / Sales Revenue", "vistas Clientes / Capacidad / Ingresos por Ventas"],
], "Traducción de variables, unidades, vistas y corridas.", widths=[4.1, 4.3, 4.1, 4.3])
p("Se siguieron las instrucciones marcadas con viñeta (➢) de la guía:")
ol(["Modelo nuevo con los límites de tiempo por defecto: INITIAL TIME = 0, FINAL TIME = 100, TIME STEP = 1, "
    "unidad de tiempo Mes. Se dibujaron los niveles, el flujo y las variables auxiliares, se escribieron las "
    "ecuaciones y unidades, y se verificó con Model > Check Model y Units Check.",
    "Se simuló con el nombre de corrida clientes1 y se revisaron Clientes Potenciales, Clientes y nuevos clientes "
    "con las herramientas Graph y Causes Strip.",
    "Se renombró la vista como Clientes (View > Rename) y se guardó como difusión 2.",
    "Se creó la vista Capacidad: nivel Capacidad, flujo ajuste de capacidad con punta de flecha en ambos extremos "
    "de la tubería (puede aumentar o disminuir la capacidad) y la variable sombra (Shadow Variable) "
    "demanda boca a boca, que conecta la vista con la de Clientes.",
    "En la vista Clientes se agregaron las sombras Capacidad y unidades por persona y se cambió la ecuación a "
    "nuevos clientes = MIN(demanda boca a boca, Capacidad/unidades por persona).",
    "Se creó la vista Ingresos por Ventas. Ingresos Acumulados se marcó como Supplementary porque no se usa en "
    "ninguna otra ecuación. Se simuló como clientes2 y se comparó con clientes1.",
    "Se guardó como difusión 3. En la vista Capacidad se borró la estructura anterior (excepto unidades por "
    "persona y la sombra demanda boca a boca) y se pegó la estructura del modelo cap1.mdl (inversión, "
    "reducciones, vida de la capacidad, producción). Se ajustaron producción deseada y nuevos clientes, que ahora "
    "depende de la sombra producción.",
    "El Units Check reportó dos errores por usar Unidad y Aparato. Se declararon sinónimos en Model > Settings > "
    "Units Equiv: Aparato, Aparatos, Unidad, Unidades. Se simuló como clientes3.",
    "Política de inversión: con Set Up a Simulation se cambió tiempo para ajustar la capacidad de 12 a 4 meses y "
    "se simuló como clientes4."])

h2("2.c. Documentación y descripción del modelo")
h3("Vista Clientes (difusión por boca a boca)")
fig("diagrama_Cap09_difusion1_clientes_Clientes.png", "Diagrama de niveles y flujos de la vista Clientes (difusion1).")
p("El modelo tiene dos niveles. Clientes Potenciales (1.000.000 personas al inicio) y Clientes (1.000 personas) "
  "están unidos por un único flujo, nuevos clientes. Nadie entra ni sale del sistema, así que el mercado total "
  "se mantiene en 1.001.000 personas.")
p("Cada cliente hace 20 contactos por mes (sociabilidad). De esos contactos, la fracción que ocurre con alguien que "
  "todavía no tiene el producto es la concentración de clientes potenciales (Clientes Potenciales / mercado total). "
  "El 1 % de los contactos con no clientes termina en compra (fructuosidad = 0,01). Al combinar las ecuaciones:")
code("nuevos clientes = sociabilidad · fructuosidad · Clientes · Clientes Potenciales / mercado total\n"
     "                = 0,2 · Clientes · (Clientes Potenciales / mercado total)        [persona/Mes]")
p("Esta es la ecuación logística. Tiene dos lazos de realimentación:")
ul(["R, boca a boca (refuerzo): más Clientes generan más contactos, más demanda boca a boca, más nuevos clientes y "
    "aún más Clientes. Domina al comienzo y produce crecimiento exponencial con tasa cercana a 0,2 por mes.",
    "B, saturación del mercado (balance): cada nuevo cliente reduce los Clientes Potenciales, y con ellos la "
    "concentración de clientes potenciales y la fracción de contactos útiles. Domina cuando la mitad del mercado ya "
    "compró y frena la difusión."])
eqtxt1 = eqs(difusion1())
code(eqtxt1)

h3("Vista Capacidad (difusion2)")
fig("diagrama_Cap09_difusion2_capacidad_Capacidad.png", "Vista Capacidad del modelo difusion2.", 12)
fig("diagrama_Cap09_difusion2_capacidad_Clientes.png", "Vista Clientes de difusion2: las sombras <Capacidad> y <unidades por persona> limitan nuevos clientes.")
p("La Capacidad de la fábrica (unidades/Mes) busca la capacidad objetivo, que es la demanda boca a boca por las "
  "unidades por persona. El ajuste cierra en cada mes 1/12 de la brecha (tiempo para ajustar la capacidad = 12 "
  "meses). Es un lazo de balance de primer orden, así que la capacidad sigue a la demanda con un retraso de unos "
  "12 meses. La conexión con la vista Clientes se hace con variables sombra: demanda boca a boca entra a Capacidad, "
  "y Capacidad vuelve a Clientes por medio de la función MIN.")
p("Mientras la capacidad sea menor que la demanda, nuevos clientes = Capacidad / unidades por persona. En ese tramo "
  "el lazo R del boca a boca deja de controlar las ventas: la demanda crece pero las ventas solo crecen al ritmo "
  "al que se construye capacidad.")
code(eqs(difusion2(), "Capacidad"))

h3("Vista Ingresos por Ventas")
fig("diagrama_Cap09_difusion2_capacidad_Ingresos_por_Ventas.png", "Vista Ingresos por Ventas.", 12)
p("Las ventas (unidades/Mes) son los nuevos clientes por las unidades por persona. Los ingresos por ventas son "
  "ventas · precio (50 dólares por unidad) y se acumulan en el nivel Ingresos Acumulados, que es suplementario: "
  "sirve para informar y no realimenta el modelo.")
code(eqs(difusion2(), "Ingresos por Ventas"))

h3("Vista Capacidad detallada (difusion3)")
fig("diagrama_Cap09-10_difusion3_capacidad_detallada_Capacidad.png", "Vista Capacidad de difusion3, con la estructura pegada de cap1.mdl.", 14)
p("La capacidad ahora tiene dos flujos. La inversión agrega capacidad según la brecha con la capacidad objetivo y "
  "las reducciones la retiran por desgaste, con una vida de la capacidad de 20 meses. La producción es el menor "
  "valor entre la producción deseada (la demanda boca a boca expresada en aparatos) y la producción potencial (la "
  "Capacidad). En la vista Clientes, nuevos clientes = MIN(demanda boca a boca, producción / unidades por persona).")
p("En equilibrio, la inversión iguala a las reducciones: (objetivo − C)/12 = C/20, de donde C = 0,625 · objetivo. "
  "Por eso la capacidad nunca alcanza la capacidad objetivo y se queda por debajo de la demanda más tiempo que en "
  "difusion2. Con tiempo para ajustar la capacidad = 4, el equilibrio sube a C = 0,833 · objetivo.")
code(eqs(difusion3(), "Capacidad") + "\n\nSinónimos de unidades (Units Equiv): Aparato, Aparatos, Unidad, Unidades")

h2("2.d. Corridas de simulación")
fig("c09_clientes1.png", "Corrida clientes1: niveles y flujo de nuevos clientes.")
p(f"clientes1 (sin restricción). Clientes crece en forma de S. Al inicio entran {n(c1['nuevos_t0'])} nuevos "
  f"clientes por mes. El flujo crece exponencialmente hasta un máximo de {n(c1['pico_nuevos'])} personas/Mes en "
  f"el mes {c1['pico_t']:.0f}. La mitad del mercado ha comprado en el mes {c1['t_50']:.0f} y el 90 % en el mes "
  f"{c1['t_90']:.0f}. Al mes 100 prácticamente todo el mercado es cliente y Clientes Potenciales ha caído a cero. "
  "La curva de nuevos clientes tiene forma de campana: el punto de inflexión de Clientes coincide con el pico del "
  "flujo, que es el momento en que el lazo B pasa a dominar sobre el lazo R.")
fig("c09_nuevos_clientes_1vs2.png", "nuevos clientes en clientes1 y clientes2.", 12)
fig("c09_clientes2_capacidad.png", "clientes2: demanda boca a boca, Capacidad y nuevos clientes; Ingresos Acumulados.")
p(f"clientes2 (capacidad con ajuste de 12 meses). La Capacidad arranca igual a la demanda inicial, pero como se "
  f"ajusta con retraso queda por debajo de una demanda que crece exponencialmente, y las ventas quedan limitadas "
  f"por la capacidad. El crecimiento es más lento y el pico de nuevos clientes baja a {n(c2['pico_nuevos'])} "
  f"personas/Mes y se atrasa al mes {c2['pico_t']:.0f}, {c2['pico_t'] - c1['pico_t']:.0f} meses después que en "
  f"clientes1. La mitad del mercado se alcanza en el mes {c2['t_50']:.0f}. El pico ocurre cuando la demanda, que "
  "ya va bajando porque quedan pocos clientes potenciales, cae por debajo de la capacidad. Desde ese punto las "
  "ventas siguen a la demanda y caen rápido. El periodo de ventas es más largo, como dice la guía. Los Ingresos "
  f"Acumulados llegan a {n(c2['ingresos_t100'] / 1e6, 1)} millones de dólares al mes 100, que son los ~1 millón "
  "de clientes por 50 dólares.")
fig("c09_capacidad_detallada.png", "Capacidad en clientes2, clientes3 y clientes4; demanda y producción en el modelo detallado.")
fig("c09_nuevos_clientes_4corridas.png", "nuevos clientes en las cuatro corridas (equivale al gráfico de la guía).", 12)
p(f"clientes3 (capacidad detallada). Las reducciones por desgaste mantienen la capacidad por debajo del 62,5 % de la "
  f"capacidad objetivo, así que la producción limita las ventas casi toda la simulación. El pico baja a "
  f"{n(c3['pico_nuevos'])} personas/Mes y llega en el mes {c3['pico_t']:.0f}. Al mes 100 todavía quedan "
  f"{n(c3['cp_t100'])} clientes potenciales y los ingresos acumulados son {n(c3['ingresos_t100'] / 1e6, 1)} "
  "millones de dólares: la difusión no termina dentro del horizonte.")
p(f"clientes4 (política: tiempo para ajustar la capacidad = 4 meses). La capacidad se construye más rápido y se "
  f"acerca a la demanda. El pico sube a {n(c4['pico_nuevos'])} personas/Mes y se adelanta al mes "
  f"{c4['pico_t']:.0f}. La mitad del mercado se alcanza en el mes {c4['t_50']:.0f} y el 90 % en el mes "
  f"{c4['t_90']:.0f}. La curva se acerca a la ideal (clientes1), aunque sigue {c4['pico_t'] - c1['pico_t']:.0f} meses "
  "atrás: la restricción se corre pero no desaparece. Una empresa que invierte más rápido gana mercado antes que "
  "un competidor que lo haga despacio.")
table(["Corrida", "Pico de nuevos clientes (pers./Mes)", "Mes del pico", "Mes con 50 % del mercado",
       "Mes con 90 %", "Clientes al mes 100"],
      [[k, n(K[k]["pico_nuevos"]), f"{K[k]['pico_t']:.0f}", f"{K[k]['t_50']:.0f}", f"{K[k]['t_90']:.0f}",
        n(K[k]["clientes_t100"])] for k in ["clientes1", "clientes2", "clientes3", "clientes4"]],
      "Resumen de las corridas del capítulo 9.")

h2("2.e. Semejanzas y diferencias con el juego de la epidemia")
p("El juego de la epidemia de clase (Epidemia8.mdl) tiene la misma estructura que la vista Clientes. La Tabla 4 "
  "muestra la correspondencia entre sus elementos.")
table(["Modelo de difusión", "Juego de la epidemia"], [
    ["Clientes Potenciales (nivel)", "No infectados (nivel)"],
    ["Clientes (nivel)", "Infectados (nivel)"],
    ["nuevos clientes (flujo)", "Infecciones por mes (flujo)"],
    ["sociabilidad = 20 contactos/persona/Mes", "Saludos por infectado por mes = 0,5 (Infectados/2/Infectados)"],
    ["fructuosidad = 0,01", "Infecciosidad = 0,5"],
    ["concentración de clientes potenciales", "Probabilidad de contacto de un contagiado con un no contagiado"],
    ["mercado total = Clientes + Clientes Potenciales", "Población total = 66 (constante)"],
    ["Tasa efectiva 20 · 0,01 = 0,2 por mes", "Tasa efectiva 0,5 · 0,5 = 0,25 por mes"],
], "Correspondencia entre el modelo de difusión y el juego de la epidemia.", widths=[8, 8.5])
p("Semejanzas: los dos modelos tienen un lazo de refuerzo (el contagio y el boca a boca se propagan por contacto "
  "entre quien ya tiene la condición y quien no) y un lazo de balance por agotamiento de la población que puede "
  "adoptar o contagiarse. Los dos producen una curva en S en el nivel de adoptantes o infectados y una campana en el "
  "flujo.")
p("Diferencias: (1) en la difusión el resultado se busca (una venta) y en la epidemia se evita (un contagio); "
  "(2) la escala es distinta: 1.001.000 personas con 1.000 clientes iniciales (0,1 %) frente a 66 personas con 1 "
  "infectado (1,5 %); (3) el juego tiene TIME STEP 0,125 y la difusión 1; (4) en el juego cada persona se cuenta y "
  "los encuentros en el salón son aleatorios, mientras que el modelo es determinista y trabaja con promedios; "
  "(5) las versiones difusion2 y difusion3 agregan una restricción de oferta (capacidad, función MIN) y una "
  "contabilidad de ingresos que la epidemia no tiene. Para un virus no hay nada equivalente a una fábrica que "
  "limite cuántos contagios pueden ocurrir.")

# =====================================================================  3
pagebreak()
h1("3. Tutorial de salidas gráficas (capítulo 10, Customizing Output)")
h2("3.a-b. Reproducción")
p("Se abrió el modelo difusion3 con las cuatro corridas (clientes1 a clientes4) cargadas desde Control Panel > "
  "Datasets, se seleccionó nuevos clientes como variable de trabajo (Workbench Variable) y se aplicaron las "
  "opciones del capítulo:")
ol(["Gráfica por defecto de la herramienta Graph: líneas finas de distinto color.",
    "Líneas gruesas: Tools > Options > Graphics > Thick Lines (pantalla). Afecta todas las gráficas abiertas.",
    "Líneas con patrón: Tools > Options > Graph Lines > Patterned. Se volvió luego a Solid for Color.",
    "Solo puntos: clic derecho sobre la herramienta Graph > Line Type > Dots Only. Se volvió a Linear Interp.",
    "Marcadores de línea (Show Line Markers on Graph Lines): cada corrida se marca con su número (1, 2, 3, 4). "
    "Sirve para imprimir en blanco y negro.",
    "Gráfico personalizado: Control Panel > Graphs > New. Título «Difusión de clientes»; variables Clientes "
    "(clientes2), Clientes (clientes4), Capacidad (clientes2) y Capacidad (clientes4); casilla Scale para que cada "
    "par comparta su eje; LineW = 2 en las dos primeras. Se mostró con Display. El gráfico queda guardado dentro del "
    "archivo difusion3 junto con otro que muestra nuevos clientes en las cuatro corridas."])
fig("c10_opciones_graficas.png", "La misma variable (nuevos clientes, cuatro corridas) con las opciones de presentación del capítulo 10.")
fig("c10_grafico_personalizado.png", "Gráfico personalizado «Difusión de clientes»: Clientes y Capacidad en las corridas clientes2 y clientes4.", 13)
h2("3.c. Descripción de las corridas")
p(f"Las gráficas de la Figura {nfig[0]-1} solo cambian la presentación. Los datos son los de la sección 2.d: el pico de "
  f"nuevos clientes se mueve del mes {c1['pico_t']:.0f} (clientes1) al {c4['pico_t']:.0f} (clientes4), al "
  f"{c2['pico_t']:.0f} (clientes2) y al {c3['pico_t']:.0f} (clientes3), y cada pico es más bajo cuanto más "
  "restringida está la capacidad. Con los marcadores numerados se distinguen las corridas aunque el documento se "
  "imprima sin color. La opción de solo puntos muestra que Vensim calcula un valor por cada TIME STEP (un mes).")
p(f"El gráfico personalizado (Figura {nfig[0]}) permite comparar en una misma ventana la variable de estado y su "
  f"restricción. En clientes4 la Capacidad crece antes y llega a su máximo ({n(c4['cap_max'])} unidades/Mes) en el "
  f"mes {c4['cap_max_t']:.0f}. En clientes2 el máximo ({n(c2['cap_max'])} unidades/Mes) llega en el mes "
  f"{c2['cap_max_t']:.0f}. Por eso Clientes llega al 90 % del mercado en el mes {c4['t_90']:.0f} en clientes4 y en "
  f"el mes {c2['t_90']:.0f} en clientes2. Después del máximo la Capacidad cae en las dos corridas porque la "
  "capacidad objetivo baja con la demanda y el ajuste se vuelve negativo; en clientes4, además, la capacidad se "
  "deprecia con la vida de la capacidad. La forma de la Capacidad copia la "
  "de nuevos clientes, lo que confirma que es la variable que limita las ventas.")

# =====================================================================  4
pagebreak()
h1("4. Tutorial de controles de entrada y salida (capítulo 12, Input Output Controls)")
h2("4.a-b. Reproducción del modelo y de los controles")
p("El capítulo usa un modelo de ventas por boca a boca y publicidad (wom1.mdl), con INITIAL TIME = 0, FINAL TIME "
  "= 5, TIME STEP = 0,0625 y unidad de tiempo Año.")
fig("diagrama_Cap12_boca_a_boca_2_controles_Estructura.png", "Vista Estructura del modelo de ventas por boca a boca y publicidad.")
p("Hay dos niveles, Clientes Potenciales y Clientes, con dos flujos entre ellos. Los nuevos clientes vienen de "
  "las ventas, que suman las ventas potenciales boca a boca (3 unidades por cliente por año) y las ventas "
  "potenciales por publicidad (0,1 unidades por dólar). Esa suma se multiplica por la fracción con prospectos reales "
  "(Clientes Potenciales / Tamaño del Mercado). Los clientes que abandonan regresan a Clientes Potenciales al cabo "
  "del tiempo de obsolescencia (2 años), es decir, vuelven a ser compradores. El gasto en publicidad es una variable "
  "de juego: GAME(c gasto en publicidad).")
ul(["R, boca a boca: Clientes → ventas potenciales boca a boca → ventas → nuevos clientes → Clientes.",
    "B, saturación: nuevos clientes reducen Clientes Potenciales y la fracción con prospectos reales.",
    "B, obsolescencia: más Clientes producen más clientes que abandonan, que reducen Clientes.",
    "La publicidad es una entrada externa: inicia la difusión aunque haya pocos clientes semilla."])
code(eqs(boca_a_boca(False)))
p("Controles construidos (vistas Simular, Juego e Inicio):")
ol(["Control de salida: con la herramienta Input Output se insertó un gráfico de ventas (Output Workbench Tool, "
    "Graph) en la mitad derecha de la vista Simular. Se llena al pulsar Simulate.",
    "Deslizador c gasto en publicidad de 0 a 200·10⁶ $/Año con incremento 0,5·10⁶, con el comentario «Gasto en "
    "publicidad ($/Año)». Deslizador tiempo de obsolescencia de 0,5 a 10 años con incremento 0,1, con el "
    "comentario «Vida del producto (años)».",
    "Sombras de las constantes efectividad de ventas por cliente y Tamaño del Mercado, que se pueden cambiar en "
    "Set Up a Simulation. Se alinearon con Layout > Center on LastSel.",
    "Con Set Up a Simulation (o SyntheSim) se movieron los deslizadores y se simuló varias veces; el gráfico "
    "muestra cada corrida.",
    "Vista Juego: se copiaron el gráfico y el deslizador y se cambió el deslizador a la variable de juego gasto en "
    "publicidad. Con el botón Game se avanza en intervalos y se cambia el gasto en cada paso.",
    "Publicación: constante suplementaria GAME INTERVAL = 0,5 años; vistas renombradas y reordenadas (Inicio, "
    "Estructura, Simular, Juego); comentarios de ayuda en Inicio con enlaces de navegación (campo Navigate de "
    "la herramienta Comment) hacia cada vista."])
fig("diagrama_Cap12_boca_a_boca_2_controles_Simular.png", "Esquema de la vista Simular: deslizadores, sombras y gráfico de salida.", 13)

h2("4.c. Descripción de las corridas")
b = w["base"]
fig("c12_base.png", "Corrida base del modelo de ventas por boca a boca.")
p(f"Corrida base (gasto 20 millones $/año, vida 2 años). Las ventas arrancan en {n(b['ventas_t0'] / 1e6, 2)} "
  f"millones de unidades/año, casi todas por publicidad, porque los 10.000 clientes semilla aportan poco boca a boca. "
  f"Después crece el boca a boca y las ventas llegan a un máximo de {n(b['pico_ventas'] / 1e6, 1)} millones/año a "
  f"los {n(b['pico_t'], 2)} años. Luego bajan a {n(b['ventas_t5'] / 1e6, 1)} millones/año al año 5. A diferencia "
  "del modelo del capítulo 9, las ventas no llegan a cero: los clientes que abandonan vuelven al mercado y se "
  f"vuelven a vender. Al año 5 hay {n(b['clientes_t5'] / 1e6, 1)} millones de clientes de un mercado de 100 "
  "millones.")
fig("c12_deslizadores.png", "Experimentos con los deslizadores de gasto en publicidad y vida del producto.")
p(f"Deslizador de publicidad. Sin publicidad la difusión depende solo de los clientes semilla: las ventas parten "
  f"de {n(w['pub_0e+00']['ventas_t0'])} unidades/año y su pico ({n(w['pub_0e+00']['pico_ventas'] / 1e6, 1)} "
  f"millones) llega a los {n(w['pub_0e+00']['pico_t'], 1)} años, unos dos años después que en la base. Con 100 y 200 "
  f"millones $/año el pico se adelanta a {n(w['pub_1e+08']['pico_t'], 2)} y {n(w['pub_2e+08']['pico_t'], 1)} años y "
  f"sube a {n(w['pub_1e+08']['pico_ventas'] / 1e6, 1)} y {n(w['pub_2e+08']['pico_ventas'] / 1e6, 1)} millones/año. "
  "Al año 5 el número de clientes casi no cambia: la publicidad adelanta la difusión pero no agranda el mercado.")
p(f"Deslizador de vida del producto. Con 0,5 años los clientes salen muy rápido: al año 5 solo hay "
  f"{n(w['vida_0.5']['clientes_t5'] / 1e6, 1)} millones de clientes, pero las ventas siguen subiendo "
  f"({n(w['vida_0.5']['ventas_t5'] / 1e6, 1)} millones/año) porque cada cliente compra de nuevo con frecuencia. "
  f"Con 10 años casi todo el mercado se vuelve cliente ({n(w['vida_10']['clientes_t5'] / 1e6, 1)} millones) y, "
  f"después del pico, las ventas caen a {n(w['vida_10']['ventas_t5'] / 1e6, 1)} millones/año porque casi no quedan "
  "compradores. Un producto que dura poco tiene ventas más sostenidas; uno durable satura su mercado.")
fig("c12_juego.png", "Juego: decisiones de gasto en publicidad cada 0,5 años y ventas resultantes.")
p(f"Juego. Se jugó con intervalos de 0,5 años: 100 millones $/año el primer año, 50 millones entre 1 y 1,5 años, "
  f"nada entre 1,5 y 3 años y 20 millones desde el año 3. Las ventas llegan a su máximo "
  f"({n(w['juego']['pico_ventas'] / 1e6, 1)} millones/año) a los {n(w['juego']['pico_t'], 2)} años, antes que en la "
  f"base, y al año 5 los clientes ({n(w['juego']['clientes_t5'] / 1e6, 1)} millones) son casi los mismos de la base. "
  "La lección del juego es que la publicidad rinde al comienzo, cuando el boca a boca es débil. Cuando la base de "
  "clientes es grande, el boca a boca y el retorno de los clientes que abandonan sostienen las ventas y la "
  "publicidad adicional aporta poco.")

# =====================================================================  5
pagebreak()
h1("5. Comparación con el modelo de la epidemia")
fig("clase_epidemia8.png", "Modelo de la epidemia de clase (Epidemia8.mdl). Se extendió a 40 meses para ver el final del proceso; la línea punteada marca FINAL TIME = 20.")
h2("5.a. Semejanzas y diferencias en la estructura")
table(["Aspecto", "Difusión de un producto (cap. 9 y 12)", "Epidemia de clase"], [
    ["Niveles", "Clientes Potenciales y Clientes", "No infectados e Infectados"],
    ["Flujo principal", "nuevos clientes", "Infecciones por mes"],
    ["Mecanismo", "contactos · fructuosidad · fracción de no clientes", "saludos · infecciosidad · probabilidad de encontrar un no infectado"],
    ["Lazo de refuerzo", "Boca a boca", "Contagio"],
    ["Lazo de balance", "Saturación del mercado", "Agotamiento de no infectados"],
    ["Población", "Cerrada (mercado total constante)", "Cerrada (Población total = 66)"],
    ["Salidas del nivel de adoptantes", "Ninguna (cap. 9); clientes que abandonan (cap. 12)", "Ninguna: nadie se recupera"],
    ["Entradas externas", "Publicidad (cap. 12)", "Ninguna: solo contagio entre personas"],
    ["Restricciones de oferta", "Capacidad y producción con MIN (difusion2 y 3)", "No tiene"],
    ["Variables económicas", "ventas, precio, Ingresos Acumulados", "No tiene"],
], "Comparación estructural.", widths=[3.6, 6.6, 6.3])
p("En su forma básica (vista Clientes de difusion1) los dos modelos son el mismo modelo logístico con otros nombres: "
  "el flujo es igual a una tasa efectiva por el nivel de adoptantes por la fracción de la población que todavía "
  "puede adoptar. Difieren en lo que se agregó encima. La difusión del capítulo 9 suma una restricción física "
  "(capacidad de producción con retraso de ajuste) y la contabilidad de ingresos. La del capítulo 12 suma una fuente "
  "externa de adopción (publicidad) y un flujo de regreso (obsolescencia), que en epidemiología equivale a perder la "
  "inmunidad (modelo SIS). El modelo de clase no tiene ninguno de estos mecanismos.")
h2("5.b. Semejanzas y diferencias en el comportamiento")
fig("comparacion_modelos.png", "Comportamiento normalizado de los tres modelos: fracción de adoptantes o infectados y flujo normalizado.")
p(f"Semejanzas: en clientes1 y en la epidemia de clase el nivel de adoptantes o infectados crece en S, el nivel "
  f"de potenciales decrece hasta casi cero y el flujo tiene forma de campana con su máximo cuando la mitad de la "
  f"población ya cambió de estado: mes {c1['pico_t']:.0f} en la difusión y mes {cl['inf_pico_t']:.1f} en la "
  f"epidemia (cuando Infectados ≈ 33). En los dos casos todos terminan adoptando o contagiados, porque nada saca "
  "personas del nivel de adoptantes.")
p(f"Diferencias: (1) la epidemia es más rápida en términos relativos. Arranca con el 1,5 % de la población infectada "
  f"y tasa 0,25/mes, y la difusión arranca con el 0,1 % y tasa 0,2/mes. En el modelo logístico el pico llega en "
  f"ln(potenciales/iniciales)/tasa: ln(65)/0,25 ≈ 16,7 meses en la epidemia y ln(1000)/0,2 ≈ 34,5 meses en la "
  f"difusión (con TIME STEP = 1 la simulación da el mes {c1['pico_t']:.0f}). (2) Con FINAL TIME = 20 la epidemia de "
  f"clase no termina: al mes 20 hay {n(cl['I_t20'], 1)} infectados de 66, y solo se completa hacia el mes 40 "
  f"({n(cl['I_t40'], 1)}). (3) Con restricción de capacidad (clientes2 a clientes4) la campana se vuelve asimétrica: "
  "sube despacio, al ritmo de la capacidad, y cae de golpe cuando la demanda queda por debajo de la capacidad. La "
  "epidemia no tiene ese quiebre. (4) En el modelo del capítulo 12 el sistema no se agota: llega a un equilibrio "
  "dinámico con ventas permanentes, que se parece a una enfermedad endémica y no al final de una epidemia.")

# =====================================================================  6
pagebreak()
h1("6. Caso 2.1 del libro de Juan Martín García: desarrollo de una epidemia")
h2("6.a. Documentación y descripción del diagrama")
fig("diagrama_JMG_2.1_desarrollo_epidemia_Epidemia.png", "Diagrama de niveles y flujos del caso 2.1 (reproducido en Vensim con los nombres del libro).")
p("El modelo toma como referencia el modelo SIR de Kermack y McKendrick (S' = −βSI, I' = βSI − γI, R' = γI) y le "
  "agrega vacunación, muertes y pérdida de inmunidad. Se construyó con INITIAL TIME = 0, FINAL TIME = 20, TIME "
  "STEP = 1 y unidad de tiempo mes. Siguiendo la Nota 1 del libro, no se asignaron unidades a las variables.")
ul(["Niveles: Susceptibles (900 al inicio), personas que pueden contagiarse; Infectados (100), personas que tienen "
    "la enfermedad y la transmiten; Recuperados (0), personas inmunes por curación o vacunación.",
    "enferman = Susceptibles · tasa de contagio · Infectados, con tasa de contagio = 0,001. Es la fórmula de "
    "Kermack y McKendrick (Nota 3: funciona bien en la práctica aunque sus unidades no son coherentes).",
    "curan = Infectados · tasa de curación (0,4). Los infectados pasan a Recuperados.",
    "muertes = Infectados · tasa de mortalidad (0,1). Salen del sistema hacia una nube; por eso la población total "
    "baja.",
    "vacunados = Susceptibles · tensión. Pasan directamente de Susceptibles a Recuperados sin enfermar.",
    "tensión = (enferman / Susceptibles) · tasa de vacunacion (0,5). Representa el riesgo percibido: la gente se "
    "vacuna más cuando ve que una mayor fracción de susceptibles enferma. Al reemplazar, vacunados = 0,5 · enferman: "
    "por cada dos personas que enferman se vacuna una.",
    "expuestos = Recuperados · tasa de exposición (0,05). Los recuperados pierden la inmunidad y vuelven a "
    "Susceptibles, lo que convierte al modelo en uno de tipo SIRS.",
    "Total poblacion = Susceptibles + Infectados + Recuperados. Se construye con variables sombra para no cruzar "
    "flechas. Es una variable de control que no influye en el resto, y por eso Vensim avisa que no se usa (Nota 2).",
    "Alerta de mínimo y máximo: a Infectados se le asignó el rango [50, 150] en la ventana de la ecuación. Al "
    f"simular, Vensim emite los avisos Above en el mes {j['warnings']['above'][0]:.0f}, In en el mes "
    f"{j['warnings']['back_in'][0]:.0f} y Below en el mes {j['warnings']['below'][0]:.0f}, igual que en el libro."])
p("Lazos de realimentación del diagrama:")
ul(["R, contagio: Infectados → enferman → Infectados.",
    "B, agotamiento de susceptibles: Susceptibles → enferman → Susceptibles.",
    "B, curación y B, mortalidad: Infectados → curan / muertes → Infectados.",
    "B, vacunación por tensión: Infectados → enferman → tensión → vacunados → Susceptibles → enferman.",
    "R, reinfección: Recuperados → expuestos → Susceptibles → enferman → Infectados → curan → Recuperados, "
    "junto con el lazo B Recuperados → expuestos → Recuperados."])
code(eqs(epidemia_jmg()))
p("Gráficos configurados en el modelo (Control Panel > Graphs): el gráfico XY de muertes frente a enferman "
  "(eje X de 0 a 110 con 11 divisiones, grosor de línea 4), el gráfico temporal de muertes y enferman, y el de los "
  "tres estados con la población total.")

h2("6.b. Semejanzas y diferencias de estructura con el modelo de clase")
table(["Aspecto", "Modelo de clase (Epidemia8)", "Caso 2.1 (J. Martín García)"], [
    ["Estados", "2: No infectados, Infectados (SI)", "3: Susceptibles, Infectados, Recuperados (SIR/SIRS)"],
    ["Contagio", "Infecciosidad · saludos · Infectados · (No infectados / Población total)",
     "tasa de contagio · Susceptibles · Infectados (acción de masas, sin dividir por la población)"],
    ["Salidas de Infectados", "Ninguna", "curan (0,4) y muertes (0,1)"],
    ["Vacunación", "No", "Sí, proporcional al riesgo percibido (tensión)"],
    ["Pérdida de inmunidad", "No", "Sí (expuestos, 0,05)"],
    ["Población", "Constante: 66", "Disminuye por las muertes; se calcula como Total poblacion"],
    ["Condiciones iniciales", "1 infectado de 66 (1,5 %)", "100 infectados de 1.000 (10 %)"],
    ["Unidades y tiempo", "Con unidades; TIME STEP 0,125; 20 meses", "Sin unidades; TIME STEP 1; 20 meses"],
    ["Lazos", "R contagio y B agotamiento", "Los mismos, más B de curación, mortalidad y vacunación, y R de reinfección"],
], "Comparación estructural entre las dos epidemias.", widths=[3.4, 6, 7.1])
p("Lo que comparten es el núcleo: un nivel de personas que se pueden contagiar, un nivel de contagiados, un flujo "
  "de contagio que crece con el producto de ambos niveles, un lazo de refuerzo y un lazo de balance por agotamiento. "
  "La diferencia principal es que en el modelo de clase la enfermedad no termina: nadie sale de Infectados. En el "
  "libro los infectados se curan o mueren, y hay políticas (vacunación) y procesos (pérdida de inmunidad) que "
  "cambian la población susceptible. Además, la incidencia del libro depende del número absoluto de susceptibles "
  "(β·S·I), mientras que la de clase depende de la fracción de no infectados (S/N): en el libro, una población más "
  "grande se contagia más rápido.")

h2("6.c. Semejanzas y diferencias de comportamiento")
fig("jmg_infectados_susceptibles.png", "Infectados (con las líneas del rango 50-150) y Susceptibles; coinciden con la página 29 del libro.")
fig("jmg_estados.png", "Los tres estados y la población total.", 12)
fig("jmg_xy.png", "Gráfico XY de muertes frente a enferman y gráfico temporal de ambas variables.")
p(f"Resultados del caso 2.1. Infectados sube de 100 a un máximo de {n(j['I_pico'], 1)} en el mes "
  f"{j['I_pico_t']:.0f} y luego baja hasta {n(j['I_t20'], 1)} en el mes 20. Susceptibles cae de 900 a un mínimo de "
  f"{n(j['S_min'], 1)} en el mes {j['S_min_t']:.0f} y después vuelve a subir hasta {n(j['S_t20'], 1)}, porque los "
  f"recuperados pierden la inmunidad. Recuperados llega a {n(j['R_max'], 1)} en el mes {j['R_max_t']:.0f}. El flujo "
  f"enferman empieza en {n(j['enferman_t0'])} personas/mes y tiene su máximo ({n(j['enferman_pico'], 1)}) en el mes "
  f"{j['enferman_pico_t']:.0f}. Mueren {n(j['muertes_total'])} personas y la población baja a "
  f"{n(j['P_t20'], 1)}. El gráfico XY forma un lazo: hay cerca de 10 muertes con unas 90 personas enfermando (mes 0) "
  "y otra vez con unas 19 (mes 7). Pasa porque muertes depende de Infectados, que va retrasado respecto a enferman.")
p("El pico de infectados se puede explicar con el umbral del modelo SIR. Infectados crece mientras enferman supera "
  "a curan + muertes, es decir, mientras Susceptibles > (tasa de curación + tasa de mortalidad) / tasa de contagio "
  "= 0,5 / 0,001 = 500. El número reproductivo inicial es R0 = 0,001 · 900 / 0,5 = 1,8. Entre los meses 2 y 3 "
  "Susceptibles cae de 609 a 456, por debajo de 500, y por eso Infectados alcanza su máximo en el mes 3.")
table(["Mes", "Susceptibles", "Infectados", "Recuperados", "enferman", "vacunados", "muertes", "Total poblacion"],
      [[str(i)] + [n(j["tabla"][c][i], 1) for c in ["Susceptibles", "Infectados", "Recuperados", "enferman",
                                                    "vacunados", "muertes", "Total poblacion"]]
       for i in range(0, 21, 2)],
      "Valores simulados del caso 2.1 (cada dos meses).")
p("Comparación con el modelo de clase:")
ul([f"Semejanza: en los dos modelos el contagio empieza de forma exponencial por el lazo R, y el flujo de contagio "
    f"(enferman o Infecciones por mes) tiene forma de campana porque el lazo de agotamiento termina dominando.",
    f"Diferencia en Infectados: en clase crece en S hasta casi toda la población ({n(cl['I_t40'], 1)} de 66 al mes "
    f"40). En el libro sube y baja (campana), porque los infectados salen por curación y muerte.",
    f"Diferencia en el final: en clase todos se contagian y No infectados llega a cero. En el libro la epidemia se "
    f"apaga con susceptibles sin contagiar (mínimo {n(j['S_min'])}), porque la transmisión se detiene al cruzar el "
    "umbral de 500 susceptibles y la vacunación protege a parte de la población.",
    f"Diferencia en la velocidad: el pico del libro llega en el mes {j['I_pico_t']:.0f} y el flujo de clase en el mes "
    f"{cl['inf_pico_t']:.1f}. El libro parte con 10 % de infectados y una tasa de contagio inicial por infectado de "
    "0,001 · 900 = 0,9 por mes. El modelo de clase parte con 1,5 % y 0,25 por mes.",
    "Diferencia en la población: en clase es constante. En el libro disminuye por las muertes.",
    "Diferencia a largo plazo: como los recuperados vuelven a ser susceptibles, en el libro Susceptibles supera otra "
    "vez el umbral de 500 hacia el mes 25. Si se extiende la simulación a 80 meses aparece un segundo brote, más "
    "pequeño, con unos 34 infectados hacia el mes 50. En el modelo de clase no puede haber un segundo brote porque no "
    "quedan susceptibles."])

# =====================================================================  ANEXO
pagebreak()
h1("Anexo. Ecuaciones completas de los modelos con varias vistas")
h3("difusion3 (capítulos 9 y 10), todas las vistas")
code(eqs(difusion3()))
h3("Modelo de ventas por boca a boca con controles (capítulo 12)")
code(eqs(boca_a_boca(True)))


# ======================================================================= render
def img_b64(name):
    with open(os.path.join(FIG, name), "rb") as f:
        return base64.b64encode(f.read()).decode()


def to_html():
    css = """
    @page { size: Letter; margin: 2cm 2cm 2cm 2cm; }
    body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; }
    h1 { font-size: 15pt; color: #12355b; border-bottom: 2px solid #12355b; padding-bottom: 3px; margin-top: 18px; }
    h2 { font-size: 12.5pt; color: #12355b; margin-top: 14px; }
    h3 { font-size: 11pt; color: #333; margin-top: 12px; }
    p { text-align: justify; margin: 6px 0; }
    pre { background: #f5f6f8; border: 1px solid #dde; padding: 7px 9px; font-size: 8.3pt; white-space: pre-wrap;
          font-family: 'DejaVu Sans Mono', monospace; page-break-inside: auto; }
    figure { margin: 10px 0; text-align: center; page-break-inside: avoid; }
    figure img { max-width: 100%; }
    figcaption { font-size: 9pt; color: #444; margin-top: 3px; }
    table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 8px 0; page-break-inside: avoid; }
    th { background: #12355b; color: white; padding: 4px; text-align: left; }
    td { border: 1px solid #ccd; padding: 3px 4px; vertical-align: top; }
    .cap { font-size: 9pt; color: #444; text-align: center; margin-bottom: 3px; }
    .pb { page-break-after: always; }
    .cover { text-align: center; padding-top: 3.2cm; }
    .cover h1 { border: none; font-size: 22pt; }
    .cover .sub { font-size: 13pt; margin: 8px; }
    .cover table { width: 70%; margin: 30px auto; font-size: 11pt; }
    li { margin: 3px 0; text-align: justify; }
    """
    o = [f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>"]
    for kind, v in B:
        if kind == "cover":
            o.append("<div class='cover'><div class='sub'>Universidad Nacional de Colombia, Sede Bogotá<br>"
                     "Facultad de Ingeniería · Departamento de Ingeniería Civil y Agrícola</div>"
                     "<div class='sub'>INGENIERÍA CIVIL SOSTENIBLE (2026135) · 2026-2S</div>"
                     "<h1>Taller 2<br>Dinámica de sistemas con Vensim:<br>difusión de un producto y epidemias</h1>"
                     "<table><tr><th>Integrantes del grupo</th></tr>"
                     + "".join("<tr><td>&nbsp;</td></tr>" for _ in range(4)) +
                     "</table><div class='sub'>Entrega: domingo 29 de noviembre de 2026</div></div><div class='pb'></div>")
        elif kind == "h1": o.append(f"<h1>{html.escape(v)}</h1>")
        elif kind == "h2": o.append(f"<h2>{html.escape(v)}</h2>")
        elif kind == "h3": o.append(f"<h3>{html.escape(v)}</h3>")
        elif kind == "p": o.append(f"<p>{html.escape(v)}</p>")
        elif kind == "ul": o.append("<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in v) + "</ul>")
        elif kind == "ol": o.append("<ol>" + "".join(f"<li>{html.escape(x)}</li>" for x in v) + "</ol>")
        elif kind == "code": o.append(f"<pre>{html.escape(v)}</pre>")
        elif kind == "pb": o.append("<div class='pb'></div>")
        elif kind == "img":
            name, cap, width = v
            o.append(f"<figure><img style='width:{min(width, 16.5)}cm' src='data:image/png;base64,{img_b64(name)}'>"
                     f"<figcaption>{html.escape(cap)}</figcaption></figure>")
        elif kind == "table":
            hd, rows, cap, widths = v
            t = "<table>"
            if widths:
                t += "<colgroup>" + "".join(f"<col style='width:{x}cm'>" for x in widths) + "</colgroup>"
            t += "<tr>" + "".join(f"<th>{html.escape(x)}</th>" for x in hd) + "</tr>"
            t += "".join("<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in r) + "</tr>" for r in rows) + "</table>"
            o.append((f"<div class='cap'>{html.escape(cap)}</div>" if cap else "") + t)
    o.append("</body></html>")
    return "\n".join(o)


def to_docx(path):
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Cm(2))
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    for kind, v in B:
        if kind == "cover":
            for t, size, bold in [("Universidad Nacional de Colombia, Sede Bogotá", 13, False),
                                  ("Facultad de Ingeniería · Departamento de Ingeniería Civil y Agrícola", 11, False),
                                  ("INGENIERÍA CIVIL SOSTENIBLE (2026135) · 2026-2S", 12, False),
                                  ("", 12, False),
                                  ("Taller 2", 22, True),
                                  ("Dinámica de sistemas con Vensim: difusión de un producto y epidemias", 16, True),
                                  ("", 12, False), ("Integrantes del grupo:", 12, True)]:
                pp = d.add_paragraph(); pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = pp.add_run(t); r.font.size = Pt(size); r.bold = bold
            tb = d.add_table(rows=4, cols=1); tb.style = "Table Grid"
            pp = d.add_paragraph("\nEntrega: domingo 29 de noviembre de 2026"); pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "h1": d.add_heading(v, level=1)
        elif kind == "h2": d.add_heading(v, level=2)
        elif kind == "h3": d.add_heading(v, level=3)
        elif kind == "p":
            pp = d.add_paragraph(v); pp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif kind in ("ul", "ol"):
            for x in v:
                d.add_paragraph(x, style="List Bullet" if kind == "ul" else "List Number")
        elif kind == "code":
            pp = d.add_paragraph()
            r = pp.add_run(v); r.font.name = "Consolas"; r.font.size = Pt(8)
        elif kind == "pb":
            d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "img":
            name, cap, width = v
            d.add_picture(os.path.join(FIG, name), width=Cm(min(width, 17)))
            d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            pp = d.add_paragraph(cap); pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pp.runs[0].font.size = Pt(9); pp.runs[0].italic = True
        elif kind == "table":
            hd, rows, cap, widths = v
            if cap:
                pp = d.add_paragraph(cap); pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pp.runs[0].font.size = Pt(9); pp.runs[0].italic = True
            tb = d.add_table(rows=1, cols=len(hd)); tb.style = "Light Grid Accent 1"
            for i, x in enumerate(hd):
                tb.rows[0].cells[i].text = x
            for r in rows:
                cells = tb.add_row().cells
                for i, x in enumerate(r):
                    cells[i].text = x
            for row in tb.rows:
                for i, c in enumerate(row.cells):
                    if widths:
                        c.width = Cm(widths[i])
                    for par in c.paragraphs:
                        for run in par.runs:
                            run.font.size = Pt(8.5)
            d.add_paragraph()
    d.save(path)


with open(os.path.join(OUT, "informe.html"), "w", encoding="utf-8") as f:
    f.write(to_html())
to_docx(os.path.join(OUT, "Informe_Taller2_ICS.docx"))
print("figuras:", nfig[0], "tablas:", ntab[0])
