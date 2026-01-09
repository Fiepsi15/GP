import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as opt
from scrips.tools import sci_round


def bodeplot(omega, U_e, U_a, Delta_phi):
    delta_omega = np.full_like(omega, 1)
    delta_U = 0.04
    delta_phi = 1
    def log_model(x, a, b):
        return a * np.log10(x) + b

    H = U_a / U_e
    H_err = np.sqrt((delta_U / U_e) ** 2 + (U_a * delta_U / U_e ** 2) ** 2)
    H_log = 20 * np.log10(H)
    H_log_err = 20 * H_err / (H * np.log(10))

    omegaende = omega[-4:]
    ende = H_log[-4:]

    popt, pcov = opt.curve_fit(log_model, omegaende, ende)
    a, delta_a = sci_round(popt[0], np.sqrt(pcov[0, 0]))
    print('Flankensteilheit im Hochfrequenzbereich:', a, '±', delta_a, 'dB/Dekade')

    plt.errorbar(omega, H_log, xerr=delta_omega, yerr=H_log_err, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(omegaende, log_model(omegaende, *popt), color='red', label=f'Flankensteilheit $\\alpha = {a} \\pm {delta_a}$ dB$/$Dekade', zorder=10, linewidth=2)
    plt.plot(omegaende, log_model(omegaende, popt[0] + np.sqrt(pcov[0,0]), popt[1]), label='Unsicherheit', color='red', zorder=10, linestyle='dashed')
    plt.plot(omegaende, log_model(omegaende, popt[0] - np.sqrt(pcov[0,0]), popt[1]), color='red', zorder=10, linestyle='dashed')
    plt.xlabel('Frequenz $\\omega(\\mathrm{Hz})$')
    plt.ylabel('Übertragungsfunktion $H(\\mathrm{dB})$')
    plt.xscale('log')
    plt.grid()
    plt.legend()
    plt.show()

    Delta_phi_rad = Delta_phi * np.pi / 180
    delta_phi_rad = delta_phi * np.pi / 180

    def model(x, a, b):
        return a * x + b

    x = omega[3:-3]
    y = Delta_phi_rad[3:-3]
    popt, pcov = opt.curve_fit(model, x, y)
    omega_g = opt.fsolve(model, x0=10 * 3, args=(popt[0], popt[1] - np.pi/4))[0]
    omegap = opt.fsolve(model, omega_g, args=(popt[0] + np.sqrt(pcov[0, 0]), popt[1] + np.sqrt(pcov[1, 1]) - np.pi/4))[0]
    omegam = opt.fsolve(model, omega_g, args=(popt[0] - np.sqrt(pcov[0, 0]), popt[1] - np.sqrt(pcov[1, 1]) - np.pi/4))[0]
    delta_omega_g = np.abs((omegap - omegam) / 2)
    omega_g_r, delta_omega_g_r = sci_round(omega_g, delta_omega_g)
    print('Grenzfrequenz:', omega_g_r, '±', delta_omega_g_r)

    plt.errorbar(omega, Delta_phi_rad, xerr=delta_omega, yerr=delta_phi_rad, label='Messwerte', fmt='.', color='blue', capsize=5)
    plt.plot(x, model(x, *popt), color='red', label='lineare Näherung im Grenzbereich', zorder=10, linewidth=2)
    plt.plot([omega_g, omega_g], [np.pi/8, np.pi * 3/8], label=f'Grenzfrequenz $\\omega_g = {omega_g_r}$', color='green', zorder=5)
    plt.plot([omega_g + delta_omega_g, omega_g + delta_omega_g_r], [np.pi/8, np.pi * 3/8], label=f'$\\delta \\omega_g = {delta_omega_g_r}$', color='green', zorder=5, linestyle='dashed')
    plt.plot([omega_g - delta_omega_g, omega_g - delta_omega_g_r], [np.pi/8, np.pi * 3/8], color='green', zorder=5, linestyle='dashed')
    plt.xlabel('Frequenz $\\omega(\\mathrm{Hz})$')
    plt.ylabel('Phasenverschiebung $\\Delta \\varphi$')
    plt.xscale('log')
    plt.yticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2], ['$0$', '$\\pi/8$', '$\\pi/4$', '$3\\pi/8$', '$\\pi/2$'])
    plt.grid(True)
    plt.legend()
    plt.show()
