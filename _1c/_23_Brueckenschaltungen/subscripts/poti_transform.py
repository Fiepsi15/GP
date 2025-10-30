import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.poti_kalibrierung as potik


potis = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/poti_kalibrierung.csv', skiprows=1, delimiter=',').transpose()

(poti_1_slope, poti_1_slope_err), (poti_1_intercept, poti_1_intercept_err) = potik.poti_kalibrierung_fused(potis[0], potis[1], 1)
#print(poti_1_slope, poti_1_slope_err, poti_1_intercept, poti_1_intercept_err)
(poti_2_slope, poti_2_slope_err), (poti_2_intercept, poti_2_intercept_err) = potik.poti_kalibrierung_fused(potis[0], potis[2], 0.1)
#print(poti_2_slope, poti_2_slope_err, poti_2_intercept, poti_2_intercept_err)
(poti_3_slope, poti_3_slope_err), (poti_3_intercept, poti_3_intercept_err) = potik.poti_kalibrierung(potis[0], potis[3], 1)
#print(poti_3_slope, poti_3_slope_err, poti_3_intercept, poti_3_intercept_err)


def poti_err_2(s1: np.ndarray, s2: np.ndarray) -> np.ndarray:
    s1_err = np.sqrt((s1 * poti_1_slope_err) ** 2 + poti_1_intercept_err ** 2)
    s2_err = s2 * poti_2_slope_err
    return np.sqrt(s1_err ** 2 + s2_err ** 2)


def poti_transform_2(setting: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    slope2 = poti_2_slope * 10
    s1 = (setting // 100) * 100
    s2 = (setting % 100)

    #print(s1, s2, "\n")
    R_1 = poti_1_slope * s1 + poti_1_intercept
    R_2 = slope2 * s2
    R = R_1 + R_2
    R_err = poti_err_2(s1, s2)

    #print(R, R_err, "\n")
    return R, R_err

