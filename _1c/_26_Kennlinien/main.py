import numpy as np
import _1c._26_Kennlinien.subscripts.Lampen as Lp
import _1c._26_Kennlinien.subscripts.diode as d
import _1c._26_Kennlinien.subscripts.diode_resist as dr
from _1c._26_Kennlinien.subscripts.transistor import transistor as t

Wolfram = np.loadtxt('_1c/_26_Kennlinien/daten/Wolframfaden.csv', skiprows=1, delimiter=',').transpose()
print(Wolfram)
Lp.make_plots(Wolfram[0], np.array([0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]), Wolfram[1] * 1e-3, np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]) * 1e-3, 5.28e-8, 0)



Kohle = np.loadtxt('_1c/_26_Kennlinien/daten/Kohlefaden.csv', skiprows=1, delimiter=',')
swap = np.copy(Kohle)
Kohle = np.array([swap[-(i + 1)] for i in range(Kohle.shape[0])]).transpose()
print(Kohle)
Lp.make_plots(Kohle[0], np.array([0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]), Kohle[1] * 1e-3, np.array([0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]) * 1e-3, 3.5e-6, 0)

diode_pass = np.loadtxt('_1c/_26_Kennlinien/daten/diode_pass.csv', skiprows=1, delimiter=',').transpose()
diode_block = np.loadtxt('_1c/_26_Kennlinien/daten/diode_impass.csv', skiprows=1, delimiter=',').transpose()

d.plots(diode_pass[0] * 1e-3, np.array([1e-3 for _ in range(diode_pass.shape[1])]), diode_pass[1], np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01]), diode_block[0], np.array([1e-3 for _ in range(diode_block.shape[1])]), diode_block[1], np.array([0.1, 0.1, 0.1, 0.01, 0.01, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.0001, 0.0001]))

diode_resist = np.loadtxt('_1c/_26_Kennlinien/daten/diode_resistor.csv', skiprows=1, delimiter=',').transpose()

dr.diode_resistor(diode_resist[0], 0.1, diode_resist[1], 0.01)

transistor_10 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_10_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_20 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_20_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_30 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_30_mu.csv', skiprows=1, delimiter=',').transpose()
transistor_39 = np.loadtxt('_1c/_26_Kennlinien/daten/transistor_39_mu.csv', skiprows=1, delimiter=',').transpose()

t(transistor_10, np.array([[0.001, 0.001, 0.001, 0.001, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]), transistor_20, np.array([[0.01, 0.001, 0.001, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1]]), transistor_30, np.array([[0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1], [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1]]), transistor_39, np.array([[0.001, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1], [0.01, 0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1]]))
