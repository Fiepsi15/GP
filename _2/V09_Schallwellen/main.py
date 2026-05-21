import numpy as np
from matplotlib import pyplot as plt
import _2.V09_Schallwellen.subscripts.festkörper as fk
import _2.V09_Schallwellen.subscripts.gase as gase


def gas_prep(data):
    nu = data[0] * 1e3
    d = np.abs(data[1] - data[2]) * 1e-3
    N = data[3]

    d_nu = 1
    d_d = np.sqrt(2) * 1e-3
    d_N = 1
    return nu, d, N, d_nu, d_d, d_N


def rule1(i):
    return i + 1 / 2


def rule2(i):
    return 2 * i + 1


frequency_1 = np.array(
    [[2.150, 6], [4.300, 6], [6.450, 6], [8.600, 5], [9.950, 2], [10.750, 5], [12.9, 2], [15.1, 3], [17.2, 2],
     [19.4, 2], [21.5, 3]]).transpose() * 1e3

frequency_2 = np.array([4.3, 8.6, 12.9, 17.2, 15.6, 19.9, 21.5]) * 1e3

fk.rod(frequency_1[0], rule1)
print('\n Second arrangement:')
s = fk.rod(frequency_2, rule2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'wspace': 0.3})
fig.suptitle('Schallgeschwindigkeit in')

# Schallgeschwindigkeit in Luft:

luft_daten = np.loadtxt('_2/V09_Schallwellen/data/Luft.csv', skiprows=1, delimiter=",").transpose()
freq, distanz, Anz, d_freq, d_distanz, d_Anz = gas_prep(luft_daten)

_ = gase.get_sonic_speed_reg(freq, distanz, Anz, ax1, d_freq, d_distanz, d_Anz, plot_title='Luft')

# Schallgeschwindigkeit in CO2:

luft_daten = np.loadtxt('_2/V09_Schallwellen/data/CO2.csv', skiprows=1, delimiter=",").transpose()
freq, distanz, Anz, d_freq, d_distanz, d_Anz = gas_prep(luft_daten)

_ = gase.get_sonic_speed_reg(freq, distanz, Anz, ax2, d_freq, d_distanz, d_Anz, plot_title='CO2')

print(2 * distanz[-1] * freq[-1] / Anz[-1])

plt.show()
