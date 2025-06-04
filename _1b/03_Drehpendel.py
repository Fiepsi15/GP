from scrips.tools import round_up
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def logarithmic_decrement(x, x_plus_T):
    return np.log(x) - np.log(x_plus_T)


def prep_y(data):
    return logarithmic_decrement(data[1][0], data[1])  # Formel aus der Ausarbeitung hat doch gepasst


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
    plt.legend()
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


def log_dec_gamma(data, T, error, dT):
    log_dec = []
    for i in range(data.shape[1] - 1):
        log = logarithmic_decrement(data[1][i], data[1][i + 1])
        log = log / ((data[0][i + 1] - data[0][i]) / T)
        log_dec.append(log)
    log_dec = np.array(log_dec)

    log_dec_bar = np.mean(log_dec)
    log_dec_err = np.std(log_dec)

    gamma = log_dec_bar / T
    dgamma = np.sqrt((log_dec_err / T) ** 2
                     + (log_dec_bar / (T ** 2) * dT) ** 2)

    print('log_dec =', log_dec)
    print(f'log_dec = {log_dec_bar} +/- {log_dec_err}')
    print(f'\ngamma from average of logarithmic decrements = {gamma} +/- {dgamma}')

    plt.plot(data[0], data[1][0] * np.exp(-gamma * data[0]), label='fit über average', color='green')
    plt.plot(data[0], data[1][0] * np.exp(-(gamma + dgamma) * data[0]), label='$\\pm\\Delta_{avg}$', color='green',
             linestyle='--')
    plt.plot(data[0], data[1][0] * np.exp(-(gamma - dgamma) * data[0]), color='green',
             linestyle='--')
    plt.legend()
    plt.show()
    return log_dec_bar, log_dec_err



print("Just air dampening:\n--------------------\n")
thingy = np.loadtxt('03_daten/Free_Airdampened.csv', skiprows=1, delimiter=',').transpose()  # read the .csv
thingy[1] = thingy[1] / 2  # Peak \\Delta to Amplitude
err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(thingy.shape[1])],
                [round_up(np.sqrt(8), 1) for _ in range(thingy.shape[1])]])
TA, dTA = 1.992, 0.001

gammaAir, dgammaAir = reg_gamma(thingy, err)
LambdaAir, dLambdaAir = log_dec_gamma(thingy, TA, err, dTA)


print('\n\n300mA eddy current Brake:\n--------------------\n')
thingy_300mA = np.loadtxt('03_daten/Free_300_mA.csv', skiprows=1, delimiter=',').transpose()
err_300 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_300mA.shape[1])],
                [round_up(np.sqrt(32), 0) for _ in range(thingy_300mA.shape[1])]])
T3, dT3 = 1.925, 0.001

gamma3, dgamma3 = reg_gamma(thingy_300mA, err_300)
log_dec_gamma(thingy_300mA, T3, err_300, dT3)


print('\n\n600mA eddy current Brake:\n--------------------\n')
thingy_600mA = np.loadtxt('03_daten/Free_600_mA.csv', skiprows=1, delimiter=',').transpose()
err_600 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_600mA.shape[1])],
                    [round_up(np.sqrt(32), 0) for _ in range(thingy_600mA.shape[1])]])
T6, dT6 = 2.03, 0.01

gamma6, dgamma6 = reg_gamma(thingy_600mA, err_600)
Lambda6, dLambda6 = log_dec_gamma(thingy_600mA, T6, err_600, dT6)




