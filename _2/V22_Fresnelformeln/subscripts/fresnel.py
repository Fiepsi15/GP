import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from scrips.tools import sci_round


def print_round(value, label='Value', unit=''):
    val, err = sci_round(value[0], value[1])
    print(f'{label} = {val} +- {err} {unit}')
    return


def reflexion_s(alpha, n2):#, n1, n2):
    n1 = 1
    numerator = n1 * np.cos(alpha) - np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    denominator = n1 * np.cos(alpha) + np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    return (numerator / denominator) ** 2


def transmission_s(alpha, n1, n2):
    numerator = 2 * n1 * np.cos(alpha)
    denominator = n1 * np.cos(alpha) + np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    return (numerator / denominator) ** 2


def reflexion_p(alpha, n2):#, n1):
    n1 = 1
    numerator = n2 * np.cos(alpha) - n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha)) ** 2)
    denominator = n2 * np.cos(alpha) + n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha) ** 2))
    return (numerator / denominator) ** 2


def transmission_p(alpha, n1, n2):
    numerator = 2 * n1 * np.cos(alpha)
    denominator = n2 * np.cos(alpha) + n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha)) ** 2)
    return (numerator / denominator) ** 2


def fresnel_rechnung(theta, pReflexion_p, pReflexion_s, pTransmission_p, pTransmission_s, referenz_p, referenz_s):
    theta = np.deg2rad(theta)
    R_s = pReflexion_s[:-1] / referenz_s
    popt, pcov = optimize.curve_fit(reflexion_s, theta[2:-1], R_s, p0=[1.5])
    n_g = popt[0]#, n_g = popt
    dn_l = np.sqrt(np.diag(pcov)[0])#, dn_g = np.sqrt(np.diag(pcov))
    n_g = (n_g, dn_l)#, n_g = (n_l, dn_l), (n_g, dn_g)
    #print_round(n_l, label='n_Luft')
    #print_round([n_l[0], n_l[0] * 0.01], label='falsch!')
    print_round(n_g, label='n_Glasplatte')
    print_round([n_g[0], n_g[0] * 0.01], label='falsch!')
    n_l = (1, 0.1)

    alpha = np.linspace(0, np.pi / 2, 100)
    fig, ax = plt.subplots()
    ax.scatter(np.rad2deg(theta[2:-1]), R_s, label='Messwerte', color='blue')
    ax.plot(np.rad2deg(alpha), reflexion_s(alpha, n_g[0]), color='red', label='Fit')
    ax.plot(np.rad2deg(alpha), reflexion_s(alpha, 1.5), label='schätzung', color='green', ls='--')
    ax.set(ylim=(0, 1))
    ax.tick_params(axis='both', which='major', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    R_p = pReflexion_p[:-1] / referenz_p
    popt, pcov = optimize.curve_fit(reflexion_p, theta[2:-1], R_p, p0=[1.5])
    n_g = popt[0]#, n_g = popt
    dn_l = np.sqrt(np.diag(pcov)[0])#, dn_g = np.sqrt(np.diag(pcov))
    n_g = (n_g, dn_l)#, n_g = (n_l, dn_l), (n_g, dn_g)
    #print_round(n_l, label='n_Luft')
    #print_round([n_l[0], n_l[0] * 0.01], label='falsch!')
    print_round(n_g, label='n_Glasplatte')
    print_round([n_g[0], n_g[0] * 0.01], label='falsch!')
    n_l = (1, 0.1)

    alpha = np.linspace(0, np.pi / 2, 100)
    fig, ax = plt.subplots()
    ax.scatter(np.rad2deg(theta[2:-1]), R_p, label='Messwerte', color='blue')
    ax.plot(np.rad2deg(alpha), reflexion_p(alpha, n_g[0]), color='red', label='Fit')
    ax.plot(np.rad2deg(alpha), reflexion_p(alpha, 1.5), label='schätzung', color='green', ls='--')
    ax.set(ylim=(0, 1))
    ax.tick_params(axis='both', which='major', direction='in')

    n_a = 1
    n_g = 1.5

    alpha = np.linspace(0, np.pi / 2, 100)
    beta = np.arcsin(n_a / n_g * np.sin(alpha))
    Tg = (n_g * np.cos(beta)) / (n_a * np.cos(alpha)) * transmission_p(alpha, n_a, n_g)
    Ta = (n_a * np.cos(alpha)) / (n_g * np.cos(beta)) * transmission_p(beta, n_g, n_a)

    ax.plot(np.rad2deg(alpha), Tg, label='Erste Transmission', color='blue')
    ax.plot(np.rad2deg(alpha), Tg * Ta, label='Zweite Transmission', color='green', ls='--')
    ax.scatter(np.rad2deg(theta[2:-1]), 1 - R_p, label='1 - R_p', color='orange')
    T_p = pTransmission_p[:-1] / referenz_p
    ax.scatter(np.rad2deg(theta[:-1]), T_p, label='T_p', color='red')
    ax.minorticks_on()
    ax.legend()
    ax.grid()
    return


def transmission_an_duenner_glasplatte():
    n_a = 1
    n_g = 1.5

    alpha = np.linspace(0, np.pi / 2, 100)
    beta = np.arcsin(n_a / n_g * np.sin(alpha))
    Tg = (n_g * np.cos(beta)) / (n_a * np.cos(alpha)) * transmission_p(alpha, n_a, n_g)
    Ta = (n_a * np.cos(alpha)) / (n_g * np.cos(beta)) * transmission_p(beta, n_g, n_a)

    fig, ax = plt.subplots()
    ax.plot(np.rad2deg(alpha), Tg, label='Erste Transmission', color='blue')
    ax.plot(np.rad2deg(alpha), Tg * Ta, label='Zweite Transmission', color='green', ls='--')
    ax.set(ylim=(0, 1))
    ax.tick_params(axis='both', which='major', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return
