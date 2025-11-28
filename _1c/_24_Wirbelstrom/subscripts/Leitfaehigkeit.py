import numpy as np
from _1c._24_Wirbelstrom.subscripts.tau_solve import get_tau
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round

def get_sigma(m, tau, beta, B_0, V):
    return m / (tau * beta * B_0 ** 2 * V)

def sigma_err(m, tau, beta, B_0, V, m_err, tau_err, B_0_err, V_err):
    term1 = (m_err / (tau * beta * B_0 ** 2 * V)) ** 2
    term2 = (m * tau_err / (tau ** 2 * beta * B_0 ** 2 * V)) ** 2
    term4 = (2 * m * B_0_err / (tau * beta * B_0 ** 3 * V)) ** 2
    term5 = (m * V_err / (tau * beta * B_0 ** 2 * V ** 2)) ** 2
    return np.sqrt(term1 + term2 + term4 + term5)

def leitfaehigkeit(Leitfaehigkeitswerte: np.ndarray, t_u_30: np.ndarray, shared_tau_30_Cu_1mm_BBB: tuple[float, float]):
    m = 25.91e-3 + 30.28e-3  # Masse in kg
    m_err = np.sqrt(2) * 0.01e-3  # Unsicherheit Masse
    B0 = 0.445  # Magnetische Flussdichte in T
    B0_err = 10e-3 + 0.05 * B0  # Unsicherheit B0
    r = 20.1e-3 / 2  # Radius in m
    r_err = 0.05e-3 / 2  # Unsicherheit Radius
    d = 1e-3  # Dicke in m
    d_err = 0.05e-3  # Unsicherheit Dicke
    V = np.pi * r ** 2 * d  # Volumen in m^3
    V_err = np.sqrt((2 * np.pi * r * d * r_err) ** 2 + (np.pi * r ** 2 * d_err) ** 2)  # Unsicherheit Volumen
    beta = np.pi / 8

    tau_1mm, tau_1mm_err = shared_tau_30_Cu_1mm_BBB
    Leitfaehigkeit = np.array([6e7, 4e7, 3.2e7])#, 8.6e6])
    #Leitfaehigkeit = np.array([5.4e7, 2e7, 1.3e7])#, 8.6e6])

    t_g = np.array([Leitfaehigkeitswerte[0], Leitfaehigkeitswerte[1]])#, Leitfaehigkeitswerte[2]])
    t_u = t_u_30

    tau = np.zeros(len(t_g) + 1)
    tau_err = np.zeros(len(t_g) + 1)
    tau[0] = tau_1mm
    tau_err[0] = tau_1mm_err
    for i in range(len(t_g)):
        tau[i + 1], tau_err[i + 1] = get_tau(t_g_arr=t_g[i], t_u_arr=t_u)

    print('\nTau bei Leitfähigkeit:')
    for i in range(len(tau)):
        tau_r, tau_err_r = sci_round(tau[i], tau_err[i])
        sigma, _ = sci_round(Leitfaehigkeit[i], Leitfaehigkeit[i] * 0.05)
        print(f'Bei σ = {sigma} ist τ = {tau_r} ± {tau_err_r}')
        sigma_calc = get_sigma(m, tau[i], beta, B0, V)
        sigma_calc_err = sigma_err(m, tau[i], beta, B0, V, m_err, tau_err[i], B0_err, V_err)
        sigma_calc, sigma_calc_err = sci_round(sigma_calc, sigma_calc_err)
        print(f'Berechnete Leitfähigkeit: {sigma_calc} ± {sigma_calc_err} S/m')

    def model(x, a, b):
        return a * x + b

    x = 1 / Leitfaehigkeit
    popt, pcov = curve_fit(model, x, tau, sigma=tau_err, absolute_sigma=True)
    a, b = popt
    a_err, b_err = np.sqrt(np.diag(pcov))

    plt.plot(x, model(x, *popt), linestyle='--', color='red', label='Fit zur bewertung der linearität')
    plt.plot(x, model(x, a + a_err, b + b_err), linestyle=':', color='gray', label='Fit Unsicherheit')
    plt.plot(x, model(x, a - a_err, b - b_err), linestyle=':', color='gray')

    plt.errorbar(x, tau, yerr=tau_err, fmt='o', capsize=5, label='$\\tau$ Werte mit Fehlerbalken')
    plt.ylabel('Zeitkonstante $\\tau$ in s')
    plt.xlabel('Leitfähigkeit $\\frac{1}{\\sigma}$ in $\\frac{m}{S}$')
    plt.minorticks_on()
    plt.tick_params(which='both', direction='in', top=True, right=True)
    plt.legend()
    plt.grid(True)
    plt.show()

    return