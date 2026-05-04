import numpy as np
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def model(x, f):
    return f * x


def get_f(g, b, dg=0, db=0):
    x = 1 / g + 1 / b
    y = np.ones_like(x)
    popt, pcov = curve_fit(model, x, y)
    f = popt[0]
    df = np.sqrt(pcov[0][0])
    return f, df


def get_f_mean(g, b, dg=0, db=0):
    f = 1 / (1 / g + 1 / b)
    delta_f = np.std(f) / np.sqrt(len(f))

    return np.mean(f), delta_f


def calculate_f(g: np.ndarray, b: np.ndarray, name: str = "") -> (np.float64, np.float64):
    f, df = get_f(g, b)
    fr, dfr = sci_round(f * 1e3, df * 1e3)
    print(f"linreg: {name} = {fr} ± {dfr} mm")

    f, df = get_f_mean(g, b)
    fr, dfr = sci_round(f * 1e3, df * 1e3)
    print(f"mean: {name} = {fr} ± {dfr} mm\n")
    return f, df


def calculate_d(f1, f2, f, df=0):
    d = (1 / f1 + 1 / f2 - 1 / f) * (f1 * f2)
    dd = np.abs(f1 * f2 / (f ** 2) * df)
    dr, ddr = sci_round(d, dd)
    return dr, ddr
