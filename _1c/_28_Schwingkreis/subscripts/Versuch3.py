import numpy as np
import matplotlib.pyplot as plt
from scrips.tools import sci_round


def bodeplot(omega, U_e, U_a, Delta_phi):
    H = 20 * np.log10(U_a / U_e)
    plt.errorbar(omega, H, label='Messwerte', fmt='o')
    plt.xlabel('Frequenz ω (Hz)')
    plt.ylabel('Übertragungsfunktion H (dB)')
    plt.xscale('log')
    plt.grid(True)
    plt.legend()
    plt.show()

    Delta_phi_rad = Delta_phi * np.pi / 180

    plt.errorbar(omega, Delta_phi_rad, label='Messwerte', fmt='o')
    plt.xlabel('Frequenz ω (Hz)')
    plt.ylabel('Phasenverschiebung Δφ')
    plt.xscale('log')
    plt.yticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2], ['$0$', '$\\pi/8$', '$\\pi/4$', '$3\\pi/8$', '$\\pi/2$'])
    plt.grid(True)
    plt.legend()
    plt.show()
