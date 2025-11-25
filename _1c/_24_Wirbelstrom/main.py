import numpy as np
from _1c._24_Wirbelstrom.subscripts.neigung import neigung as ng
from _1c._24_Wirbelstrom.subscripts.volumen import volumen as vol

Neigungswerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Neigung.csv', delimiter=',', skiprows=1).transpose()
Ne48, Ne40, Ne30, Ne20, Ne10 = Neigungswerte[0:2], Neigungswerte[2:4], Neigungswerte[4:6], Neigungswerte[6:8], Neigungswerte[8:10]

t_u_30 = Neigungswerte[5]
print(t_u_30)

tau_30_Cu_1mm_BBB = ng(Neigungswerte)

Volumenwerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Volumen.csv', delimiter=',', skiprows=1).transpose()

vol(Volumenwerte, t_u_30, tau_30_Cu_1mm_BBB)