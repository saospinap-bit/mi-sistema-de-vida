"""Definicion de los modelos del Taller 2 ICS (en espanol)."""
from sd import Model

# ============================================================================
# Capitulo 9 - Modelo de difusion de un producto (cust1 / cust2 / cust3)
# ============================================================================

def vista_clientes(m, sombra_limite=None):
    """Vista 'Clientes' (difusion por boca a boca).
    sombra_limite: None (difusion1), 'Capacidad' (difusion2) o 'producción' (difusion3)."""
    m.stock("Clientes Potenciales", "1e+06", "persona", 150, 150, w=55,
            comment="Personas que aún no tienen el producto pero podrían comprarlo.")
    m.stock("Clientes", "1000", "persona", 650, 150,
            comment="Personas que ya poseen el producto.")
    if sombra_limite is None:
        eq = "demanda boca a boca"
    elif sombra_limite == "Capacidad":
        eq = "MIN(demanda boca a boca, Capacidad/unidades por persona)"
    else:
        eq = "MIN(demanda boca a boca, producción/unidades por persona)"
    m.flow("nuevos clientes", eq, "persona/Mes", "Clientes Potenciales", "Clientes",
           valve=(400, 150), comment="Personas que compran el producto cada mes.")
    m.aux("demanda boca a boca", "contactos de no clientes con clientes * fructuosidad",
          "persona/Mes", 400, 250, comment="Compras que generaría el boca a boca si no hubiera restricciones.")
    m.aux("fructuosidad", "0.01", "persona/contactos", 225, 290,
          comment="Fracción de contactos con clientes que termina en una compra.")
    m.aux("contactos de no clientes con clientes",
          "contactos con clientes * concentración de clientes potenciales", "contactos/Mes",
          400, 345, w=62)
    m.aux("contactos con clientes", "Clientes * sociabilidad", "contactos/Mes", 650, 345)
    m.aux("sociabilidad", "20", "contactos/persona/Mes", 800, 290,
          comment="Contactos que hace cada cliente por mes.")
    m.aux("concentración de clientes potenciales", "Clientes Potenciales / mercado total",
          "Dmnl", 150, 345, w=58,
          comment="Probabilidad de que un contacto de un cliente sea con un no cliente.")
    m.aux("mercado total", "Clientes + Clientes Potenciales", "persona", 400, 55)
    m.arrow("Clientes", "contactos con clientes")
    m.arrow("sociabilidad", "contactos con clientes")
    m.arrow("contactos con clientes", "contactos de no clientes con clientes")
    m.arrow("concentración de clientes potenciales", "contactos de no clientes con clientes")
    m.arrow("Clientes Potenciales", "concentración de clientes potenciales")
    m.arrow("mercado total", "concentración de clientes potenciales", via=(70, 250))
    m.arrow("Clientes Potenciales", "mercado total", via=(255, 75))
    m.arrow("Clientes", "mercado total", via=(545, 75))
    m.arrow("contactos de no clientes con clientes", "demanda boca a boca")
    m.arrow("fructuosidad", "demanda boca a boca")
    m.arrow("demanda boca a boca", "nuevos clientes")
    m.loop("R", 560, 255, clockwise=True)
    m.loop("B", 205, 245, clockwise=False)
    if sombra_limite:
        m.shadow(sombra_limite, 545, 205, w=35)
        m.shadow("unidades por persona", 285, 218, w=55)
        m.arrow(sombra_limite, "nuevos clientes")
        m.arrow("unidades por persona", "nuevos clientes")


