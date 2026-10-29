"""Resolvedor de Laplace por diferencias finitas + construccion de redes de flujo
con tubos de caudal igual (lineas de corriente integradas por RK4)."""
import numpy as np


def solve(hval, fixed, inactive=None, Kx=1.0, Kz=1.0, iters=60000, tol=1e-9):
    """h[z, x]. Bordes del dominio = sin flujo por reflexion (pad 'edge').
    fixed: mascara booleana de nodos de carga constante.
    inactive: nodos fuera del dominio (se reflejan desde abajo)."""
    h = hval.copy().astype(float)
    if inactive is None:
        inactive = np.zeros_like(fixed)
    h[(~fixed) & (~inactive)] = hval[fixed].mean()
    nz, nx = h.shape
    K_, I_ = np.meshgrid(np.arange(nz), np.arange(nx), indexing='ij')
    parity = (K_ + I_) % 2
    w = 1.90                       # SOR rojo-negro (estable para w < 2)
    cx, cz = Kx / (2 * (Kx + Kz)), Kz / (2 * (Kx + Kz))

    def reflect(a):
        if inactive.any():
            for k in range(1, nz):
                m = inactive[k]
                a[k, m] = a[k - 1, m]

    d = np.inf
    for it in range(iters):
        prev = h.copy()
        for color in (0, 1):
            hp = np.pad(h, 1, mode='edge')
            new = (cx * (hp[1:-1, 2:] + hp[1:-1, :-2])
                   + cz * (hp[2:, 1:-1] + hp[:-2, 1:-1]))
            m = (parity == color) & (~fixed) & (~inactive)
            h[m] = h[m] + w * (new[m] - h[m])
            h[fixed] = hval[fixed]
            reflect(h)
        d = np.max(np.abs(h - prev))
        if not np.isfinite(d):
            raise RuntimeError('divergio')
        if d < tol and it > 200:
            break
    return h, it, d


def velocity(h, dx, dz, Kx=1.0, Kz=1.0):
    """q = -K grad h, por diferencias centradas."""
    dhdx = np.zeros_like(h)
    dhdz = np.zeros_like(h)
    dhdx[:, 1:-1] = (h[:, 2:] - h[:, :-2]) / (2 * dx)
    dhdx[:, 0] = (h[:, 1] - h[:, 0]) / dx
    dhdx[:, -1] = (h[:, -1] - h[:, -2]) / dx
    dhdz[1:-1, :] = (h[2:, :] - h[:-2, :]) / (2 * dz)
    dhdz[0, :] = (h[1, :] - h[0, :]) / dz
    dhdz[-1, :] = (h[-1, :] - h[-2, :]) / dz
    return -Kx * dhdx, -Kz * dhdz


def interp2(F, x, z, xs, zs, dx, dz):
    """Interpolacion bilineal de F[z,x] en (x,z) fisicos."""
    fx = (x - xs) / dx
    fz = (z - zs) / dz
    i = int(np.clip(np.floor(fx), 0, F.shape[1] - 2))
    k = int(np.clip(np.floor(fz), 0, F.shape[0] - 2))
    tx, tz = np.clip(fx - i, 0, 1), np.clip(fz - k, 0, 1)
    return ((1 - tx) * (1 - tz) * F[k, i] + tx * (1 - tz) * F[k, i + 1]
            + (1 - tx) * tz * F[k + 1, i] + tx * tz * F[k + 1, i + 1])


def streamline(qx, qz, x0, z0, xs, zs, dx, dz, xmax, zmax, ds=None, nmax=20000):
    """Integra una linea de corriente por RK4 con paso normalizado."""
    if ds is None:
        ds = min(dx, dz) * 0.45
    pts = [(x0, z0)]
    x, z = x0, z0
    for _ in range(nmax):
        def vel(xx, zz):
            u = interp2(qx, xx, zz, xs, zs, dx, dz)
            v = interp2(qz, xx, zz, xs, zs, dx, dz)
            n = np.hypot(u, v)
            return (0.0, 0.0) if n < 1e-300 else (u / n, v / n)
        u1, v1 = vel(x, z)
        if u1 == 0 and v1 == 0:
            break
        u2, v2 = vel(x + .5 * ds * u1, z + .5 * ds * v1)
        u3, v3 = vel(x + .5 * ds * u2, z + .5 * ds * v2)
        u4, v4 = vel(x + ds * u3, z + ds * v3)
        x += ds * (u1 + 2 * u2 + 2 * u3 + u4) / 6
        z += ds * (v1 + 2 * v2 + 2 * v3 + v4) / 6
        x = np.clip(x, xs, xmax)
        z = np.clip(z, zs, zmax)
        pts.append((x, z))
        if x <= xs + 1e-9 or x >= xmax - 1e-9 or z <= zs + 1e-9 or z >= zmax - 1e-9:
            break
    return np.array(pts)


def equal_flux_starts(flux, coord, n):
    """Dados flujos locales y coordenadas a lo largo de una frontera de entrada,
    devuelve n puntos de arranque en el centro de tubos de caudal igual."""
    f = np.abs(flux)
    c = np.concatenate([[0.0], np.cumsum(f)])
    c /= c[-1]
    cc = np.concatenate([[coord[0]], coord])
    targets = (np.arange(n) + 0.5) / n
    return np.interp(targets, c, cc)


def smooth_path(p, w=15):
    """Media movil sobre una polilinea para quitar el ruido de la malla."""
    import numpy as _np
    if len(p) < w * 2:
        return p
    k = _np.ones(w) / w
    x = _np.convolve(p[:, 0], k, mode='valid')
    z = _np.convolve(p[:, 1], k, mode='valid')
    out = _np.column_stack([x, z])
    return _np.vstack([p[0], out, p[-1]])
