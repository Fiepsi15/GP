import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def temperature_proportionality_order(temperature: np.ndarray, voltage: np.ndarray, current: np.ndarray, temperature_uncertainty: np.ndarray = np.array([0.1]),
                        voltage_uncertainty: np.ndarray = np.array([0.1]), current_uncertainty: np.ndarray = np.array([0.1]),):
    def model(x, a):
        return a * x

    y = np.log(voltage * current / (voltage[0] * current[0]))
    delta_y = np.sqrt((voltage_uncertainty / voltage) ** 2 + (current_uncertainty / current) ** 2)
    x = np.log(temperature / temperature[0])
    delta_x = temperature_uncertainty / temperature
    popt, pcov = optimize.curve_fit(model, x, y, sigma=delta_y, absolute_sigma=True)
    n = popt[0]
    delta_n = np.sqrt(np.diag(pcov))[0]
    n_r, dn_r = sci_round(n, delta_n)
    print(f'\nProportionalität: P zu T ^ ({n_r} pm {dn_r})\n---')

    fig, ax = plt.subplots()

    ax.errorbar(x, y, xerr=delta_x, yerr=delta_y, fmt='.', label=f'Messreihe', capsize=5, color='blue')
    ax.plot(x, model(x, n), label=f'Lineare Regression', color='green')
    ax.fill_between(x, model(x, n - delta_n), model(x, n + delta_n), color='green', alpha=0.2, label='Unsicherheit')
    ax.set(xlabel='$\\log(T/T_0)$', ylabel='$\\log(P/P_0)$')
    ax.tick_params(axis='both', direction='in', which='both')
    ax.minorticks_on()
    ax.grid()
    ax.legend()
    plt.show()

    return n, delta_n
