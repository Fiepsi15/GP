import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scrips.tools import sci_round


def get_U_B(U_A, alpha):
    return U_A / (alpha + 1)


def get_U_B_err(U_A, U_A_err, alpha, alpha_err):
    return np.sqrt((U_A_err / (alpha + 1)) ** 2 + (U_A * alpha_err / (alpha + 1) ** 2) ** 2)



def poggendorf(R_S: np.ndarray, R_D: np.ndarray, R_S_err, R_D_err) -> tuple[float, float]:
    def model(R_S, alpha):
        return alpha * R_S

    x_data = R_S
    y_data = R_D
    x_err = R_S_err
    y_err = R_D_err
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
    return get_U_B(2, alpha), get_U_B_err(2, 0.01, alpha, alpha_err)
