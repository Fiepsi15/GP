import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def plots(T, __color):

    U_CE, I_CE = T
    plt.scatter(U_CE, I_CE, label='Transistor Kennlinie', color=__color)

    return

def transistor(T10, T20, T30, T39):
    colors = ["#4BB6A7", "#4D96C2", "#5578D1", "#6A5DCB", "#8B56B1"]
    plots(T10, colors[0])
    plots(T20, colors[1])
    plots(T30, colors[2])
    plots(T39, colors[3])
    plt.xlabel('$U_{CE} (V)$')
    plt.ylabel('$I_{CE} (mA)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True)
    #plt.legend()
    plt.show()