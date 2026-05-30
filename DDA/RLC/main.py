import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

data_directory = 'DDA/RLC/data/'


def square_wave():
    square_waveform_data = np.loadtxt(data_directory + 'Square_220µF_10Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                                      delimiter='\t').transpose()
    print(square_waveform_data.shape)
    time = square_waveform_data[0]
    Ue = square_waveform_data[1] - 2.5
    U_R = square_waveform_data[2] - 2.5

    R = 5  # Ohm

    I = U_R / R

    fig, ax = plt.subplots()

    plrange = 200

    ax.plot(time[:plrange], Ue[:plrange])
    ax.plot(time[:plrange], U_R[:plrange])
    plt.show()


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


def find_cuts(phase_diff):
    '''
    Locates sudden jumps in ``phase_diff`` to identify the reset of the sweep.
    :param phase_diff: phase difference of the driving function and the oscillating current
    :return:
    '''
    cuts = []
    skip = 0
    for i in range(5, len(phase_diff)):
        if skip > 0:
            skip -= 1
            continue
        if np.abs(phase_diff[i] - phase_diff[i - 5]) > 0.5:
            cuts.append(i)
            skip = 4
    return cuts


def sweep():
    sweep_data = np.loadtxt(data_directory + 'Sweep_150µF_10Hz_250Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                            delimiter='\t').transpose()  # Load Data
    # Extract measured Quantities
    time = sweep_data[0]
    Ue = sweep_data[1] - 2.5
    U_LC = sweep_data[
               2] - 2.5  # Hier wurde versehentlich die Spannung über das LC Glied gemessen, anstatt über den Widerstand.
    U_R = Ue - U_LC  # Dies wird in dieser Zeile korrigiert

    R = 5  # Ohm

    I = U_R / R  # Berechnung der Stromstärke anhand des Widerstands.

    # Hilbert-Transformationen und Extraktion von Amplitude und Phasendifferenz
    U_ana = signal.hilbert(Ue)
    I_ana = signal.hilbert(I)
    U_amp = np.abs(U_ana)
    I_amp = np.abs(I_ana)
    frequency = np.diff(np.unwrap(np.angle(U_ana))) / (time[1] - time[0]) / (2 * np.pi)
    phase_diff = np.unwrap(np.angle(U_ana)) - np.unwrap(np.angle(I_ana)) + 2 * np.pi

    Z = U_amp / I_amp  # Berechnung der Impedanz

    # Herausfiltern der Schwankungen der Hilbert-Transformation zur vereinfachten Detektierung des Frequenzsprungs
    sampling_width = 100
    compressed_time = np.array([time[i * sampling_width] for i in range(len(time) // sampling_width)])
    smoothed_I = smooth_curves(I_amp, sampling_width)
    smoothed_Z = smooth_curves(Z, sampling_width)
    smoothed_phase_diff = smooth_curves(phase_diff, sampling_width)
    smoothed_frequency = smooth_curves(frequency, sampling_width)

    # Zuschneiden auf einen Sweep
    cuts = find_cuts(smoothed_phase_diff)
    start = cuts[0] + 1
    end = cuts[1]
    compressed_time, smoothed_I, smoothed_Z, smoothed_phase_diff, smoothed_frequency = (compressed_time[start:end] - compressed_time[start],
                                                                    smoothed_I[start:end],
                                                                    smoothed_Z[start:end],
                                                                    smoothed_phase_diff[start:end],
                                                                    smoothed_frequency[start:end])

    print(compressed_time[-1])
    i_0 = 0
    for i in range(1, len(smoothed_phase_diff)):
        if (smoothed_phase_diff[i] * smoothed_phase_diff[i - 1]) < 0:
            print(compressed_time[i])
            print(smoothed_frequency[i])
            i_0 = i



    fig, ax = plt.subplots(2, 2, figsize=(8, 7))
    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    ax[0,0].plot(smoothed_frequency, smoothed_I, color='blue', label='Gemessene Stromstärke')
    ax[0,0].plot([smoothed_frequency[i_0], smoothed_frequency[i_0]], [0, 0.15])
    ax[0,0].set_ylabel('$I_R / \\mathrm{A}$')

    ax[0,1].plot(smoothed_frequency, smoothed_Z, color='red', label='Gemessene Impedanz')
    ax[0,1].plot([smoothed_frequency[i_0], smoothed_frequency[i_0]], [0, 40])
    ax[0,1].set_ylabel('$|Z| / \\mathrm{\\Omega}$')

    ax[1,0].plot(smoothed_frequency, smoothed_phase_diff, color='green', label='Gemessene Phasendifferenz')
    ax[1,0].plot([smoothed_frequency[i_0], smoothed_frequency[i_0]], [-1, 1])
    ax[1,0].plot(smoothed_frequency, np.zeros_like(smoothed_frequency), color='black', ls='-.')
    ax[1,0].set_ylabel('$\\Delta \\varphi / \\mathrm{rad}$')
    ax[1,0].set_ylim(-np.pi / 2, np.pi / 2)
    #ax[1,0].set_xscale('log')

    ax[1,1].plot(compressed_time, smoothed_frequency, color='orange', label='Gemessene Frequenz')
    ax[1,1].set_ylabel('$\\nu / \\mathrm{Hz}$')

    for a in ax:
        for x in a:
            x.legend()
            x.grid()
            x.minorticks_on()
            x.set_xlabel('$\\nu / \\mathrm{Hz}$')
    ax[1,1].set_xlabel('$t / \\mathrm{s}$')

    plt.show()


sweep()
