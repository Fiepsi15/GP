import numpy as np
from scipy import optimize
from scrips.tools import sci_round
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


def calculate_single(n, d, z, g, delta_d, delta_z, ax=None, messreihe=0):
    colors = ['blue', 'green', 'red']

    def model(x, a):
        return a * x

    alpha = np.arctan(d / z)
    y = np.sin(alpha)
    delta_y = np.sqrt((np.cos(alpha) * 1 / (1 + (d/z) ** 2) / z * delta_d) ** 2
                      + (np.cos(alpha) * 1 / (1 + (d/z) ** 2) * d / z ** 2 * delta_z) ** 2)
    x = n
    popt, pcov = optimize.curve_fit(model, x, y, sigma=delta_y, absolute_sigma=True)
    kappa = popt[0]
    delta_kappa = np.sqrt(np.diag(pcov))[0]
    wavelength = kappa / g
    delta_wavelength = delta_kappa / g
    lambda_r, delta_lambda_r = sci_round(wavelength * 1e9, delta_wavelength * 1e9)
    print(f'Wellenlänge (Messung {messreihe}): {lambda_r} ± {delta_lambda_r} nm')

    if ax is None:
        return wavelength, delta_wavelength

    ax.errorbar(x, y, yerr=delta_y, color=colors[messreihe], label=f'Messreihe {messreihe + 1}', fmt='o', capsize=5)
    ax.plot(x, model(x, kappa), color=colors[messreihe], label=f'Lineare Regression',
            ls='--')
    ax.fill_between(x, model(x, kappa - delta_kappa), model(x, kappa + delta_kappa), color=colors[messreihe], alpha=0.2, label=f'Unsicherheit\n Regression')

    return wavelength, delta_wavelength


def calculate_wavelength(n, d, z, g, delta_d, delta_z):
    fig, ax = plt.subplots(1,3, figsize=(8, 4), sharey=True)
    ax[0].set(ylabel='$\\sin(\\alpha)$')
    fig.subplots_adjust(wspace=0.05, left=0.1, right=0.95)
    wavelength, delta_wavelength = np.zeros_like(z), np.zeros_like(z)
    for i in range(len(d)):
        wavelength[i], delta_wavelength[i] = calculate_single(n, d[i], z[i], g, delta_d[i], delta_z[i], ax[i], i)
        ax[i].set(xlabel='Ordnung $n$')
        ax[i].xaxis.set_major_locator(MaxNLocator(integer=True))
        ax[i].tick_params(which='both', direction='in')
        ax[i].tick_params(axis='x', which='minor', length=0)
        ax[i].minorticks_on()
        ax[i].legend()
        ax[i].grid()

    lambda_bar = np.mean(wavelength)
    #delta_lambda_bar = np.std(wavelength) / np.sqrt(len(wavelength))
    delta_lambda_bar = np.sqrt(np.sum(delta_wavelength ** 2)) / len(delta_wavelength)
    lambda_r, delta_lambda_r = sci_round(lambda_bar * 1e9, delta_lambda_bar * 1e9)
    print(f'Wellenlänge (Mittel): {lambda_r} ± {delta_lambda_r} nm')


    return lambda_bar, delta_lambda_bar


def visible_spectrum(z, g, d1, d2, delta_z, delta_d1, delta_d2):
    alpha1 = np.arctan(d1 / z)
    alpha2 = np.arctan(d2 / z)
    delta_l1 = np.sqrt((np.cos(alpha1) * 1 / (1 + (d1/z) ** 2) / z * delta_d1) ** 2
                      + (np.cos(alpha1) * 1 / (1 + (d1/z) ** 2) * d1 / z ** 2 * delta_z) ** 2) / g
    delta_l2 = np.sqrt((np.cos(alpha2) * 1 / (1 + (d2/z) ** 2) / z * delta_d2) ** 2
                       + (np.cos(alpha2) * 1 / (1 + (d2/z) ** 2) * d2 / z ** 2 * delta_z) ** 2) / g
    spectrum = np.array([np.sin(alpha1) / g, np.sin(alpha2) / g])

    l1, delta_l1 = sci_round(spectrum[0] * 1e9, delta_l1 * 1e9)
    l2, delta_l2 = sci_round(spectrum[1] * 1e9, delta_l2 * 1e9)

    print(f'Sichtbares Lichtspektrum: ({l1} ± {delta_l1}) nm bis ({l2} ± {delta_l2}) nm')
