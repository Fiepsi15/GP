import numpy as np
import _1c._26_Kennlinien.subscripts.Lampen as Lp
import _1c._26_Kennlinien.subscripts.diode as d
import _1c._26_Kennlinien.subscripts.diode_resist as dr
from _1c._26_Kennlinien.subscripts.transistor import transistor as t

Wolfram = np.loadtxt('_1c/_26_Kennlinien/daten/Wolframfaden.csv', skiprows=1, delimiter=',').transpose()
print(Wolfram)
Lp.make_plots(Wolfram[0], Wolfram[1] * 1e-3, 5.28e-8)



Kohle = np.loadtxt('_1c/_26_Kennlinien/daten/Kohlefaden.csv', skiprows=1, delimiter=',')
swap = np.copy(Kohle)
Kohle = np.array([swap[-(i + 1)] for i in range(Kohle.shape[0])]).transpose()
print(Kohle)
Lp.make_plots(Kohle[0], Kohle[1] * 1e-3, 3.5e-6)

diode_pass = np.loadtxt('_1c/_26_Kennlinien/daten/diode_pass.csv', skiprows=1, delimiter=',').transpose()
diode_block = np.loadtxt('_1c/_26_Kennlinien/daten/diode_impass.csv', skiprows=1, delimiter=',').transpose()

d.plots(diode_pass[0] * 1e-3, diode_pass[1], diode_block[0], diode_block[1])

diode_resist = np.loadtxt('_1c/_26_Kennlinien/daten/diode_resistor.csv', skiprows=1, delimiter=',').transpose()

dr.diode_resistor(diode_resist[0], diode_resist[1])

transistor_10 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_10_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_20 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_20_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_30 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_30_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_39 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_39_mu.csv', skiprows=1, delimiter=',').transpose()

t(transistor_10, transistor_20, transistor_30, transistor_39)
