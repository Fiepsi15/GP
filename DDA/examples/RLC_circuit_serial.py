import numpy as np
import matplotlib.pyplot as plt

R1 = 5
R2 = 10
C = 10e-6
L = 10e-3

fR = 1 / (2 * np.pi * np.sqrt(L * C) )

f = np.arange(0.5, 5000.0, 0.5)
w = 2 * np.pi * f

## parallel
## Zpar = 1 / ( (1 / R2) + 1.0j * w * C + (1 / (1.0j * w * L ) ) )
## T = Zpar / ( R1 + Zpar )

## serial
Ztot =  R2 + 1 / (1.0j * w * C) + 1.0j * w * L
Zlc =   1 / (1.0j * w * C) + 1.0j * w * L
Tr = R2 / Ztot
Tlc = Zlc / Ztot

fig, (ax0, ax1) = plt.subplots(nrows=2, sharex='all', tight_layout=True)

ax0.set_title("Amplitude and Phase of a serial RLC circuit")

ax0.set_ylabel("Amplitude")
ax0.plot(f, np.abs(Tr), label=r'$|T_{R}(f)|$')
ax0.plot(f, np.abs(Tlc), label=r'$|T_{LC}(f)|$')
#ax0.plot(f, np.real(T), label=r'$\Re[T(f)]$')
ax0.legend()

ax1.set_ylabel("Phase")
ax1.set_xlabel("Frequency / (Hz)")
ax1.plot(f, np.angle(Tr), label=r'$\arg(T_{R})$')
ax1.plot(f, np.angle(Tlc), label=r'$\arg(T_{LC})$')
ax1.legend()


plt.show()
