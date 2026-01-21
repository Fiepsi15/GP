import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def power(U: np.ndarray, I: np.ndarray) -> np.ndarray:
    """Calculate power from voltage and current."""
    return U * I


def power_err(U: np.ndarray, U_err: np.ndarray, I: np.ndarray, I_err: np.ndarray) -> np.ndarray:
    """Calculate error of power from voltage and current errors."""
    return np.sqrt((I * U_err) ** 2 + (U * I_err) ** 2)


def resistance(U: np.ndarray, I: np.ndarray) -> np.ndarray:
    """Calculate resistance from voltage and current."""
    return U / I


def resistance_err(U: np.ndarray, U_err: np.ndarray, I: np.ndarray, I_err: np.ndarray) -> np.ndarray:
    """Calculate error of resistance from voltage and current errors."""
    return np.sqrt((1 / I * U_err) ** 2 + (U / I ** 2 * I_err) ** 2)


def get_radius(rho, A, R):
    return np.cbrt(rho * A / (2 * np.pi ** 2 * R))


def get_radius_err(rho, rho_err, A, A_err, R, R_err):
    return np.sqrt((1/3 * np.cbrt(rho/(2 * np.pi ** 2 * R * A ** 2)) * A_err) ** 2
                   + (1/3 * np.cbrt(A * rho / (2 * np.pi ** 2 * R ** 4)) * R_err) ** 2
                   + (1/3 * np.cbrt(A / (2 * np.pi ** 2 * R * rho ** 2)) * rho_err) ** 2)


def get_length(rho, A, R):
    return np.cbrt(A ** 2 * R / (4 * np.pi * rho))


def get_length_err(rho, rho_err, A, A_err, R, R_err):
    return np.sqrt((1/3 * np.cbrt(2 * R / (np.pi * rho * A)) * A_err) ** 2
                   + (1/3 * np.cbrt(A ** 2 / (4 * np.pi * rho * R ** 2)) * R_err) ** 2
                   + (1/3 * np.cbrt(A ** 2 * R / (4 * np.pi * rho ** 4)) * rho_err) ** 2)


def stefan_boltzmann(r, P, P_err=None):
    def model(r, A, c):
        sigma = 5.67e-10
        Delta_T = r / c
        return sigma * A * ((290.15 + Delta_T) ** 4 - 290.15 ** 4)

    x_data = r
    y_data = P
    popt, pcov = curve_fit(model, xdata=x_data, ydata=y_data, p0=[1e-5, -1])
    #popt, pcov = curve_fit(model, xdata=x_data, ydata=y_data, p0=[1, 1])
    A, c = popt
    A_err, c_err = np.sqrt(np.diag(pcov))
    plt.plot(x_data, model(x_data, A, c), label='Fit', color='red')
    plt.plot(x_data, model(x_data, A + A_err, c + c_err), linestyle='dashed', color='green', label='Fit Unsicherheit')
    plt.plot(x_data, model(x_data, A - A_err, c - c_err), linestyle='dashed', color='green')
    plt.title('Stefan Boltzmann')
    return A, c, A_err, c_err


def make_plots(U: np.ndarray, U_err: np.ndarray, I: np.ndarray, I_err: np.ndarray, rho, rho_err):
    P = power(U, I)
    P_err = power_err(U, U_err, I, I_err)
    R = resistance(U, I)
    R_err = resistance_err(U, U_err, I, I_err)

    # Current over Voltage
    plt.errorbar(U, I, xerr=U_err, yerr=I_err, label='Messwerte', color='blue', fmt='o', capsize=5)
    plt.title('$(I, U)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.xlabel('$U (V)$')
    plt.ylabel('$I (A)$')
    plt.legend()
    plt.grid(True)
    plt.show()

    r = R / R[0] - 1
    r_err = R_err / R[0]
    plt.scatter(r, P, label='Messwerte', color='blue')

    A, c, A_err, c_err = stefan_boltzmann(R / R[0] - 1, P, P_err=P_err)
    T_72 = 290.15 + r[13] / c
    T_72_err = np.sqrt((r_err[13] / c) ** 2 + (r[13] * c_err / c ** 2) ** 2)
    T_72, T_72_err = sci_round(T_72, T_72_err)
    T_80 = 290.15 + r[14] / c
    T_80_err = np.sqrt((r_err[14] / c) ** 2 + (r[14] * c_err / c ** 2) ** 2)
    T_80, T_80_err = sci_round(T_80, T_80_err)

    print(f'\nTemperature at 72V: {T_72 - 273.15} ± {T_72_err} °C, at 80V: {T_80 - 273.15} ± {T_80_err} °C')
    xi, xi_err = sci_round(get_radius(rho, A, R[0]), get_radius_err(rho, rho_err, A, A_err, R[0], R_err[0]))
    L, L_err = sci_round(get_length(rho, A, R[0]), get_length_err(rho, rho_err, A, A_err, R[0], R_err[0]))
    (A, A_err), (c, c_err) = sci_round(A, A_err), sci_round(c, c_err)
    print(f'A = {A} ± {A_err}', f'c = {c} ± {c_err}', f'radius = {xi} ± {xi_err}', f'length = {L} ± {L_err}\n', sep='\n')

    plt.xlabel('$r (-)$')
    plt.ylabel('$P (W)$')
    plt.legend()
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True, which='both')
    #plt.loglog()
    plt.yscale('log')
    plt.show()
