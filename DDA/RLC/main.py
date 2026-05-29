import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

data_directory = 'DDA/RLC/data/'


def square_wave():
    square_waveform_data = np.loadtxt(data_directory + 'Square_220µF_10Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                                      delimiter='\t').transpose()
    print(square_waveform_data.shape)
    time = square_waveform_data[0]
    Ue = square_waveform_data[1]
    U_R = square_waveform_data[2]

    R = 5  # Ohm

    I = U_R / R

    fig, ax = plt.subplots()

    plrange = 200

    ax.plot(time[:plrange], Ue[:plrange])
    ax.plot(time[:plrange], U_R[:plrange])
    plt.show()


def sweep():
    sweep_data = np.loadtxt(data_directory + 'Sweep_150µF_10Hz_250Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                            delimiter='\t').transpose()
    print(sweep_data.shape)
    time = sweep_data[0]
    Ue = sweep_data[1]
    U_R = sweep_data[2]

    R = 5  # Ohm

    I = U_R / R

    U_ana = signal.hilbert(Ue)
    I_ana = signal.hilbert(I)
    U_amp = np.abs(U_ana)
    I_amp = np.abs(I_ana)

    Z = U_amp / I_amp

    fig, ax = plt.subplots()

    plrange = 200
    ax.plot(time[:plrange], Ue[:plrange])
    ax.plot(time[:plrange], U_amp[:plrange])
    plt.show()


sweep()
