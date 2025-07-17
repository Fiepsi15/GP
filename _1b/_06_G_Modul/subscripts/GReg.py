import numpy as np
from scipy.optimize import curve_fit


def g_mod_regression(T: np.ndarray, dT: float, J: np.ndarray, dJ: np.ndarray, length: float = 1.0, dl=0.1,
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
    y = T ** 2 - T[0] ** 2
    dy = 2 * T * dT
    popt, pcov = curve_fit(model, x, y, sigma=dy, absolute_sigma=True)
    c = popt[0]
    dc = np.sqrt(np.diag(pcov)[0])
    G, dG = G(c, dc, length, dl, radius, dr)

    return G, dG
