import numpy as np
from scipy.optimize import curve_fit


def delta_T_quadrat(T, delta_T):
    '''
    Calculate the uncertainty of T^2.
    :param T: Period duration
    :param delta_T: Uncertainty of the period duration
    :return: Uncertainty of T^2
    '''
    return 2 * T * delta_T


def linear_regression_pendulum(Periodendauer, delta_Periodendauer, Laenge, delta_Laenge):
    '''
    Fitting a linear regression to the pendulum data.
    :param Periodendauer:
    :param delta_Periodendauer:
    :param Laenge:
    :param delta_Laenge:
    :return: k(slope), delta_k, b(y_shift), delta_b
    '''

    def model(x, k, b):
        return x * k + b

    x = Periodendauer ** 2
    y = Laenge
    popt, pcov = curve_fit(model, x, y, sigma=delta_Periodendauer, absolute_sigma=True)
    k, b = popt
    delta_k, delta_b = np.sqrt(np.diag(pcov))

    '''
    plt.errorbar(Periodendauer**2, Laenge, xerr=delta_Periodendauer, yerr=delta_Laenge, fmt='o', label='Messwerte', capsize=5)
    plt.plot(Periodendauer**2, model(x, k, b), '--', label='Linear Regression')
    plt.xlabel('Periodendauer$^2 [s^2]$')
    plt.ylabel('Länge [m]')
    plt.grid(True)
    plt.legend()
    plt.show()
    '''

    return k, delta_k, b, delta_b
