# 🏗️ Guía: Diseño de Viguetas, Vigas y Riostras (NSR-10 / ACI 318)

> Material de estudio para entender el método y aplicarlo a TU proyecto.
> Acompaña a la herramienta `Herramienta-Diseno-Viguetas-Vigas.xlsx`.
> Unidades SI: f'c, fy en MPa · dimensiones en mm · Mu/Tu en kN·m · Vu en kN · As en mm².

---

## 0) De dónde salen los datos
Mu (momento), Vu (cortante) y Tu (torsión) **se leen de tu modelo** (ETABS/SAP) ya con las combinaciones de carga mayoradas (1.2D+1.6L, combinaciones sísmicas, etc.). Tú tomas los **valores máximos** de cada elemento y los metes en la herramienta.

---

## 1) DISEÑO DE VIGUETAS

Una vigueta trabaja como **viga T**: el nervio (ancho `bw`) más la loseta superior (ancho efectivo `bf`) que actúa como ala a compresión.

### 1.1 Flexión positiva (acero inferior) — comportamiento de viga T
El momento positivo comprime la **loseta** (arriba), así que el ancho a compresión es `bf` (grande).

**Pasos:**
1. `Rn = Mu⁺ / (φ·bf·d²)` con φ = 0.90
2. `ρ = (0.85·f'c/fy)·(1 − √(1 − 2·Rn/(0.85·f'c)))`
3. `As⁺ = ρ·bf·d`
4. Verifica que el bloque de compresión cae dentro de la loseta: `a = As·fy/(0.85·f'c·bf)`. Si **a ≤ hf** → la fórmula rectangular es válida (caso casi siempre en viguetas).
5. `As,min = máx(1.4/fy ; 0.25·√f'c/fy)·bw·d`
6. **Adopta** `As⁺ = máx(As⁺, As,min)`

### 1.2 Flexión negativa (acero superior) — sección rectangular
El momento negativo (sobre apoyos) comprime **abajo**, donde solo está el nervio → ancho `bw` (pequeño). Mismo procedimiento pero con `bw`.
- Verifica **ductilidad**: `ρ ≤ ρmax = 0.85·β1·(f'c/fy)·(3/8)` (deformación del acero ≥ 0.005).
- `β1 = 0.85` para f'c ≤ 28 MPa.

### 1.3 Cortante
- `Vc = 0.17·√f'c·bw·d` (en N; divide /1000 → kN)
- **Viguetas:** la NSR-10 permite `1.1·Vc` (sistemas de viguetas, C.8.13).
- Si `Vu ≤ φ·(1.1·Vc)` → el concreto resiste, solo estribos de **montaje**.
- Si no: `Vs = Vu/φ − 1.1·Vc` ; separación `s = Av·fyt·d/Vs` ; con `s ≤ d/2 ≤ 600 mm`.

### 1.4 Torsión
- Umbral: `φ·Tth = φ·0.083·√f'c·(Acp²/pcp)`, con `Acp = bw·h`, `pcp = 2(bw+h)`.
- Si `Tu < φ·Tth` → **torsión despreciable** (lo normal en viguetas).

### 1.5 Deflexiones a largo plazo (NSR-10 C.9.5)
- Altura mínima `hmin = L/factor` (factor: 16 simple, 18.5 un extremo continuo, 21 ambos continuos, 8 voladizo).
- Si `h ≥ hmin` → **no es obligatorio** calcular deflexiones.
- Si hay que calcular: deflexión diferida = `λΔ · δ_inmediata_sostenida`, con `λΔ = ξ/(1+50·ρ')`, ξ=2.0 a 5 años.

### 1.6 Despiece (lo que va al plano)
- **Bastones** (refuerzo superior en apoyos) se cortan donde el momento negativo se reduce → punto teórico de corte + `ld` (longitud de desarrollo) o `12·db` o `d`, lo que mande.
- **Ganchos estándar** a 90° o 180° donde no haya longitud recta suficiente.
- `ld` (tracción, simplificada): `ld = (fy·ψt·ψe)/(1.1·λ·√f'c·(cb+Ktr)/db)·db` — para barras inferiores ψt=1.0.
- Estribos de montaje en viguetas: típicamente #2 cada ~250–300 mm solo para sostener el armado.

