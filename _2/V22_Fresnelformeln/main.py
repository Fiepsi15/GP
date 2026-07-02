import numpy as np
from matplotlib import pyplot as plt
from _2.V22_Fresnelformeln.subscripts.maluskurve import calculate_polarization
from _2.V22_Fresnelformeln.subscripts.fresnel import transmission_an_duenner_glasplatte


def spannungsunsicherheit(Spannung, verstaerkung, digits):
    sigma = np.sqrt((Spannung * 0.03) ** 2
                    + (Spannung * 0.005) ** 2
                    + (digits * 2 / verstaerkung) ** 2)
    return sigma


directory = '_2/V22_Fresnelformeln/daten/'

# Malus-kurve:

Pol_winkel, Photospannung = np.loadtxt(directory + 'Malus_formel.csv', skiprows=1, delimiter=',', unpack=True)

delta_winkel = 1  # grad
Pol_winkel = np.array([Pol_winkel, np.full_like(Pol_winkel, delta_winkel)])
delta_spannung = spannungsunsicherheit(Photospannung, 1, 1e-3) # (..., Verstärkung, 1mV last digit)
Photospannung = np.array([Photospannung, delta_spannung])

calculate_polarization(Pol_winkel, Photospannung)

transmission_an_duenner_glasplatte()

plt.show()