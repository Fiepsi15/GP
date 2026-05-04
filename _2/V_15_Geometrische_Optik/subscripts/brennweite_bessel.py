import numpy as np
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def model(x, f):
    return f * x


def get_f(d, a, dd: np.float64 = 0, da: np.float64 = 0):
    x = 4 * d
    y = d ** 2 - a ** 2
    y_err = np.sqrt((2 * d * dd) ** 2 + (2 * a * da) ** 2)
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    f = popt[0]
    df = np.sqrt(pcov[0][0])
    return f, df


def get_f_mean(d, a, dd: np.float64 = 0, da: np.float64 = 0):
    f = (d ** 2 - a ** 2) / (4 * d)
    delta_f = np.std(f) / np.sqrt(len(f))

    return np.mean(f), delta_f


def calculate_f(d: np.ndarray, a: np.ndarray, dd: np.float64 = 0, da: np.float64 = 0, name: str = "") \
        -> (np.float64, np.float64):

    f1, df1 = get_f(d, a, dd, da)
    fr, dfr = sci_round(f1 * 1e3, df1 * 1e3)
    print(f"linreg: {name} = {fr} ± {dfr} mm")

    f, df = get_f_mean(d, a)
    fr, dfr = sci_round(f * 1e3, df * 1e3)
    print(f"mean: {name} = {fr} ± {dfr} mm\n")
    return f1, df1
