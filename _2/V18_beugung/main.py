import numpy as np
from matplotlib import pyplot as plt
from _2.V18_beugung.subscripts.gitter import calculate_wavelength, visible_spectrum
from _2.V18_beugung.subscripts.spalt import camera, wall, lens

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
delta_d = 1e-3 # mm
delta_z = 1e-3 # mm

lamb, delta_lamb = calculate_wavelength(n, d_i, z_i, g, np.full_like(d_i, delta_d), np.full_like(z_i, delta_z))

delta_d = 0.5e-3 # mm

camera(0.5771e3, lamb, 515e-3, delta_lamb, delta_z)
n, d_0 = np.loadtxt(data_directory + 'spaltbeugung_0.csv', delimiter=',', skiprows=1).transpose()
d_0 = d_0 / 1e3
_, d_1 = np.loadtxt(data_directory + 'spaltbeugung_1.csv', delimiter=',', skiprows=1).transpose() / 1e3
_, d_2 = np.loadtxt(data_directory + 'spaltbeugung_2.csv', delimiter=',', skiprows=1).transpose() / 1e3
d_i = np.array([d_0, d_1, d_2])
z_i = np.array([140.5, 120, 100]) / 1e2

wall(n, lamb, z_i, d_i, delta_lamb, delta_z, delta_d)

lens(1.134, 132e-3, 1.5e-3, 1e-3, 1e-3, 0.5e-3)

visible_spectrum(999e-3, g, 31e-3, 56e-3, delta_z, delta_d, delta_d)

plt.show()