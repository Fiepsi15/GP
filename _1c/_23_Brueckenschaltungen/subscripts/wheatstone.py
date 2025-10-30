import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scrips.tools import sci_round


def get_R_x(R_1, alpha, C: bool):
    if C:
        return R_1 / alpha
    return R_1 * alpha


def get_R_x_err(R_1, R_1_err, alpha, alpha_err, C: bool):
    if C:
        return np.sqrt((R_1_err / alpha) ** 2 + (R_1 * alpha_err / alpha ** 2) ** 2)
    return np.sqrt((R_1_err * alpha) ** 2 + (R_1 * alpha_err) ** 2)


def wheatstone_C(R_1: float, R_1_err: float, R_s: np.ndarray, R_p: np.ndarray, R_s_err: np.ndarray, R_p_err: np.ndarray):
    return wheatstone(R_1, R_1_err, R_s, R_p, R_s_err, R_p_err, C=True)


def wheatstone_R(R_1: float, R_1_err: float, R_s: np.ndarray, R_p: np.ndarray, R_s_err: np.ndarray, R_p_err: np.ndarray):
    return wheatstone(R_1, R_1_err, R_s, R_p, R_s_err, R_p_err, C=False)


def wheatstone(R_1: float, R_1_err: float, R_s: np.ndarray, R_p: np.ndarray, R_s_err: np.ndarray, R_p_err: np.ndarray, C: bool):
    def model(R_s, alpha):
        return R_s * alpha

    x_data = R_s
    y_data = R_p
    x_err = R_s_err
    y_err = R_p_err
    popt, pcov = curve_fit(model, x_data, y_data, sigma=y_err, absolute_sigma=True)
    alpha = popt[0]
    alpha_err = np.sqrt(np.diag(pcov))[0]

    al, al_err = sci_round(alpha, alpha_err)

    plt.errorbar(x_data, y_data, xerr=x_err, yerr=y_err, label='Widerstands Wertepaare', fmt='o', capsize=5, color='blue')
    plt.plot(x_data, model(x_data, alpha), label=f'Regression: $\\alpha = ${al}', color='red')
    plt.plot(x_data, model(x_data, alpha + alpha_err), label=f'$\\pm \\delta\\alpha = {al_err}$', color='red', linestyle='--')
    plt.plot(x_data, model(x_data, alpha - alpha_err), linestyle='--', color='red')
    plt.xlabel('$R_S (\\Omega)$')
    plt.ylabel('$R_D (\\Omega)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='minor')
    plt.grid(True)
    plt.legend()
    plt.show()

    return get_R_x(R_1, alpha, C), get_R_x_err(R_1, R_1_err, alpha, alpha_err, C)

