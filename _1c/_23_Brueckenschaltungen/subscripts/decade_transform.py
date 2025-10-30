import numpy as np
import _1c._23_Brueckenschaltungen.subscripts.Schalt_decade_kalibrierung as sdk


def decade_err(d1, d2, d3, zehner_err, hunderter_err, tausender_err) -> np.ndarray:
    R_3_err = d1 * tausender_err
    R_2_err = d2 * hunderter_err
    R_1_err = d3 * zehner_err
    R_err = np.sqrt(R_1_err ** 2 + R_2_err ** 2 + R_3_err ** 2)
    return R_err


def decade_trafo(setting: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    (zehner, hunderter, tausender), (zehner_err, hunderter_err, tausender_err) = sdk.decade_kalibrierung()
    d1 = (setting // 1000)
    d2 = ((setting % 1000) // 100)
    d3 = ((setting % 100) // 10)

    R_3 = d1 * tausender
    R_2 = d2 * hunderter
    R_1 = d3 * zehner
    R = R_1 + R_2 + R_3
    R_err = decade_err(d1, d2, d3, zehner_err, hunderter_err, tausender_err)
    return R, R_err
