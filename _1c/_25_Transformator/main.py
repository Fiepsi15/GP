import numpy as np
from scrips.tools import sci_round
from matplotlib import pyplot as plt
import _1c._25_Transformator.subscripts.Induktivitaet as Ind
import _1c._25_Transformator.subscripts.plots as pl
import _1c._25_Transformator.subscripts.last as last

# Induktivität 1

U_130 = np.loadtxt('_1c/_25_Transformator/daten/U_130Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, U1, U2 = U_130

L1_130, L1_130_err = Ind.get_self_inductance(130 / (2 * np.pi), 1 / (2 * np.pi), U_130[2], 0.01, U_130[1] * 1e-3, 0.1 * 1e-3)
L1_130_r, L1_130_err_r = sci_round(-np.imag(L1_130), -np.imag(L1_130_err))
#print(f'L_1_130 = {L1_130_r * -1j} ± {L1_130_err_r * 1j} H')

L_12_130 = np.array([Ind.get_gegen_inductance(130 / (2 * np.pi), U_130[3][i], U_130[1][i] * 1e-3) for i in range(len(U_130[1]))])
#print(np.array([U_130[0], L_12_130]).transpose())

pl.plot_leerlauf(U1, U2, 50, N2, 0.01, 0.01)

U_320 = np.loadtxt('_1c/_25_Transformator/daten/U_320Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, U1, U2 = U_320

L1_320, L1_320_err = Ind.get_self_inductance(320 / (2 * np.pi), 1 / (2 * np.pi), U_320[2], 0.01, U_320[1] * 1e-3, 0.1 * 1e-3)
L1_320_r, L1_320_err_r = sci_round(-np.imag(L1_320), -np.imag(L1_320_err))
#print(f'L_1_320 = {L1_320_r * -1j} ± {L1_320_err_r * 1j} H')

L_12_320 = np.array([Ind.get_gegen_inductance(320 / (2 * np.pi), U_320[3][i], U_320[1][i] * 1e-3) for i in range(len(U_320[1]))])
#print(np.array([U_320[0], L_12_320]).transpose())

pl.plot_leerlauf(U1, U2, 50, N2, 0.01, 0.01)

#plt.scatter(N2, -np.imag(L_12_130), label='L_12 bei 130 Hz')
#plt.scatter(N2, -np.imag(L_12_320), label='L_12 bei 320 Hz')
#plt.show()

I_130 = np.loadtxt('_1c/_25_Transformator/daten/I_130Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, I2, U1 = I_130

pl.plot_short(I1, I2, 50, N2, 0.01, 0.01)

L2_130 = Ind.get_self_inductance_2(L_12_130, I1, I2)
#print(L2_130)

I_320 = np.loadtxt('_1c/_25_Transformator/daten/I_320Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, I2, U1 = I_320

L2_320 = Ind.get_self_inductance_2(L_12_320, I1, I2)
#print(L2_320)

pl.plot_short(I1, I2, 50, N2, 0.01, 0.01)

kappa_130 = Ind.get_coupping_coefficient(L_12_130, L1_130, L2_130)
kappa_130_avg, kappa_130_sig = np.mean(kappa_130), np.std(kappa_130)
kappa_130_r, kappa_130_sig_r = sci_round(kappa_130_avg, kappa_130_sig)

kappa_320 = Ind.get_coupping_coefficient(L_12_320, L1_320, L2_320)
kappa_320_avg, kappa_320_sig = np.mean(kappa_320), np.std(kappa_320)
kappa_320_r, kappa_320_sig_r = sci_round(kappa_320_avg, kappa_320_sig)

print(f'{kappa_130_r} +- {kappa_130_sig_r}', f'{kappa_320_r} +- {kappa_320_sig_r}', sep='\n')

plt.plot(N2, np.real(kappa_130), 'o', label='Kopplungskoeffizient bei 130 Hz')
plt.plot(N2, np.real(kappa_320), 'o', label='Kopplungskoeffizient bei 320 Hz')
plt.legend()
plt.show()

I_130_300 = np.loadtxt('_1c/_25_Transformator/daten/I_last_300Ohm_130Hz.csv', delimiter=',', skiprows=1).transpose()
N ,I1, I2, U1 = I_130_300

last.plot_U_N_withreg(300, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L_12_130, L1_130)
last.plot_U_N_withreg_corrected(300, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L1_130, L2_130, L_12_130, 130 / (2 * np.pi))
last.plot_power(300, N, I2 * 1e-3)

I_320_300 = np.loadtxt('_1c/_25_Transformator/daten/I_last_300Ohm_320Hz.csv', delimiter=',', skiprows=1).transpose()
N ,I1, I2, U1 = I_320_300

last.plot_U_N_withreg(300, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L_12_320, L1_320)
last.plot_U_N_withreg_corrected(300, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L1_320, L2_320, L_12_320, 320 / (2 * np.pi))
last.plot_power(300, N, I2 * 1e-3)

I_130_2000 = np.loadtxt('_1c/_25_Transformator/daten/I_last_2kOhm_130Hz.csv', delimiter=',', skiprows=1).transpose()
N ,I1, I2, U1 = I_130_2000

last.plot_U_N_withreg(2000, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L_12_130, L1_130)
last.plot_U_N_withreg_corrected(2000, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L1_130, L2_130, L_12_130, 130 / (2 * np.pi))
last.plot_power(2000, N, I2 * 1e-3)

I_320_2000 = np.loadtxt('_1c/_25_Transformator/daten/I_last_2kOhm_320Hz.csv', delimiter=',', skiprows=1).transpose()
N ,I1, I2, U1 = I_320_2000

last.plot_U_N_withreg(2000, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L_12_320, L1_320)
last.plot_U_N_withreg_corrected(2000, 1, 50, N, U1, I2 * 1e-3, 0.1 * 1e-3, L1_320, L2_320, L_12_320, 320 / (2 * np.pi))
last.plot_power(2000, N, I2 * 1e-3)
