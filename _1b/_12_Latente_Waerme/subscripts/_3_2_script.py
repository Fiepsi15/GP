import numpy as np


def Eis_Ls(C_k, T_h, T_c, T_f, m_h, m_c):
    '''
    Calculate the latent heat of fusion of ice based on the calorimeter's heat capacity and temperature changes.
    :param C_k:
    :param T_h:
    :param T_c:
    :param T_f:
    :param m_h:
    :param m_c:
    :return:
    '''
    c_w= 4184  # J/(kg*K), specific heat capacity of water
    L_s = -((C_k + c_w * m_h) * (T_f - T_h) + c_w * m_c * (T_f - T_c)) / m_c
    print(L_s)
    return L_s
