import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp

duration, fs = 1, 1000  # 1 s signal with sampling frequency of 1000 Hz
t = np.arange(0, duration, 0.001)  # timestamps of samples

print(np.size(t))

#signal = chirp(t, 20.0, t[-1], 100.0)
#signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*4.0*t) )
signal_1 = 1.0 * np.sin( 2.0 * np.pi * 4.0 * t )
signal_2 = 1.0 * np.sin( np.pi*((t - 0.5)**2) + 2.0 * np.pi * 4.0 * t  )


analytic_signal_1 = hilbert(signal_1)
analytic_signal_2 = hilbert(signal_2)

amplitude_envelope_1 = np.abs(analytic_signal_1)
amplitude_envelope_2 = np.abs(analytic_signal_2)

instantaneous_phase_1 = np.unwrap(np.angle(analytic_signal_1))
instantaneous_phase_2 = np.unwrap(np.angle(analytic_signal_2))

#instantaneous_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * fs

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, sharex='all', tight_layout=True)

ax0.set_title("Amplitude Signals")

ax0.set_ylabel("Amplitude")
#ax0.set_xlabel("Time / (s)")

ax0.plot(t, signal_1, label='Signal 1')
ax0.plot(t, amplitude_envelope_1, label='Signal 2')
ax0.legend()

ax1.plot(t, instantaneous_phase_1, label='Instantaneous Phase 1')
ax1.plot(t, instantaneous_phase_2, label='Instantaneous Phase 2')
ax1.legend()

pha_diff = ( instantaneous_phase_2 - instantaneous_phase_1 )
ax2.set(ylabel="Phase diff.")
ax2.plot(t, pha_diff, label='Phase diff.')

ax2.set(xlabel="Time / (s)")
ax2.legend()


plt.show()

