import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round

def linear_regression(U, i, T):
    def model(U, a, b):
        return a * U + b

    y = np.log(U)
    y_err = 0.08 / U
    x = i * T
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    a, b = popt
    delta_a, delta_b = np.sqrt(np.diag(pcov))

    plt.errorbar(x, y, yerr=y_err, label='Messdaten', color='blue', fmt='o', capsize=4)
    a_r, delta_a_r = sci_round(a, delta_a)
    b_r, delta_b_r = sci_round(b, delta_b)
    plt.plot(x, model(x, a, b), label=f'Regressionsgerade: \n$({a_r} \\pm {delta_a_r}) \\cdot t + ({b_r} \\pm {delta_b_r})$ ', color='red')
    plt.plot(x, model(x, a + delta_a, b + delta_b), label='Unsicherheit', color='grey', linestyle='--')
    plt.plot(x, model(x, a - delta_a, b - delta_b), color='grey', linestyle='--')
    plt.xlabel('$t$ in s')
    plt.ylabel('$\\log(U(t))$')
    plt.grid(True)
    plt.legend()
    plt.show()

    print(f'delta aus linearer Regression: \ndelta = ({-a_r} \\pm {delta_a_r}) s^-1')

    return a, b, delta_a, delta_b


def logarithmic_plot(U, i, T, a, b, delta_a, delta_b):
    def model(x, a, b):
        return np.exp(a * x + b)

    x = i * T
    y = U
    y_err = 0.08
    theorie = model(x, a, b)

    plt.errorbar(x, y, yerr=y_err, label='Messdaten', color='blue', fmt='o', capsize=4)
    plt.plot(x, theorie, label='Theoriekurve', color='red')
    plt.plot(x, model(x, a + delta_a, b + delta_b), label='Unsicherheit', color='grey', linestyle='--')
    plt.plot(x, model(x, a - delta_a, b - delta_b), color='grey', linestyle='--')
    plt.xlabel('$t$ in s')
    plt.ylabel('$U(t)$ in V')
    plt.grid(True)
    plt.legend()
    plt.show()

    return


def logarithmic_decrement(U, i, T):
    log = []

    for i in range(len(U) - 1):
        log.append(np.log(U[i] / U[i + 1]))
    plt.plot(range(len(U)-1), log)
    plt.show()
    Lambda, delta_Lambda = np.mean(log), np.std(log)
    delta, delta_delta = sci_round(Lambda/T, delta_Lambda/T)
    Lambda_r, delta_Lambda_r = sci_round(Lambda, delta_Lambda)
    print(f'\nLambda = ({Lambda_r} ± {delta_Lambda_r}')
    print(f'delta = ({delta} ± {delta_delta}) s^-1')

    return Lambda, delta_Lambda