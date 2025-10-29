import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poti_kalibrierung as potik
import _1c._23_Brueckenschaltungen.subscripts.poggendorf as pogg
import _1c._23_Brueckenschaltungen.daten as data

potis = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/poti_kalibrierung.csv', skiprows=1, delimiter=',').transpose()
(poti_1_slope, poti_1_slope_err), (poti_1_intercept, poti_1_intercept_err) = potik.poti_kalibrierung(potis[0], potis[1])
#print(poti_1_slope, poti_1_slope_err, poti_1_intercept, poti_1_intercept_err)
(poti_2_slope, poti_2_slope_err), (poti_2_intercept, poti_2_intercept_err) = potik.poti_kalibrierung(potis[0], potis[2])
#print(poti_2_slope, poti_2_slope_err, poti_2_intercept, poti_2_intercept_err)
(poti_3_slope, poti_3_slope_err), (poti_3_intercept, poti_3_intercept_err) = potik.poti_kalibrierung(potis[0], potis[3])
#print(poti_3_slope, poti_3_slope_err, poti_3_intercept, poti_3_intercept_err)

poggendorf = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Poggendorf_Messreihe.csv', skiprows=1, delimiter=',').transpose()
print(poggendorf)
U_B, alpha_err = pogg.poggendorf(poggendorf[0], poggendorf[1])
print(U_B, alpha_err)