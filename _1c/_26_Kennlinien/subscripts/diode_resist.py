import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def plot_UU(U_e, U_e_err, U_a, U_a_err, G, G_err, b, b_err):

    plt.errorbar(U_e, U_a, xerr=U_e_err, yerr=U_a_err, label='Messwerte', color='blue', fmt='o', capsize=5)
    plt.plot(U_e, U_e * 1/G + b, label=f'Glättungsfaktor: $G = {G} \\pm {G_err} \\frac{{V}}{{V}}$', color='red')
    plt.plot(U_e, U_e * (1/G + 1/G ** 2 * G_err) + b + b_err, label=f'Unsicherheit', color='red', linestyle='dashed')
    plt.plot(U_e, U_e * (1/G - 1/G ** 2 * G_err) + b - b_err, color='red', linestyle='dashed')
    plt.xlabel('$U_e (V)$')
    plt.ylabel('$U_a (V)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.legend()
    plt.grid(True)
    plt.show()

    return


def linreg(U_e, U_a):
    def model(U_e, G, b):
        return U_e * G + b
    popt, pcov = curve_fit(model, xdata=U_e, ydata=U_a)
    G, b = popt
    G_err, b_err = np.sqrt(np.diag(pcov))
    return G, G_err, b, b_err


def diode_resistor(U_e, U_e_err, U_a, U_a_err):
    G, G_err, b, b_err = linreg(U_e[:5], U_a[:5])
    G, G_err = sci_round(1/G, 1/G ** 2 * G_err)
    print(f'Glättungsfaktor: G = {G} ± {G_err} V/V')
    plot_UU(U_e, U_e_err, U_a, U_a_err, G, G_err, b, b_err)
