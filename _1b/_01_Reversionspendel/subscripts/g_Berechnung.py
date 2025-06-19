import numpy as np


def g(T, dT, L, dL):
    '''
    :param T:
    :param dT:
    :param L:
    :param dL:
    :return: g, dg:
    '''
    
    g = 4 * np.pi**2 * L / T**2

    dg = np.sqrt((dL * 4 * np.pi**2 / T**2) ** 2 + (dT * 4 * np.pi**2 * L / T**3) ** 2)

    return g, dg
