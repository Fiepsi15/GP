import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize


def calculate_n(delta_min, epsilon=60):
    epsilon = np.deg2rad(epsilon)
    delta_min = np.deg2rad(delta_min)

    n = np.sin((delta_min[0] + epsilon)/2) / np.sin(epsilon / 2)
    delta_n = np.abs(np.cos((delta_min[0] + epsilon)/2) / np.sin(epsilon / 2) * 1/2 * delta_min[1])

    return n, delta_n

def get_n_of_lambda(wavelength, delta_min, epsilon = 60):
    def model(x, a, b):
        return a + b / x ** 2

    n = calculate_n(delta_min, epsilon)
    popt, pcov = optimize.curve_fit(model, wavelength, n[0], sigma=n[1], absolute_sigma=True)
    a, b = zip(popt, np.sqrt(np.diag(pcov)))

    def n_of(wavelength):
        n = a[0] + b[0] / wavelength ** 2
        delta_n = np.sqrt((a[1] ** 2) + (b[1] / wavelength ** 2) ** 2)
        return n, delta_n


    x = np.linspace(wavelength[0], wavelength[-1], 100)
    fig, ax = plt.subplots()
    ax.errorbar(wavelength, delta_min[0], yerr=delta_min[1], label='delta_min', color='blue', fmt='o', capsize=2)
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    fig, ax = plt.subplots()
    ax.errorbar(wavelength, n[0], yerr=n[1], label='Messwerte $n_{\\lambda}$', color='blue', fmt='o', capsize=2)
    ax.plot(x, n_of(x)[0], label='Ausgleichskurve $n(\\lambda)$', color='red')
    ax.fill_between(x, n_of(x)[0] + n_of(x)[1], n_of(x)[0] - n_of(x)[1], label='Unsicherheit', color='red', alpha=0.2)
    ax.set(xlabel='Wellenlänge $\\lambda\\,[\\mathrm{nm}]$', ylabel='Brechungsindex $n\\,(\\lambda)$', title='Brechungsindex in Abhängigkeit der Wellenlänge')
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return n_of
