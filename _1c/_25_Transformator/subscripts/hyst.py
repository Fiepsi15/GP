import numpy as np
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def plot_remanence(T, U1, U2):
    def f(x, a, b, c, d, e):
        return e * x ** 4 * d * x ** 3 * a * x ** 2 + b * x + c

    U = (U1 + U2) / 2
    popt, pcov = curve_fit(f, T[:-1], U[:-1])
    x0 = fsolve(f, 0, args=tuple(popt))
    print(x0)

    plt.errorbar(T, U, label='Messdaten', fmt='o', color='blue', capsize=5)
    plt.plot(T , f(T, *popt), label='Fit 4. Grades zur Bestimmung der Nullstelle', color='red')
    plt.legend()
    plt.ylabel('Remanenzspannung $U_r (\\mathrm{V})$')
    plt.xlabel('$T (\\mathrm{°C})$')
    plt.grid()
    plt.show()

    return
