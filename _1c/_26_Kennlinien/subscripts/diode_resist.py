import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def plot_UU(U_e, U_a, G, G_err, b):

    plt.scatter(U_e, U_a, label='Messwerte', color='blue')
    plt.plot(U_e, U_e * G + b, label=f'Glättungsfaktor: $G = {G} \\pm {G_err} \\frac{{V}}{{V}}$', color='red')
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


def diode_resistor(U_e, U_a):

    G, G_err, b, b_err = linreg(U_e[:6], U_a[:6])
    G, G_err = sci_round(G, G_err)
    plot_UU(U_e, U_a, G, G_err, b)
