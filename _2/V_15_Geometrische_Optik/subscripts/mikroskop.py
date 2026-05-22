import numpy as np


def get_vergroesserung(s, d, f_obj, f_ok, dd):
    V = s * (d - f_ok - f_obj) / (f_obj * f_ok)
    dV = s / (f_obj * f_ok) * dd
    return V, dV


def get_ges_meas(V_Obj, f_Ok, s, dV_Obj):
    V = V_Obj * s / f_Ok
    dV = s / f_Ok * dV_Obj
    return V, dV


def get_vergroesserung_obj(s1, s2, ds1=0, ds2=0):
    V = s1 / s2
    dV = np.sqrt((1 / s2 * ds1) ** 2
                 + (s1 / s2 ** 2 * ds2) ** 2)
    return V, dV
