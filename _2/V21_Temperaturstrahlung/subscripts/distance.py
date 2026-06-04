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

    ax.errorbar(x, y, xerr=delta_x, yerr=delta_y, fmt='.', label=f'Messreihe {messreihe}', capsize=5, color=('blue' if messreihe == 1 else 'red'))
    ax.plot(x, model(x, n), label=f'Lineare Regression {messreihe}', color=('green' if messreihe == 1 else 'orange'))
    ax.fill_between(x, model(x, n - delta_n), model(x, n + delta_n), color='green', alpha=0.2)
    ax.set(xlabel='$\\log(r/r_0)$', ylabel='$\\log(U/U_0)$')
    ax.minorticks_on()

    return n, delta_n
