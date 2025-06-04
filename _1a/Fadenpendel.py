import numpy as np


def Auswertung(t, L):
    T = t / 50
    l, l_err = L
    T_mean = np.average(T)
    T_err = np.std(T) / np.sqrt(len(T))
    print(f"{T_mean}+-{T_err}\n{np.std(T)}")
    g = l / (T_mean / (2 * np.pi)) ** 2
    # Fehler:
    g_err = np.sqrt((8 * np.pi ** 2 * l / (T_mean ** 3) * T_err) ** 2
                 + (4 * np.pi ** 2 / (T_mean ** 2) * l_err) ** 2)
    print(f"g = {g}+-{g_err}m/s^2")



l = 0.882
dl = 0.0005
t = np.array([94.367, 94.366, 94.364, 94.365, 94.366, 94.367, 94.365, 94.368, 94.361, 94.364])
Auswertung(t, [l, dl])
