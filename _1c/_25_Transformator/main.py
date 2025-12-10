import numpy as np
from scrips.tools import sci_round
from matplotlib import pyplot as plt
import _1c._25_Transformator.subscripts.Induktivitaet as Ind
import _1c._25_Transformator.subscripts.plots as pl

# Induktivität 1

U_130 = np.loadtxt('_1c/_25_Transformator/daten/U_130Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, U1, U2 = U_130

L1, L1_err = Ind.get_self_inductance(130 / (2 * np.pi), 1 / (2 * np.pi), U_130[2], 0.01, U_130[1] * 1e-3, 0.1 * 1e-3)
L1_r, L1_err_r = sci_round(-np.imag(L1), -np.imag(L1_err))
#print(f'L_1_130 = {L1_r * -1j} ± {L1_err_r * 1j} H')

L_12 = np.array([Ind.get_gegen_inductance(130 / (2 * np.pi), U_130[3][i], U_130[1][i] * 1e-3) for i in range(len(U_130[1]))])
#print(np.array([U_130[0], L_12]).transpose())

pl.plot_leerlauf(U1, U2, 50, N2, 0.01, 0.01)

U_320 = np.loadtxt('_1c/_25_Transformator/daten/U_320Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N2, I1, U1, U2 = U_320

L1, L1_err = Ind.get_self_inductance(320 / (2 * np.pi), 1 / (2 * np.pi), U_320[2], 0.01, U_320[1] * 1e-3, 0.1 * 1e-3)
L1_r, L1_err_r = sci_round(-np.imag(L1), -np.imag(L1_err))
#print(f'L_1_320 = {L1_r * -1j} ± {L1_err_r * 1j} H')

L_12 = np.array([Ind.get_gegen_inductance(320 / (2 * np.pi), U_320[3][i], U_320[1][i] * 1e-3) for i in range(len(U_320[1]))])
#print(np.array([U_320[0], L_12]).transpose())

pl.plot_leerlauf(U1, U2, 50, N2, 0.01, 0.01)



I_130 = np.loadtxt('_1c/_25_Transformator/daten/I_130Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N, I1, I2, U1 = I_130

pl.plot_short(I1, I2, 50, N2, 0.01, 0.01)

I_320 = np.loadtxt('_1c/_25_Transformator/daten/I_320Hz_ohnelast.csv', delimiter=',', skiprows=1).transpose()
N, I1, I2, U1 = I_320

pl.plot_short(I1, I2, 50, N2, 0.01, 0.01)
