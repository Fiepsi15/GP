import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def plot(x, y, y_err, model, popt, pcov, ylabel):
    alpha, alpha_err = sci_round(popt[0], np.sqrt(np.diag(pcov))[0])

    plt.errorbar(x, y, yerr=y_err, label='Messdaten', color='blue', fmt='o', capsize=5)
    plt.plot(x, model(x, 1), color='green', label='Theorie: $\\alpha = 1$')
    plt.plot(x, model(x, popt), color='red', label=f'Lineare Regression: $\\alpha = {alpha}$')
    plt.plot(x, model(x, alpha + alpha_err), color='red', label=f'$\\delta\\alpha = \\pm{alpha_err}$', linestyle='--')
    plt.plot(x, model(x, alpha - alpha_err), color='red', linestyle='--')
    plt.xlabel('$\\frac{N_2}{N_1}$')
    plt.ylabel(ylabel)
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_leerlauf(U1, U2, N1, N2, U1_err, U2_err):
    def model(x, alpha):
        return alpha * x

    x = N2 / N1
    y = U2 / U1
    y_err = np.sqrt((U2_err / U1) ** 2 + (U2 * U1_err / U1 ** 2) ** 2)
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    plot(x, y, y_err, model, popt, pcov, '$\\frac{U_2}{U_1}$')


def plot_short(I1, I2, N1, N2, I1_err, I2_err):
    """
    :param I1:
    :param I2:
    :param N1:
    :param N2:
    :param I1_err:
    :param I2_err:
    :return:
    """
    def model(x, alpha):
        return alpha * x

    x = N2 / N1
    y = I1 / I2
    y_err = np.sqrt((I1_err / I2) ** 2 + (I1 * I2_err / I2 ** 2) ** 2)
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    plot(x, y, y_err, model, popt, pcov, '$\\frac{I_1}{I_2}$')
