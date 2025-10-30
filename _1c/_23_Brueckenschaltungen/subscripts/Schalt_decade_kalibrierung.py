import numpy as np
from scipy.optimize import curve_fit

schalt_data = np.loadtxt('_1c/_23_Brueckenschaltungen/daten/Widerstandsdekade_kalibrierung.csv', skiprows=1, delimiter=',')

def decade_kalibrierung() -> tuple[np.ndarray, np.ndarray]:
    set = np.array([1, 5, 10])
    zehner = schalt_data[0][1:]
    hunderter = schalt_data[1][1:]
    tausender = schalt_data[2][1:]
    def model(x, m):
        return m * x

    popt, pcov = curve_fit(model, set, zehner)
    zehner_slope = popt[0]
    zehner_slope_err = np.sqrt(np.diag(pcov))
    popt, pcov = curve_fit(model, set, hunderter)
    hunderter_slope = popt[0]
    hunderter_slope_err = np.sqrt(np.diag(pcov))
    popt, pcov = curve_fit(model, set, tausender)
    tausender_slope = popt[0]
    tausender_slope_err = np.sqrt(np.diag(pcov))
    return np.array([zehner_slope, hunderter_slope, tausender_slope]), np.array([zehner_slope_err, hunderter_slope_err, tausender_slope_err])

