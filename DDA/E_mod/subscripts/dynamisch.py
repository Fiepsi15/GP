import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, signal
from scrips.tools import sci_round

Datenbank = {'Kupfer': {'l_ges': 319.5e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 27.17e-3},
             'Stahl_dünn': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 0.55e-3, 'm': 26.59e-3},
             'Stahl_dick': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 1e-3, 'm': 46.84e-3},
             'Alu_dünn': {'l_ges': 302e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 8.93e-3},
             'Alu_dick': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 2e-3, 'm': 32.16e-3}}


def find_sampling_rate(file):
    with open(file, 'r') as f:
        f.readline()
        f.readline()
        line = f.readline()
        words = []
        temp = ''
        for c in line:
            if c == ' ':
                words.append(temp)
                temp = ''
                continue
            temp += c
        rate = words[-1]
    return int(rate)


def find_start_index(daten):
    for i in range(len(daten)):
        if daten[i] * daten[i + 1] < 0:
            return i


def Traegheitsmoment(b, d):
    I = b[0] * d[0] ** 3 / 12
    dI = np.sqrt((d[0] ** 3 / 12 * b[1]) ** 2
                 + (b[0] * d[0] ** 2 / 4 * d[1]) ** 2)
    return I, dI


def get_c(n):
    if n == 1:
        return 0.59686
    if n == 2:
        return 1.49418
    if n == 3:
        return 2.50025
    return 3.49999


def E_mod(n, L, mu, I, omega):
    c = get_c(n)
    beta = c * np.pi / L[0]
    E = mu[0] * omega[0] ** 2 / (I[0] * beta ** 4)
    delta_E = np.sqrt((E * mu[1] / mu[0]) ** 2 + (4 * E * L[1] / L[0]) ** 2
                      + (2 * E * omega[1] / omega[0]) ** 2 + (E * I[1] / I[0]) ** 2)
    return E, delta_E


def attenuation(daten):
    def model(t, p_V0, p_gamma):
        return p_V0 * np.exp(-p_gamma * t)

    def delta_model(t, p_U0, p_gamma):
        delta = np.sqrt((np.exp(-p_gamma[0] * t) * p_U0[1]) ** 2
                        + (p_U0[0] * t * np.exp(-p_gamma[0] * t) * p_gamma[1]) ** 2)
        return delta

    time = daten[0]
    spannung = daten[1]

    spannung_ana = signal.hilbert(spannung)
    envelope = np.abs(spannung_ana)
    start, end = int(0.0 * len(envelope)), int(0.98 * len(envelope))
    time, envelope = time[start:end], envelope[start:end]

    popt, pcov = optimize.curve_fit(model, time, envelope)
    V0, gamma = popt
    d_V0, d_gamma = np.sqrt(np.diag(pcov))

    V0r = sci_round(V0, d_V0)
    gamma_r = sci_round(gamma, d_gamma)

    print(f'Attenuation: {gamma_r[0]} +- {gamma_r[1]}')

    fig, ax = plt.subplots()
    ax.plot(time, envelope, color='green', label='Messdaten')
    ax.plot(time, model(time, V0, gamma), color='red', label='Fit nach $A(t) = A_0 \\cdot \\exp(- \\delta \\cdot t)$')
    ax.fill_between(time, model(time, V0, gamma) + delta_model(time, (V0, d_V0), (gamma, d_gamma)), model(time, V0, gamma) - delta_model(time, (V0, d_V0), (gamma, d_gamma)), color='red', alpha=0.2, label='Unsicherheit')
    ax.set(xlabel='Zeit $\\mathrm{[s]}$', ylabel='Spannung $\\mathrm{[V]}$', title='Einhüllende Funktion')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    #ax.plot(time, spannung, color='red')
    ax.legend()
    ax.grid()

    return (gamma, d_gamma), (V0, d_V0)


def plot(daten):
    daten = daten[:, :int(len(daten[0])/4)]
    time = daten[0]
    spannung = daten[1]

    fig, ax = plt.subplots()
    ax.plot(time, spannung, color='red', label='Messdaten')
    ax.set(xlabel='Zeit $\\mathrm{[s]}$', ylabel='Spannung $\\mathrm{[V]}$', title='Balkenschwingung')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return


