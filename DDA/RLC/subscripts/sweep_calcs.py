import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import optimize
from scrips.tools import sci_round
from DDA.RLC.subscripts import shared


def smooth_curves(curve, averaging_width):
    '''
    Applies a moving average to the curve, and downsamples by ``averaging_width``.
    :param curve: noisy curve
    :param averaging_width: number of samples to be compressed into one
    :return: the smoothed curve
    '''
    new_length = len(curve) // averaging_width
    smoothed_curve = np.zeros(new_length)
    for i in range(new_length):
        smoothed_curve[i] = np.mean(curve[i * averaging_width:(i + 1) * averaging_width])
    return smoothed_curve


def find_cuts(freq):
    '''
    Locates sudden jumps in ``frequency`` to identify the reset of the sweep.
    :param freq: frequency of the driving function
    :return:
    '''
    cuts = []
    cut = ()
    down = False
    for i in range(5, len(freq)):
        if down:
            if freq[i] - freq[i - 1] < 0:
                continue
            cut = (cut, i)
            cuts.append(cut)
            down = False
        if freq[i] - freq[i - 1] < 0:
            cut = i
            down = True
    return cuts


def theoretical_impedance(omega, r, l, c, d_r, d_c, d_l):
    Z = np.sqrt(r ** 2 + (omega * l - 1 / (omega * c)) ** 2)
    d_Z = np.sqrt((1 / Z * 2 * r * d_r) ** 2
                  + (1 / Z * 2 * (omega * l - 1 / (omega * c)) * omega * d_l) ** 2
                  + (1 / Z * 2 * (omega * l - 1 / (omega * c)) * 1 / (omega * c ** 2) * d_c) ** 2)
    return Z, d_Z


def capacitance_regression(frequency, impedance):
    def model(omega, C):
        return omega * C

    x = frequency * 2 * np.pi
    y = 1 / impedance
    popt, pcov = optimize.curve_fit(model, x, y)
    C = popt[0]
    d_c = np.sqrt(np.diag(pcov))[0]

    plt.scatter(x, y, label='Messdaten', color='blue')
    plt.plot(x, model(x, C), label='Fit', color='red')
    plt.fill_between(x, model(x, C + d_c), model(x, C - d_c), color='red', alpha=0.2)
    plt.xlabel('$\\omega / \\mathrm{rad/s}$')
    plt.ylabel('$|Z|^{-1} / \\mathrm{\\Omega}^{-1}$')
    plt.grid()
    plt.legend()
    plt.show()

    return C, d_c


def inductance_regression(frequency, impedance):
    def model(omega, L):
        return omega * L

    x = frequency * 2 * np.pi
    y = impedance
    popt, pcov = optimize.curve_fit(model, x, y)
    L = popt[0]
    d_L = np.sqrt(np.diag(pcov))[0]

    plt.scatter(x, y, label='Messdaten', color='blue')
    plt.plot(x, model(x, L), label='Fit', color='red')
    plt.fill_between(x, model(x, L + d_L), model(x, L - d_L), color='red', alpha=0.2)
    plt.xlabel('$\\omega / \\mathrm{rad/s}$')
    plt.ylabel('$|Z| / \\mathrm{\\Omega}$')
    plt.grid()
    plt.legend()
    plt.show()

    return L, d_L


def find_value(field, value):
    indices = []
    for i in range(1, len(field)):
        if (field[i] - value) * (field[i - 1] - value) < 0:
            indices.append(i - 1)
    return indices


