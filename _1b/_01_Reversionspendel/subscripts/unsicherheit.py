import numpy as np


def get_unsicherheit():
    data = np.loadtxt('_1b/_01_Reversionspendel/daten/Fehlerschwingungen.csv', skiprows=1, delimiter=',').transpose()
    delta_T = np.std(data[1])
    print("Aus den 10 messungen zur bestimmung der Unsicherheit ergibt sich:\n$\\bar{T} = $", np.mean(data[1]),
          "$\\pm$", delta_T)
    return delta_T
