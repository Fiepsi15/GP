import numpy as np
from matplotlib import pyplot as plt
from _2.V22_Fresnelformeln.subscripts.maluskurve import calculate_polarization
from _2.V22_Fresnelformeln.subscripts.fresnel import transmission_an_duenner_glasplatte, fresnel_rechnung


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

# Fresnel Formeln
# transmission_an_duenner_glasplatte()

_, reflexion_p, reflexion_s = np.loadtxt(directory + 'fresnel_reflexion.csv', skiprows=1, delimiter=',', unpack=True)

theta, transmission_p, transmission_s = np.loadtxt(directory + 'fresnel_transmission.csv', skiprows=1, delimiter=',', unpack=True)
reflexion_p = reflexion_p / 10

referenz_p = 109 # mV
delta = spannungsunsicherheit(referenz_p, 1, 1e-3)
referenz_p = np.array([referenz_p, delta])

referenz_s = 114 # mV
delta = spannungsunsicherheit(referenz_s, 1, 1e-3)
referenz_s = np.array([referenz_s, delta])

theta = np.array([theta - 0.3, np.full_like(theta, 0.1)])
delta = spannungsunsicherheit(reflexion_p, 10, 1e-3)
reflexion_p = np.array([reflexion_p, delta])
delta = spannungsunsicherheit(reflexion_s, 1, 1e-3)
reflexion_s = np.array([reflexion_s, delta])
delta = spannungsunsicherheit(transmission_p, 1, 1e-3)
transmission_p = np.array([transmission_p, delta])
delta = spannungsunsicherheit(transmission_s, 1, 1e-3)
transmission_s = np.array([transmission_s, delta])

fresnel_rechnung(theta, reflexion_p, reflexion_s, transmission_p, transmission_s, referenz_p, referenz_s)

plt.show()