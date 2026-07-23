import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def get_f_mean(d, a, dd: np.float64 = 0, da: np.float64 = 0):
    f = (d ** 2 - a ** 2) / (4 * d)
    df = np.sqrt(((d ** 2 + a ** 2) / (4 * d ** 2) * dd) ** 2
                 + (a / (2 * d) * da) ** 2)

    f_b = np.mean(f)
    df_b = np.std(f) / np.sqrt(len(f))

    return f_b, df_b, f, df


def calculate_f(d: np.ndarray, a: np.ndarray, dd, da, name: str = "") \
        -> (np.float64, np.float64):
    f_b, df_b, f, df = get_f_mean(d, a, dd, da)
    fr, dfr = sci_round(f_b * 1e3, df_b * 1e3)

    # a2t(np.array([d, a, f]) * 1e3, np.array([dd, da, df]) * 1e3, [["$d$", "$a$", "$f$"], ["mm", "mm", "mm"]])
    print(f"mean: {name} = {fr} ± {dfr} mm\n")
    return f_b, df_b
