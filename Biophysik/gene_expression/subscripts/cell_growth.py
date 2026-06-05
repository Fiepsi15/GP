import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def calculate_doubleling_coefficient(t, OD_600):
    def model(x, b):
        return b * x

    x = (t[1:] - t[1])
    y = np.log(OD_600 / OD_600[1])
    y_err = 0.001 / OD_600
    popt, pcov = curve_fit(model, x, y[1:])#, sigma=y_err[1:], absolute_sigma=True)
    b = popt[0]
    delta_b = np.sqrt(np.diag(pcov))[0]

    tau = np.log(2) / b / 60
    delta_tau = tau * delta_b / b /60
    tau_r, delta_tau_r = sci_round(tau, delta_tau)

    T = np.linspace(20, 80, 600)


    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(wspace=0.4, left=0.1, right=0.95, top=0.85)
    fig.suptitle('Wachstum der Hauptkultur', size=17, weight='semibold')

    ax.errorbar(t / 60, OD_600, xerr=1, yerr=0.001, fmt='.', color='blue', capsize=5, label='Messdaten')
    ax.plot(T, np.exp(model(T * 60 - t[1], b)) * OD_600[1], color='red', label=f'Verdopplungszeit: \n$\\tau = {tau_r} \\pm {delta_tau_r}$' + ' $\\mathrm{min}$')
    ax.fill_between(np.linspace(0, 20, 100), np.full(100, 0.05), np.full(100, 0.15), color='red', alpha=0.2, label='Aufwärmung auf $37\\mathrm{ °C}$')
    ax.set_xlabel('$t/\\mathrm{min}$')
    ax.set_ylabel('$OD_{600}$')
    ax.set_title('Exponentielle Wachstumskurve')
    ax.legend()
    ax.grid()

    ax2.set_title('Lineare Regression über linearisierte Kurve')
    ax2.errorbar(t / 60, y, xerr=1, yerr=y_err, fmt='.', color='blue', capsize=5, label='Messdaten (log)')
    ax2.plot(T, model(T * 60 - t[1], b), color='red', label='Lineare Regression')
    ax2.fill_between(np.linspace(0, 20, 100), np.full(100, -0.3), np.full(100, 0.1), color='red', alpha=0.2, label='Aufwärmung auf $37\\mathrm{ °C}$')
    ax2.set_xlabel('$t/\\mathrm{min}$')
    ax2.set_ylabel('$\\log(\\frac{OD_{600}}{OD_{600}^0})$')
    ax2.legend()
    ax2.grid()

    return
