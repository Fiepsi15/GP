import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math

def round_up(n, decimals=0):
    n = n * 10 ** decimals
    n = math.ceil(n)
    return n * 10 ** -decimals


#Hey there
def prep_params(calibration_data, g, dg, rho_w):
    h = np.array(calibration_data[0]) / 1000
    p0 = rho_w * g * h[0]
    p = rho_w * g * h - p0
    dp = np.sqrt((rho_w * g * 0.01e-3) ** 2 + (rho_w * h * dg) ** 2)
    U = np.array(calibration_data[1])
    for i in range(U.shape[0]):
        U[-1 - i] -= U[0]
    return p, U, dp, calibration_data[2]


def calibrate(calibration_data):
    g = 9.766
    dg = 0.006
    rho_w = 1000

    def linmodel(alpha, U):
        return alpha * U

    p, U, dp, dU = prep_params(calibration_data, g, dg, rho_w)
    print(p, U)
    popt, pcov = curve_fit(f=linmodel, xdata=U, ydata=p)
    alpha = popt[0]
    dalpha = np.sqrt(pcov[0, 0])

    # plt.errorbar(U, linmodel(popt[0], U), yerr=np.sqrt(pcov[0][0]), label='Ausgleichsgerade', color='red', capsize=2)
    plt.plot(U, linmodel(alpha, U), label='$\\alpha = 171\\, \\text{(Pa/V)}$', color='red')
    plt.plot(U, linmodel(alpha + dalpha, U), label='$\\delta \\alpha = \\pm5\\, \\text{(Pa/V)}$', color='red',
             linestyle='--')
    plt.plot(U, linmodel(alpha - dalpha, U), color='red', linestyle='--')
    plt.errorbar(U, p, xerr=dU, yerr=dp, fmt='o', label='Gemessene Spannung', color='blue', capsize=5)
    plt.xlabel('$\\Delta$U in V')
    plt.ylabel('$\\Delta$p in Pa')
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.legend()
    plt.show()

    return popt[0], np.sqrt(pcov[0, 0])


def calculate_linreg(alpha, dalpha, r, dr, dU, ddU):
    def p_model(r, sigma):
        return sigma * 2 / r

    def p_measure(alpha, dU, dalpha, ddU):
        return alpha * dU, np.sqrt((dU * dalpha) ** 2 + (alpha * ddU) ** 2)

    p, dp = p_measure(alpha, dU, dalpha, ddU)
    popt, pcov = curve_fit(f=p_model, xdata=r, ydata=p, sigma=dp, absolute_sigma=True)
    sigma = popt[0]
    dsigma = np.sqrt(pcov[0][0])

    plt.errorbar(2 / r, p, yerr=dp, fmt='o', label='Maximale Druckdifferenz $\\Delta p$', color='blue', capsize=5)
    plt.plot(2 / r, p_model(r, sigma), color='red', label='$\\sigma = $' + str(np.round(sigma, 4) * 1e3) + '$\\,$mN/m')
    plt.plot(2 / r, p_model(r, sigma + dsigma), color='red',
             label='$\\delta \\sigma = \\pm $' + str(round_up(dsigma, 4) * 1e3) + '$\\,$mN/m', linestyle='--')
    plt.plot(2 / r, p_model(r, sigma - dsigma), color='red', linestyle='--')
    plt.xlabel('$2/r$ in $\\text{m}^{-1}$')
    plt.ylabel('$\\Delta p$ in Pa')
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.legend()
    plt.show()
    return sigma, dsigma


def saltwater_density(h, dh, du, ddU, alpha, dalpha):
    g = 9.766
    dg = 0.006
    def linmodel(rho, x):
        return rho * x

    y = du * alpha / g
    y_err = np.sqrt((du / g * dalpha) ** 2 + (alpha / g * ddU) ** 2 + (alpha * dU / (g ** 2) * dg) ** 2)
    popt, pcov = curve_fit(f=linmodel, xdata=h, ydata=y, sigma=y_err, absolute_sigma=True)
    rho_SW = popt[0]
    drho_SW = np.sqrt(pcov[0][0])

    plt.plot(h, rho_SW * h, color='red', label='$\\rho = $' + str(int(np.round(rho_SW, 0))) + '$\\,\\text{kg}/\\text{m}^3$')
    plt.plot(h, (rho_SW + drho_SW) * h, color='red', label='$\\delta \\rho = \\pm $' + str(round_up(drho_SW, 0)) + '$\\,\\text{kg}/\\text{m}^3$', linestyle='--')
    plt.plot(h, (rho_SW - drho_SW) * h, color='red', linestyle='--')
    plt.errorbar(h, y, yerr=y_err, xerr=dh, label='Messwerte $p/g$', color='blue', fmt='o', capsize=5)
    plt.ylabel('$\\Delta p/g$ in $\\text{kg}/\\text{m}^2$')
    plt.xlabel('$\\Delta h$ in $\\text{m}$')
    plt.legend()
    plt.show()
    print('\nDichte des Salzwassers:\n' + str((rho_SW, drho_SW)))



ddU = np.sqrt(2) * 0.01
dU = np.array([0.9, 0.55, 0.48])
dU2 = np.array([0.95, 0.57, 0.56])
r = np.array([1.85, 2.90, 3.90]) / (2 * 1000)
dr = 0.05 / (2 * 1000)

calibration_data = [[0, 4, 8, 12, 16, 20],
                    [-1.73, -1.5, -1.27, -1.10, -0.86, -0.53],
                    [ddU]]

alpha, dalpha = calibrate(calibration_data)
print(f"alpha = {alpha} +- {dalpha}")
# print('\nBerechnung durch Average(dest):\n' + str(calculate_avg(alpha, dalpha, dU, ddU, r, dr, 'destilliertes Wasser')))

# print('\nBerechnung durch Average(salz):\n' + str(calculate_avg(alpha, dalpha, dU2, ddU, r, dr, 'Salzwasserlösung')))

print('\nBerechnung durch lin. Regression:\n' + str(calculate_linreg(alpha, dalpha, r, dr, dU, ddU)))

print('\nBerechnung durch lin. Regression:\n' + str(calculate_linreg(alpha, dalpha, r, dr, dU2, ddU)))

h = np.array([0, 4, 8, 12, 16, 20]) / 1e3
dh = 0.01 / 1e3
dU = np.array([-3.62, -3.45, -3.33, -3.15, -2.94, -2.62])
dU = np.array([dU[i] - np.min(dU) for i in range(len(dU))])
ddU = 0.01
saltwater_density(h, dh, dU, ddU, alpha, dalpha)

