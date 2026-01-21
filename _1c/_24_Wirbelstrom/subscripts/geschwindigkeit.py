import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.array_to_tex import array_to_tex as a2t


def geschwindigkeit(t: np.ndarray, a: np.ndarray):
    def model(sina, f, b):
        return sina * f + b

    alpha = np.arctan(a / 50) * 360 / (2 * np.pi)
    alpha_err = 1 / (1 + (a / 50) ** 2) * (1 / 50) * 360 / (2 * np.pi) * 0.1

    s = 0.1
    s_err = 1e-3
    v = np.zeros(len(t))
    v_err = np.zeros(len(t))
    for i in range(len(t)):
        v[i] = s / np.mean(t[i])
        v_err[i] = np.sqrt((s / (v[i] ** 2) * np.std(t[i])) ** 2 + (s_err / v[i]) ** 2)

    werte = np.array([alpha, v])
    werte_err = np.array([alpha_err, v_err])
    a2t(werte, werte_err, [['$\\alpha$', '$v_\\infty$'], ['°', '$\\frac{\\mathrm{m}}{\\mathrm{s}}$']],
        'Mittelwerte der Endgeschwindigkeiten bei Variation des Neigungswinkels', 'neigung_geschwindigkeit')

    x = np.sin(np.arctan(a / 50))
    popt, pcov = curve_fit(model, xdata=x, ydata=v, sigma=v_err, absolute_sigma=True)
    f, b = popt
    f_err, b_err = np.sqrt(np.diag(pcov))

    plt.errorbar(x, v, yerr=v_err, fmt='o', capsize=5, label='Geschwindigkeiten mit Fehlerbalken')
    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der linearität')
    plt.plot(x, model(x, f + f_err, b + b_err), linestyle=':', color='grey', label='Unsicherheit des Fits')
    plt.plot(x, model(x, f - f_err, b - b_err), linestyle=':', color='grey')
    plt.xlabel('Sinus des Neigungswinkels sin(α)')
    plt.ylabel('Finalgeschwindigkeit $v$ in $\\frac{\\mathrm{m}}{\\mathrm{s}}$')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return f, f_err
