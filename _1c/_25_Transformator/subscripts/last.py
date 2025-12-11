import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def plot_U_N_withreg(R, delta_R, N1, N2, U1, I2, delta_I2):
    def model(x, alpha):
        return alpha * x

    U2 = R * I2

    x = N2 / N1
    y = U2 / U1
    y_err = np.sqrt((R * delta_I2) ** 2 + (I2 * delta_R) ** 2)

    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)

    alpha, alpha_err = sci_round(popt[0], np.sqrt(np.diag(pcov))[0])

    plt.errorbar(x, y, yerr=y_err, fmt='o', label='data', capsize=5, color='blue')
    plt.plot(x, model(x, *popt), label=f'fit: $\\alpha=${alpha} $\\pm$ {alpha_err}', color='red')
    plt.plot(x, model(x, alpha + alpha_err), label=f'$\\pm\\delta\\alpha$', color='red', linestyle='--')
    plt.plot(x, model(x, alpha - alpha_err), linestyle='--', color='red')
    plt.xlabel('$\\frac{N_2}{N_1}$')
    plt.ylabel('$\\frac{U_1}{I_2 R}$')
    plt.legend()
    plt.grid()
    plt.show()
    return


def plot_U_N_withreg_corrected(R, delta_R, N1, N2, U1, I2, delta_I2, L1, L2, omega):
    R_N = 5.5
    N_ges = 500
    R_i2 = R_N * (N2 / N_ges)
    R_corr = R + R_i2

    alpha = np.abs(1 + R_N * (N1 / N_ges) * (1j * omega * L2 + R) / (1j * omega * L1 * R))
    U1 = U1 / alpha

    plot_U_N_withreg(R_corr, delta_R, N1, N2, U1, I2, delta_I2)
