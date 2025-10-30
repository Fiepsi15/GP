import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poti_transform as ptt
import _1c._23_Brueckenschaltungen.subscripts.decade_transform as dct
import _1c._23_Brueckenschaltungen.subscripts.poggendorf as pogg
import _1c._23_Brueckenschaltungen.subscripts.wheatstone as wheat
import _1c._23_Brueckenschaltungen.subscripts.Imballance as ib
import scrips.tools as to
from scrips.array_to_tex import array_to_tex as a2t


poggendorf = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Poggendorf_Messreihe.csv', skiprows=1, delimiter=',').transpose()
poggendorf[0], poggendorfs_err = dct.decade_trafo(poggendorf[0])
poggendorf[1], poggendorfp_err = ptt.poti_transform_2(poggendorf[1])
print("\nPoggendorf-Kompensation:\n", poggendorf, "\n")
U_B, U_B_err = pogg.poggendorf(poggendorf[0], poggendorf[1], poggendorfs_err, poggendorfp_err)
a2t(poggendorf, np.array([poggendorfs_err, poggendorfp_err]), [['$R_S$', '$R_P$'], ['$\\Omega$', '$\\Omega$']], 'Poggendorf Messreihe', 'poggendorf_data')
print(U_B, U_B_err)
U_B, U_B_err = to.sci_round(U_B, U_B_err)
print("\nBatteriespannung:\nU = ", U_B, "±", U_B_err, "V")


wheatstone_R2 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_R2.csv', skiprows=1, delimiter=',').transpose()
wheatstone_R2[0], wheatstone_R2s_err = dct.decade_trafo(wheatstone_R2[0])
wheatstone_R2[1], wheatstone_R2p_err = ptt.poti_transform_2(wheatstone_R2[1])
print("\n------\n\nWheatstone:\nR_2:\n", np.round(wheatstone_R2, 2))
R2_x, R2_x_err = wheat.wheatstone_R(150, 1.5, wheatstone_R2[0], wheatstone_R2[1], wheatstone_R2s_err, wheatstone_R2p_err)
a2t(wheatstone_R2, np.array([wheatstone_R2s_err, wheatstone_R2p_err]), [['$R_S$', '$R_P$'], ['$\\Omega$', '$\\Omega$']], 'Wheatstone $R_2$ Messreihe', 'Widerstand 1')
print(R2_x, R2_x_err)
R2_x, R2_x_err = to.sci_round(R2_x, R2_x_err)
print("\nUnbekannter Widerstand R_2:\nR_x = ", R2_x, "±", R2_x_err, "Ω")

wheatstone_R5 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_R5.csv', skiprows=1, delimiter=',').transpose()
wheatstone_R5[0], wheatstone_R5s_err = dct.decade_trafo(wheatstone_R5[0])
wheatstone_R5[1], wheatstone_R5p_err = ptt.poti_transform_2(wheatstone_R5[1])
print("\n\nR_5:\n", np.round(wheatstone_R5, 2))
R5_x, R5_x_err = wheat.wheatstone_R(150, 1.5, wheatstone_R5[0], wheatstone_R5[1], wheatstone_R5s_err, wheatstone_R5p_err)
a2t(wheatstone_R5, np.array([wheatstone_R5s_err, wheatstone_R5p_err]), [['$R_S$', '$R_P$'], ['$\\Omega$', '$\\Omega$']], 'Wheatstone $R_5$ Messreihe', 'Widerstand 2')
print(R5_x, R5_x_err)
R5_x, R5_x_err = to.sci_round(R5_x, R5_x_err)
print("\nUnbekannter Widerstand R_5:\nR_x = ", R5_x, "±", R5_x_err, "Ω")

wheatstone_C1 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_C1.csv', skiprows=1, delimiter=',').transpose()
wheatstone_C1[0], wheatstone_C1s_err = dct.decade_trafo(wheatstone_C1[0])
wheatstone_C1[1], wheatstone_C1p_err = ptt.poti_transform_2(wheatstone_C1[1])
print("\n\nC_1:\n", np.round(wheatstone_C1, 2))
C1_x, C1_x_err = wheat.wheatstone_C(476e-9, 4.76e-9, wheatstone_C1[0], wheatstone_C1[1], wheatstone_C1s_err, wheatstone_C1p_err)
a2t(wheatstone_C1, np.array([wheatstone_C1s_err, wheatstone_C1p_err]), [['$R_S$', '$R_P$'], ['$\\Omega$', '$\\Omega$']], 'Wheatstone $C_x$ Messreihe', 'Wheatstone Kapazität')
print(C1_x, C1_x_err)
C1_x, C1_x_err = to.sci_round(C1_x, C1_x_err)
print("\nUnbekannter kondensator C_1:\nC_x = ", C1_x * 1e9, "±", C1_x_err * 1e9, "nF")


wheatstone_RC1 = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_RC1.csv', skiprows=1, delimiter=',').transpose()
wheatstone_RC1[0], wheatstone_RC1s_err = dct.decade_trafo(wheatstone_RC1[0])
wheatstone_RC1[1], wheatstone_RC1p_err = ptt.poti_transform_2(wheatstone_RC1[1])
print("\n\nRC_1:\n", np.round(wheatstone_RC1, 2))
RC1C_x, RC1C_x_err = wheat.wheatstone_C(476e-9, 4.76e-9, wheatstone_RC1[0], wheatstone_RC1[1], wheatstone_RC1s_err, wheatstone_RC1p_err)
print(RC1C_x, RC1C_x_err)
RC1C_x, RC1C_x_err = to.sci_round(RC1C_x, RC1C_x_err)
print("\nUnbekannter kondensator (RC) C_1:\nC_x = ", RC1C_x * 1e9, "±", RC1C_x_err * 1e9, "nF")
R_1, R_1_err = ptt.poti_transform(np.array([160]))
RC1R_x, RC1R_x_err = wheat.wheatstone_R(float(R_1[0]), float(R_1_err[0]), wheatstone_RC1[0], wheatstone_RC1[1], wheatstone_RC1s_err, wheatstone_RC1p_err)
a2t(wheatstone_RC1, np.array([wheatstone_RC1s_err, wheatstone_RC1p_err]), [['$R_S$', '$R_P$'], ['$\\Omega$', '$\\Omega$']], 'Wheatstone $R_x,\\,C_x$ Messreihe', 'R-C-Reihenschaltung')
print(RC1R_x, RC1R_x_err)
RC1R_x, RC1R_x_err = to.sci_round(RC1R_x, RC1R_x_err)
print("\nUnbekannter Widerstand (RC) R_1:\nR_x = ", RC1R_x, "±", RC1R_x_err, "Ω")

Imbalance_data = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Wheatstone_Imbalance.csv', skiprows=1, delimiter=',').transpose()
Imbalance_data[0], Imbalance_datap_err = ptt.poti_transform_2(Imbalance_data[0])
Imbalance_U_err = np.array([0.1 for _ in range(Imbalance_data.shape[1])])
a2t(Imbalance_data, np.array([Imbalance_datap_err, Imbalance_U_err]), [['$R_P$', '$U$'], ['$\\Omega$', '$mV$']], 'Spannung in abhängigkeit des Widerstands ', 'Ausschlagmethode')
alpha, alpha_err = ib.imballance(Imbalance_data[0], Imbalance_data[1], Imbalance_datap_err, Imbalance_U_err)
print(alpha, alpha_err)
alpha, alpha_err = to.sci_round(alpha, alpha_err)
print(alpha, alpha_err)

alphas, alphas_err = dct.dec()
print(alphas, alphas_err)