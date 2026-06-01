import numpy as np
from matplotlib import pyplot as plt
import _2.V09_Schallwellen.subscripts.festkörper as fk
import _2.V09_Schallwellen.subscripts.gase as gase
from scrips.tools import sci_round


def gas_prep(data):
    nu = data[0] * 1e3
    d = np.abs(data[1] - data[2]) * 1e-3
    N = data[3]

    d_nu = 1
    d_d = np.sqrt(2) * 1e-3
    d_N = 0
    return nu, d, N, d_nu, d_d, d_N


def rule1(i):
    return i + 1 / 2


def rule2(i):
    return 2 * i + 1

_, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'wspace': 0.3})

frequency_1 = np.array(
    [[2.150, 6], [4.300, 6], [6.450, 6], [8.600, 5], [9.950, 2], [10.750, 5], [12.9, 2], [15.1, 3], [17.2, 2],
     [19.4, 2], [21.5, 3]]).transpose() * 1e3

frequency_2 = np.array([4.3, 8.6, 12.9, 17.2, 15.6, 19.9, 21.5]) * 1e3

c1, dc1 = fk.rod(frequency_1[0], rule1, ax1, 'Einspannung bei $1/2$ der Länge')
print('\n Second arrangement:')
c2, dc2 = fk.rod(frequency_2, rule2, ax2, 'Einspannung bei $1/4$ und $3/4$ der Länge')
plt.show()

c1/2 + c2/2

c_S = np.mean([c1, c2])
dc_S = np.sqrt((dc1 / 2) ** 2 + (dc2 / 2) ** 2)
c_Sr, dc_Sr = sci_round(c_S, dc_S)
print(f'Metall: c = {c_Sr} pm {dc_Sr}')

# Gase:

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'wspace': 0.3})
fig.suptitle('Schallgeschwindigkeit in')

# Schallgeschwindigkeit in Luft:

luft_daten = np.loadtxt('_2/V09_Schallwellen/data/Luft.csv', skiprows=1, delimiter=",").transpose()
freq, distanz, Anz, d_freq, d_distanz, d_Anz = gas_prep(luft_daten)

_ = gase.get_sonic_speed_reg(freq, distanz, Anz, ax1, d_freq, d_distanz, d_Anz, plot_title='Luft')

# Schallgeschwindigkeit in CO2:

CO2_daten = np.loadtxt('_2/V09_Schallwellen/data/CO2.csv', skiprows=1, delimiter=",").transpose()
freq, distanz, Anz, d_freq, d_distanz, d_Anz = gas_prep(CO2_daten[:,0:-1])

_ = gase.get_sonic_speed_reg(freq, distanz, Anz, ax2, d_freq, d_distanz, d_Anz, plot_title='CO2')

freq, distanz, Anz, d_freq, d_distanz, d_Anz = gas_prep(CO2_daten[:,-1])
c_CO2_true = 2 * distanz * freq / Anz
dc_CO2_true = np.sqrt((2 * freq / Anz * d_distanz) ** 2
                     + (2 * distanz / Anz * d_freq) ** 2
                     + (2 * distanz * freq / Anz ** 2 * d_Anz) ** 2)
c, dc = sci_round(c_CO2_true, dc_CO2_true)
print(c, dc)
plt.show()
