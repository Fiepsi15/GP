import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, signal

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


def test(daten:np.ndarray, masse, L, b, d, l_ges):
    I = Traegheitsmoment(b, d)
    mu = masse / l_ges

    sampling_rate = 100
    shift = np.mean(daten)
    daten = daten - shift

    f, Pxx_den = signal.welch(daten, fs=sampling_rate, nperseg=1024)
    plt.semilogy(f, Pxx_den)
    plt.ylim([0.5e-4, 1])
    plt.xlim([-1, 30])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.grid()

    plt.show()
    peak_pos, _ = signal.find_peaks(Pxx_den, prominence=0.0001)
    omega = f[peak_pos[-1]] * 2 * np.pi
    print(omega)

    print(E_mod(1, L, mu, I, omega) / 1e9)