---

## ✍️ EJEMPLO RESUELTO (vigueta tipo)
**Datos:** f'c=21 MPa, fy=fyt=420 MPa, bw=100, h=400, d=360, hf=50, bf=850 mm, L=5000 mm (un extremo continuo), Mu⁺=25, Mu⁻=30 kN·m, Vu=35 kN, Tu=0.3 kN·m, estribo #2 2 ramas (Av=64 mm²).

| Verificación | Resultado |
|---|---|
| **Flexión +** | Rn=0.252 MPa, ρ=0.00060, **As⁺=185 mm²**, a=5.1 mm ≤ hf → rectangular OK (As,min=120) |
| **Flexión −** | Rn=2.572 MPa, ρ=0.00664 ≤ ρmax=0.0136 (dúctil), **As⁻=239 mm²** |
| **Cortante** | Vc=28.0, 1.1Vc=30.9, φVc=23.1 kN; Vu=35 > φVc → **estribos #2 @ 180 mm** (s_max=d/2) |
| **Torsión** | φTth=0.456 kN·m; Tu=0.3 < 0.456 → **despreciable** |
| **Deflexión** | hmin=270 mm; h=400 ≥ 270 → **no es obligatorio calcular** |

> Lectura: As⁺≈185 mm² ≈ 1 barra #5 (200 mm²) abajo; As⁻≈239 mm² ≈ 2 barras #4 (258 mm²) arriba sobre el apoyo. (Verifica recubrimiento y separaciones).

---

## 2) DISEÑO DE VIGAS (rectangulares)
Igual que viguetas pero:
- Sección **rectangular** (sin ala): flexión + y − usan el ancho `b`.
- **Casi siempre requieren estribos.** Lógica de cortante:
  - `Vu ≤ φVc/2` → sin estribos.
  - `φVc/2 < Vu ≤ φVc` → estribos **mínimos**.
  - `Vu > φVc` → diseñar `Vs = Vu/φ − Vc` y separación.
  - `s_max = d/2 ≤ 600 mm` si `Vs ≤ 0.33√f'c·b·d`; si no, `d/4 ≤ 300 mm`.
  - `Av,min` por `máx(0.062√f'c·b/fyt ; 0.35·b/fyt)`.
- **Torsión** (vigas de borde): si `Tu ≥ φTth`, se diseña refuerzo:
  - `Aoh=(b−2cc)(h−2cc)`, `ph=2[(b−2cc)+(h−2cc)]`, `Ao=0.85·Aoh`.
  - Estribos por torsión: `At/s = Tu/(φ·2·Ao·fyt·cotθ)` (θ=45°, cotθ=1).
  - Acero longitudinal por torsión: `Al = (At/s)·ph·(fyt/fy)`, repartido en el perímetro.
  - **Estribo total** por rama = (cortante: ½·Av/s) + (torsión: At/s).
- **Diseño por capacidad** (si el sistema es DMO/DES): el cortante de diseño sale de los momentos probables `Mpr` en los extremos, no solo del análisis.
- **Longitudes de desarrollo y empalmes:** empalmes por traslapo Clase B = `1.3·ld`; ubícalos donde el esfuerzo sea bajo (centro de luz para acero negativo, apoyos para positivo).

---

## 3) DISEÑO DE RIOSTRAS
Elementos transversales que arriostran las viguetas. Diseño simple:
- **Flexión:** mismo procedimiento (rectangular).
- **Cortante:** `Vc` y estribos si `Vu > φVc`.
- Despiece sencillo (2 barras arriba, 2 abajo + estribos típicos).

---

## 4) La herramienta de Excel (`Herramienta-Diseno-Viguetas-Vigas.xlsx`)
3 hojas: **Viguetas**, **Vigas**, **Riostras**.
- Llena solo las **celdas azules** (datos de entrada).
- Todo lo demás se calcula con fórmulas: As, estribos, verificaciones de torsión y deflexión.
- Los resultados clave salen resaltados (verde = acero adoptado, amarillo = resultado/decisión).

> Esta es tu **herramienta propia** que exige el proyecto. Entiéndela: en la sustentación pueden pedirte explicar cualquier celda.
