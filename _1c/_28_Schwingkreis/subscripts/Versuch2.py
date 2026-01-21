import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scrips.tools import sci_round


def gesamtbereich(omega, U_r, U, R, C, L, delta_R, delta_C, delta_L, omega_0, delta_omega_0):
    delta_omega = np.full_like(omega, 1)
    delta_Ur = 0.04
    delta_U = 0.02
    R_v = 82
    delta_R = 1  # Ohm
    I = U_r / R_v
    Z = U / I
    delta_Z = np.sqrt((delta_U / I) ** 2 + (U / U_r * delta_R) ** 2 + (U * R_v / U_r ** 2 * delta_Ur) ** 2)
    omega_0_r, delta_omega_0_r = sci_round(omega_0, delta_omega_0)

    Z_theo = np.sqrt(R ** 2 + (omega * L - 1 / (omega * C)) ** 2)
    delta_theo = np.sqrt((R / Z_theo * delta_R) ** 2 + ((omega ** 2 * L - 1/C ) / Z_theo * delta_L) ** 2 + ((- L / C ** 2 + 1/ (omega ** 2 * C ** 3))/ Z_theo) ** 2 )

    plt.errorbar(omega, Z, xerr=delta_omega, yerr=delta_Z, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(omega, Z_theo, label='Theoriekurve', color='red')
    #plt.plot(omega, Z_theo + delta_theo, label='Unsicherheit', color='red', linestyle='--')
    #plt.plot(omega, Z_theo - delta_theo, color='red', linestyle='--')
    plt.plot([omega_0_r, omega_0_r], [0, 500], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.plot([omega_0_r - delta_omega_0_r, omega_0_r - delta_omega_0_r], [0, 500], color='green', linestyle='--')
    plt.plot([omega_0_r + delta_omega_0_r, omega_0_r + delta_omega_0_r], [0, 500], color='green', linestyle='--')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    # plt.xscale('log')
    plt.legend()
    plt.grid()
    plt.show()


def widerstand(omega, U_r, U, omega_0, delta_omega_0):
    delta_omega = np.full_like(omega, 1)
    delta_Ur = 0.04
    delta_U = 0.02
    R_v = 82  # Ohm
    delta_R = 1  # Ohm
    I = U_r / R_v
    Z = U / I
    delta_Z = np.sqrt((delta_U / I) ** 2 + (U / U_r * delta_R) ** 2 + (U * R_v / U_r ** 2 * delta_Ur) ** 2)

    omega_0_r, delta_omega_0_r = sci_round(omega_0, delta_omega_0)

    def model(omega, a, b, c):
        return a * omega ** 2 + b * omega + c

    grenzomega = np.array([omega[i] for i in range(3, 8)])
    grenzZ = np.array([Z[i] for i in range(3, 8)])
    popt, pcov = opt.curve_fit(model, grenzomega, grenzZ)
    a, b, c = popt
    aerr, berr, cerr = np.sqrt(np.diag(pcov))
    Z_0 = model(omega_0, *popt)
    Z_0p = model(omega_0 + delta_omega_0, a + aerr, b, c)
    Z_0m = model(omega_0 - delta_omega_0, a - aerr, b, c)
    delta_Z_0 = np.abs((Z_0p - Z_0m) / 2)
    Z_0r, delta_Z_0r = sci_round(Z_0, delta_Z_0)
    x = np.linspace(grenzomega[0], grenzomega[-1], 100)
    print(Z_0r, delta_Z_0r)

    plt.errorbar(omega, Z, xerr=delta_omega, yerr=delta_Z, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(x, model(x, *popt), color='red', label='quadratische näherung um $\\omega_0$ zur Interpolation')
    plt.plot([omega_0, omega_0], [100, 200], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.plot([omega_0 - delta_omega_0, omega_0 - delta_omega_0], [100, 200], color='green', linestyle='--')
    plt.plot([omega_0 + delta_omega_0, omega_0 + delta_omega_0], [100, 200], color='green', linestyle='--')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    plt.legend()
    plt.grid()
    plt.show()
    return Z_0, delta_Z_0


def capacity(omega, U_r, U):
    delta_omega = np.full_like(omega, 1)
    delta_Ur = 0.04
    delta_U = 0.02
    R_v = 82
    delta_R = 1  # Ohm
    I = U_r / R_v
    Z = U / I
    delta_Z = np.sqrt((delta_U / I) ** 2 + (U / U_r * delta_R) ** 2 + (U * R_v / U_r ** 2 * delta_Ur) ** 2)

    def model(x, a):
        return a * x

    x = omega
    y = 1 / Z
    y_err = delta_Z / Z ** 2
    popt, pcov = opt.curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    C = popt[0]
    delta_C = np.sqrt(pcov[0, 0])
    C_r, delta_C_r = sci_round(C, delta_C)

    print(C_r, delta_C_r)

    plt.errorbar(omega, y, xerr=delta_omega, yerr=y_err, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(x, model(x, *popt), color='red', label='lineare Regression')
    plt.plot(x, model(x, C + delta_C), label='Unsicherheit', color='red', linestyle='dashed')
    plt.plot(x, model(x, C - delta_C), color='red', linestyle='dashed')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$1/Z \\;(\\Omega^{-1})$')
    plt.legend()
    plt.grid()
    plt.show()

    return C, delta_C


def inductance(omega, U_r, U):
    delta_omega = np.full_like(omega, 1)
    delta_Ur = 0.04
    delta_U = 0.02
    R_v = 82
    delta_R = 1  # Ohm
    I = U_r / R_v
    Z = U / I
    delta_Z = np.sqrt((delta_U / I) ** 2 + (U / U_r * delta_R) ** 2 + (U * R_v / U_r ** 2 * delta_Ur) ** 2)

    def model(x, a):
        return a * x

    x = omega
    y = Z
    y_err = delta_Z
    popt, pcov = opt.curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    L = popt[0]
    delta_L = np.sqrt(pcov[0, 0])
    L_r, delta_L_r = sci_round(L, delta_L)

    print(L_r, delta_L_r)

    plt.errorbar(omega, Z, xerr=delta_omega, yerr=y_err, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(x, model(x, *popt), color='red', label='lineare näherung')
    plt.plot(x, model(x, L + delta_L), color='red', label='Unsicherheit', linestyle='dashed')
    plt.plot(x, model(x, L - delta_L), color='red', linestyle='dashed')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    plt.legend()
    plt.grid()
    plt.show()

    return L, delta_L


def phasenverschiebung(omega, phi):
    delta_omega = np.full_like(omega, 1)
    delta_phi = np.full_like(phi, 1)

    def model(omega, a, b):
        return omega * a + b

    grenzomega = np.array([omega[i] for i in range(16, 19)])
    grenzphi = np.array([phi[i] for i in range(16, 19)])

    popt, pcov = opt.curve_fit(model, grenzomega, grenzphi, sigma=[delta_phi[0] for _ in grenzphi], absolute_sigma=True)

    omega_0 = opt.fsolve(model, x0=0, args=(popt[0], popt[1]))[0]
    omega_0p = opt.fsolve(model, omega_0, args=(popt[0] + np.sqrt(pcov[0, 0]), popt[1]))[0]
    omega_0m = opt.fsolve(model, omega_0, args=(popt[0] - np.sqrt(pcov[0, 0]), popt[1]))[0]

    delta_omega_0 = np.abs((omega_0p - omega_0m) / 2)
    print(omega_0, delta_omega_0)
    omega_0_r, delta_omega_0_r = sci_round(omega_0, delta_omega_0)

    plt.errorbar(omega, phi, xerr=delta_omega, yerr=delta_phi, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(grenzomega, model(grenzomega, *popt), color='red', label='lineare näherung um $\\omega_0$')
    plt.plot(grenzomega, model(grenzomega, popt[0] + np.sqrt(pcov[0, 0]), popt[1]), color='red', linestyle='dashed')
    plt.plot(grenzomega, model(grenzomega, popt[0] - np.sqrt(pcov[0, 0]), popt[1]), color='red', linestyle='dashed')
    plt.plot([omega_0, omega_0], [-20, 20], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.plot([omega_0 - delta_omega_0, omega_0 - delta_omega_0], [-20, 20], linestyle='dashed', color='green')
    plt.plot([omega_0 + delta_omega_0, omega_0 + delta_omega_0], [-20, 20], linestyle='dashed', color='green')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('Phasenverschiebung $\\Delta \\varphi (\\mathrm{°})$')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

    return omega_0, delta_omega_0
