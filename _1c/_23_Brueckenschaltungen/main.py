import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poggendorf as pogg
import _1c._23_Brueckenschaltungen.subscripts.potitransform as ptt
import _1c._23_Brueckenschaltungen.daten as data


poggendorf = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Poggendorf_Messreihe.csv', skiprows=1, delimiter=',').transpose()
print(poggendorf)
poggendorf[1], poggendorf_err = ptt.poti_transform_2(poggendorf[1])
U_B, alpha_err = pogg.poggendorf(poggendorf[0], poggendorf[1], poggendorf_err)
print(U_B, alpha_err)