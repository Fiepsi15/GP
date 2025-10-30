import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round

def imballance(R_S: np.ndarray, U_B: np.ndarray, R_S_err: np.ndarray, U_B_err: np.ndarray) -> tuple[float, float]:
    def model(R_S, alpha, beta):
        return alpha * R_S + beta

    x_data = R_S
    y_data = U_B
    x_err = R_S_err
    y_err = U_B_err
    popt, pcov = curve_fit(model, x_data, y_data, sigma=y_err, absolute_sigma=True)
    alpha, beta = popt
    alpha_err, beta_err = np.sqrt(np.diag(pcov))

    al, al_err = sci_round(alpha, alpha_err)

    plt.errorbar(x_data, y_data, xerr=x_err, yerr=y_err, label='Widerstands Wertepaare', fmt='o', capsize=5, color='blue')
    plt.plot(x_data, model(x_data, alpha, beta), label=f'Regression: $\\alpha = ${al}', color='red')
    plt.plot(x_data, model(x_data, alpha + alpha_err, beta), label=f'$\\pm \\delta\\alpha = {al_err}$', color='red', linestyle='--')
    plt.plot(x_data, model(x_data, alpha - alpha_err, beta), linestyle='--', color='red')
    plt.xlabel('$R_S (\\Omega)$')
    plt.ylabel('$U \\;(mV)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='minor')
    plt.grid(True)
    plt.legend()
    plt.show()

    return alpha, alpha_err