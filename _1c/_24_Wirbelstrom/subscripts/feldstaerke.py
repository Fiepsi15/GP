import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def feldstaerke(Feldstaerkewerte: np.ndarray, t_u_30: np.ndarray, shared_tau_30_Cu_1mm_BBB: tuple[float, float]):
    tau_1mm, tau_1mm_err = shared_tau_30_Cu_1mm_BBB
    Feldstaerke = np.array([445, 394, 353, 298]) * 1e-3
    Feldstaerke_err = Feldstaerke * 0.05 + 10e-3

    t_g = np.array([Feldstaerkewerte[0], Feldstaerkewerte[1], Feldstaerkewerte[2]])
    t_u = t_u_30

    t_u_m = np.zeros(len(t_g) + 1)
    t_u_err = np.zeros(len(t_g) + 1)
    t_g_m = np.zeros(len(t_g) + 1)
    t_g_err = np.zeros(len(t_g) + 1)
    tau = np.zeros(len(t_g) + 1)
    tau_err = np.zeros(len(t_g) + 1)
    t_u_m[0] = 0.478
    t_u_err[0] = 0.016
    t_g_m[0] = 2.739
    t_g_err[0] =0.016
    tau[0] = tau_1mm
    tau_err[0] = tau_1mm_err
    for i in range(len(t_g)):
        t_u_m[i + 1], t_u_err[i + 1], t_g_m[i + 1], t_g_err[i + 1], tau[i + 1], tau_err[i + 1] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u)

    print('\nTau bei Feldstärke:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        F, _ = sci_round(Feldstaerke[i], Feldstaerke[i] * 0.05)
        print(f'Bei B = {F} ist τ = {tau_r} ± {tau_err_r}')

    t_t_tau = np.array([Feldstaerke, t_u_m, t_g_m, tau])
    t_t_tau_err = np.array([Feldstaerke_err, t_u_err, t_g_err, tau_err])
    a2t(t_t_tau, t_t_tau_err, [['$B$', '$t_u$', '$t_g$', '$\\tau$'], ['A/m', 's', 's', 's']],
        'Mittelwerte der ungebremsten und gebremsten Ablaufzeiten und $\\tau$', 'Feldstaerke_tau')

    def model(x, a, b):
        return a * x + b

    x = Feldstaerke ** 2
    y = 1 / tau
    y_err = 1 / tau ** 2 * tau_err
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    a, b = popt
    a_err, b_err = np.sqrt(np.diag(pcov))

    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der quadratischen Abhängigkeit')
    plt.plot(x, model(x, a + a_err, b + b_err), linestyle=':', color='gray', label='Fit Unsicherheit')
    plt.plot(x, model(x, a - a_err, b - b_err), linestyle=':', color='gray')

    plt.errorbar(x, y, yerr=y_err, fmt='o', capsize=5, label='$\\tau$ Werte mit Fehlerbalken')
    plt.ylabel('Zeitkonstante $\\frac{1}{\\tau}$ in s$^{-1}$')
    plt.xlabel('Feldstärke $B^2$ in $\\frac{A^2}{m^2}$')
    #plt.ylim(0, 0.3)
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return
