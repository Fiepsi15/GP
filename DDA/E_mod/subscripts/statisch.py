import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from scrips.tools import sci_round

Datenbank_statisch = {'Kupfer': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 27.24e-3},
                      'Stahl_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.55e-3, 'm': 26.74e-3},
                      'Stahl_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 49.13e-3},
                      'Alu_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 15.61e-3},
                      'Alu_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 2e-3, 'm': 32.08e-3}}


def Traegheitsmoment(b, d):
    return b * d ** 3 / 12


def model(px, pa, pb):
    return pa * px + pb


def delta_model(px, pa, pb):
    return np.sqrt((px * pa[1]) ** 2 + pb[1] ** 2)


def get_E_from_factor(a, L, I):
    E = (L[0] ** 3) / (48 * I[0] * a[0])
    delta_E = np.sqrt((L[0] ** 2 / (16 * a[0] * I[0]) * L[1]) ** 2
                      + (E * a[1] / a[0]) ** 2 + (E * I[1] / I[0]) ** 2)
    return E, delta_E


def regression(daten):
    sensor_factor = 2.34  # N/V
    distance = daten[0]
    voltage = daten[1]
    force = voltage * sensor_factor

    x = force
    y = distance
    # y_err = distance[1]
    popt, pcov = optimize.curve_fit(model, x, y)  # , sigma=y_err, absolute_sigma=True)
    a, b = popt
    da, db = np.sqrt(np.diag(pcov))
    a_r = sci_round(a, da)

    print(f'Fit: a = {a_r[0]} +- {a_r[1]}')

    fig, ax = plt.subplots()
    # ax.errorbar(x, y, xerr=force[1], yerr=y_err, label='Messwerte', fmt='o', color='blue', capsize=5)
    ax.errorbar(x, y * 1e3, label='Messwerte', fmt='o', color='blue', capsize=5)
    ax.plot(x, model(x, a, b) * 1e3, label='Fit: $w = a \\cdot F$', color='red')
    ax.fill_between(x, (model(x, a, b) + delta_model(x, (a, da), (b, db))) * 1e3,
                    (model(x, a, b) - delta_model(x, (a, da), (b, db))) * 1e3, label='Unsicherheit', alpha=0.2,
                    color='red')
    ax.set(xlabel='$F\\, \\mathrm{[N]}$', ylabel='$d\\, \\mathrm{[mm]}$')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return a, da


def alu(data_dir, strength_list):
    daten = []
    for strength in strength_list:
        daten_reihe_vor = np.loadtxt(f'{data_dir}/Al_{strength}mm.csv', skiprows=4, delimiter=',', unpack=True,
                                     max_rows=10)
        daten_reihe_rueck = np.loadtxt(f'{data_dir}/Al_{strength}mm.csv', skiprows=17, delimiter=',', unpack=True,
                                       max_rows=10)
        daten.append(daten_reihe_vor)
        daten.append(daten_reihe_rueck)
    daten = np.array(daten)

    daten[:, 0] = daten[:, 0] / 1000
    daten[:, 1] = daten[:, 1] * (5 / 1024)

    print(daten, '\n')

    a_list = []
    for reihe in daten:
        a = regression(reihe)
        a_list.append(a)
    a_list = np.array(a_list)

    E_thin = []
    s = 'dünn'
    for i in range(2):
        for j in range(2):
            parameter = Datenbank_statisch[f'Alu_{s}']
            L = parameter['l_ges']
            breite = parameter['b']
            dicke = parameter['d']
            I = Traegheitsmoment(breite, dicke)
            L = L, 1e-3
            I = I, 0.1 * I
            E = get_E_from_factor(a_list[2 * i + j], L, I)
            E_thin.append(E)
        s = 'dick'
    E_thin = np.array(E_thin) / 1e9

    for E in E_thin:
        E_r = sci_round(E[0], E[1])
        print(f'E_mod = {E_r[0]} +- {E_r[1]} GPa')

    plt.show()
