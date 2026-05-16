import numpy as np
from matplotlib import pyplot as plt
import _2.V09_Schallwellen.subscripts.festkörper as fk
import _2.V09_Schallwellen.subscripts.gase as gase

def gasprep(data):
    nu = data[0] * 1e3
    dist = np.abs(data[1] - data[2]) * 1e-3
    N = data[3]

    d_nu = 1
    d_dist = np.sqrt(2) * 1e-3
    d_N = 1
    return nu, dist, N, d_nu, d_dist, d_N


fig, (ax1, ax2) = plt.subplots(1, 2)

# Schallgeschwindigkeit in Luft:

luft_daten = np.loadtxt('_2/V09_Schallwellen/data/Luft.csv', skiprows=1, delimiter=",").transpose()
nu, dist, N, d_nu, d_dist, d_N = gasprep(luft_daten)

_ = gase.get_sonic_speed_reg(nu, dist, N, ax1, d_nu, d_dist, d_N)


# Schallgeschwindigkeit in CO2:

luft_daten = np.loadtxt('_2/V09_Schallwellen/data/CO2.csv', skiprows=1, delimiter=",").transpose()
nu, dist, N, d_nu, d_dist, d_N = gasprep(luft_daten)

_ = gase.get_sonic_speed_reg(nu, dist, N, ax2, d_nu, d_dist, d_N)

plt.show()