def vista_ingresos(m):
    m.view("Ingresos por Ventas")
    m.shadow("nuevos clientes", 140, 250)
    m.shadow("unidades por persona", 140, 340, w=55)
    m.aux("ventas", "nuevos clientes * unidades por persona", "Unidad/Mes", 320, 295, w=25)
    m.aux("precio", "50", "dólar/Unidad", 490, 300, w=25)
    m.cloud("nube ingresos", 330, 150)
    m.stock("Ingresos Acumulados", "0", "dólar", 650, 150, w=55, supplementary=True,
            comment="Ingresos totales recibidos por la venta del producto.")
    m.flow("ingresos por ventas", "ventas * precio", "dólar/Mes", "nube ingresos",
           "Ingresos Acumulados", valve=(490, 150))
    m.arrow("nuevos clientes", "ventas")
    m.arrow("unidades por persona", "ventas")
    m.arrow("ventas", "ingresos por ventas")
    m.arrow("precio", "ingresos por ventas")


def difusion1():
    m = Model(0, 100, 1, "Mes")
    m.views[0].name = "Clientes"
    vista_clientes(m)
    return m


def difusion2():
    m = Model(0, 100, 1, "Mes")
    m.views[0].name = "Clientes"
    vista_clientes(m, "Capacidad")
    m.view("Capacidad")
    m.cloud("nube capacidad", 170, 150)
    m.stock("Capacidad", "capacidad objetivo", "Unidad/Mes", 420, 150,
            comment="Capacidad de producción de la fábrica.")
    m.flow("ajuste de capacidad",
           "(capacidad objetivo - Capacidad) / tiempo para ajustar la capacidad",
           "Unidad/Mes/Mes", "nube capacidad", "Capacidad", valve=(290, 150), both_heads=True,
           comment="Puede ser positivo (ampliar) o negativo (reducir) la capacidad.")
    m.aux("capacidad objetivo", "demanda boca a boca * unidades por persona", "Unidad/Mes",
          420, 280)
    m.aux("tiempo para ajustar la capacidad", "12", "Mes", 180, 270, w=55)
    m.aux("unidades por persona", "1", "Unidad/persona", 610, 330, w=55)
    m.shadow("demanda boca a boca", 420, 380, w=55)
    m.arrow("Capacidad", "ajuste de capacidad", via=(350, 215))
    m.arrow("capacidad objetivo", "ajuste de capacidad")
    m.arrow("tiempo para ajustar la capacidad", "ajuste de capacidad")
    m.arrow("unidades por persona", "capacidad objetivo")
    m.arrow("demanda boca a boca", "capacidad objetivo")
    m.arrow("capacidad objetivo", "Capacidad", via=(470, 215), init_link=True)
    vista_ingresos(m)
    return m


def difusion3():
    m = Model(0, 100, 1, "Mes")
    m.views[0].name = "Clientes"
    vista_clientes(m, "producción")
    m.view("Capacidad")
    m.cloud("nube inversión", 130, 150)
    m.stock("Capacidad", "capacidad objetivo", "Aparato/Mes", 400, 150,
            comment="Capacidad instalada; crece con la inversión y se deprecia con su vida útil.")
    m.cloud("nube reducciones", 680, 150)
    m.flow("inversión", "ajuste de capacidad", "Aparato/Mes/Mes", "nube inversión", "Capacidad",
           valve=(260, 150))
    m.flow("reducciones", "Capacidad / vida de la capacidad", "Aparato/(Mes*Mes)",
           "Capacidad", "nube reducciones", valve=(550, 150))
    m.aux("ajuste de capacidad",
          "(capacidad objetivo - Capacidad) / tiempo para ajustar la capacidad",
          "Aparato/Mes/Mes", 260, 250)
    m.aux("tiempo para ajustar la capacidad", "12", "Mes", 110, 300, w=55)
    m.aux("capacidad objetivo", "producción deseada", "Aparato/Mes", 400, 300)
    m.aux("vida de la capacidad", "20", "Mes", 690, 250)
    m.aux("producción potencial", "Capacidad", "Aparato/Mes", 560, 330)
    m.aux("producción", "MIN(producción deseada, producción potencial)", "Aparato/Mes", 560, 440,
          w=35)
    m.aux("producción deseada", "demanda boca a boca * unidades por persona", "Aparato/Mes",
          300, 420)
    m.aux("unidades por persona", "1", "Unidad/persona", 140, 480, w=55)
    m.shadow("demanda boca a boca", 330, 510, w=55)
    m.arrow("Capacidad", "ajuste de capacidad", via=(345, 210))
    m.arrow("capacidad objetivo", "ajuste de capacidad")
    m.arrow("tiempo para ajustar la capacidad", "ajuste de capacidad")
    m.arrow("ajuste de capacidad", "inversión")
    m.arrow("Capacidad", "reducciones", via=(470, 105))
    m.arrow("vida de la capacidad", "reducciones")
    m.arrow("Capacidad", "producción potencial", via=(500, 240))
    m.arrow("producción potencial", "producción")
    m.arrow("producción deseada", "producción")
    m.arrow("producción deseada", "capacidad objetivo")
    m.arrow("demanda boca a boca", "producción deseada")
    m.arrow("unidades por persona", "producción deseada")
    m.arrow("capacidad objetivo", "Capacidad", via=(445, 225), init_link=True)
    vista_ingresos(m)
    m.unit_equivs.append("Aparato,Aparatos,Unidad,Unidades")
    # Capitulo 10 - grafico personalizado
    m.custom_graph("Difusion_de_clientes", "Difusión de clientes",
                   [("Clientes", "clientes2", 2), ("Clientes", "clientes4", 2),
                    ("Capacidad", "clientes2", None), ("Capacidad", "clientes4", None)],
                   scale_groups=[0, 2])
    m.custom_graph("nuevos_clientes_4_corridas", "nuevos clientes en las 4 corridas",
                   [("nuevos clientes", "clientes1", 2), ("nuevos clientes", "clientes2", 2),
                    ("nuevos clientes", "clientes3", 2), ("nuevos clientes", "clientes4", 2)])
    return m


