import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def mixed(U_d, U_d_err, I_d, I_d_err, U_s, U_s_err, I_s, I_s_err):
    P_max = 0.25  # in Watt
    plt.errorbar(U_d, I_d, xerr=U_d_err, yerr=I_d_err, label='Diode Durchlassrichtung', color='blue', fmt='o', capsize=5)
    plt.errorbar(-U_s, -I_s, xerr=U_s_err, yerr=I_s_err, label='Diode Sperrrichtung', color='red', fmt='o', capsize=5)

    plt.plot(np.array([1, *U_d]), P_max/np.array([1, *U_d]) * 1e3, label='Verlustleistungshyperbeln', color='green', linestyle='dashed')
    plt.plot(-np.array([*U_s, 3]), -P_max/np.array([*U_s, 3]) * 1e3, color='green', linestyle='dashed')
    plt.title('Diode Kennlinien')
    plt.xlabel('$U (V)$')
    plt.ylabel('$I (mA)$')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True)
    plt.legend()
    plt.show()


def single(U, U_err, I, I_err, str: str):
    plt.errorbar(U, I, xerr=U_err, yerr=I_err, label='Diode' + str, color='blue', fmt='o', capsize=5)
    plt.title('Log')
    plt.xlabel('$U (V)$')
    plt.ylabel('$I (mA)$')
    plt.yscale('log')
    plt.minorticks_on()
    plt.tick_params(direction='in', which='both')
    plt.grid(True)
    plt.legend()
    plt.show()


def plots(U_d, U_d_err, I_d, I_d_err, U_s, U_s_err, I_s, I_s_err):
    # Diode Current-Voltage Characteristic
    mixed(U_d, U_d_err, I_d, I_d_err, U_s, U_s_err, I_s, I_s_err)
    single(U_d, U_d_err, I_d, I_d_err, ' Durchlassrichtung')
    single(U_s, U_s_err, I_s, I_s_err, ' Sperrrichtung')