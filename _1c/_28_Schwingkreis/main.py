import numpy as np
import _1c._28_Schwingkreis.subscripts.Versuch1 as v1

Versuch1_daten = np.loadtxt('_1c/_28_Schwingkreis/daten/Versuch1.csv', skiprows=1, delimiter=',').transpose()
a, b, delta_a, delta_b = v1.linear_regression(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)

v1.logarithmic_plot(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3, a, b, delta_a, delta_b)
Lambda, delta_Lambda = v1.logarithmic_decrement(Versuch1_daten[1], Versuch1_daten[0], 1.96e-3)
