import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from DDA.RLC.subscripts import shared
from scrips.tools import sci_round


def autocorrelation_approach(time, data, start):
    data = data - data[-1]
    autocorrelation = signal.correlate(data, data, mode='full', method='direct')
    autocorrelation = autocorrelation[len(autocorrelation) // 2:]
    peaks, _ = signal.find_peaks(-autocorrelation)
    T = time[peaks[1]] - time[peaks[0]]
    peaks, _ = signal.find_peaks(autocorrelation)
    #T = (time[peaks[1] + start] - time[start]) / 2

    return 1 / T, autocorrelation


def find_jumps(data):
    jumps = []
    wait = 0
    for i in range(len(data)):
        if wait != 0:
            wait -= 1
            continue
        if np.abs(data[i] - data[i - 5]) > 0.5:
            jumps.append(i)
            wait = 5
    return jumps


def square_wave(data_directory):
    square_waveform_data = np.loadtxt(data_directory + 'Square_220µF_10Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                                      delimiter='\t').transpose()
    time = square_waveform_data[0]
    Ue = square_waveform_data[1] - 2.5
    U_LC = square_waveform_data[2] - 2.5
    fs = 2000

    R = 5  # Ohm
    L = 15e-3
    C = 220e-6

    jumps = find_jumps(Ue)
    f = np.zeros(len(jumps) - 1)
    auto = []
    for i in range(len(jumps) - 1):
        f[i], a = autocorrelation_approach(time, U_LC[jumps[i]:jumps[i + 1]-5], jumps[i])
        auto.append(a)

    l = np.min([len(auto[i]) for i in range(len(auto))])
    auto_arr = np.zeros((len(auto), l))
    for i in range(len(auto)):
        auto_arr[i] = np.array(auto[i][:l])
    U_LC_m = np.array([(U_LC[jumps[i]:jumps[i] + l] - U_LC[jumps[i] + l]) * (-1) ** i for i in range(len(jumps) - 1)])

    auto = np.mean(auto_arr, axis=0)
    auto = auto / np.max(auto)
    U_LC_m = np.mean(U_LC_m, axis=0)


    f_bar = np.mean(f)
    f_std = np.std(f) / len(f)
    f_r, df_r = sci_round(f_bar, f_std)
    print(f'Frequenz aus Autokorrelation: {f_r} pm {df_r}\n')

    # FT
    f, Pxx_den_e = signal.welch(Ue, fs, nperseg=1024)
    _, Pxx_den_LC = signal.welch(U_LC, fs, nperseg=1024)

    # Abziehen der Schwingungskomponenten der Rechteckwelle
    i_0 = shared.max_index(Pxx_den_e)
    P_e_max = Pxx_den_e[i_0]
    free_dampened = np.abs(Pxx_den_LC - Pxx_den_e * (Pxx_den_LC[i_0] / P_e_max))

    nu_0 = np.average(f, weights=free_dampened)  # Erwartungswert zeigt die Eigenfrequenz
    d_nu_0 = np.sqrt(np.abs(np.average(f ** 2, weights=free_dampened) - nu_0 ** 2))
    nu_r, d_nu_r = sci_round(nu_0, d_nu_0)
    print(f'Eigenfrequenz aus Square (gedämpft): {nu_r} pm {d_nu_r}')
    nu_prime = np.sqrt(1 / (L * C) - (R / (2 * L)) ** 2) / (2 * np.pi)
    d_nu_prime = 1 / nu_prime * 0.1 / np.sqrt(L * C)
    nu_r, d_nu_r = sci_round(nu_prime, d_nu_prime)
    print(f'Theorie: {nu_r} pm {d_nu_r}')

    # Plotting
    plt.plot(f, Pxx_den_e, label='$FT[U_e](\\nu)/\\mathrm{Hz}$')
    plt.plot(f, Pxx_den_LC, label='$FT[U_R](\\nu)/\\mathrm{Hz}$')
    plt.xlim(-10, 200)
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()

    plt.plot(f, free_dampened, label='Leistungsdichtespektrum der freien Schwingung', color='blue')
    plt.xlabel('$f / \\mathrm{Hz}$')
    plt.ylabel('$PSD$')
    plt.xlim(-10, 250)
    plt.legend()
    plt.grid()
    plt.show()

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax2.plot(time[:l], auto, color='red')
    ax.plot(time[:l], U_LC_m, label='$U_\\mathrm{LC}$', color='blue')
    ax.tick_params(direction='in', which='both')
    ax2.tick_params(direction='in', which='both')
    ax.set(xlabel='$t / \\mathrm{s}$')
    ax.set_ylabel('$U/\\mathrm{V}$', color='blue')
    ax2.set_ylabel('Autokorrelation / a.u.', color='red')
    ax.minorticks_on()
    ax2.minorticks_on()
    ax.grid()

    fig, ax = plt.subplots()

    ax.plot(time, Ue, label='Eingangsspannung', color='orange')
    ax.plot(time, U_LC, label='Spannung $U_\\mathrm{LC}$', color='blue')
    ax.set(xlim=(time[jumps[201] - 10], time[jumps[203] - 10]), xlabel='$t / \\mathrm{s}$', ylabel='$U/\\mathrm{V}$')
    ax.minorticks_on()
    ax.tick_params(direction='in', which='both')
    ax.legend()
    ax.grid()
    plt.show()

    return
