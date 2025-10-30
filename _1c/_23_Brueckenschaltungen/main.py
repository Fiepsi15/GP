import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poti_transform as ptt
import _1c._23_Brueckenschaltungen.subscripts.poggendorf as pogg
import _1c._23_Brueckenschaltungen.subscripts.wheatstone as wheat
import _1c._23_Brueckenschaltungen.daten as data


poggendorf = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Poggendorf_Messreihe.csv', skiprows=1, delimiter=',').transpose()
print(poggendorf)
poggendorf[1], poggendorf_err = ptt.poti_transform_2(poggendorf[1])
U_B, alpha_err = pogg.poggendorf(poggendorf[0], poggendorf[1], poggendorf_err)
print("\n", U_B, alpha_err)

wheatstone_R2 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_R2.csv', skiprows=1, delimiter=',').transpose()
print("\n", wheatstone_R2)
wheatstone_R2[1], wheatstone_R2_err = ptt.poti_transform_2(wheatstone_R2[1])
R2_x, R2_x_err = wheat.wheatstone(150, 1, wheatstone_R2[0], wheatstone_R2[1], wheatstone_R2_err)
print("\n", R2_x, R2_x_err)