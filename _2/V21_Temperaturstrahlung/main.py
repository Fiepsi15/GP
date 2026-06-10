import numpy as np
from scrips.tools import sci_round
from matplotlib import pyplot as plt
from _2.V21_Temperaturstrahlung.subscripts import leslie
from _2.V21_Temperaturstrahlung.subscripts import distance
from _2.V21_Temperaturstrahlung.subscripts import stefan_boltzmann
from _2.V21_Temperaturstrahlung.subscripts import pyrometrie

data_directory = 'data/'


def run_leslie_cube(directory):
    data = np.loadtxt(directory + 'leslie.csv', skiprows=1, delimiter=',').transpose()
    Temperatur = data[1]  # in °C
    Schwarz = data[2]  # in V
    Weiss = data[3]  # in V
    Matt = data[4]  # in V
    Verspiegelt = data[5]  # in V
    delta_relative = 0.1

    leslie.emissionsvermoegen(Temperatur, Schwarz, Weiss, Matt, Verspiegelt, delta_relative)
    return


def run_distance_dependence(data_directory):
    fig, ax = plt.subplots(2, 1, figsize=(8, 8))
    fig.subplots_adjust(top=0.9, bottom=0.1, hspace=0.3)
    fig.suptitle('Distanzabhängigkeit der Strahlungsintensität')

    print(f'\nDistanzabhängigkeit:')

    data = np.loadtxt(data_directory + 'distanzabhängigkeit_reihe_1.csv', skiprows=1, delimiter=',').transpose()
    r = data[0] / 1e3  # Distanz in m
    delta_r = np.full_like(r, 1e-3)
    U = data[1] / 1e3  # Spannung in V
    delta_U = 0.1 * U
    n_1, delta_n_1 = distance.distance_dependence(r, U, ax[0], 1, delta_r, delta_U)

    data = np.loadtxt(data_directory + 'distanzabhängigkeit_reihe_2.csv', skiprows=1, delimiter=',').transpose()
    r = data[0] / 1e3  # Distanz in m
    U = data[1] / 1e3  # Spannung in V
    n_2, delta_n_2 = distance.distance_dependence(r, U, ax[1], 2, delta_r, delta_U)

    n = np.mean([n_1, n_2])
    delta_n = 1 / 2 * np.sqrt(delta_n_1 ** 2 + delta_n_2 ** 2)
    n_r, delta_n_r = sci_round(n, delta_n)
    print(f'Im Mittel: {n_r} ± {delta_n_r}\n---')

    # t = np.linspace(0.25, 0.5, 100)
    # ax = ax[2]
    # ax.plot(t, t ** n, label='Resultierende Kurve für den Mittelwert', color='red')
    # ax.plot(t, t ** -2, label='$1 / r^2$', ls='--', color='blue')
    # ax.fill_between(t, t ** (n - delta_n), t ** (n + delta_n), color='red', alpha=0.2, label='Unsicherheit')
    # ax.set(xlabel='$r/\\mathrm{m}$', ylabel='$U/\\text{Arbitrary}$', title=f'Mittelwert')
    # ax.tick_params(axis='both', direction='in', which='both')
    # ax.minorticks_on()
    # ax.legend()
    # ax.grid()
    plt.show()

    return n, delta_n


def run_stefan_boltzmann(directory):
    data = np.loadtxt(directory + 'Stefan_Boltzmann.csv', skiprows=1, delimiter=',')[2:].transpose()
    T = data[0] + 273.15  # in K
    delta_T = 0.3  # K
    U = data[2] / 1e3  # in V
    delta_U = 0.1 * U
    A_blende = np.pi * (19.9 * 1e-3 / 2) ** 2  # pi * (d/2)^2 in m^2
    d_Ab = 0.05 * 1e-3  # m
    A_strahler = np.pi * (19.5 * 1e-3 / 2) ** 2  # pi * (d/2)^2 in m^2
    d_As = 0.1 * 1e-3  # m
    r = 0.5  # m
    d_r = 1e-3  # m

    stefan_boltzmann.stefan_boltzmann_konstante(T, delta_T, U, delta_U, A_blende, d_Ab, A_strahler, d_As, r, d_r)

    return


def messunsicherheit_pyrometer(T):
    delta_T = np.zeros_like(T)
    for i in range(len(T)):
        dT1 = 4
        if T[i] < 1500:  # 1500°C
            dT2 = 0.005 * T[i]
        else:
            dT2 = 0.0075 * T[i]
        delta_T[i] = max(dT1, dT2)
    return delta_T


def run_pyrometrie(directory):
    data = np.loadtxt(directory + 'pyrometer.csv', skiprows=1, delimiter=',')[4:].transpose()
    U = data[0]  # in V
    delta_U = 0.1 * U
    I = data[1]  # in A
    delta_I = 0.1 * I
    T = data[2]  # in °C
    delta_T = messunsicherheit_pyrometer(T)
    T = T + 273.15  # in K

    pyrometrie.temperature_proportionality_order(T, U, I, delta_T, delta_U, delta_I)


run_leslie_cube(data_directory)
run_distance_dependence(data_directory)
run_stefan_boltzmann(data_directory)
run_pyrometrie(data_directory)
