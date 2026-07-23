import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from scrips.tools import sci_round
from scipy import optimize


def camera(a, wellenlaenge, z, delta_lambda, delta_z):
    b = z * a * wellenlaenge
    delta_b = a * np.sqrt((z * delta_lambda) ** 2
                          + (wellenlaenge * delta_z) ** 2)
    b_r, db_r = sci_round(b * 1e6, delta_b * 1e6)
    print(f'\nSpaltbreite (cam): {b_r} ± {db_r} µm\n')

    return b, delta_b


def wall_single(n, lamb, z, d, delta_lamb, delta_z, delta_d, ax=None, messreihe=0):
    colors = ['blue', 'green', 'red']

    def model(x, a):
        return a * x

    x = n
    y = d / z
    delta_y = np.sqrt((delta_d / z) ** 2
                      + (y * delta_z / z) ** 2)
    popt, pcov = optimize.curve_fit(model, x, y, sigma=delta_y, absolute_sigma=True)
    kappa = popt[0]
    d_kappa = np.sqrt(np.diag(pcov))[0]
    b = lamb / kappa
    d_b = np.sqrt((delta_lamb / kappa) ** 2
                  + (b * d_kappa / kappa) ** 2)
    b_r, db_r = sci_round(b * 1e6, d_b * 1e6)
    print(f'Spaltbreite (wand): {b_r} ± {db_r} µm')

    if ax is None:
        return b, d_b

    ax.errorbar(x, y, yerr=delta_y, color=colors[messreihe], label=f'Messreihe {messreihe + 1}', fmt='o', capsize=5)
    ax.plot(x, model(x, kappa), color=colors[messreihe], label=f'Lineare Regression',
            ls='--')
    ax.fill_between(x, model(x, kappa - d_kappa), model(x, kappa + d_kappa), color=colors[messreihe], alpha=0.2, label=f'Unsicherheit\n Regression')

    return b, d_b


def wall(n, lamb, z, d, delta_lamb, delta_z, delta_d):
    fig, ax = plt.subplots(1,3, figsize=(8, 4), sharey=True)
    ax[0].set(ylabel='$d\\,/\\,z_0$')
    fig.subplots_adjust(wspace=0.05, left=0.1, right=0.95)
    b, delta_b = np.zeros_like(z), np.zeros_like(z)
    for i in range(len(d)):
        b[i], delta_b[i] = wall_single(n, lamb, z[i], d[i], delta_lamb, delta_z, delta_d, ax[i], i)
        ax[i].set(xlabel='Ordnung $n$')
        ax[i].xaxis.set_major_locator(MaxNLocator(integer=True))
        ax[i].tick_params(which='both', direction='in')
        ax[i].tick_params(axis='x', which='minor', length=0)
        ax[i].minorticks_on()
        ax[i].legend()
        ax[i].grid()

    b_bar = np.mean(b)
    #delta_b_bar = np.std(b) / np.sqrt(len(b))
    delta_b_bar = np.sqrt(np.sum(delta_b ** 2)) / len(delta_b)
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

