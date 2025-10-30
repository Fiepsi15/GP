import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round

def poti_kalibrierung_fused(setting: np.ndarray, measurement: np.ndarray, m_err: float) -> tuple[tuple[float, float], tuple[float, float]]:
    def linear_model(x, m):
        return m * x + 5.3

    x_data = setting
    y_data = measurement
    popt, pcov = curve_fit(linear_model, x_data, y_data)
    slope = popt[0]
    intercept = 5.3
    slope_err = np.sqrt(np.diag(pcov))[0]
    intercept_err = 0.1

    alpha, alpha_err = sci_round(slope, slope_err)

    plt.errorbar(x_data, y_data, yerr=[m_err for _ in y_data], fmt='o', capsize=5, color='blue', label='Gemessener Widerstand')
    plt.plot(x_data, linear_model(x_data, slope), label=f'Regression: $\\alpha = $ {alpha}', color='red')
    plt.plot(x_data, linear_model(x_data, slope + slope_err), label=f'$\\pm \\delta\\alpha = {alpha_err}$', color='red', linestyle='--')
    plt.plot(x_data, linear_model(x_data, slope - slope_err), linestyle='--', color='red')
    plt.xlabel('Einstellung Potentiometer')
    plt.ylabel('$R_P (\\Omega)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='minor')
    plt.grid(True)
    plt.legend()
    plt.show()
    return (slope, slope_err), (intercept, intercept_err)


def poti_kalibrierung(setting: np.ndarray, measurement: np.ndarray, m_err) -> tuple[tuple[float, float], tuple[float, float]]:
    def linear_model(x, m, b):
        return m * x + b

    x_data = setting
    y_data = measurement
    popt, pcov = curve_fit(linear_model, x_data, y_data)
    slope, intercept = popt
    slope_err, intercept_err = np.sqrt(np.diag(pcov))

    alpha, alpha_err = sci_round(slope, slope_err)

    plt.errorbar(x_data, y_data, yerr=[m_err for _ in y_data], fmt='o', capsize=5, color='blue', label='Gemessener Widerstand')
    plt.plot(x_data, linear_model(x_data, slope, intercept), label=f'Regression: $\\alpha = $ {alpha}', color='red')
    plt.plot(x_data, linear_model(x_data, slope + slope_err, intercept + intercept_err), label=f'$\\pm \\delta\\alpha = {alpha_err}$', color='red', linestyle='--')
    plt.plot(x_data, linear_model(x_data, slope - slope_err, intercept - intercept_err), linestyle='--', color='red')
    plt.xlabel('Einstellung Potentiometer')
    plt.ylabel('$R_P (\\Omega)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='minor')
    plt.grid(True)
    plt.legend()
    plt.show()
    return (slope, slope_err), (intercept, intercept_err)
