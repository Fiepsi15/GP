import numpy as np
import _1c._26_Kennlinien.subscripts.Lampen as Lp

Wolfram = np.loadtxt('_1c/_26_Kennlinien/daten/Wolframfaden.csv', skiprows=1, delimiter=',').transpose()
print(Wolfram)
Lp.make_plots(Wolfram[0], Wolfram[1])



Kohle = np.loadtxt('_1c/_26_Kennlinien/daten/Kohlefaden.csv', skiprows=1, delimiter=',').transpose()
print(Kohle)
Lp.make_plots(Kohle[0], Kohle[1])
