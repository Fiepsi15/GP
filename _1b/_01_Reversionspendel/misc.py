import numpy as np

d = np.loadtxt('_1b/_01_Reversionspendel/daten/Fehlerschwingungen.csv', skiprows=1, delimiter=',').transpose()

print(np.mean(d[1]), np.std(d[1]))
