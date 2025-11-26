import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def feldstaerke(Feldstaerkewerte: np.ndarray, t_u_30: np.ndarray, shared_tau_30_Cu_1mm_BBB: tuple[float, float]):
    tau_1mm, tau_1mm_err = shared_tau_30_Cu_1mm_BBB
    Feldstaerke = np.array([445, 394, 353, 298]) * 1e-3

    t_g = np.array([Feldstaerkewerte[0], Feldstaerkewerte[1], Feldstaerkewerte[2]])
    t_u = t_u_30

    tau = np.zeros(len(t_g) + 1)
    tau_err = np.zeros(len(t_g) + 1)
    tau[0] = tau_1mm
    tau_err[0] = tau_1mm_err
    for i in range(len(t_g)):
        tau[i + 1], tau_err[i + 1] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u)

    print('\nTau bei Feldstärke:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        F, _ = sci_round(Feldstaerke[i], Feldstaerke[i] * 0.05)
        print(f'Bei F = {F} ist τ = {tau_r} ± {tau_err_r}')

    def model(x, a, b, c):
        return a * x ** 2 + b * x + c

    x = 1 / Feldstaerke
    popt, pcov = curve_fit(model, x, tau, sigma=tau_err, absolute_sigma=True)
    a, b, c = popt
    a_err, b_err, c_err = np.sqrt(np.diag(pcov))

    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der linearität')
    plt.plot(x, model(x, a + a_err, b + b_err, c + c_err), linestyle=':', color='gray', label='Fit Unsicherheit')
    plt.plot(x, model(x, a - a_err, b - b_err, c - c_err), linestyle=':', color='gray')

    plt.errorbar(x, tau, yerr=tau_err, fmt='o', capsize=5, label='$\\tau$')
    plt.ylabel('Zeitkonstante $\\tau$ in s')
    plt.xlabel('Feldstärke $\\frac{1}{B}$ in $\\frac{m}{A}$')
    plt.ylim(0, 0.3)
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return
