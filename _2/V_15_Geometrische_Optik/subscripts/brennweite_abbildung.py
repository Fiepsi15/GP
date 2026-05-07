import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def model(x, f):
    return f * x


def get_f_mean(g, b, dg=0, db=0):
    f = 1 / (1 / g + 1 / b)
    delta_f = np.sqrt((g ** 2 / (b + g) ** 2 * db) ** 2
                      + (b ** 2 / (b + g) ** 2 * dg) ** 2)

    f_bar = np.mean(f)
    delta_f_bar = np.std(f) / np.sqrt(len(f))

    return f, delta_f, f_bar, delta_f_bar


def calculate_f(g: np.ndarray, b: np.ndarray, dg, db, name: str = "") -> (
np.float64, np.float64):
    f, df, f_b, df_b = get_f_mean(g, b, dg, db)

    fr, dfr = sci_round(f_b * 1e3, df_b * 1e3)
    #a2t(np.array([g, b, f]) * 1e3, np.array([dg, db, df]) * 1e3, [["$g$", "$b$", "$f$"], ["mm", "mm", "mm"]])
    print(f"mean: {name} = {fr} ± {dfr} mm\n")
    return f_b, df_b


def calculate_d(f1, f2, f, df=0):
    d = (1 / f1 + 1 / f2 - 1 / f) * (f1 * f2)
    dd = np.abs(f1 * f2 / (f ** 2) * df)
    dr, ddr = sci_round(d, dd)
    return dr, ddr
