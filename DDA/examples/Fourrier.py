import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def fourier_transform(data):
    y = data[:, 1]
    f, Pw_den = signal.welch(y, fs=1e3, nperseg=len(y))
    plt.plot(f, Pw_den)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power spectral density')
    plt.title('Fourier Transform (Welch)')
    plt.xlim(0, 16)
    plt.ylim(-0.01, 3)
    plt.show()


x = np.linspace(0, 10, 10000)
test = np.sin(2 * np.pi * 10 * x) + np.sin(2 * np.pi * 15 * x)

data = np.loadtxt('Measurement_3.txt', skiprows=4)


fourier_transform(np.array([x,test]).transpose())
fourier_transform(data)
