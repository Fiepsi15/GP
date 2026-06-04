import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def get_sigma(a, da, A_B, dA_B, A_S, dA_S, r, dr):
    b = np.pi * r ** 2
    c = 0.16 * 1000 * A_B * A_S
    delta_sigma = np.sqrt((b / c * da) ** 2
                          + (a * 2 * np.pi * r / c * dr) ** 2
                          + (a * b / c * dA_B / A_B) ** 2
                          + (a * b / c * dA_S / A_S) ** 2)
    return a * b / c, delta_sigma


def stefan_boltzmann_konstante(T, dT, U, dU, A_Blende, dA_Blende, A_Strahler, dA_Strahler, r, dr):
    def model(x, sigma):
        return sigma * x

    x = T ** 4
    delta_x = 4 * T ** 3 * dT
    y = U
    delta_y = dU
    popt, pcov = optimize.curve_fit(model, x, y, sigma=delta_y, absolute_sigma=True)
    a = popt[0]
    delta_a = np.sqrt(np.diag(pcov))[0]
    sigma, delta_sigma = get_sigma(a, delta_a, A_Blende, dA_Blende, A_Strahler, dA_Strahler, r, dr)
    sigma_r, delta_sigma_r = sci_round(sigma, delta_sigma)
    print(f'\nErrechneter wert für die Stefan-Boltzmann-Konstante: {sigma_r} pm {delta_sigma_r}\n---')

    fig, ax = plt.subplots()
    #fig.suptitle('Bestimmung der Stefan-Boltzmann-Konstante')

    ax.errorbar(x, y, xerr=delta_x, yerr=delta_y, fmt='.', label=f'Messreihe', capsize=5, color='blue')
    ax.plot(x, model(x, a), label=f'Lineare Regression ', color='green')
    ax.fill_between(x, model(x, a - delta_a), model(x, a + delta_a), color='green', alpha=0.2)
    ax.set(xlabel='$T^4/\\mathrm{K}^4$', ylabel='$U/\\mathrm{V}$')
    ax.tick_params(axis='both', direction='in', which='both')
    ax.minorticks_on()
    ax.grid()
    ax.legend()
    plt.show()

    return
