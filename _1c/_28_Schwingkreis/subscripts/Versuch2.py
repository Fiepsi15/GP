import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scrips.tools import sci_round


def gesamtbereich(omega, U_r, U):
    R_v = 82
    omega_0_r = 3070
    delta_omega_0_r = 200
    Z = U * R_v / U_r

    plt.errorbar(omega, Z, label='Messwerte', fmt='o')
    plt.plot([omega_0_r, omega_0_r], [0, 50], label=f'$\\omega_0 = {omega_0_r} \\pm {delta_omega_0_r}$', color='green')
    plt.show()


def phasenverschiebung(omega, phi):
    def model(omega, a, b):
        return omega * a + b

    grenzomega = np.array([omega[i] for i in range(4, 7)])
    grenzphi = np.array([phi[i] for i in range(4, 7)])

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
    plt.legend()
    plt.grid(True)
    plt.show()
