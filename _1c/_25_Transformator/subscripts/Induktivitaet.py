import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def get_coupping_coefficient(L_12, L_1, L_2):
    kappa = L_12 / np.sqrt(L_1 * L_2)
    return kappa


def get_delta_gegen_inductance(omega, U_2, I_1, omega_err, U_2_err, I_1_err):
    """
    Calculates the uncertainty of the mutual inductance L_12.
    :param omega:
    :param U_2:
    :param I_1:
    :param omega_err:
    :param U_2_err:
    :param I_1_err:
    :return:
    """
    dL_12 = np.sqrt((U_2_err / (1j * omega * I_1)) ** 2 +
                    (U_2 * omega_err / (1j * omega ** 2 * I_1)) ** 2 +
                    (U_2 * I_1_err / (1j * omega * I_1 ** 2)) ** 2)
    return dL_12


def get_gegen_inductance(omega, U_2, I_1, omega_err=0, U_2_err=0, I_1_err=0):
    L_12 = U_2 / (1j * omega * I_1)
    L_12_err = get_delta_gegen_inductance(omega, U_2, I_1, omega_err, U_2_err, I_1_err)
    return L_12, L_12_err


def get_self_inductance_2(L_12, I_1, I_2, delta_L_12=0, delta_I_1=0, delta_I_2=0):
    """
    Calculates the self-inductance L_2 from the mutual inductance L_12 and the currents I_1 and I_2.
    :param L_12:
    :param I_1:
    :param I_2:
    :return:
    """
    L_2 = L_12 * (I_1 / I_2)

    delta_L_2 = np.sqrt((delta_L_12 * (I_1 / I_2)) ** 2 +
                        (L_12 * (delta_I_1 / I_2)) ** 2 +
                        (L_12 * I_1 * delta_I_2 / I_2 ** 2) ** 2)

    return L_2, delta_L_2


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
    plt.errorbar(x, y, xerr=I_1_err, yerr=U_1_err, fmt='o', label='Messdaten', capsize=5, color='blue')
    plt.plot(x, model(x, *popt), label=f'Lineare Regression: $\\alpha=${alpha}', color='red')
    plt.plot(x, model(x, alpha + alpha_err), label=f'$\\delta\\alpha = \\pm {alpha_err}$', color='red', linestyle='--')
    plt.plot(x, model(x, alpha - alpha_err), linestyle='--', color='red')
    plt.xlabel('$I_1$ (A)')
    plt.ylabel('$U_1$ (V)')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return L, dL
