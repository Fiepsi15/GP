import numpy as np
import _1c._28_Schwingkreis.subscripts.Versuch1 as v1
import _1c._28_Schwingkreis.subscripts.Versuch2 as v2
import _1c._28_Schwingkreis.subscripts.Versuch3 as v3

Versuch1_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Versuch1.csv', skiprows=1, delimiter=',').transpose()
a, b, delta_a, delta_b = v1.linear_regression(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)

v1.logarithmic_plot(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3, a, b, delta_a, delta_b)
Lambda, delta_Lambda = v1.logarithmic_decrement(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)

def swap_rows(matrix, col1, col2):
    h = np.copy(matrix[col1])
    matrix[col1] = matrix[col2]
    matrix[col2] = h
    return matrix

niederfrequenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/niederfrequenzbereich.csv', skiprows=1, delimiter=',').transpose()
grenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Grenzbereich.csv', skiprows=1, delimiter=',').transpose()
hochfrequenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/hochfrequenzbereich.csv', skiprows=1, delimiter=',').transpose()
hochfrequenz_daten[3] = hochfrequenz_daten[3] - 180
hochfrequenz_daten[0] = hochfrequenz_daten[0] * 1e3  # Umrechnung kHz in Hz

niederfrequenz_daten = swap_rows(niederfrequenz_daten, 1, 2)
grenz_daten = swap_rows(grenz_daten, 1, 2)

Versuch2_daten = np.concatenate((niederfrequenz_daten, grenz_daten, hochfrequenz_daten), axis=1)

omega_0, delta_omega_0 = v2.phasenverschiebung(Versuch2_daten[0], Versuch2_daten[3])

R, delta_R = v2.widerstand(grenz_daten[0], grenz_daten[1], grenz_daten[2], omega_0, delta_omega_0)

C, delta_C = v2.capacity(niederfrequenz_daten[0], niederfrequenz_daten[1], niederfrequenz_daten[2])

L, delta_L = v2.inductance(hochfrequenz_daten[0], hochfrequenz_daten[1], hochfrequenz_daten[2])

v2.gesamtbereich(Versuch2_daten[0], Versuch2_daten[1], Versuch2_daten[2], R, C, L, delta_R, delta_C, delta_L)

Versuch3_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Versuch3.csv', skiprows=1, delimiter=',').transpose()

v3.bodeplot(Versuch3_daten[0], Versuch3_daten[1], Versuch3_daten[2], Versuch3_daten[3])