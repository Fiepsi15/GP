import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def neigung(Neigungswerte: np.ndarray):
    alpha = np.arctan(np.array([10, 20, 30.4, 40.2, 48]) / 50) * 360 / (2 * np.pi)
    t_g = np.array([Neigungswerte[0], Neigungswerte[2], Neigungswerte[4], Neigungswerte[6], Neigungswerte[8]])
    t_u = np.array([Neigungswerte[1], Neigungswerte[3], Neigungswerte[5], Neigungswerte[7], Neigungswerte[9]])

    tau = np.zeros(len(t_g))
    tau_err = np.zeros(len(t_g))
    for i in range(len(t_g)):
        tau[i], tau_err[i] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u[i])

    print('\nTau bei Neigung:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        print(tau_r, '+-', tau_err_r)

    tau_avg, _ = sci_round(np.average(tau), np.std(tau))

    plt.errorbar(alpha, tau, yerr=tau_err, fmt='o', label='$\\tau$ Werte mit Fehlerbalken', capsize=5)
    plt.plot(alpha, [np.average(tau) for _ in range(len(alpha))],
             linestyle='--', color='red', label=f'Durchschnittswert: {tau_avg}s')
    plt.title('3.3.1 Unabhängigkeit von der Neigung')
    plt.xlabel('Neigungswinkel α in °')
    plt.ylabel('Zeitkonstante τ in s')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.ylim(0, 0.05)
    plt.grid(True)
    plt.show()

    return tau[2], tau_err[2]  # Rückgabe von tau und tau_err für 30° Neigung
