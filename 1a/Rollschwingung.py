import numpy as np

d_K = np.array([2, 2, 2, 2.005, 2])
d_Z = np.array([2, 2, 2, 2, 2])
d_HZ_i = np.array([3, 3, 3, 3, 3])
d_HZ_a = np.array([2.595, 2.590, 2.590, 2.585, 2.590])
'''
r_K = np.mean(d_K/2)
r_K_err = np.std(d_K/2)
print(f"r_K = {r_K}+-{r_K_err}")

r_Z = np.mean(d_Z/2)
r_Z_err = np.std(d_Z/2)
print(f"r_Z = {r_Z}+-{r_Z_err}")

r_HZ_i = np.mean(d_HZ_i/2)
r_HZ_i_err = np.std(d_HZ_i/2)
print(f"r_HZ_i = {r_HZ_i}+-{r_HZ_i_err}")

r_HZ_a = np.mean(d_HZ_a/2)
r_HZ_a_err = np.std(d_HZ_a/2)/np.sqrt(5)
print(f"r_HZ_a = {r_HZ_a}+-{r_HZ_a_err}")
'''


def Kugel():
    t = np.array([6.22, 6.29, 6.35, 6.22, 6.22])
    T = t / 5
    T_mean = np.mean(T)
    T_err = np.std(T) / np.sqrt(len(T))
    return T_mean, T_err


def Zylinder():
    t = np.array([6.5, 6.35, 6.42, 6.55, 6.41])
    m = 11.9/1e3
    r_a = 0.01
    T = t / 5
    I = m * r_a ** 2 * ((9.81 * T ** 2) / (4 * np.pi ** 2 * (0.28823 - r_a)) - 1)
    I_mean = np.mean(I)
    I_err = np.std(I) / np.sqrt(5)
    print(f"Zylinder:\nI = {I_mean*1e9}e-09+-{I_err}kg*m^2")
    T_mean = np.mean(T)
    T_err = np.std(T) / np.sqrt(len(T))
    return T_mean, T_err


def Hohlzylinder():
    t = np.array([7.33, 7.12, 7.01, 7.08, 7])
    T = t / 5
    m = 6.67/1e3
    r = 0.015
    I = m * r ** 2 * ((9.81 * T ** 2) / (4 * np.pi ** 2 * (0.28823 - r)) - 1)
    I_mean = np.mean(I)
    I_err = np.std(I) / np.sqrt(5)
    print(f"Hohlzylinder:\nI = {I_mean * 1e6}e-06+-{I_err}kg*m^2")
    T_mean = np.mean(T)
    T_err = np.std(T) / np.sqrt(len(T))
    return T_mean, T_err


K = Kugel()
print(f"Kugel:\nT = {K[0]} +- {K[1]}s")
Z = Zylinder()
print(f"T = {Z[0]} +- {Z[1]}s")
HZ = Hohlzylinder()
print(f"T = {HZ[0]} +- {HZ[1]}s")