# ============================================================================
# Capitulo 12 - Controles de entrada y salida (modelo de ventas boca a boca)
# ============================================================================

def boca_a_boca(con_controles=True):
    m = Model(0, 5, 0.0625, "Año")
    m.views[0].name = "Estructura"
    m.stock("Clientes Potenciales", "Tamaño del Mercado - Clientes Semilla", "persona", 150, 200, w=55)
    m.stock("Clientes", "Clientes Semilla", "persona", 600, 200)
    m.flow("nuevos clientes", "ventas / tamaño de la venta", "persona/Año",
           "Clientes Potenciales", "Clientes", valve=(375, 200))
    m.flow("clientes que abandonan", "Clientes / tiempo de obsolescencia", "persona/Año",
           "Clientes", "Clientes Potenciales", valve=(375, 90), src_corner=(600, 90),
           dst_corner=(150, 90), label_off=(0, -22), w=50)
    m.aux("Clientes Semilla", "10000", "persona", 375, 145)
    m.aux("ventas", "(ventas potenciales boca a boca + ventas potenciales por publicidad) * fracción con prospectos reales",
          "Unidad/Año", 375, 300, w=25)
    m.aux("tamaño de la venta", "1", "Unidad/persona", 215, 265)
    m.aux("fracción con prospectos reales", "Clientes Potenciales / Tamaño del Mercado", "Dmnl",
          200, 380, w=55)
    m.aux("Tamaño del Mercado", "1e+08", "persona", 110, 470)
    m.aux("ventas potenciales boca a boca", "Clientes * efectividad de ventas por cliente",
          "Unidad/Año", 580, 380, w=55)
    m.aux("efectividad de ventas por cliente", "3", "Unidad/(Año*persona)", 730, 460, w=55)
    m.aux("ventas potenciales por publicidad",
          "gasto en publicidad * efectividad de la publicidad", "Unidad/Año", 380, 440, w=55)
    m.aux("gasto en publicidad", "GAME(c gasto en publicidad)", "dólar/Año", 380, 530)
    m.aux("c gasto en publicidad", "2e+07", "dólar/Año", 380, 610)
    m.aux("efectividad de la publicidad", "0.1", "Unidad/dólar", 580, 520, w=50)
    m.aux("tiempo de obsolescencia", "2", "Año", 560, 35, w=50)
    m.arrow("Clientes Potenciales", "fracción con prospectos reales")
    m.arrow("Tamaño del Mercado", "fracción con prospectos reales")
    m.arrow("Tamaño del Mercado", "Clientes Potenciales", via=(70, 330), init_link=True)
    m.arrow("Clientes Semilla", "Clientes Potenciales", init_link=True)
    m.arrow("Clientes Semilla", "Clientes", init_link=True)
    m.arrow("fracción con prospectos reales", "ventas")
    m.arrow("ventas potenciales boca a boca", "ventas")
    m.arrow("ventas potenciales por publicidad", "ventas")
    m.arrow("ventas", "nuevos clientes")
    m.arrow("tamaño de la venta", "nuevos clientes")
    m.arrow("Clientes", "ventas potenciales boca a boca")
    m.arrow("efectividad de ventas por cliente", "ventas potenciales boca a boca")
    m.arrow("gasto en publicidad", "ventas potenciales por publicidad")
    m.arrow("efectividad de la publicidad", "ventas potenciales por publicidad")
    m.arrow("c gasto en publicidad", "gasto en publicidad")
    m.arrow("Clientes", "clientes que abandonan", via=(500, 130))
    m.arrow("tiempo de obsolescencia", "clientes que abandonan")
    m.loop("R", 500, 300, clockwise=True)
    m.loop("B", 250, 320, clockwise=False)
    if con_controles:
        m.aux("GAME INTERVAL", "0.5", "Año", 760, 35, supplementary=True,
              comment="Intervalo por defecto entre pasos del juego.")
        m.custom_graph("Ventas", "ventas", [("ventas", None, 2)])
        m.view("Simular")
        m.comment("Gasto en publicidad ($/Año)", 160, 60, w=110)
        m.slider("c gasto en publicidad", 0, "2e+08", 500000, 160, 95)
        m.comment("Vida del producto (años)", 160, 150, w=110)
        m.slider("tiempo de obsolescencia", 0.5, 10, 0.1, 160, 185)
        m.shadow("efectividad de ventas por cliente", 160, 250, w=60)
        m.shadow("Tamaño del Mercado", 160, 300, w=60)
        m.graph_obj("Ventas", 560, 190, w=260, h=170)
        m.view("Juego")
        m.comment("Gasto en publicidad ($/Año)", 160, 60, w=110)
        m.slider("gasto en publicidad", 0, "2e+08", 500000, 160, 95)
        m.graph_obj("Ventas", 560, 190, w=260, h=170)
        m.view("Inicio")
        m.comment("Modelo de ventas por boca a boca y publicidad", 400, 60, w=300, size=13)
        m.comment("Estructura: diagrama de niveles y flujos del modelo.", 400, 120, w=300)
        m.comment("Simular: mueva los deslizadores y pulse Simular (o SyntheSim).", 400, 150, w=300)
        m.comment("Juego: pulse Game, fije el gasto en publicidad y avance cada 0.5 años.", 400, 180, w=300)
        m.views = [m.views[-1]] + m.views[:-1]
    return m


