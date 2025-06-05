import numpy as np
from matplotlib import pyplot as plt
from _1b._03_subscripts.funcs import logarithmic_decrement

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
    plt.grid()
    plt.minorticks_on()
    plt.tick_params(direction='in')
    plt.tick_params(direction='in', which='minor')
    plt.show()
    return log_dec_bar, log_dec_err


