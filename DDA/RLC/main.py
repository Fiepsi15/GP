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
                            delimiter='\t').transpose() # Load Data
    # Extract measured Quantities
    time = sweep_data[0]
    Ue = sweep_data[1] - 2.5
    U_LC = sweep_data[2] - 2.5 # Hier wurde versehentlich die Spannung über das LC Glied gemessen, anstatt über den Widerstand.
    U_R = Ue - U_LC # Dies wird in dieser Zeile korrigiert

    R = 5 # Ohm

    I = U_R / R # Berechnung der Stromstärke anhand des Widerstands.

    # Hilbert-Transformationen und Extraktion von Amplitude und Phasendifferenz
    U_ana = signal.hilbert(Ue)
    I_ana = signal.hilbert(I)
    U_amp = np.abs(U_ana)
    I_amp = np.abs(I_ana)
    phase_diff = np.unwrap(np.angle(U_ana)) - np.unwrap(np.angle(I_ana)) + 2 * np.pi

    Z = U_amp / I_amp # Berechnung der Impedanz

    # Herausfiltern der Schwankungen der Hilbert-Transformation zur vereinfachten Detektierung des Frequenzsprungs
    sampling_width = 100
    compressed_time = np.array([time[i * sampling_width] for i in range(len(time) // sampling_width)])
    smoothed_I = smooth_curves(I_amp, sampling_width)
    smoothed_Z = smooth_curves(Z, sampling_width)
    smoothed_phase_diff = smooth_curves(phase_diff, sampling_width)

    cuts = find_cuts(smoothed_phase_diff)

    fig, ((ax00, ax01), (ax10, ax11)) = plt.subplots(2, 2)

    start = cuts[0] + 5
    end = cuts[1]
    print(compressed_time.shape)

    ax00.plot(compressed_time[start:end], smoothed_I[start:end], color='blue', label='Amplitude')

    ax01.plot(compressed_time[start:end], smoothed_Z[start:end], color='red', label='Impedance')

    ax10.plot(compressed_time[start:end], smoothed_phase_diff[start:end], color='green', label='Phase diff')

    ax00.legend()
    ax01.legend()
    ax10.legend()

    plt.show()



sweep()
