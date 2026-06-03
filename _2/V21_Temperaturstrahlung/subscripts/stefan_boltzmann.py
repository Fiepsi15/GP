import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def calculate_x(T, T_0, A_B, A_S, r):
    a = 0.16 * 1000 * A_B * A_S
    t = (T ** 4 - T_0 ** 4)
    return a * t / (np.pi * r ** 2)


def stefan_boltzmann_konstante(T, U, T_0, A_Blende, A_Strahler, r):
    def model(x, sigma):
        return sigma * x

    x = calculate_x(T, T_0, A_Blende, A_Strahler, r)
    y = U
    popt, pcov = optimize.curve_fit(model, x, y)
    sigma = popt[0]
    delta_sigma = np.sqrt(np.diag(pcov))[0]
    sigma_r, delta_sigma_r = sci_round(sigma, delta_sigma)
    print(sigma_r, delta_sigma_r)

    fig, ax = plt.subplots()
    fig.suptitle('Bestimmung der Stefan-Boltzmann-Konstante')

    ax.errorbar(x, y, fmt='.', label=f'Messreihe', capsize=5, color='blue')
    ax.plot(x, model(x, sigma), label=f'Lineare Regression ', color='green')
    ax.fill_between(x, model(x, sigma - delta_sigma), model(x, sigma + delta_sigma), color='green', alpha=0.2)
    ax.set(xlabel='$\\log(r/r_0)$', ylabel='$\\log(U/U_0)$')
    ax.minorticks_on()

    return

