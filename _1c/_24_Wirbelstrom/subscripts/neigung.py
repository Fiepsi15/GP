import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def neigung(Neigungswerte: np.ndarray):
    a = np.array([48, 40.2, 30.4, 20, 10])
    alpha = np.arctan(a / 50) * 360 / (2 * np.pi)
    alpha_err = 1 / (1 + (a / 50) ** 2) * (1 / 50) * 360 / (2 * np.pi) * 0.1
    t_g = np.array([Neigungswerte[0], Neigungswerte[2], Neigungswerte[4], Neigungswerte[6], Neigungswerte[8]])
    t_u = np.array([Neigungswerte[1], Neigungswerte[3], Neigungswerte[5], Neigungswerte[7], Neigungswerte[9]])
    print(alpha)

    t_u_m = np.zeros(len(t_g))
    t_u_err = np.zeros(len(t_g))
    t_g_m = np.zeros(len(t_g))
    t_g_err = np.zeros(len(t_g))
    tau = np.zeros(len(t_g))
    tau_err = np.zeros(len(t_g))
    for i in range(len(t_g)):
        t_u_m[i], t_u_err[i], t_g_m[i], t_g_err[i], tau[i], tau_err[i] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u[i])

    t_t_tau = np.array([alpha, t_u_m, t_g_m, tau])
    t_t_tau_err = np.array([alpha_err, t_u_err, t_g_err, tau_err])
    a2t(t_t_tau, t_t_tau_err, [['$\\alpha$', '$t_u$', '$t_g$', '$\\tau$'], ['°', 's', 's', 's']],
        'Mittelwerte der ungebremsten und gebremsten Ablaufzeiten und $\\tau$', 'neigung_tau', override_row_len=3)

    print('\nTau bei Neigung:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        print(tau_r, '+-', tau_err_r)

    tau_avg, tau_std = sci_round(np.average(tau), np.std(tau))

    plt.errorbar(alpha, tau, yerr=tau_err, fmt='o', label='$\\tau$ Werte mit Fehlerbalken', capsize=5)
    plt.plot(alpha, [np.average(tau) for _ in range(len(alpha))],
             linestyle='--', color='red', label=f'Durchschnittswert: {tau_avg}s')
    plt.plot(alpha, [np.average(tau) + tau_std for _ in range(len(alpha))],
             linestyle=':', color='grey', label='Standardabweichung')
    plt.plot(alpha, [np.average(tau) - tau_std for _ in range(len(alpha))],
             linestyle=':', color='grey')
    plt.xlabel('Neigungswinkel α in °')
    plt.ylabel('Zeitkonstante τ in s')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.ylim(0, 0.05)
    plt.grid(True)
    plt.show()

    return tau[2], tau_err[2]  # Rückgabe von tau und tau_err für 30° Neigung
