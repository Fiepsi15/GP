import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from scrips.tools import sci_round


def model(px, pa):
    return pa * px


def get_E_from_factor(a, L, I):
    E = (L[0] ** 3) / (48 * I[0] * a[0])
    delta_E = np.sqrt((L[0] ** 2 / (16 * a[0] * I[0]) * L[1]) ** 2
                      + (E * a[1] / a[0]) ** 2 + (E * I[1] / I[0]) ** 2)
    return E, delta_E


def regression(daten):
    sensor_factor = 2.34  # N/V
    distance = daten[0]
    voltage = daten[1]
    force = voltage * sensor_factor

    x = force[0]
    y = distance[0]
    y_err = distance[1]
    popt, pcov = optimize.curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    a = popt[0], np.sqrt(np.diag(pcov))[0]
    a_r = sci_round(a[0], a[1])

    print(f'\nFit: a = {a_r[0]} +- {a_r[1]}\n')

    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=force[1], yerr=y_err, label='Messwerte', fmt='o', color='blue', capsize=5)
    ax.plot(x, model(x, a[0]), label='Fit: $w = a \\cdot F$', color='red')
    ax.fill_between(x, model(x, np.sum(a)), model(x, a[0] - a[1]), label='Unsicherheit')
    ax.set(xlabel='$F$', ylabel='$d$ (m)')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return a
