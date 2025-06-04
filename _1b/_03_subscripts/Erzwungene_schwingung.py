import numpy as np
import matplotlib.pyplot as plt


def alpha_omega_plot(data, error):
    """
    Plots the relationship between alpha and omega with error bars.
    :param data: [omega, alpha]
    :param error: [omega_err, alpha_err]
    :return:
    """
    omega = data[0]
    alpha = data[1]
    omega_err = error[0]
    alpha_err = error[1]
    # Plotting the data
    plt.errorbar(omega, alpha, xerr=omega_err, yerr=alpha_err, fmt='o', capsize=5, label='Data', color='blue')
    plt.xlabel(r'$\omega$ (1/s)')
    plt.ylabel(r'$\alpha$ (V)')
    plt.title('Alpha vs Omega')
    plt.grid()
    plt.legend()
    plt.show()
    return




