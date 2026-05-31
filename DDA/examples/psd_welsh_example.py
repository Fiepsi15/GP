import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
rng = np.random.default_rng()

fs = 10e3
N = 1e5
amp = 2*np.sqrt(2)
freq = 1234.0
noise_power = 0.0001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time) + 2*amp*np.sin(2*np.pi*(freq*2)*time)
x += rng.normal(scale=np.sqrt(noise_power), size=time.shape)

p1 = plt.figure(1)
plt.plot( time, x )

p2 = plt.figure(2)
f, Pxx_den = signal.welch(x, fs, nperseg=1024)
plt.semilogy(f, Pxx_den)
plt.ylim([0.5e-4, 1])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')

plt.show()
