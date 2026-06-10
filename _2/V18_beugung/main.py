import numpy as np
from matplotlib import pyplot as plt
from _2.V18_beugung.subscripts.gitter import calculate_wavelength as get_lambda

data_directory = '_2/V18_beugung/daten/'

data = np.loadtxt(data_directory + 'gitterbeugung_0.csv', delimiter=',', skiprows=1).transpose()
n = data[0]
d_0 = data[1] / 1e3
z_0 = 399 / 1e3

data = np.loadtxt(data_directory + 'gitterbeugung_1.csv', delimiter=',', skiprows=1).transpose()
d_1 = data[1] / 1e3
z_1 = 599 / 1e3

data = np.loadtxt(data_directory + 'gitterbeugung_2.csv', delimiter=',', skiprows=1).transpose()
d_2 = data[1] / 1e3
z_2 = 799 / 1e3
d_i = np.array([d_0, d_1, d_2])
z_i = np.array([z_0, z_1, z_2])

g = 80 * 1e3 # linien pro m

get_lambda(n, d_i, z_i, g)

plt.show()