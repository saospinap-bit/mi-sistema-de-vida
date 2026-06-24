# Paso a paso — Cómo usar y entregar el Proyecto PEPI (Acueducto de Tadó)

Guía rápida para que sepas **qué entregar**, **cómo descargarlo** y **cómo defenderlo**.

---

## 1. ¿Qué hay en esta carpeta `Solucion/`?

| Archivo | Para qué sirve | ¿Se entrega? |
|---|---|---|
| **`INFORME_PEPI.docx`** | El informe completo en Word, con formato y árboles incrustados. | ✅ **ESTE es el que entregas** |
| **`MODELO FINANCIERO PEPI.xlsx`** | Excel con TODOS los cálculos (fórmulas vivas) + hoja de diseño de caudal. | ✅ Anexo de cálculos |
| `INFORME_PEPI.md` | El mismo informe en Markdown (se ve con los árboles como imagen en GitHub). | Opcional / referencia |
| `arbol_problemas.png` / `arbol_objetivos.png` | Los árboles como esquema visual. | Soporte |
| `modelo_financiero.py` | El cálculo (diseño de caudal + WACC, TIR, VPN, flujos, social). | Soporte / anexo |
| `resultados_modelo.csv` | Resultados y flujos exportados. | Soporte / anexo |
| `generar_word.py` / `generar_excel.py` / `generar_arboles.py` | Scripts que generan los entregables. | Solo herramientas |
| `COMO SE CALCULO TODO - metodologia.md` | Explica cómo se hizo cada cálculo (para sustentar). | Para estudiar |
| `PASO A PASO - como usar y entregar.md` | Este documento. | Para ti |

> El enunciado original (`PROYECTO PEPI.pdf`) está en la carpeta de arriba (`Proyectos/PEPI/`).

---

## 2. Cómo descargar los entregables

Como trabajas desde el navegador, los archivos están en GitHub. Para descargar cada uno:

1. Entra al archivo en GitHub (p. ej. `Proyectos/PEPI/Solucion/INFORME_PEPI.docx`).
2. Dale al botón **"Download raw file"** (icono de descarga ⬇).
3. Ábrelo en Word / Excel / Google Docs.

---

## 3. Antes de entregar — checklist

- [ ] Cambia **tu nombre, código, materia y profesor** en la portada del Word.
- [ ] Verifica que el informe **no pase de 10 páginas** (límite del enunciado). Si se pasa, puedes mover la tabla de flujos completa al Excel y dejar solo el extracto.
- [ ] Confirma que los **árboles** se vean claros (están incrustados como imagen en el Word).
- [ ] Si tu profesor quiere otros **supuestos** o cifras, cámbialos en `modelo_financiero.py` y vuelve a generar.

---

## 4. Cómo defenderlo (puntos clave de sustentación)

1. **La paradoja de Tadó:** "es uno de los lugares más lluviosos del planeta (~7.900 mm/año) y aun así no tenía agua **potable** continua". Esa es la fuerza del problema.
2. **Diseño de caudal (Res. 0330):** "dimensioné la PTAP en 45 L/s a partir del caudal máximo diario (41,5 L/s), con población de diseño a 25 años, dotación de clima cálido (140 L/hab·día) y coeficientes k1=1,30 y k2=1,60".
3. **El resultado financiero honesto:** "el proyecto **no es rentable solo con tarifas** (VPN negativo), igual que casi todos los acueductos del Pacífico. Por eso se cofinancia con recursos públicos".
4. **La evaluación que decide:** "lo que justifica el proyecto es la **evaluación socioeconómica**: con la tasa social del DNP (9 %) el VPN es +19.626 MM y la relación beneficio/costo es 1,56".
5. **Es un caso real:** "MinVivienda y la cooperación española invirtieron COP 19.971 millones para llevar continuidad 24 h y 98 % de cobertura a Tadó".
6. **Riesgos:** "los más críticos son ambientales (turbiedad, minería ilegal, inundaciones); intervine 10 (5 ambientales) y el riesgo residual baja a Medio/Bajo".

---

## 5. Si quieres cambiar algo

Dime y lo ajusto:
- Cambiar **supuestos** (CAPEX, tarifas, % de aporte público, beneficios sociales).
- Sustituir el desglose del presupuesto por un **APU detallado** si consigues precios reales.
- Incorporar **datos oficiales** de cobertura/IANC del SUI o del Plan Departamental de Aguas del Chocó (harían el informe 100 % real).
- Ajustar el informe a una **rúbrica específica** de tu profesor.
