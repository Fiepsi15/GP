import numpy as np

def Latentnt_heat_of_condensation(C_K, T_h, T_c, T_f, m_h, m_c):
    '''
    Calculate the latent heat of condensation of water based on the calorimeter's heat capacity and temperature changes.
    :param C_K: Heat capacity of the calorimeter
    :param T_h: Initial temperature of the hot water
    :param T_c: Initial temperature of the cold water
    :param T_f: Final temperature after mixing
    :param m_h: Mass of the hot water
    :param m_c: Mass of the cold water
    :return: Latent heat of condensation
    '''
    c_w = 4184  # J/(kg*K), specific heat capacity of water
    L_d = ((C_K + c_w * m_c) * (T_f - T_c) - c_w * m_h * (T_f - T_h)) / m_h
    print(L_d)
    return L_d

def Latent_heat_of_boiling_water(U, I, t, m):
    '''
    Calculate the latent heat of boiling water based on the electrical energy supplied.
    :param U: Voltage in volts
    :param I: Current in amperes
    :param t: Time in seconds
    :param m: Mass of water in kg
    :return: Latent heat of boiling water
    '''
    P = U * I  # Power in watts
    Q = P * t  # Energy in joules
    L_b = Q / m  # Latent heat of boiling water in J/kg
    print(L_b)
    return L_b