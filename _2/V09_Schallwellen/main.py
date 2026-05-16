import numpy as np
from matplotlib import pyplot as plt
#import _2.V09_Schallwellen.subscripts.festkörper as fk
import _2.V09_Schallwellen.subscripts.gase as gase

def gas_prep(data):
    nu = data[0] * 1e3
    d = np.abs(data[1] - data[2]) * 1e-3
    N = data[3]

    d_nu = 1
    d_d = np.sqrt(2) * 1e-3
    d_N = 1
    return nu, d, N, d_nu, d_d, d_N


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