def test(daten: np.ndarray, masse, L_einsp, b, d, l_ges, sampling_rate):
    L_einsp = L_einsp, 1e-3
    b = b, 0.5e-3
    d = d, 0.05e-3
    masse = masse, 0.01e-3
    l_ges = l_ges, 0.5e-3
    I = Traegheitsmoment(b, d)
    mu = masse[0] / l_ges[0], np.sqrt((masse[1] / l_ges[0]) ** 2 + (masse[0] / l_ges[0] ** 2 * l_ges[1]) ** 2)

    shift = np.mean(daten[1])
    daten[1] = daten[1] - shift
    start = find_start_index(daten[1])
    daten = daten[:, start:]
    shift = np.mean(daten[1])
    daten[1] = daten[1] - shift
    plot(daten)

    f, Pxx_den = signal.welch(daten[1], fs=sampling_rate, nperseg=1024)
    fig, ax = plt.subplots()
    ax.semilogy(f, Pxx_den, color='blue')
    #ax.ylim([0, 1])
    #ax.xlim([0, 50])
    ax.set(title=f'Leistungsdichtespektrum der Balkenschwingung', xlabel='Frequenz $\\mathrm{[Hz]}$', ylabel='$\\mathrm{PSD}$')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.grid()

    attenuation(daten)

    peak_pos, _ = signal.find_peaks(Pxx_den, prominence=0.0001)
    omega = f[peak_pos[-1]] * 2 * np.pi
    d_omega = 2 * np.pi * sampling_rate / len(daten[1])
    omega = np.array(omega), d_omega
    # print(f'omega = {omega}')

    E = E_mod(1, L_einsp, mu, I, omega)
    E_r = sci_round(E[0]/1e9, E[1]/1e9)

    print(f'{L_einsp[0]}: E = ({E_r[0]} +- {E_r[1]}) GPa')

    return E


def run(staerke, metall, einspannlaenge, data_dir):
    mess_daten = np.zeros(0)
    fp = ''
    if staerke == 'dünn':
        fp = f'{data_dir}/Duenner-{metall}-{einspannlaenge}.txt'
        mess_daten = np.loadtxt(fp, skiprows=4, unpack=True,
                                delimiter='\t')
    elif staerke == 'dick':
        fp = f'{data_dir}/Dicker-{metall}-{einspannlaenge}.txt'
        mess_daten = np.loadtxt(fp, skiprows=4, unpack=True,
                                delimiter='\t')
    else:
        fp = f'{data_dir}/{metall}-{einspannlaenge}.txt'
        mess_daten = np.loadtxt(fp, skiprows=4, unpack=True, delimiter='\t')

    parameter = Datenbank
    if staerke != '':
        parameter = Datenbank[f'{metall}_{staerke}']
    else:
        parameter = Datenbank[metall]

    L = einspannlaenge / 1e3
    sampling_rate = find_sampling_rate(fp)

    E = test(mess_daten, masse=parameter['m'], L_einsp=L, b=parameter['b'], d=parameter['d'],
             l_ges=parameter['l_ges'], sampling_rate=sampling_rate)

    #plt.title(f'{metall} {staerke} bei  {einspannlaenge} mm')
    plt.show()

    return E


def alu(staerken, data_dir):
    E_mods = []
    for staerke in staerken:
        E_mods_s = []
        for laenge in staerke:
            E = run(laenge[0], 'Alu', laenge[1], data_dir)
            E_mods_s.append(E)
        E_mods.append(E_mods_s)
    E_mods = np.array(E_mods)

    return


def stahl(staerken, data_dir):
    E_mods = []
    for staerke in staerken:
        E_mods_s = []
        for laenge in staerke:
            E = run(laenge[0], 'Stahl', laenge[1], data_dir)
            E_mods_s.append(E)
        E_mods.append(E_mods_s)
    E_mods = np.array(E_mods)

    return


def kupfer(laengen, data_dir):
    E_mods = []
    for laenge in laengen:
        E = run('', 'Kupfer', laenge, data_dir)
        E_mods.append(E)
    E_mods = np.array(E_mods)

    return
