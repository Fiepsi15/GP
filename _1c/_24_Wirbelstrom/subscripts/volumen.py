import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def volumen(Volumenwerte: np.ndarray, t_u_30: np.ndarray, shared_tau_30_Cu_1mm_BBB: tuple[float, float]):
    tau_1mm, tau_1mm_err = shared_tau_30_Cu_1mm_BBB
    Volumen = np.array([1e-3, 2e-3, 3e-3]) * np.pi * (20.1e-3 / 2) ** 2

    t_g = np.array([Volumenwerte[0], Volumenwerte[1]])
    t_u = t_u_30

    tau = np.zeros(len(t_g) + 1)
    tau_err = np.zeros(len(t_g) + 1)
    tau[0] = tau_1mm
    tau_err[0] = tau_1mm_err
    for i in range(len(t_g)):
        tau[i + 1], tau_err[i + 1] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u[i])

    plt.errorbar(Volumen, tau, yerr=tau_err, fmt='o', capsize=5, label='$\\tau$')
    plt.ylabel('Zeitkonstante $\\tau$ in s')
    plt.xlabel('Volumen V in $m^3$')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return
