import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plots(U_d, I_d, U_s, I_s):
    # Diode Current-Voltage Characteristic
    plt.scatter(U_d, I_d, label='Diode Durchlassrichtung', color='blue')
    #plt.scatter(U_s, I_s, label='Diode Sperrrichtung', color='red')
    plt.title('Diode Kennlinie')
    plt.xlabel('$U (V)$')
    plt.ylabel('$I (mA)$')
    plt.yscale('log')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True)
    plt.legend()
    plt.show()