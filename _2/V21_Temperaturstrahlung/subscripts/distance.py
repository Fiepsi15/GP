import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def distance_dependence(distance: np.ndarray, voltage: np.ndarray, ax, messreihe, distance_uncertainty: np.ndarray = np.array([0]),
                        voltage_uncertainty: np.ndarray = np.array([0])):
    def model(x, a):
        return a * x

    y = np.log(voltage / voltage[0])
    delta_y = voltage_uncertainty / voltage
    x = np.log(distance / distance[0])
    delta_x = distance_uncertainty / distance
    popt, pcov = optimize.curve_fit(model, x, y, sigma=delta_y, absolute_sigma=True)
    n = popt[0]
    delta_n = np.sqrt(np.diag(pcov))[0]
    n_r, dn_r = sci_round(n, delta_n)
    print(f'Proportionalität nach Messreihe {messreihe}: I zu r ^ ({n_r} pm {dn_r})')

    ax.errorbar(x, y, xerr=delta_x, yerr=delta_y, label=f'Messreihe {messreihe}', capsize=5, color=('green' if messreihe == 1 else 'purple'), fmt=('v' if messreihe == 1 else '^'))
    ax.plot(x, model(x, n), label=f'Lineare Regression {messreihe}', color=('green' if messreihe == 1 else 'purple'))
    ax.fill_between(x, model(x, n - delta_n), model(x, n + delta_n), color=('green' if messreihe == 1 else 'purple'), alpha=0.2)
    ax.set(xlabel='$\\log(r/r_0)$', ylabel='$\\log(U/U_0)$')
    ax.tick_params(axis='both', direction='in', which='both')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return n, delta_n
