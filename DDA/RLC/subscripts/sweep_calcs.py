import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import optimize
from scrips.tools import sci_round


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

    f, Pxx_den = signal.welch(I, fs, nperseg=1024)
    plt.plot(f, Pxx_den, label='$FT[I](\\nu)/\\mathrm{Hz}$')
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()
    nu_0 = 0
    P_max = 0
    for i in range(len(f)):
        if Pxx_den[i] > P_max:
            P_max = Pxx_den[i]
            nu_0 = f[i]
    print(f'Measured resonance frequency from FT: {nu_0} Hz')

    # Hilbert-Transformationen und Extraktion von Amplitude und Phasendifferenz
    U_ana = signal.hilbert(Ue)
    I_ana = signal.hilbert(I)
    U_amp = np.abs(U_ana)
    I_amp = np.abs(I_ana)
    frequency = np.diff(np.unwrap(np.angle(U_ana))) * fs / (2 * np.pi)
    phase_diff = np.unwrap(np.angle(U_ana)) - np.unwrap(np.angle(I_ana))

    Z = U_amp / I_amp  # Berechnung der Impedanz

    # Herausfiltern der Schwankungen der Hilbert-Transformation zur vereinfachten Detektierung des Frequenzsprungs
    sampling_width = 100
    compressed_time = np.array([time[i * sampling_width] for i in range(len(time) // sampling_width)])
    smoothed_I = smooth_curves(I_amp, sampling_width)
    smoothed_Z = smooth_curves(Z, sampling_width)
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

    smoothed_phase_diff = smoothed_phase_diff - (np.mean(smoothed_phase_diff) // (2 * np.pi) * (2 * np.pi))

    # Bestimmen der Resonanzfrequenz anhand der Phasenverschiebung
    i_0 = 0
    nu_0 = 0
    for i in range(1, len(smoothed_phase_diff)):
        if (smoothed_phase_diff[i] * smoothed_phase_diff[i - 1]) < 0:
            i_0 = i - 1
            break

    print(f'Time of resonance: {compressed_time[i_0]}')
    nu_0 = smoothed_frequency[i_0]
    print(f'Resonance frequency: {nu_0}')
    print(f'Theoretical value from param.: {1 / np.sqrt(L * C) / (2 * np.pi)}')

    # Bestimmen von R, C und L
    R_exp = np.min(smoothed_Z)
    print(f'Measured resistance of the setup: {R_exp}')
    C_exp, d_C_exp = capacitance_regression(smoothed_frequency[:i_0 // 4], smoothed_Z[:i_0 // 4])
    C_r, d_C_r = sci_round(C_exp, d_C_exp)
    print(f'Measured Capacitance: {C_r} pm {d_C_r}')
    L_exp, d_L_exp = inductance_regression(smoothed_frequency[i_0 * 2:], smoothed_Z[i_0 * 2:])
    L_r, d_L_r = sci_round(L_exp, d_L_exp)
    print(f'Measured Inductance: {L_r} pm {d_L_r}')

    # Plotting
    theo_imp, d_theo_imp = theoretical_impedance(omega=smoothed_frequency * 2 * np.pi, r=R + R_L, l=L, c=C,
                                                 d_r=0.1 * (R + R_L), d_l=0.1 * L, d_c=0.1 * C)
    exp_imp_param, d_exp_imp = theoretical_impedance(omega=smoothed_frequency * 2 * np.pi, r=R_exp, l=L_exp, c=C_exp,
                                                     d_r=0.1 * R_exp, d_l=d_L_exp, d_c=d_C_exp)
    theo_curr = np.mean(U_amp) / theo_imp
    exp_curr = np.mean(U_amp) / exp_imp_param
    theo_phase = np.arctan((smoothed_frequency * 2 * np.pi * L - 1 / (smoothed_frequency * 2 * np.pi * C)) / (R + R_L))
    exp_phase = np.arctan(
        (smoothed_frequency * 2 * np.pi * L_exp - 1 / (smoothed_frequency * 2 * np.pi * C_exp)) / R_exp)

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    ax[0, 0].plot(smoothed_frequency, smoothed_I, color='red', label='Gemessen')
    ax[0, 0].plot([nu_0, nu_0], [smoothed_I[i_0] * 0.8, smoothed_I[i_0] * 1.2])
    ax[0, 0].plot(smoothed_frequency, theo_curr, color='blue', label='Theoretische param.')
    ax[0, 0].plot(smoothed_frequency, exp_curr, color='green', label='exp. param.')
    ax[0, 0].set(ylabel='$I_R / \\mathrm{A}$', title='Stromstärke')

    ax[0, 1].plot(smoothed_frequency, smoothed_Z, color='red', label='Gemessen')
    ax[0, 1].plot(smoothed_frequency, theo_imp, color='blue', label='Theoretische param')
    ax[0, 1].fill_between(smoothed_frequency, theo_imp + d_theo_imp, theo_imp - d_theo_imp, color='blue', alpha=0.2)
    ax[0, 1].plot(smoothed_frequency, exp_imp_param, color='green', label='exp. param.')
    ax[0, 1].fill_between(smoothed_frequency, exp_imp_param + d_exp_imp, exp_imp_param - d_exp_imp, color='green',
                          alpha=0.2)
    ax[0, 1].plot([nu_0, nu_0], [0, smoothed_Z[i_0] * 2])
    ax[0, 1].set(ylabel='$|Z| / \\mathrm{\\Omega}$', title='Impedanz')

    ax[1, 0].plot(smoothed_frequency, smoothed_phase_diff, color='red', label='Gemessen')
    ax[1, 0].plot(smoothed_frequency, theo_phase, color='blue', label='Theoretische param')
    ax[1, 0].plot(smoothed_frequency, exp_phase, color='green', label='exp. param.')
    ax[1, 0].plot([nu_0, nu_0], [-0.5, 0.5])
    ax[1, 0].plot(smoothed_frequency, np.zeros_like(smoothed_frequency), color='black', ls='-.')
    ax[1, 0].set(ylabel='$\\Delta \\varphi / \\mathrm{rad}$', ylim=(-np.pi / 2, np.pi / 2), title='Phasenverschiebung')

    ax[1, 1].plot(compressed_time, smoothed_frequency, color='orange', label='Gemessen')
    ax[1, 1].set(ylabel='$\\nu / \\mathrm{Hz}$', ylim=(0, 260), title='Frequenz')

    for a in ax:
        for x in a:
            x.legend()
            x.grid()
            x.minorticks_on()
            x.set_xlabel('$\\nu / \\mathrm{Hz}$')
    ax[1, 1].set_xlabel('$t / \\mathrm{s}$')

    plt.show()
    return
