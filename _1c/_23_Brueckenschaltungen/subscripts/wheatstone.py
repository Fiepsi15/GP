import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def get_R_x(R_1, alpha):
    return R_1 * alpha

def get_R_x_err(R_1, R_1_err, alpha, alpha_err):
    return np.sqrt((R_1_err * alpha) ** 2 + (R_1 * alpha_err) ** 2)


def wheatstone(R_1: float, R_1_err: float, R_s: np.ndarray, R_p: np.ndarray, R_p_err: np.ndarray):
    def model(R_s, alpha):
        return R_s * alpha

    x_data = R_s
    y_data = R_p
    y_err = R_p_err
    popt, pcov = curve_fit(model, x_data, y_data, sigma=y_err, absolute_sigma=True)
    alpha = popt[0]
    alpha_err = np.sqrt(np.diag(pcov))[0]

    plt.scatter(x_data, y_data, label='Datenpunkte')
    plt.plot(x_data, model(x_data, alpha), label='Fit: $R_P = {:.4f} R_S$'.format(alpha), color='red')
    plt.show()

    return get_R_x(R_1, alpha), get_R_x_err(R_1, R_1_err, alpha, alpha_err)

