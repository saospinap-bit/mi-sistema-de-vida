# Paso a paso — Cómo usar y entregar el Proyecto PEPI

Guía rápida para que sepas **qué entregar**, **cómo descargarlo** y **cómo defenderlo**.

---

## 1. ¿Qué hay en esta carpeta `Solucion/`?

| Archivo | Para qué sirve | ¿Se entrega? |
|---|---|---|
| **`INFORME_PEPI.docx`** | El informe completo en Word, con formato. | ✅ **ESTE es el que entregas** |
| `INFORME_PEPI.md` | El mismo informe en Markdown (se ve con los árboles como diagramas en GitHub). | Opcional / referencia |
| `modelo_financiero.py` | El cálculo financiero (WACC, TIR, VPN, flujos). | Soporte / anexo |
| `resultados_modelo.csv` | Resultados y tabla de flujos exportados. | Soporte / anexo |
| `generar_word.py` | Script que arma el Word automáticamente. | Solo herramienta |
| `COMO SE CALCULO TODO - metodologia.md` | Explica cómo se hizo cada cálculo (para sustentar). | Para estudiar |
| `PASO A PASO - como usar y entregar.md` | Este documento. | Para ti |

> El enunciado original (`PROYECTO PEPI.pdf`) está en la carpeta de arriba (`Proyectos/PEPI/`).

---

## 2. Cómo descargar el Word para entregarlo

Como trabajas desde el navegador, el archivo está en GitHub. Para descargarlo:

1. Entra al archivo en GitHub: `Proyectos/PEPI/Solucion/INFORME_PEPI.docx`
2. Dale al botón **"Download raw file"** (icono de descarga ⬇, arriba a la derecha del archivo).
3. Se descarga el `.docx` a tu computador. Ábrelo en Word/Google Docs.

---

## 3. Antes de entregar — checklist

- [ ] Cambia los datos de **tu nombre, código, materia y profesor** en la portada.
- [ ] Verifica que el informe **no pase de 10 páginas** (es el límite del enunciado).
- [ ] Revisa que los **árboles** (problemas y objetivos) se vean claros. En el Word están como listas jerárquicas; si tu profesor exige una **gráfica tipo diagrama**, dímelo y te genero una imagen.
- [ ] Confirma que los **números financieros** son los que quieres (si no, se cambian en `modelo_financiero.py`).

---

## 4. Cómo defenderlo (puntos clave de sustentación)

1. **Resumen ejecutivo:** sé capaz de decir en 30 segundos qué es el proyecto, cuánto cuesta y por qué es viable.
2. **Árbol de problemas → objetivos:** explica que el de objetivos es el "espejo positivo" del de problemas.
3. **MML:** las 4 filas van de lo general (Fin) a lo concreto (Actividades); las 4 columnas dicen qué se hace, cómo se mide, dónde se verifica y qué supuestos asume.
4. **WACC:** "es el costo promedio de la plata, pesando deuda y equity; la deuda cuesta menos por el escudo fiscal".
5. **TIR vs. tasa de descuento:** "el proyecto es viable porque su TIR (18,13 %) supera el WACC (11,07 %)".
6. **Riesgos:** "calificamos 20 con P×I; intervenimos los 10 críticos (5 ambientales) y el riesgo residual baja".

---

## 5. Si quieres cambiar algo

Dime y lo ajusto:
- Cambiar el **tema del proyecto** (si no es de acueducto).
- Cambiar **supuestos financieros** (montos, tasas, plazos).
- Generar los **árboles como imágenes/diagramas** para pegarlos en el Word.
- Ajustar el informe a una **rúbrica específica** de tu profesor.
