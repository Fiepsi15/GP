import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def linreg(V, delta_V, T, delta_T, m, dm, r, dr, p, dp):
    def model(x, c):
        return c * x

    def gamma(m, r, p, c):
        return (4 * m) / (r ** 4 * p * c)

    def Delta_gamma(m, dm, r, dr, p, dp, c, dc):
        return np.sqrt(
            (4 * dm / (r ** 4 * p * c)) ** 2 +
            (16 * m * dr / (r ** 5 * p * c)) ** 2 +
            (4 * m * dp / (p ** 2 * r ** 4 * c)) ** 2 +
            (4 * m * dc / (r ** 4 * p * c ** 2)) ** 2
        )

    x = V
    y = T ** 2
    y_min = np.min(y)
    y = y - y_min
    sigma_y = 2 * T * delta_T

    popt, pcov = curve_fit(model, x, y, sigma=sigma_y, absolute_sigma=True)
    c = popt[0]
    Delta_c = np.sqrt(pcov[0][0])

    gamma = gamma(m, r, p, c)
    Delta_gamma = Delta_gamma(m, dm, r, dr, p, dp, c, Delta_c)
    gamma_r, sigma_r = sci_round(gamma, Delta_gamma)

    plt.errorbar(x, y, xerr=delta_V, yerr=sigma_y, fmt='o', label='Messwerte', color='blue', capsize=5)
    plt.plot(x, model(x, c), label='Fit: $\\gamma = ' + str(gamma_r) + '\\pm' + str(sigma_r) + '$', color='red')
    plt.plot(x, model(x, c + Delta_c), label='$\\sigma$', color='red', linestyle='--')
    plt.plot(x, model(x, c - Delta_c), color='red', linestyle='--')
    plt.xlabel('$V$ in m')
    plt.ylabel('$T^2$ in $\\text{s}^2$')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(gamma, Delta_gamma)
    print(f'γ = {gamma_r} ± {sigma_r}')
    return gamma, Delta_gamma


def run():
    m = 9.66e-3  # kg
    dm = 0.01e-3  # kg
    r = 16.55e-3 / 2  # m
    dr = 0.005e-3  # m
    p = 1024.7e2  # Pa
    dp = 10  # Pa
    R = 103e-3 / 2  # m
    dR = 0.2e-3  # m

    def V(l, R):
        return np.pi * R ** 2 * l

    def V_err(l, dl, R, dR):
        return np.sqrt((np.pi * R ** 2 * dl) ** 2 + (2 * np.pi * R * l * dR) ** 2)


    print("\nN2:")
    data_N2 = np.loadtxt('_1b/_10_Adiabatenexponent/daten/V_02_N2.csv', skiprows=1, delimiter=',')
    V_N2= V(data_N2[:, 0] * 1e-2, R)  # m^3
    delta_V = V_err(data_N2[:, 0] * 1e-2, 1e-3, R, dR)  # m^3
    T = data_N2[:, 1] / 30  # s
    delta_T = [1e-3 for _ in T]  # s

    linreg(V_N2, delta_V, T, delta_T, m, dm, r, dr, p, dp)

    print("\nAr:")
    data_Ar = np.loadtxt('_1b/_10_Adiabatenexponent/daten/V_02_Ar.csv', skiprows=1, delimiter=',')
    V_Ar = V(data_Ar[:, 0] * 1e-2, R)  # m^3
    delta_V = V_err(data_Ar[:, 0] * 1e-2, 1e-3, R, dR)  # m^3
    T = data_Ar[:, 1] / 30  # s
    delta_T = [1e-3 for _ in T]  # s

    linreg(V_Ar, delta_V, T, delta_T, m, dm, r, dr, p, dp)

    print("\nCO2:")
    data_CO2 = np.loadtxt('_1b/_10_Adiabatenexponent/daten/V_02_CO2.csv', skiprows=1, delimiter=',')
    V_CO2 = V(data_CO2[:, 0] * 1e-2, R)  # m^3
    delta_V = V_err(data_CO2[:, 0] * 1e-2, 1e-3, R, dR)  # m^3
    T = data_CO2[:, 1] / 30  # s
    delta_T = [1e-3 for _ in T]  # s

    linreg(V_CO2, delta_V, T, delta_T, m, dm, r, dr, p, dp)
