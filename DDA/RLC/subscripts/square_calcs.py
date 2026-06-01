import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from DDA.RLC.subscripts import shared


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

    # FT
    f, Pxx_den_e = signal.welch(Ue, fs, nperseg=1024)
    _, Pxx_den_LC = signal.welch(U_LC, fs, nperseg=1024)

    # Abziehen der Schwingungskomponenten der Rechteckwelle
    i_0 = shared.max_index(Pxx_den_e)
    P_e_max = Pxx_den_e[i_0]
    free_dampened = np.abs(Pxx_den_LC - Pxx_den_e * (Pxx_den_LC[i_0] / P_e_max))

    nu_0 = np.average(f, weights=free_dampened) # Erwartungswert zeigt die Eigenfrequenz
    print(f'Eigenfrequenz aus Square (gedämpft): {nu_0}')
    nu_prime = np.sqrt(1 / (L * C) - (R / (2 * L)) ** 2) / (2 * np.pi)
    print(f'Theorie: {nu_prime}')

    # Plotting
    plt.plot(f, Pxx_den_e, label='$FT[U_e](\\nu)/\\mathrm{Hz}$')
    plt.plot(f, Pxx_den_LC, label='$FT[U_R](\\nu)/\\mathrm{Hz}$')
    plt.xlim(-10, 200)
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()

    plt.plot(f, free_dampened, label='Free Oscillation')
    plt.xlim(-10,250)
    plt.legend()
    plt.grid()
    plt.show()

    fig, ax = plt.subplots()

    ax.plot(time, Ue)
    ax.plot(time, U_LC)
    ax.set(xlim=(1.78, 1.93))
    ax.grid()
    plt.show()

    return
