import numpy as np
import matplotlib.pyplot as plt
from _1b._01_Reversionspendel.subscripts.unsicherheit import get_unsicherheit
from _1b._01_Reversionspendel.subscripts.pendel import linear_regression_pendulum, delta_T_quadrat
from _1b._01_Reversionspendel.subscripts.Schnittpunkt import Schnittpunkt
from _1b._01_Reversionspendel.subscripts.g_Berechnung import g

delta_T = get_unsicherheit() / 50
delta_L = 1e-3  # 1mm

# Berechnungen für die erste Aufhängung
daten_Aufhaengung_1 = np.loadtxt('_1b/_01_Reversionspendel/daten/Aufhaengung_1.csv', skiprows=1,
                                 delimiter=',').transpose()

L_1 = daten_Aufhaengung_1[0] * 1e-3
T_1 = daten_Aufhaengung_1[1] = daten_Aufhaengung_1[1] / 50
dT_1 = [delta_T for _ in range(len(T_1))]
dL_1 = [delta_L for _ in range(len(L_1))]
k1, d_k1, b1, d_b1 = linear_regression_pendulum(T_1, dT_1, L_1, dL_1)

# Berechnungen für die zweite Aufhängung
daten_Aufhaengung_2 = np.loadtxt('_1b/_01_Reversionspendel/daten/Aufhaengung_2.csv', skiprows=1,
                                 delimiter=',').transpose()

L_2 = daten_Aufhaengung_2[0] * 1e-3
T_2 = daten_Aufhaengung_2[1] / 50
dT_2 = [delta_T for _ in range(len(T_2))]
dL_2 = [delta_L for _ in range(len(L_2))]
k2, d_k2, b2, d_b2 = linear_regression_pendulum(T_2, dT_2, L_2, dL_2)

# Berechnung von g
x, y, dx, dy = Schnittpunkt(k1, d_k1, b1, d_b1, k2, d_k2, b2, d_b2)
print(f'Schnittpunkt: (T={np.sqrt(x)}, L={y})')
g, dg = g(np.sqrt(x), 1 / 2 * 1 / np.sqrt(x) * dx, y, dy)
print(g, dg)

# Plotting
# Erste gerade
plt.errorbar(T_1 ** 2, L_1, xerr=delta_T_quadrat(T_1, dT_1), yerr=dL_1, fmt='^', label='Aufhängung 1', capsize=5,
             color='blue')
plt.plot(T_1 ** 2, T_1 ** 2 * k1 + b1, label='Fit Aufhängung 1', color='red')
dy_1 = np.sqrt((T_1 ** 2 * d_k1) ** 2 + d_b1 ** 2)
plt.plot(T_1 ** 2, T_1 ** 2 * k1 + b1 + dy_1, color='red', linestyle='--')
plt.plot(T_1 ** 2, T_1 ** 2 * k1 + b1 - dy_1, color='red', linestyle='--')

# Zweite gerade
plt.errorbar(T_2 ** 2, L_2, xerr=delta_T_quadrat(T_2, dT_2), yerr=dL_2, fmt='^', label='Aufhängung 2', capsize=5,
             color='slateblue')
plt.plot(T_2 ** 2, T_2 ** 2 * k2 + b2, label='Fit Aufhängung 2', color='tomato')
dy_2 = np.sqrt((T_2 ** 2 * d_k2) ** 2 + d_b2 ** 2)
plt.plot(T_2 ** 2, T_2 ** 2 * k2 + b2 + dy_2, color='tomato', linestyle='--')
plt.plot(T_2 ** 2, T_2 ** 2 * k2 + b2 - dy_2, color='tomato', linestyle='--')

# Schnittpunkt
plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='D', label='Schnittpunkt', color='green', capsize=5)

# Settings
plt.xlabel('$T^2 \\text{ in s}^2$')
plt.ylabel('$L$ in m')
plt.minorticks_on()
plt.tick_params(direction='in', top=True, bottom=True, left=True, right=True)
plt.tick_params(direction='in', which='minor', top=True, bottom=True, left=True, right=True)
plt.grid(True)
plt.legend()
plt.show()