# ============================================================================
# Libro J. Martin Garcia, 2.1 - Desarrollo de una epidemia (SIR con vacunacion)
# ============================================================================

def epidemia_jmg():
    m = Model(0, 20, 1, "Mes")
    m.views[0].name = "Epidemia"
    m.stock("Susceptibles", "900", "", 200, 250)
    m.stock("Infectados", "100", "", 520, 250, rng=(50, 150),
            comment="Rango [50,150]: Vensim avisa (warning) cuando Infectados sale de este rango.")
    m.stock("Recuperados", "0", "", 850, 250)
    m.flow("enferman", "Susceptibles*tasa de contagio*Infectados", "", "Susceptibles",
           "Infectados", valve=(360, 250),
           comment="Fórmula de Kermack y McKendrick: beta*S*I.")
    m.flow("curan", "Infectados*tasa de curación", "", "Infectados", "Recuperados",
           valve=(690, 250))
    m.flow("expuestos", "Recuperados*tasa de exposición", "", "Recuperados", "Susceptibles",
           valve=(520, 120), src_corner=(850, 120), dst_corner=(200, 120), label_off=(0, -20),
           comment="Recuperados que pierden la inmunidad y vuelven a ser susceptibles.")
    m.flow("vacunados", "Susceptibles*tensión", "", "Susceptibles", "Recuperados",
           valve=(360, 520), src_corner=(200, 520), dst_corner=(850, 520), label_off=(0, 22))
    m.cloud("nube muertes", 520, 445)
    m.flow("muertes", "Infectados*tasa de mortalidad", "", "Infectados", "nube muertes",
           valve=(520, 360), vertical=True, label_off=(42, 0), w=28)
    m.aux("tasa de contagio", "0.001", "", 330, 175, w=40)
    m.aux("tasa de curación", "0.4", "", 650, 175, w=40)
    m.aux("tasa de exposición", "0.05", "", 720, 55, w=45)
    m.aux("tensión", "(enferman/Susceptibles)*tasa de vacunacion", "", 400, 400, w=25,
          comment="Riesgo percibido: fracción de susceptibles que enferma, por la tasa de vacunación.")
    m.aux("tasa de vacunacion", "0.5", "", 430, 470, w=45)
    m.aux("tasa de mortalidad", "0.1", "", 660, 410, w=45)
    m.aux("Total poblacion", "Infectados+Recuperados+Susceptibles", "", 860, 630, w=45,
          comment="Variable de control: no influye en el resto del modelo.")
    m.shadow("Susceptibles", 660, 590, w=45)
    m.shadow("Infectados", 660, 630, w=40)
    m.shadow("Recuperados", 660, 670, w=45)
    m.arrow("Susceptibles", "enferman", via=(285, 300))
    m.arrow("Infectados", "enferman", via=(445, 305))
    m.arrow("tasa de contagio", "enferman")
    m.arrow("Infectados", "curan", via=(600, 205))
    m.arrow("tasa de curación", "curan")
    m.arrow("Recuperados", "expuestos", via=(720, 165))
    m.arrow("tasa de exposición", "expuestos")
    m.arrow("Infectados", "muertes")
    m.arrow("tasa de mortalidad", "muertes")
    m.arrow("enferman", "tensión")
    m.arrow("Susceptibles", "tensión", via=(270, 390))
    m.arrow("tasa de vacunacion", "tensión")
    m.arrow("Susceptibles", "vacunados", via=(245, 470))
    m.arrow("tensión", "vacunados")
    m.arrow("<Susceptibles>", "Total poblacion")
    m.arrow("<Infectados>", "Total poblacion")
    m.arrow("<Recuperados>", "Total poblacion")
    m.loop("R", 440, 215, clockwise=True, r=15)
    m.loop("B", 280, 210, clockwise=False, r=15)
    m.custom_graph("XY_enferman_muertes", "muertes frente a enferman (XY)",
                   [("muertes", None, 4)], xaxis="enferman", xmin=0, xmax=110, xdiv=11)
    m.custom_graph("muertes_y_enferman", "muertes y enferman",
                   [("muertes", None, 2), ("enferman", None, 2)], scale_groups=[0, 1])
    m.custom_graph("Estados_SIR", "Susceptibles, Infectados y Recuperados",
                   [("Susceptibles", None, 2), ("Infectados", None, 2), ("Recuperados", None, 2),
                    ("Total poblacion", None, 1)])
    return m


MODELOS = {
    "Cap09_difusion1_clientes.mdl": difusion1,
    "Cap09_difusion2_capacidad.mdl": difusion2,
    "Cap09-10_difusion3_capacidad_detallada.mdl": difusion3,
    "Cap12_boca_a_boca_1_estructura.mdl": lambda: boca_a_boca(False),
    "Cap12_boca_a_boca_2_controles.mdl": boca_a_boca,
    "JMG_2.1_desarrollo_epidemia.mdl": epidemia_jmg,
}
