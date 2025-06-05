import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from _1b._03_subscripts.funcs import prep_y

def reg_gamma(data, error):
    def model(T, gamma):
        return gamma * T  # lin term

    # Vorbereitung der reg
    y = prep_y(data)
    # y_err = np.sqrt(2) * error[1] / (data[1][0] * data[1])
    y_err = np.sqrt((1 / data[1]) ** 2 + (1 / data[1][0]) ** 2) * error[
        1]  # darauf bin ich bei der Fortpflanzung gekommen
    x = data[0]

    # Actual reg and coe-extraction
    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    gamma = popt[0]
    dgamma = np.sqrt(pcov[0][0])
    print(f'gamma from linear reg over varying period count = {gamma} +/- {dgamma}')

    # plot der reg-gerade
    plt.errorbar(x, y, xerr=error[0], yerr=y_err, label='data', color='blue', fmt='o', capsize=5)
    plt.plot(x, model(x, gamma), label='fit', color='red')
    plt.plot(x, model(x, gamma + dgamma), label='$\\pm\\Delta$', color='red', linestyle='--')
    plt.plot(x, model(x, gamma - dgamma), color='red', linestyle='--')
    plt.grid()
    plt.xlabel(r"$T (s)$")
    plt.ylabel(r"$\Lambda$")
    plt.legend()
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.show()

    # plot der rückführung auf original
    plt.errorbar(data[0], data[1], xerr=error[0], yerr=error[1], label='data', color='blue', fmt='o', capsize=5)
    plt.plot(data[0], data[1][0] * np.exp(-gamma * data[0]), label='fit über reg',
             color='red')  # this plot is sad, gamma seems to have to be converted to work in time based reality as opposed to period based reality... thats not in our reports theory yet (as far as I can see... idk, I may just be a lil stoopid).
    plt.plot(data[0], data[1][0] * np.exp(-(gamma + dgamma) * data[0]), label='$\\pm\\Delta_{reg}$', color='red',
             linestyle='--')
    plt.plot(data[0], data[1][0] * np.exp(-(gamma - dgamma) * data[0]), color='red',
             linestyle='--')

    return gamma, dgamma


