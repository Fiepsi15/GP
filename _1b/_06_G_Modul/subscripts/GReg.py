import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def g_mod_regression(T: np.ndarray, dT: np.ndarray, J: np.ndarray, dJ: np.ndarray, length: float = 1.0, dl=0.1,
                     radius: float = 1.0, dr=0.1) -> tuple[float, float]:
    """
    Perform a regression analysis for the G-Modul from the torsion oscillation of a given length of Wire.
    :param length: Length of the wire.
    :param dl: Uncertainty in length.
    :param radius: Radius of the wire.
    :param dr: Uncertainty in radius.
    :param T: Periods of the torsion oscillation.
    :param dT: Uncertainty in the period.
    :param J: Moments of inertia.
    :param dJ: Uncertainty in the moments of inertia.
    :return: G-Modulus and its uncertainty.
    """

    def model(x, c):
        return c * x

    def G(c, dc, length, dl, radius, dr) -> tuple[float, float]:
        return (8 * np.pi * length) / (c * radius ** 4), np.sqrt(((8 * np.pi) / (c * radius ** 4) * dl) ** 2
                                                                 + ((8 * np.pi) / (c ** 2 * radius ** 4) * dc) ** 2
                                                                 + ((32 * np.pi * length) / (c * radius ** 5) * dr) ** 2)

    x = J
    y = (T ** 2 - T[0] ** 2)[1:]
    dy = (2 * T * dT)[1:]
    popt, pcov = curve_fit(model, x, y, sigma=dy, absolute_sigma=True)
    c = popt[0]
    dc = np.sqrt(np.diag(pcov)[0])
    G, dG = G(c, dc, length, dl, radius, dr)

    plt.errorbar(J, y, xerr=dJ, yerr=dy, fmt='o', label='Data', capsize=5)
    plt.plot(J, model(J, c), label='Fit', color='red')
    plt.plot(J, model(J, c + dc), label='$\\sigma$', color='red', linestyle='--')
    plt.plot(J, model(J, c - dc), color='red')
    plt.xlabel('$I\\text{ in kg m}^2$')
    plt.ylabel('$T^2\\text{ in s}^2$')
    plt.minorticks_on()
    plt.tick_params(direction='in', top=True, bottom=True, left=True, right=True)
    plt.tick_params(direction='in', which='minor', top=True, bottom=True, left=True, right=True)
    plt.grid(True)
    plt.legend()
    plt.show()

    return G, dG
