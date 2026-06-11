import numpy as np
from scrips.tools import sci_round
from scipy import optimize


def camera(a, wellenlaenge, z, delta_lambda, delta_z):
    b = z * a * wellenlaenge
    delta_b = a * np.sqrt((z * delta_lambda) ** 2
                          + (wellenlaenge * delta_z) ** 2)
    b_r, db_r = sci_round(b * 1e6, delta_b * 1e6)
    print(f'\nSpaltbreite (cam): {b_r} ± {db_r} µm\n')

    return b, delta_b


def wall_single(n, lamb, z, d):
    def model(x, a):
        return a * x

    x = n
    y = d
    popt, pcov = optimize.curve_fit(model, x, y)
    kappa = popt[0]
    d_kappa = np.sqrt(np.diag(pcov))[0]
    b = lamb * z / kappa
    d_b = b * d_kappa / kappa
    b_r, db_r = sci_round(b * 1e6, d_b * 1e6)
    print(f'Spaltbreite (wall): {b_r} ± {db_r} µm')

    return b, d_b


def wall(n, lamb, z, d):
    b, delta_b = np.zeros_like(d), np.zeros_like(d)
    for i in range(len(d)):
        b[i], delta_b[i] = wall_single(n, lamb, z[i], d[i])

    b_bar = np.mean(b)
    delta_b_bar = np.std(b) / np.sqrt(len(b))
    b_r, delta_b_r = sci_round(b_bar * 1e6, delta_b_bar * 1e6)
    print(f'Spaltbreite (Mittel): {b_r} ± {delta_b_r} µm')

    return b_bar, delta_b_bar


def lens(b, g, B, delta_b, delta_g, delta_B):
    G = g * B / b
    delta_G = np.sqrt((B * delta_g / b) ** 2
                      + (g * delta_B / b) ** 2
                      + (g * B / b ** 2 * delta_b) ** 2)
    G_r, delta_G_r = sci_round(G * 1e6, delta_G * 1e6)

    print(f'\nSpaltbreite (Linse): {G_r} ± {delta_G_r} µm')

    return G


def visible_spectrum(z, g, d1, d2):
    alpha1 = np.arctan(d1 / z)
    alpha2 = np.arctan(d2 / z)

    spectrum = np.array([np.sin(alpha1) / g, np.sin(alpha2) / g])
    print(spectrum * 1e9)
