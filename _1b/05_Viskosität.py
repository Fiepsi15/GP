import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


def Arrheniusreg(Temperatur, Viskosität, dTemp, dVis):
    R = 8.3145

    def model(x, m, b):
        return m * x + b

    y = np.log(Viskosität)
    y_err = dVis / Viskosität
    x = 1 / (Temperatur)
    x_err = dTemp / (Temperatur ** 2)
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    E_A = R * popt[0]
    B = np.exp(popt[1])
    dE_A, d_B = R * np.sqrt(pcov[0][0]), np.exp(popt[1]) * np.sqrt(pcov[1][1])

    plt.errorbar(x, y, xerr=x_err, yerr=y_err, label="Daten", color='blue', fmt='o', capsize=5)
    plt.plot(x, model(x, *popt), label="Fit", color='red')
    plt.plot(x, model(x, popt[0] + np.sqrt(pcov[0][0]), popt[1] + np.sqrt(pcov[1][1])), color='red',
             label="$\\pm$ error", linestyle='--')
    plt.plot(x, model(x, popt[0] - np.sqrt(pcov[0][0]), popt[1] - np.sqrt(pcov[1][1])), color='red', linestyle='--')
    plt.xlabel('$1/T$ in $1/\\text{K}$')
    plt.ylabel('$log(\\eta)$')
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.legend()
    plt.show()

    plt.errorbar(Temperatur, Viskosität, xerr=dTemp, yerr=dVis, color='blue', label='Messwerte', fmt='o', capsize=5)
    plt.plot(Temperatur, (B * np.exp(E_A / (R * Temperatur))), color='red', label='Fit')
    plt.plot(Temperatur, ((B + d_B) * np.exp((E_A + dE_A) / (R * Temperatur))), linestyle='--', color='red', label='$\\pm$ error')
    plt.plot(Temperatur, ((B - d_B) * np.exp((E_A - dE_A) / (R * Temperatur))), linestyle='--', color='red')
    plt.legend()
    plt.xlabel('$T$ in K')
    plt.ylabel('$\\eta$ in $\\text{mPas}$')
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.show()

    return E_A, dE_A, B, d_B

data = np.loadtxt('../scrips/csv_data.csv', skiprows=1, delimiter=',').transpose()
Temperature = data[0] + 273.55
Viscosity = data[1]
dTemp, dVis = 0.1, 0.1
print(Arrheniusreg(Temperature, Viscosity, dTemp, dVis))
