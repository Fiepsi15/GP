import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, signal

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


def Traegheitsmoment(b, d):
    return b * d ** 3 / 12


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
    beta = c * np.pi / L
    E = mu * omega ** 2 / (I * beta ** 4)
    return E


def test(daten: np.ndarray, masse, L_einsp, b, d, l_ges, sampling_rate):
    I = Traegheitsmoment(b, d)
    mu = masse / l_ges

    shift = np.mean(daten)
    daten = daten - shift

    f, Pxx_den = signal.welch(daten, fs=sampling_rate, nperseg=1024)
    plt.semilogy(f, Pxx_den)
    plt.ylim([0.5e-4, 1])
    plt.xlim([-1, 50])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.grid()

    peak_pos, _ = signal.find_peaks(Pxx_den, prominence=0.0001)
    omega = f[peak_pos[-1]] * 2 * np.pi
    # print(f'omega = {omega}')

    E = E_mod(1, L_einsp, mu, I, omega)
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

    E = test(mess_daten[1], masse=parameter['m'], L_einsp=L, b=parameter['b'], d=parameter['d'],
             l_ges=parameter['l_ges'], sampling_rate=sampling_rate)

    plt.title(f'{metall} {staerke} bei  {einspannlaenge} mm')
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

    print(E_mods / 1e9)
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

    print(E_mods / 1e9)
    return


def kupfer(laengen, data_dir):
    E_mods = []
    for laenge in laengen:
        E = run('', 'Kupfer', laenge, data_dir)
        E_mods.append(E)
    E_mods = np.array(E_mods)

    print(E_mods / 1e9)
    return
