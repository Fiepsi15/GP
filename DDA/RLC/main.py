import numpy as np
import matplotlib.pyplot as plt
from DDA.RLC.subscripts.sweep_calcs import sweep
from scipy import signal

data_directory = 'DDA/RLC/data/'


def square_wave():
    square_waveform_data = np.loadtxt(data_directory + 'Square_220µF_10Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                                      delimiter='\t').transpose()
    time = square_waveform_data[0]
    Ue = square_waveform_data[1] - 2.5
    U_LC = square_waveform_data[2] - 2.5
    U_R = Ue - U_LC
    fs = 2000

    R = 5  # Ohm

    I = U_R / R

    f, Pxx_den_e = signal.welch(Ue, fs, nperseg=1024)
    plt.plot(f, Pxx_den_e, label='$FT[U_e](\\nu)/\\mathrm{Hz}$')
    f, Pxx_den_R = signal.welch(U_R, fs, nperseg=1024)
    plt.plot(f, Pxx_den_R, label='$FT[U_R](\\nu)/\\mathrm{Hz}$')
    plt.xlim(-10,200)
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()
    i_0 = 0
    P_max = 0
    for i in range(len(f)):
        if Pxx_den_e[i] > P_max:
            P_max = Pxx_den_e[i]
            i_0 = i
    Einschwingung = Pxx_den_R - Pxx_den_e * (Pxx_den_R[i_0] / P_max)
    plt.plot(f, Einschwingung, label='Overswing')
    plt.xlim(-10,250)
    plt.legend()
    plt.grid()
    plt.show()
    nu_0 = 0
    P_max = 0
    for i in range(len(f)):
        if Einschwingung[i] > P_max:
            P_max = Einschwingung[i]
            nu_0 = f[i]
    print(f'Eigenfrequenz aus Square (gedämpft): {nu_0}')

    fig, ax = plt.subplots()

    plrange = 400

    ax.plot(time[:plrange], Ue[:plrange])
    ax.plot(time[:plrange], U_R[:plrange])
    plt.show()



square_wave()
sweep(220, 2000, data_directory)
