import numpy as np
from _1c._24_Wirbelstrom.subscripts.neigung import neigung as ng
from _1c._24_Wirbelstrom.subscripts.volumen import volumen as vol
from _1c._24_Wirbelstrom.subscripts.feldstaerke import feldstaerke as fs
from _1c._24_Wirbelstrom.subscripts.Leitfaehigkeit import leitfaehigkeit as lf
from _1c._24_Wirbelstrom.subscripts.geschwindigkeit import geschwindigkeit as gs

Neigungswerte = np.loadtxt('_1c/_24_Wirbelstrom/daten/Neigung.csv', delimiter=',', skiprows=1).transpose()
Ne48, Ne40, Ne30, Ne20, Ne10 = Neigungswerte[0:2], Neigungswerte[2:4], Neigungswerte[4:6], Neigungswerte[6:8], Neigungswerte[8:10]

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

gs(t, a)


