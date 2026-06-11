import numpy as np
from matplotlib.lines import lineStyles
from scipy import optimize
from scrips.tools import sci_round
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


def calculate_single(n, d, z, g, ax=None, messreihe=0):
    colors = ['blue', 'orange', 'green']
    markers = ['v', '^', '<']

    def model(x, a):
        return a * x

    alpha = np.arctan(d / z)
    y = np.sin(alpha)
    x = n
    popt, pcov = optimize.curve_fit(model, x, y)
    kappa = popt[0]
    delta_kappa = np.sqrt(np.diag(pcov))[0]
    wavelength = kappa / g
    delta_wavelength = delta_kappa / g
    lambda_r, delta_lambda_r = sci_round(wavelength * 1e9, delta_wavelength * 1e9)
    print(f'Wellenlänge (Messung {messreihe}): {lambda_r} ± {delta_lambda_r} nm')

    if ax is None:
        return wavelength, delta_wavelength

    ax.errorbar(x, y, color=colors[messreihe], label=f'Messreihe {messreihe + 1}', fmt=markers[messreihe])
    ax.plot(x, model(x, kappa), color=colors[messreihe], label=f'Fit Messreihe {messreihe + 1}', ls=(2 * messreihe, (2, 4)))

    return wavelength, delta_wavelength


def calculate_wavelength(n, d, z, g):
    fig, ax = plt.subplots()
    wavelength, delta_wavelength = np.zeros_like(d), np.zeros_like(d)
    for i in range(len(d)):
        wavelength[i], delta_wavelength[i] = calculate_single(n, d[i], z[i], g, ax, i)

    lambda_bar = np.mean(wavelength)
    delta_lambda_bar = np.std(wavelength) / np.sqrt(len(wavelength))
    lambda_r, delta_lambda_r = sci_round(lambda_bar * 1e9, delta_lambda_bar * 1e9)
    print(f'Wellenlänge (Mittel): {lambda_r} ± {delta_lambda_r} nm')

    ax.set(xlabel='Ordnung $n$', ylabel='$\\sin(\\alpha)$')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(which='both', direction='in')
    ax.tick_params(axis='x', which='minor', length=0)
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return lambda_bar, delta_lambda_bar
