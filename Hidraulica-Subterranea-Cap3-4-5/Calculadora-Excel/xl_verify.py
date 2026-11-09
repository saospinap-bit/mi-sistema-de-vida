"""Calcula el libro con el motor `formulas` y compara contra los resultados de la guía."""
import sys, time, math, io, contextlib
sys.path.insert(0, '/projects/sandbox/.calc')
with contextlib.redirect_stdout(io.StringIO()):
    import xl_build                                    # reconstruye y guarda
from xl_part1 import SH
import formulas

PATH = xl_build.OUT
t0 = time.time()
xl = formulas.ExcelModel().loads(PATH).finish()
sol = xl.calculate()
print(f'calculado en {time.time() - t0:.0f} s, {len(sol)} celdas')

FN = PATH.split('/')[-1].upper()
idx = {}
for k, v in sol.items():
    ku = k.upper()
    if '!' in ku and ku.startswith("'["):
        sheet = ku.split(']')[1].split("'")[0]
        cell = ku.split('!')[1].replace('$', '')
        idx[(sheet, cell)] = v


def val(sheet, ref):
    key = (sheet.upper(), ref.replace('$', '').upper())
    x = idx.get(key)
    if x is None:
        return None
    try:
        x = x.value[0, 0]
    except Exception:
        pass
    return x


def get(sheet, key):
    return val(sheet, SH[sheet].v[key])


FAIL = []


def check(sheet, key, expected, tol=0.01, ref=None):
    x = val(sheet, ref) if ref else get(sheet, key)
    label = f'{sheet}.{key or ref}'
    if isinstance(expected, str):
        ok = isinstance(x, str) and expected in x
    else:
        try:
            xf = float(x)
            ok = (abs(xf - expected) <= tol * abs(expected)) if expected != 0 else abs(xf) < tol
        except Exception:
            ok = False
    print(f'  {"OK " if ok else "XX "} {label:<34} obtenido={x!s:<28.28} esperado={expected}')
    if not ok:
        FAIL.append(label)


print('--- Unidades / Papel_log / Darcy')
check('Unidades', 'kd', 0.1033, 0.01)
check('Papel_log', 'ds', 0.82)
check('Papel_log', 't0', 3.71)
check('Papel_log', 'T', 268.2)
check('Darcy', 'q', 1.9e-8)
check('Darcy', 'v', 1.9e-7)
check('Darcy', 'hpp', 168)
check('Darcy', 'az', 225)
d = SH['Darcy']
print('    tabla 3.7:', [val('Darcy', f'{c}{r}') for r in range(1, 60) for c in 'KLM'
                       if isinstance(val('Darcy', f'K{r}'), (int, float)) and c == 'K'][:4])
print('--- Capas / Almacenamiento / Redes / Esfuerzos')
check('Capas', 'Kh', 3.7e-7)
check('Capas', 'Kv', 2.7027e-8)
check('Almacenamiento', 'bp2', 3.657e-10)
check('Almacenamiento', 'Sinc', 8.4758e-5)
check('Almacenamiento', 'V3', 300)
check('Almacenamiento', 'S4', 0.275)
check('Almacenamiento', 'nu', 625000)
check('Almacenamiento', 'dhb', -0.04587)
check('Redes_flujo', 'Qm', 5e-4 * 20 * 5 / 14)
check('Redes_flujo', 'Keq', 6.3246e-5)
check('Esfuerzos', 'u', 4368)
check('Esfuerzos', 'FS0', 1.4309)
check('Esfuerzos', 'FS', 1.1442)
check('Esfuerzos', 'dcw', 30.064)
check('Esfuerzos', 'dcd', 15.056)
print('--- Pruebas de bombeo')
check('Cooper_Jacob', 'n', 5, 0.001)
check('Cooper_Jacob', 'ds', 0.9121)
check('Cooper_Jacob', 'T', 301.4)
check('Cooper_Jacob', 'S', 9.80e-4, 0.02)
check('Cooper_Jacob', 'umax', 0.0083, 0.05)
check('Cooper_Jacob', 'mT', 301.9, 0.01)
check('Theis', 'Ta', 13677)
check('Theis', 'rmse', 0.0, 0.03)
check('Dist_abatimiento', 'T', 300.5)
check('Dist_abatimiento', 'S', 9.9e-4, 0.02)
check('Recuperacion', 'T', 300.1)
check('Thiem_Dupuit', 'T', 396.0)
check('Thiem_Dupuit', 'Kl', 8.89)
print('--- Cálculos en el acuífero / superposición')
check('Calc_acuifero', 'sT', 2.477)
check('Calc_acuifero', 'sw', 8.20)
check('Calc_acuifero', 'to', 2.26)
check('Calc_acuifero', 'Qmx', 1346)
check('Calc_acuifero', 'qv', 0.0477)
sp = SH['Superposicion']
tot = [val('Superposicion', f'C{r}') for r in range(1, 60)]
check('Superposicion', 'sr', 7.774)
mapa = val('Superposicion', 'O22')
print(f'    celda del mapa O22 = {mapa}')
print('--- Dupuit / Costa / Canal')
check('Dupuit_recarga', 'q0_A', -2.4586)
check('Dupuit_recarga', 'qL_A', -2.4914)
check('Dupuit_recarga', 'd_A', -14966.6)
check('Dupuit_recarga', 'd_B', 45299.7)
check('Dupuit_recarga', 'hmax_B', 'no existe')
check('Costa', 'Qmu', 7.005e-3)
check('Costa', 'xt', 2061.3)
check('Costa', 'C', 161.73)
check('Costa', 'xT_A', 924.4, 0.001)
check('Costa', 'xT_B', 885.2, 0.001)
check('Costa', 'Hx_A', 32.877, 0.001)
check('Costa', 'Hx_B', 33.285, 0.001)
check('Costa', 'Ht', 0.750, 0.002)
check('Canal', 'nu', 125.25)
check(None or 'Canal', None, 11.86, 0.002, ref='K9')
check('Canal', None, 10.67, 0.002, ref='K10')
check('Canal', None, 1.254e-2, 0.005, ref='M7')

# --- textos de verificación: ninguno debe salir con ✘ en los ejemplos cargados
from xl_lib import CHECKS
malos = []
for wsx, r, c0, c1 in CHECKS:
    for col in sorted({c0, c1}):
        x = val(wsx.title, f'{col}{r}')
        if isinstance(x, str) and x.startswith('✘'):
            malos.append((wsx.title, f'{col}{r}', x))
print('--- verificaciones con ✘ en los ejemplos:', len(malos))
for m in malos:
    print('   ', m)
# --- errores en cualquier celda (excepto #N/A buscados a propósito)
errs = {}
for (sh_, cell), v in idx.items():
    try:
        x = v.value[0, 0]
    except Exception:
        x = v
    s = str(x)
    if s.startswith('#') and s not in ('#N/A',) and sh_ != 'AUX_MAPA':
        errs.setdefault((sh_, s), []).append(cell)
print('--- celdas con error (no #N/A):', sum(len(x) for x in errs.values()))
for k, cells in list(errs.items())[:20]:
    print('   ', k, cells[:8])
print('\nRESULTADO:', 'TODO OK' if not FAIL else f'{len(FAIL)} FALLAS: {FAIL}')
