import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp

duration, fs = 1, 1000  # 1 s signal with sampling frequency of 400 Hz
t = np.arange(int(fs*duration)) / fs  # timestamps of samples

signal = chirp(t, 20.0, t[-1], 100.0)
signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*4.0*t) )

analytic_signal = hilbert(signal)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal))
instantaneous_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * fs

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharex='all', tight_layout=True)

ax0.set_title("Amplitude-modulated Chirp Signal")
ax0.set_ylabel("Amplitude")
ax0.plot(t, signal, label='Signal')
ax0.plot(t, amplitude_envelope, label='Envelope')
ax0.legend()

ax1.set(xlabel="Time in seconds", ylabel="Frequency in Hz", ylim=(0, 120))
ax1.plot(t[1:], instantaneous_frequency, 'C2-',
         label='Instantaneous Frequency')
ax1.legend()

ax2.set(ylabel="Instantaneous phase")
ax2.plot(t, instantaneous_phase, label='Phase')
ax2.legend()

plt.show()

