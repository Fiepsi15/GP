import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def get_coupping_coefficient(L_12, L_1, L_2):
    kappa = L_12 / np.sqrt(L_1 * L_2)
    return kappa


def get_gegen_inductance(omega, U_2, I_1):
    L_12 = U_2 / (1j * omega * I_1)
    return L_12


def get_self_inductance_2(L_12, I_1, I_2):
    """
    Calculates the self-inductance L_2 from the mutual inductance L_12 and the currents I_1 and I_2.
    :param L_12:
    :param I_1:
    :param I_2:
    :return:
    """
    L_2 = L_12 * (I_1 / I_2)
    return L_2


def get_self_inductance(omega, omega_err, U_1, U_1_err, I_1, I_1_err):
    """
    Calculates the self-inductance with regression.
    :param omega: Frequency
    :param U_1: Voltage array
    :param I_1: Current array
    :return: Inductance L, uncertainty dL
    """

    def model(x, alpha):
        return alpha * x

    x = I_1
    y = U_1
    y_err = U_1_err
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    L = popt[0] / (omega * 1j)
    dL = np.sqrt(np.diag(pcov))[0] / (omega * 1j)

    alpha, alpha_err = sci_round(popt[0], np.sqrt(np.diag(pcov))[0])
    plt.errorbar(x, y, xerr=I_1_err, yerr=U_1_err, fmt='o', label='data', capsize=5, color='blue')
    plt.plot(x, model(x, *popt), label=f'fit: $\\alpha=${alpha} $\\pm$ {alpha_err}', color='red')
    plt.plot(x, model(x, alpha + alpha_err), label=f'$\\pm\\delta\\alpha$', color='red', linestyle='--')
    plt.plot(x, model(x, alpha - alpha_err), linestyle='--', color='red')
    plt.xlabel('$I_1$ (A)')
    plt.ylabel('$U_1$ (V)')
    plt.legend()
    plt.show()

    return L, dL
