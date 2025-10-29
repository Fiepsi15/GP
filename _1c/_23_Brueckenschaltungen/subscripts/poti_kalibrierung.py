import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def poti_kalibrierung(setting: np.ndarray, measurement: np.ndarray) -> tuple[tuple[float, float], tuple[float, float]]:
    def linear_model(x, m, b):
        return m * x + b

    x_data = setting
    y_data = measurement
    popt, pcov = curve_fit(linear_model, x_data, y_data)
    slope, intercept = popt
    slope_err, intercept_err = np.sqrt(np.diag(pcov))
    plt.scatter(x_data, y_data)
    plt.plot(x_data, linear_model(x_data, slope, intercept))
    plt.show()
    return (slope, slope_err), (intercept, intercept_err)