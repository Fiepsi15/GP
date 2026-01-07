import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scrips.tools import sci_round


def gesamtbereich(omega, U_r, U, R, C, L, delta_R, delta_C, delta_L):
    R_v = 82
    I = U_r / R_v
    omega_0_r = 3070
    delta_omega_0_r = 200
    Z = U / I

    Z_theo = np.sqrt(R ** 2 + (omega * L - 1 / (omega * C)) ** 2)

    plt.errorbar(omega, Z, label='Messwerte', fmt='o', color='blue')
    plt.plot(omega, Z_theo, label='Theoriekurve', color='red')
    plt.plot([omega_0_r, omega_0_r], [0, 500], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.plot([omega_0_r - delta_omega_0_r, omega_0_r - delta_omega_0_r], [0, 500], color='green', linestyle='--')
    plt.plot([omega_0_r + delta_omega_0_r, omega_0_r + delta_omega_0_r], [0, 500], color='green', linestyle='--')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    plt.xscale('log')
    plt.legend()
    plt.show()


def widerstand(omega, U_r, U, omega_0, delta_omega_0):
    R_v = 82
    I = U_r / R_v
    Z = U / I
    omega_0_r, delta_omega_0_r = sci_round(omega_0, delta_omega_0)
    def model(omega, a, b, c):
        return a * omega ** 2 + b * omega + c

    grenzomega = np.array([omega[i] for i in range(3, 8)])
    grenzZ = np.array([Z[i] for i in range(3, 8)])
    popt, pcov = opt.curve_fit(model, grenzomega, grenzZ)
    Z_0 = model(omega_0, *popt)
    Z_0p = model(omega_0 + delta_omega_0, *popt)
    Z_0m = model(omega_0 - delta_omega_0, *popt)
    delta_Z_0 = np.abs((Z_0p - Z_0m) / 2)
    Z_0r, delta_Z_0r = sci_round(Z_0, delta_Z_0)
    print(Z_0r, delta_Z_0r)


    plt.errorbar(omega, Z, label='Messwerte', fmt='o', color='blue')
    x = np.linspace(grenzomega[0], grenzomega[-1], 100)
    plt.plot(x, model(x, *popt), color='red', label='quadratische näherung um $\\omega_0$')
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
    R_v = 82
    I = U_r / R_v
    Z = U / I
    def model(x, a):
        return a * x

    x = omega
    y = 1 / Z
    popt, pcov = opt.curve_fit(model, x, y)
    C = popt[0]
    delta_C = np.sqrt(pcov[0, 0])
    C_r, delta_C_r = sci_round(C, delta_C)

    print(C_r, delta_C_r)

    plt.errorbar(omega, Z, label='Messwerte', fmt='o', color='blue')
    plt.plot(x, 1 / model(x, *popt), color='red', label='hyperbolische näherung')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    plt.legend()
    plt.grid()
    plt.show()

    return C, delta_C


def inductance(omega, U_r, U):
    R_v = 82
    I = U_r / R_v
    Z = U / I

    def model(x, a):
        return a * x

    x = omega
    y = Z
    popt, pcov = opt.curve_fit(model, x, y)
    L = popt[0]
    delta_L = np.sqrt(pcov[0, 0])
    L_r, delta_L_r = sci_round(L, delta_L)

    print(L_r, delta_L_r)


    plt.errorbar(omega, Z, label='Messwerte', fmt='o', color='blue')
    plt.plot(x, model(x, *popt), color='red', label='lineare näherung')
    plt.xlabel('Frequenz $\\omega (\\mathrm{Hz})$')
    plt.ylabel('$Z \\;(\\Omega)$')
    plt.legend()
    plt.grid()
    plt.show()

    return L, delta_L


def phasenverschiebung(omega, phi):
    def model(omega, a, b):
        return omega * a + b

    grenzomega = np.array([omega[i] for i in range(16, 19)])
    grenzphi = np.array([phi[i] for i in range(16, 19)])

    popt, pcov = opt.curve_fit(model, grenzomega, grenzphi, sigma=[0.5 for _ in grenzphi], absolute_sigma=True)
    a, b = popt
    delta_a, delta_b = np.sqrt(np.diag(pcov))
    a, delta_a = sci_round(a, delta_a)
    b, delta_b = sci_round(b, delta_b)
    print(a, delta_a,'\n', b, delta_b)

    omega_0 = opt.fsolve(model, x0=0, args=(popt[0], popt[1]))[0]
    omega_0p = opt.fsolve(model, omega_0, args=(popt[0] + np.sqrt(pcov[0, 0]), popt[1] + np.sqrt(pcov[1, 1])))[0]
    omega_0m = opt.fsolve(model, omega_0, args=(popt[0] - np.sqrt(pcov[0, 0]), popt[1] - np.sqrt(pcov[1, 1])))[0]

    delta_omega_0 = np.abs((omega_0p - omega_0m)/2)
    print(omega_0, delta_omega_0)
    omega_0_r, delta_omega_0_r = sci_round(omega_0, delta_omega_0)

    plt.errorbar(omega, phi, label='Messwerte', fmt='o', color='blue')
    plt.plot(grenzomega, model(grenzomega, *popt), color='red', label='lineare näherung um $\\omega_0$')
    plt.plot([omega_0, omega_0], [-20, 20], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.plot([omega_0 - delta_omega_0, omega_0 - delta_omega_0], [-20, 20], linestyle='dashed', color='green')
    plt.plot([omega_0 + delta_omega_0, omega_0 + delta_omega_0], [-20, 20], linestyle='dashed', color='green')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

    return omega_0, delta_omega_0
