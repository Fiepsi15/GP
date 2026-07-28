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
    I = b[0] * d[0] ** 3 / 12
    dI = np.sqrt((d[0] ** 3 / 12 * b[1]) ** 2
                 + (b[0] * d[0] ** 2 / 4 * d[1]) ** 2)
    return I, dI


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
    y_err = np.full_like(distance, 1e-3 / 200)
    popt, pcov = optimize.curve_fit(model, x, y) # , sigma=y_err, absolute_sigma=True)
    a, b = popt
    da, db = np.sqrt(np.diag(pcov))
    a_r = sci_round(a, da)

    #print(f'Fit: a = {a_r[0]} +- {a_r[1]}')

    fig, ax = plt.subplots()
    ax.errorbar(x, y * 1e3, xerr=np.full_like(force, 2.34 * 5 / 1024), yerr=y_err * 1e3, label='Messwerte', fmt='o', color='blue', capsize=5)
    #ax.errorbar(x, y * 1e3, label='Messwerte', fmt='o', color='blue', capsize=5)
    ax.plot(x, model(x, a, b) * 1e3, label='Fit: $w = a \\cdot F$', color='red')
    ax.fill_between(x, (model(x, a, b) + delta_model(x, (a, da), (b, db))) * 1e3,
                    (model(x, a, b) - delta_model(x, (a, da), (b, db))) * 1e3, label='Unsicherheit', alpha=0.2,
                    color='red')
    ax.set(xlabel='$F\\, \\mathrm{[N]}$', ylabel='$d\\, \\mathrm{[mm]}$', title='Biegung eines Balkens')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return a, da, ax


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

    a_list = []
    for reihe in daten:
        a = regression(reihe)
        a_list.append(a)
    a_list = np.array(a_list)

    E_list = []
    s = 'dünn'
    for i in range(2):
        for j in range(2):
            parameter = Datenbank_statisch[f'Alu_{s}']
            L = parameter['l_ges'], 1e-3
            breite = parameter['b'], 0.5e-3
            dicke = parameter['d'], 0.05e-3
            I = Traegheitsmoment(breite, dicke)
            E = get_E_from_factor(a_list[2 * i + j], L, I)
            E_list.append(E)
        s = 'dick'
    E_list = np.array(E_list) / 1e9

    for E in E_list:
        E_r = sci_round(E[0], E[1])
        print(f'E_mod = {E_r[0]} +- {E_r[1]} GPa')

    plt.show()
    return


def stahl(data_dir, strength_list):
    daten = []
    for strength in strength_list:
        daten_reihe_vor = np.loadtxt(f'{data_dir}/Stahl_{strength}mum.csv', skiprows=4, delimiter=',', unpack=True,
                                     max_rows=10)
        daten_reihe_rueck = np.loadtxt(f'{data_dir}/Stahl_{strength}mum.csv', skiprows=17, delimiter=',', unpack=True,
                                       max_rows=10)
        daten.append(daten_reihe_vor)
        daten.append(daten_reihe_rueck)
    daten = np.array(daten)

    daten[:, 0] = daten[:, 0] / 1000
    daten[:, 1] = daten[:, 1] * (5 / 1024)

    a_list = []
    for reihe in daten:
        a = regression(reihe)
        a_list.append(a)
    a_list = np.array(a_list)

    E_list = []
    s = 'dünn'
    for i in range(2):
        for j in range(2):
            parameter = Datenbank_statisch[f'Stahl_{s}']
            L = parameter['l_ges'], 1e-3
            breite = parameter['b'], 0.5e-3
            dicke = parameter['d'], 0.05e-3
            I = Traegheitsmoment(breite, dicke)
            E = get_E_from_factor(a_list[2 * i + j], L, I)
            E_list.append(E)
        s = 'dick'
    E_list = np.array(E_list) / 1e9

    for E in E_list:
        E_r = sci_round(E[0], E[1])
        print(f'E_mod = {E_r[0]} +- {E_r[1]} GPa')

    plt.show()
    return


def kupfer(data_dir):
    daten_vor = np.loadtxt(f'{data_dir}/Cu_500mum.csv', skiprows=4, delimiter=',', unpack=True, max_rows=10)
    daten_nach = np.loadtxt(f'{data_dir}/Cu_500mum.csv', skiprows=17, delimiter=',', unpack=True, max_rows=10)
    daten = np.array([daten_vor, daten_nach])

    daten[:, 0] = daten[:, 0] / 1000
    daten[:, 1] = daten[:, 1] * (5 / 1024)

    a_list = []
    for reihe in daten:
        a = regression(reihe)
        a_list.append(a)
    a_list = np.array(a_list)

    E_list = []
    for i in range(2):
        parameter = Datenbank_statisch[f'Kupfer']
        L = parameter['l_ges'], 1e-3
        breite = parameter['b'], 0.5e-3
        dicke = parameter['d'], 0.05e-3
        I = Traegheitsmoment(breite, dicke)
        E = get_E_from_factor(a_list[i], L, I)
        E_list.append(E)
    E_list = np.array(E_list) / 1e9

    for E in E_list:
        E_r = sci_round(E[0], E[1])
        print(f'E_mod = {E_r[0]} +- {E_r[1]} GPa')

    plt.show()

    return


def analyze(data_dir, metall, strength_list):
    print(f'\nMetall: {metall}')
    if metall == 'Alu':
        alu(data_dir, strength_list)
        return
    if metall == 'Stahl':
        stahl(data_dir, strength_list)
        return
    kupfer(data_dir)
    return


