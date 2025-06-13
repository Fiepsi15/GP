import numpy as np


def calculate_kalorimeter_heat_capacity(data):
    '''
    Calculate the heat capacity of a calorimeter based on the provided data.
    :param data: T_h, T_c, T_f, m_h, m_c
    :return: C_kalorimeter
    '''

    c_w = 4184  # J/(kg*K), specific heat capacity of water
    T_h, T_c, T_f, m_h, m_c = data
    C_k = c_w * (((T_f - T_c) / (T_h - T_f)) * m_c - m_h)

    print(C_k)
    return C_k