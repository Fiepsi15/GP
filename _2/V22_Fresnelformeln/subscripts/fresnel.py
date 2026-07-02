import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from scrips.tools import sci_round


def reflexion_s(alpha, n1, n2):
    numerator = n1 * np.cos(alpha) - np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    denominator = n1 * np.cos(alpha) + np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    return numerator / denominator


def transmission_s(alpha, n1, n2):
    numerator = 2 * n1 * np.cos(alpha)
    denominator = n1 * np.cos(alpha) + np.sqrt(n2 ** 2 - n1 ** 2 * np.sin(alpha) ** 2)
    return numerator / denominator


def reflexion_p(alpha, n1, n2):
    numerator = n2 * np.cos(alpha) - n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha)) ** 2)
    denominator = n2 * np.cos(alpha) + n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha) ** 2))
    return numerator / denominator


def transmission_p(alpha, n1, n2):
    numerator = 2 * n1 * np.cos(alpha)
    denominator = n2 * np.cos(alpha) + n1 * np.sqrt(1 - (n1 / n2 * np.sin(alpha)) ** 2)
    return numerator / denominator


def fresnel_rechnung(theta, pReflexion_p, pReflexion_s, pTransmission_p, pTransmission_s, referenz_p, referenz_s):


    return


def transmission_an_duenner_glasplatte():
    n_a = 1
    n_g = 1.5

    alpha = np.linspace(0, np.pi / 2, 100)
    beta = np.arcsin(n_a / n_g * np.sin(alpha))
    Tg = (n_g * np.cos(beta)) / (n_a * np.cos(alpha)) * transmission_p(alpha, n_a, n_g) ** 2
    Ta = (n_a * np.cos(alpha)) / (n_g * np.cos(beta)) * transmission_p(beta, n_g, n_a) ** 2

    fig, ax = plt.subplots()
    ax.plot(np.rad2deg(alpha), Tg, label='Erste Transmission', color='blue')
    ax.plot(np.rad2deg(alpha), Tg * Ta, label='Zweite Transmission', color='green', ls='--')
    ax.set(ylim=(0, 1))
    ax.tick_params(axis='both', which='major', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return
