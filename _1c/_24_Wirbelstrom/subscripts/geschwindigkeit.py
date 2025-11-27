import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


def geschwindigkeit(t: np.ndarray, a: np.ndarray):
    def model(sina, f):
        return sina * f

    s = 0.1
    s_err = 1e-3
    v = np.zeros(len(t))
    v_err = np.zeros(len(t))
    for i in range(len(t)):
        v[i] = s / np.mean(t[i])
        v_err[i] = np.sqrt((s / (v[i] ** 2) * np.std(t[i])) ** 2 + (s_err / v[i]) ** 2)


    x = np.sin(np.arctan(a / 50))
    popt, pcov = curve_fit(model, xdata=x, ydata=v, sigma=v_err, absolute_sigma=True)
    f = popt[0]
    f_err = np.sqrt(np.diag(pcov))[0]

    plt.errorbar(x, v, yerr=v_err, fmt='o', capsize=5, label='Geschwindigkeiten mit Fehlerbalken')
    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der linearität')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()