def sweep(Capacitance, Aquisition_rate, data_directory):
    '''
    :param Capacitance: in µF
    :param Aquisition_rate: in Hz
    :return: None
    '''
    sweep_data = np.loadtxt(data_directory + f'Sweep_{Capacitance}µF_10Hz_250Hz_Aqui_{Aquisition_rate}Hz_12052026.csv',
                            skiprows=4,
                            delimiter='\t').transpose()  # Load Data

    # Extract measured Quantities
    time = sweep_data[0]
    Ue = sweep_data[1] - 2.5
    U_LC = sweep_data[2] - 2.5  # Hier wurde versehentlich die Spannung über das LC Glied gemessen,
    # anstatt über den Widerstand.
    U_R = Ue - U_LC  # Dies wird in dieser Zeile korrigiert

    R = 5  # Ohm
    R_L = 0.12  # Ohm, Widerstand der Spule
    L = 15e-3  # Henry
    C = Capacitance * 1e-6  # Farad
    fs = (len(time) - 1) / (time[-1] - time[0])  # Hz, sampling rate

    I = U_R / R  # Berechnung der Stromstärke anhand der Spannung über den Widerstand.

    # Fourier-Transformation
    _, Pxx_den_Ue = signal.welch(Ue, fs, nperseg=1024)
    f, Pxx_den_I = signal.welch(U_R, fs, nperseg=1024)
    nu_0_fourier = f[shared.max_index(Pxx_den_I)]
    d_nu_0_f = fs / len(U_R)
    nu_0_fr, d_nu_0_fr = sci_round(nu_0_fourier, d_nu_0_f)
    print(f'Measured resonance frequency from FT: {nu_0_fr} pm {d_nu_0_fr} Hz')

    # Hilbert-Transformationen und Extraktion von Amplitude und Phasendifferenz und frequenz
    U_ana = signal.hilbert(Ue)
    I_ana = signal.hilbert(I)
    U_amp = np.abs(U_ana) # Amplitude
    I_amp = np.abs(I_ana)
    frequency = np.diff(np.unwrap(np.angle(U_ana))) * fs / (2 * np.pi) # Frequenz
    phase_diff = np.unwrap(np.angle(U_ana)) - np.unwrap(np.angle(I_ana)) # Phasendifferenz

    Z = U_amp / I_amp  # Berechnung der Impedanz
    trans_func = I_amp / U_amp * R

    # Herausfiltern der Schwankungen der Hilbert-Transformation zur vereinfachten Detektierung des Frequenzsprungs und für klarere Plots
    sampling_width = 100
    compressed_time = np.array([time[i * sampling_width] for i in range(len(time) // sampling_width)])
    smoothed_I = smooth_curves(I_amp, sampling_width)
    smoothed_Z = smooth_curves(Z, sampling_width)
    smoothed_trans = smooth_curves(trans_func, sampling_width)
    smoothed_phase_diff = smooth_curves(phase_diff, sampling_width)
    smoothed_frequency = smooth_curves(frequency, sampling_width)

    # Zuschneiden auf einen Sweep
    cuts = find_cuts(smoothed_frequency)
    start = cuts[0][1]
    end = cuts[1][0]
    compressed_time, smoothed_I, smoothed_Z, smoothed_phase_diff, smoothed_frequency = (
        compressed_time[start:end] - compressed_time[start],
        smoothed_I[start:end],
        smoothed_Z[start:end],
        smoothed_phase_diff[start:end],
        smoothed_frequency[start:end])
    smoothed_trans = smoothed_trans[start:end]

    # Verschieben der Phasendifferenz um Vielfache von 2 pi um auf 0 zu zentrieren
    smoothed_phase_diff = smoothed_phase_diff - (np.mean(smoothed_phase_diff) // (2 * np.pi) * (2 * np.pi))

    # Bestimmen der Resonanzfrequenz anhand der Phasenverschiebung
    i_0 = 0
    for i in range(1, len(smoothed_phase_diff)):
        if (smoothed_phase_diff[i] * smoothed_phase_diff[i - 1]) < 0:
            i_0 = i - 1
            break

    nu_0_phase = smoothed_frequency[i_0]
    d_nu_0_p = np.abs(smoothed_frequency[i_0 + 1] - smoothed_frequency[i_0])
    nu_0_pr, d_nu_0_pr = sci_round(nu_0_phase, d_nu_0_p)
    print(f'Resonance frequency: {nu_0_pr} pm {d_nu_0_pr} Hz')
    print(f'Theoretical value from param.: {1 / np.sqrt(L * C) / (2 * np.pi)}')

    # Bestimmung des Gütefaktors
    I_hm = smoothed_I[i_0] / np.sqrt(2)
    i_minus, i_plus = find_value(smoothed_I, I_hm)
    nu_m = smoothed_frequency[i_plus]
    nu_p = smoothed_frequency[i_minus]
    dnu_m = np.abs(smoothed_frequency[i_minus + 1] - smoothed_frequency[i_minus])
    dnu_p = np.abs(smoothed_frequency[i_plus + 1] - smoothed_frequency[i_plus])
    Q = nu_0_phase / np.abs(nu_m - nu_p)
    d_Q = np.sqrt((d_nu_0_p / (nu_p - nu_m)) ** 2
                  + (Q / np.abs(nu_m - nu_p) * dnu_m) ** 2
                  + (Q / np.abs(nu_m - nu_p) * dnu_p) ** 2)
    Qr, d_Qr = sci_round(Q, d_Q)
    print(f'Gütefaktor Q: {Qr} pm {d_Qr}')
    Q_theo = 1 / (R + R_L) * np.sqrt(L / C)
    d_Q_theo = Q_theo * 0.1
    Q_r, d_Q_r = sci_round(Q_theo, d_Q_theo)
    print(f'Theo: {Q_r} pm {d_Q_r}')


    # Bestimmen von R, C und L
    #R_exp = np.min(smoothed_Z)
    #print(f'Measured resistance of the setup: {R_exp}')
    #C_exp, d_C_exp = capacitance_regression(smoothed_frequency[:i_0 // 4], smoothed_Z[:i_0 // 4])
    #C_r, d_C_r = sci_round(C_exp, d_C_exp)
    #print(f'Measured Capacitance: {C_r} pm {d_C_r}')
    #L_exp, d_L_exp = inductance_regression(smoothed_frequency[i_0 * 2:], smoothed_Z[i_0 * 2:])
    #L_r, d_L_r = sci_round(L_exp, d_L_exp)
    #print(f'Measured Inductance: {L_r} pm {d_L_r}')

    # Plotting
    ## Berechnung von Theoriekurven
    theo_imp, d_theo_imp = theoretical_impedance(omega=smoothed_frequency * 2 * np.pi, r=R + R_L, l=L, c=C,
                                                 d_r=0.1 * (R + R_L), d_l=0.1 * L, d_c=0.1 * C)
    #exp_imp_param, d_exp_imp = theoretical_impedance(omega=smoothed_frequency * 2 * np.pi, r=R_exp, l=L_exp, c=C_exp,
    #                                                 d_r=0.1 * R_exp, d_l=d_L_exp, d_c=d_C_exp)
    theo_curr = np.mean(U_amp) / theo_imp
    d_theo_curr = theo_curr * d_theo_imp / theo_imp
    #exp_curr = np.mean(U_amp) / exp_imp_param
    theo_phase = np.arctan((smoothed_frequency * 2 * np.pi * L - 1 / (smoothed_frequency * 2 * np.pi * C)) / (R + R_L))
    #d_theo_phase = 1 / (1 + (smoothed_frequency * 2 * np.pi * L - 1 / (smoothed_frequency * 2 * np.pi * C)) / (R + R_L) ** 2) * np.sqrt(
        #(smoothed_frequency / R * 0.1 * L) ** 2
        #+ (1 / (smoothed_frequency * R * C ** 2) * 0.1 * C) ** 2
        #+ ((smoothed_frequency * L - 1 / (smoothed_frequency * C)) * 0.1 / (R + R_L)) ** 2
    #)
    #exp_phase = np.arctan(
    #    (smoothed_frequency * 2 * np.pi * L_exp - 1 / (smoothed_frequency * 2 * np.pi * C_exp)) / R_exp)

    ## Plot der Fourier-Transformation
    plt.plot(f, Pxx_den_Ue, label='der Eingangsspannung $U_\\mathrm{e}$', color='orange')
    plt.plot(f, Pxx_den_I, label='der Spannung $U_\\mathrm{R}$ über $R$', color='blue')
    plt.xlabel('$f/\\mathrm{Hz}$')
    plt.ylabel('$PSD$')
    plt.title('Leistungsdichtespektrum')
    plt.xlim(0, 260)
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    fig.subplots_adjust(hspace=0.3, wspace=0.2, left=0.1, right=0.95, bottom=0.1)
    fig.suptitle(f'Getriebene Schwingung mit $C = {Capacitance} \\mathrm{'{'} \\mu F{'}'}$ und ${Aquisition_rate} \\mathrm{'{'} Hz{'}'}$ sampling Rate')

    # Stromstärke
    ax[0, 0].plot(smoothed_frequency, smoothed_I, color='red', label='Gemessen')
    ax[0, 0].plot([nu_0_phase, nu_0_phase], [smoothed_I[i_0] * 0.8, smoothed_I[i_0] * 1.2], color='green', linestyle='--', label='Resonanzfrequenz')
    ax[0, 0].plot(smoothed_frequency, theo_curr, color='blue', label='Theoriekurve')
    ax[0, 0].fill_between(smoothed_frequency, theo_curr + d_theo_curr, theo_curr - d_theo_curr, color='blue', alpha=0.2)
    #ax[0, 0].plot(smoothed_frequency, exp_curr, color='green', label='exp. param.')
    ax[0, 0].plot([smoothed_frequency[i_minus], smoothed_frequency[i_plus]], [I_hm for _ in range(2)], color='black', ls='--', label='FWHM')
    ax[0, 0].set(ylabel='$I_R / \\mathrm{A}$', title='a) Stromstärke')

    # Impedanz
    ax[0, 1].plot(smoothed_frequency, smoothed_Z, color='red', label='Gemessen')
    ax[0, 1].plot(smoothed_frequency, theo_imp, color='blue', label='Theoriekurve')
    ax[0, 1].fill_between(smoothed_frequency, theo_imp + d_theo_imp, theo_imp - d_theo_imp, color='blue', alpha=0.2)
    #ax[0, 1].plot(smoothed_frequency, exp_imp_param, color='green', label='exp. param.')
    #ax[0, 1].fill_between(smoothed_frequency, exp_imp_param + d_exp_imp, exp_imp_param - d_exp_imp, color='green',
    #                      alpha=0.2)
    ax[0, 1].plot([nu_0_phase, nu_0_phase], [0, smoothed_Z[i_0] * 2], color='green', linestyle='--', label='Resonanzfrequenz')
    ax[0, 1].set(ylabel='$|Z| / \\mathrm{\\Omega}$', title='b) Impedanz')

    # Phasendifferenz
    ax[1, 0].plot(smoothed_frequency, smoothed_phase_diff, color='red', label='Gemessen')
    ax[1, 0].plot(smoothed_frequency, theo_phase, color='blue', label='Theoriekurve')
    #ax[1, 0].fill_between(smoothed_frequency, theo_phase + d_theo_phase, theo_phase - d_theo_phase, color='blue', alpha=0.2)
    #ax[1, 0].plot(smoothed_frequency, exp_phase, color='green', label='exp. param.')
    ax[1, 0].plot([nu_0_phase, nu_0_phase], [-0.5, 0.5], color='green', linestyle='--', label='Resonanzfrequenz')
    ax[1, 0].plot(smoothed_frequency, np.zeros_like(smoothed_frequency), color='black', ls='-.', label='Nulllinie')
    ax[1, 0].set(ylabel='$\\Delta \\varphi / \\mathrm{rad}$', ylim=(-np.pi / 2, np.pi / 2), title='c) Phasenverschiebung')

    # Frequenz
    ax[1, 1].plot(compressed_time, smoothed_frequency, color='orange', label='Gemessen')
    ax[1, 1].set(ylabel='$f / \\mathrm{Hz}$', ylim=(0, 260), title='d) Frequenz')

    for a in ax:
        for x in a:
            x.legend()
            x.grid()
            x.minorticks_on()
            x.tick_params(direction='in', which='both')
            x.set(xlabel='$f / \\mathrm{Hz}$')
    ax[1, 1].set_xlabel('$t / \\mathrm{s}$')
    plt.show()

    # Bode Plot
    fig, ax = plt.subplots(2, 1, figsize=(5, 5))
    fig.subplots_adjust(hspace=0.5, wspace=0.2, left=0.15, right=0.95, bottom=0.15)
    fig.suptitle('Bode plot')

    ax[0].plot(smoothed_frequency, smoothed_trans, color='red', label='Übertragungsfunktion')
    ax[0].set(xscale='log', xlabel='$f / \\mathrm{Hz}$ (log)', ylabel='$U_R/U_e$')

    ax[1].plot(smoothed_frequency, smoothed_phase_diff, color='red', label='Phasenverschiebung')
    ax[1].set(xscale='log', xlabel='$f / \\mathrm{Hz}$ (log)', ylabel='$\\Delta \\varphi / \\mathrm{rad}$')
    for a in ax:
        a.legend()
        a.grid()
        a.tick_params(direction='in', which='both')
        a.minorticks_on()
    plt.show()


    return
