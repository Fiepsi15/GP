import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def power(U: np.ndarray, I: np.ndarray) -> np.ndarray:
    """Calculate power from voltage and current."""
    return U * I

def resistance(U: np.ndarray, I: np.ndarray) -> np.ndarray:
    """Calculate resistance from voltage and current."""
    return U / I


def stefan_boltzmann(r, P):
    def model(r, A, c):
        sigma = 5.67e-10
        Delta_T = r / c
        return sigma * A * ((293 + Delta_T) ** 4 - 293 ** 4)

    x_data = r
    y_data = P
    popt, pcov = curve_fit(model, xdata=x_data, ydata=y_data)
    A, c = popt
    A_err, c_err = np.sqrt(np.diag(pcov))
    plt.plot(x_data, model(x_data, A, c), label='Fit', color='green', linestyle='dotted')
    plt.plot(x_data, model(x_data, 7.7571e-3, -0.0002656), label='pls kill me', color='orange', linestyle='dashed')
    plt.title('$P(W) = \\sigma\\cdot A\\cdot((T_0 + \\frac{r}{c})^4 - T_0^4)$')
    return A, c, A_err, c_err


def make_plots(U: np.ndarray, I: np.ndarray):
    P = power(U, I)
    R = resistance(U, I)

    # Current over Voltage
    plt.scatter(U, I, label='Messwerte', color='blue')
    plt.title('$(I, U)$')
    plt.xlabel('$U (V)$')
    plt.ylabel('$I (A)$')
    plt.legend()
    plt.grid(True)
    plt.show()

    r = R / R[0] - 1
    plt.scatter(r, P, label='Messwerte', color='red')
    print(stefan_boltzmann(R / R[0] - 1, P))
    plt.xlabel('$r (-)$')
    plt.ylabel('$P (W)$')
    plt.legend()
    plt.minorticks_on()
    plt.tick_params(direction='in', which='minor')
    plt.grid(True, which='both')
    #plt.loglog()
    #plt.yscale('log')
    plt.show()

