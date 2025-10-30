import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def imballance(R_S: np.ndarray, U_B: np.ndarray, U_B_err: np.ndarray) -> tuple[float, float]:
    def model(R_S, alpha):
        return alpha * R_S

    x_data = R_S
    y_data = U_B
    y_err = U_B_err
    popt, pcov = curve_fit(model, x_data, y_data, sigma=y_err, absolute_sigma=True)
    alpha = popt[0]
    alpha_err = np.sqrt(np.diag(pcov))[0]

    return alpha, alpha_err