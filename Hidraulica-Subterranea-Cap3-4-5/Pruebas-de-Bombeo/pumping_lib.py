import numpy as np

def W(u):
    """Funcion de pozo de Theis = E1(u), por serie o continued fraction."""
    u = np.asarray(u, dtype=float)
    out = np.empty_like(u)
    small = u < 1.0
    # serie para u pequeno
    us = u[small]
    if us.size:
        s = -0.5772156649015329 - np.log(us)
        term = np.ones_like(us)
        for n in range(1, 40):
            term = term * (-us) / n
            s = s - term / n
        out[small] = s
    # fraccion continua para u grande
    ub = u[~small]
    if ub.size:
        b = ub + 1.0
        c = 1e300
        d = 1.0 / b
        h = d
        for i in range(1, 100):
            a = -i * i
            b = b + 2.0
            d = 1.0 / (a * d + b)
            c = b + a / c
            de = c * d
            h = h * de
            if np.all(np.abs(de - 1.0) < 1e-12):
                break
        out[~small] = h * np.exp(-ub)
    return out


