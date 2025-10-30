import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poti_transform as ptt
import _1c._23_Brueckenschaltungen.subscripts.poggendorf as pogg
import _1c._23_Brueckenschaltungen.subscripts.wheatstone as wheat
import scrips.tools as to
import _1c._23_Brueckenschaltungen.daten as data


poggendorf = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Poggendorf_Messreihe.csv', skiprows=1, delimiter=',').transpose()
poggendorf[1], poggendorf_err = ptt.poti_transform_2(poggendorf[1])
print("\nPoggendorf-Kompensation:\n", np.round(poggendorf, 2))
U_B, U_B_err = pogg.poggendorf(poggendorf[0], poggendorf[1], poggendorf_err)
print(U_B, U_B_err)
U_B, U_B_err = to.sci_round(U_B, U_B_err)
print("\nBatteriespannung:\nU = ", U_B, "±", U_B_err, "V")


wheatstone_R2 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_R2.csv', skiprows=1, delimiter=',').transpose()
wheatstone_R2[1], wheatstone_R2_err = ptt.poti_transform_2(wheatstone_R2[1])
print("\n------\n\nWheatstone:\nR_2:\n", np.round(wheatstone_R2, 2))
R2_x, R2_x_err = wheat.wheatstone_R(150, 1.5, wheatstone_R2[0], wheatstone_R2[1], wheatstone_R2_err)
print(R2_x, R2_x_err)
R2_x, R2_x_err = to.sci_round(R2_x, R2_x_err)
print("\nUnbekannter Widerstand R_2:\nR_x = ", R2_x, "±", R2_x_err, "Ω")

wheatstone_R5 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_R5.csv', skiprows=1, delimiter=',').transpose()
wheatstone_R5[1], wheatstone_R5_err = ptt.poti_transform_2(wheatstone_R5[1])
print("\n\nR_5:\n", np.round(wheatstone_R5, 2))
R5_x, R5_x_err = wheat.wheatstone_R(150, 1.5, wheatstone_R5[0], wheatstone_R5[1], wheatstone_R5_err)
print(R5_x, R5_x_err)
R5_x, R5_x_err = to.sci_round(R5_x, R5_x_err)
print("\nUnbekannter Widerstand R_5:\nR_x = ", R5_x, "±", R5_x_err, "Ω")

wheatstone_C1 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_C1.csv', skiprows=1, delimiter=',').transpose()
wheatstone_C1[1], wheatstone_C1_err = ptt.poti_transform_2(wheatstone_C1[1])
print("\n\nC_1:\n", np.round(wheatstone_C1, 2))
C1_x, C1_x_err = wheat.wheatstone_C(476e-9, 4.76e-9, wheatstone_C1[0], wheatstone_C1[1], wheatstone_C1_err)
print(C1_x, C1_x_err)
C1_x, C1_x_err = to.sci_round(C1_x, C1_x_err)
print("\nUnbekannter kondensator C_1:\nC_x = ", C1_x * 1e9, "±", C1_x_err * 1e9, "nF")


wheatstone_RC1 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_RC1.csv', skiprows=1, delimiter=',').transpose()
wheatstone_RC1[1], wheatstone_RC1_err = ptt.poti_transform_2(wheatstone_RC1[1])
print("\n\nRC_1:\n", np.round(wheatstone_RC1, 2))
RC1C_x, RC1C_x_err = wheat.wheatstone_C(476e-9, 4.76e-9, wheatstone_RC1[0], wheatstone_RC1[1], wheatstone_RC1_err)
print(RC1C_x, RC1C_x_err)
RC1C_x, RC1C_x_err = to.sci_round(RC1C_x, RC1C_x_err)
print("\nUnbekannter kondensator (RC) C_1:\nC_x = ", RC1C_x * 1e9, "±", RC1C_x_err * 1e9, "nF")
RC1R_x, RC1R_x_err = wheat.wheatstone_R(160, 1.6, wheatstone_RC1[0], wheatstone_RC1[1], wheatstone_RC1_err)
print(RC1R_x, RC1R_x_err)
RC1R_x, RC1R_x_err = to.sci_round(RC1R_x, RC1R_x_err)
print("\nUnbekannter Widerstand (RC) R_1:\nR_x = ", RC1R_x, "±", RC1R_x_err, "Ω")
