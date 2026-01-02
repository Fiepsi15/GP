import numpy as np
import _1c._28_Schwingkreis.subscripts.Versuch1 as v1
import _1c._28_Schwingkreis.subscripts.Versuch2 as v2
import _1c._28_Schwingkreis.subscripts.Versuch3 as v3

Versuch1_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Versuch1.csv', skiprows=1, delimiter=',').transpose()
a, b, delta_a, delta_b = v1.linear_regression(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)

v1.logarithmic_plot(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3, a, b, delta_a, delta_b)
Lambda, delta_Lambda = v1.logarithmic_decrement(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)

niederfrequenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/niederfrequenzbereich.csv', skiprows=1, delimiter=',').transpose()
grenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Grenzbereich.csv', skiprows=1, delimiter=',').transpose()
hochfrequenz_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/hochfrequenzbereich.csv', skiprows=1, delimiter=',').transpose()
hochfrequenz_daten[0] = hochfrequenz_daten[0] * 1e3  # Umrechnung kHz in Hz

Versuch2_daten = np.concatenate((niederfrequenz_daten, grenz_daten), axis=1)
v2.gesamtbereich(Versuch2_daten[0], Versuch2_daten[1], Versuch2_daten[2])

v2.phasenverschiebung(grenz_daten[0], grenz_daten[3])

Versuch3_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Versuch3.csv', skiprows=1, delimiter=',').transpose()

v3.bodeplot(Versuch3_daten[0], Versuch3_daten[1], Versuch3_daten[2], Versuch3_daten[3])