import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def get_U_B(U_A, alpha):
    return U_A / (alpha + 1)


def poggendorf(R_S: np.ndarray, R_D: np.ndarray) -> tuple[float, float]:
    def model(R_S, alpha):
        return alpha * R_S

    x_data = R_S
    y_data = R_D
    popt, pcov = curve_fit(model, x_data, y_data)
    alpha = popt[0]
    alpha_err = np.sqrt(np.diag(pcov))[0]
    plt.scatter(x_data, y_data, label='Datenpunkte')
    plt.plot(x_data, model(x_data, alpha), label='Fit: $R_D = {:.4f} R_S$'.format(alpha), color='red')
    plt.show()
    return get_U_B(2, alpha), alpha_err