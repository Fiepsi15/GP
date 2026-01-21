import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex  # Import hinzugefügt
from _1c._24_Wirbelstrom.subscripts.neigung import neigung as ng
from _1c._24_Wirbelstrom.subscripts.volumen import volumen as vol
from _1c._24_Wirbelstrom.subscripts.feldstaerke import feldstaerke as fs
from _1c._24_Wirbelstrom.subscripts.Leitfaehigkeit import leitfaehigkeit as lf
from _1c._24_Wirbelstrom.subscripts.geschwindigkeit import geschwindigkeit as gs
from _1c._24_Wirbelstrom.subscripts.beta import beta_bestimmung

Neigungswerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Neigung.csv', delimiter=',', skiprows=1).transpose()
Ne48, Ne40, Ne30, Ne20, Ne10 = Neigungswerte[0:2], Neigungswerte[2:4], Neigungswerte[4:6], Neigungswerte[6:8], Neigungswerte[8:10]

# Messwerte tabellieren
quantities_and_units = [['$t_g$', '$t_u$', '$t_g$', '$t_u$', '$t_g$', '$t_u$', '$t_g$', '$t_u$', '$t_g$', '$t_u$'], ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's']]
error = np.full_like(Neigungswerte, 0.001)  # Beispiel: Fehler 0.01 für alle Werte
caption = 'Messwerte der Neigungsmessung'
label = 'tab:neigungsmessung'
#array_to_tex(Neigungswerte, error, quantities_and_units, caption, label)

t_u_30 = Neigungswerte[5]

tau_30_Cu_1mm_BBB = ng(Neigungswerte)

Volumenwerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Volumen.csv', delimiter=',', skiprows=1).transpose()

vol(Volumenwerte, t_u_30, tau_30_Cu_1mm_BBB)

Feldstaerkenwerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Feldstaerke.csv', delimiter=',', skiprows=1).transpose()

fs(Feldstaerkenwerte, t_u_30, tau_30_Cu_1mm_BBB)

Leitfaehigkeitswerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Leitfaehigkeit.csv', delimiter=',', skiprows=1).transpose()

#print(np.average(t_u_30), np.average(Leitfaehigkeitswerte[2]))
lf(Leitfaehigkeitswerte, t_u_30, tau_30_Cu_1mm_BBB)

Geschwindigkeitswerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Geschwindigkeit.csv', delimiter=',', skiprows=1).transpose()

a = Geschwindigkeitswerte[0]
t = Geschwindigkeitswerte[1:].transpose()

k, k_err = gs(t, a)
k_r, k_err_r = sci_round(k, k_err)
print(f'k: {k_r} ± {k_err_r} m/s²')

# Beispielwerte für die Parameter (bitte durch echte Werte ersetzen)
m = 25.91e-3 + 30.28e-3       # Masse in kg
m_err = np.sqrt(2) * 0.01e-3  # Unsicherheit Masse
sigma = 6e7                   # Leitfähigkeit in S/m
sigma_err = 1e7               # Unsicherheit Leitfähigkeit
B0 = 0.445                    # Magnetische Flussdichte in T
B0_err = 10e-3 + 0.05 * B0    # Unsicherheit B0
r = 20.1e-3 / 2               # Radius in m
r_err = 0.05e-3 / 2           # Unsicherheit Radius
d = 1e-3                      # Dicke in m
d_err = 0.05e-3               # Unsicherheit Dicke
g = 9.81                      # Erdbeschleunigung in m/s^2
m_r, m_err_r = sci_round(m, m_err)
print(f'Masse: {m_r} ± {m_err_r} kg')

beta, beta_err = beta_bestimmung(m, m_err, g, sigma, sigma_err, B0, B0_err, r, r_err, d, d_err, k, k_err)
beta_r, beta_err_r = sci_round(beta, beta_err)
print(f"Beta: {beta_r} ± {beta_err_r}")
