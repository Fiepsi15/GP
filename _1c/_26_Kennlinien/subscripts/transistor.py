import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def plots(T, T_err, __color):
    U_CE, I_CE = T
    U_CE_err, I_CE_err = T_err
    plt.errorbar(U_CE, I_CE, xerr=U_CE_err, yerr=I_CE_err, label='Transistor Kennlinie', color=__color, fmt='o',
                 capsize=5)
    return


def linreg(T, i):
    U_CE, I_CE = T

    def model(I_CE, r, b):
        return r * I_CE + b

    popt, pcov = curve_fit(model, xdata=I_CE[i:], ydata=U_CE[i:])
    r, b = popt
    r_err, b_err = np.sqrt(np.diag(pcov))
    plt.plot(U_CE, (U_CE - b) / r, color='red')
    plt.plot(U_CE, (U_CE - (b + b_err)) / (r + r_err), color='red', linestyle='dashed')
    plt.plot(U_CE, (U_CE - (b - b_err)) / (r - r_err), color='red', linestyle='dashed')
    return sci_round(r, r_err)


def signal_boost(I_BE, I_CE):
    def model(I_BE, beta):
        return beta * I_BE

    popt, pcov = curve_fit(model, xdata=I_BE, ydata=I_CE)
    beta = popt[0]
    beta_err = np.sqrt(np.diag(pcov))[0]
    return sci_round(beta, beta_err)


def transistor(T10, T10_err, T20, T20_err, T30, T30_err, T39, T39_err):
    I_BE = np.array([10, 20, 30, 39]) * 1e-6  # in Amperes
    I_CE = np.array([T10[1][6], T20[1][6], T30[1][6], T39[1][6]]) * 1e-3  # in Amperes
    beta, beta_err = signal_boost(I_BE, I_CE)
    print(f'Stromverstärkung: β = {beta} ± {beta_err}')

    colors = ["#4BB6A7", "#4D96C2", "#5578D1", "#6A5DCB", "#8B56B1"]
    r, r_err = linreg(T10, 3)
    print(f'Ausgangswiderstand bei 10: r_CE = {r} ± {r_err} Ohm')
    plots(T10, T10_err, colors[0])
    r, r_err = linreg(T20, 3)
    print(f'Ausgangswiderstand bei 20: r_CE = {r} ± {r_err} Ohm')
    plots(T20, T20_err, colors[1])
    r, r_err = linreg(T30, 3)
    print(f'Ausgangswiderstand bei 30: r_CE = {r} ± {r_err} Ohm')
    plots(T30, T30_err, colors[2])
    r, r_err = linreg(T39, 3)
    print(f'Ausgangswiderstand bei 39: r_CE = {r} ± {r_err} Ohm')
    plots(T39, T39_err, colors[3])
    plt.xlabel('$U_{CE} (V)$')
    plt.ylabel('$I_{CE} (mA)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True)
    # plt.legend()
    plt.show()
