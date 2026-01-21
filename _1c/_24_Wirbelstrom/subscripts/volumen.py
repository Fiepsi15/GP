import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def volumen(Volumenwerte: np.ndarray, t_u_30: np.ndarray, shared_tau_30_Cu_1mm_BBB: tuple[float, float]):
    tau_1mm, tau_1mm_err = shared_tau_30_Cu_1mm_BBB
    dicke = np.array([1e-3, 2e-3, 3e-3])
    dicke_err = np.array([0.05e-3 for _ in range(len(dicke))])
    Volumen = dicke * np.pi * (20.1e-3 / 2) ** 2


    t_g = np.array([Volumenwerte[0], Volumenwerte[1]])
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

    t_t_tau = np.array([dicke, t_u_m, t_g_m, tau])
    t_t_tau_err = np.array([dicke_err, t_u_err, t_g_err, tau_err])
    a2t(t_t_tau, t_t_tau_err, [['$d$', '$t_u$', '$t_g$', '$\\tau$'], ['m', 's', 's', 's']],
        'Mittelwerte der ungebremsten und gebremsten Ablaufzeiten und $\\tau$', 'volumen_tau', override_row_len=3)

    print('\nTau bei Volumen:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        vol, _ = sci_round(1/Volumen[i], 1/Volumen[i] * 0.1)
        print(f'Bei 1/V = {vol} ist τ = {tau_r} ± {tau_err_r}')


    def model(x, a, b):
        return a * x + b

    x = 1/Volumen
    popt, pcov = curve_fit(model, x, tau, sigma=tau_err, absolute_sigma=True)
    a, b = popt
    a_err, b_err = np.sqrt(np.diag(pcov))

    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der linearität')
    plt.plot(x, model(x, a + a_err, b + b_err), linestyle=':', color='gray', label='Fit Unsicherheit')
    plt.plot(x, model(x, a - a_err, b - b_err), linestyle=':', color='gray')

    plt.errorbar(x, tau, yerr=tau_err, fmt='o', capsize=5, label='$\\tau$ Werte mit Fehlerbalken')
    plt.ylabel('Zeitkonstante $\\tau$ in s')
    plt.xlabel('Volumen $\\frac{1}{V}$ in $m^{-3}$')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return
