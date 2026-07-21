import numpy as np
import matplotlib.pyplot as plt
from _2.V20_Prismenspektrometer.subscripts import prism_calculation as prism
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def decimal_deg(deg, min, delta_min, theta_0):
    angle = (theta_0[0] - deg) + (theta_0[1] - min) / 60
    delta_angle = np.sqrt((delta_min / 60) ** 2 + (theta_0[2] / 60) ** 2)

    return angle, delta_angle


def print_array(Hg, He, Uk):
    values = np.zeros((3, np.max([len(Hg[0]), len(He[0]), len(Uk[0])])))
    for i in range(len(Hg[0])):
        values[0, i] = Hg[0][i]
    for i in range(len(He[0])):
        values[1, i] = He[0][i]
    for i in range(len(Uk[0])):
        values[2, i] = Uk[0][i]

    errors = np.zeros_like(values)
    for i in range(len(Hg[0])):
        errors[0, i] = Hg[1][i]
    for i in range(len(He[0])):
        errors[1, i] = He[1][i]
    for i in range(len(Uk[0])):
        errors[2, i] = Uk[1][i]

    a2t(values, errors, [['$\\lambda$(Hg)', '$\\lambda$(He)', '$\\lambda$(Uk)'], ['nm', 'nm', 'nm']])


def Hg_prism(dir, i, theta_0):
    prism1 = np.loadtxt(dir + f'Hg_prism{i}.csv', delimiter=',', skiprows=1).transpose()

    wavelength = prism1[1]
    delta_angle = 10  # Bogenminuten
    delta_min = decimal_deg(
        prism1[2], prism1[3], np.full_like(wavelength, delta_angle),
        theta_0)  # (grad, minuten, unsicherheit in min, theta_0) → (grad, unsicherheit in grad)
    label = ''
    if i == 1:
        label = 'I'
    elif i == 3:
        label = 'III'

    return prism.get_lambda_of_n(wavelength, delta_min, plabel=label)


def make_spectrum(dir, lambda_of_n, lamp, prism_num, theta_0, hg=False):
    data = np.loadtxt(dir + f'{lamp}_prism{prism_num}.csv', delimiter=',', skiprows=1).transpose()

    delta_angle = 10
    delta_min = decimal_deg(data[1], data[2], np.full_like(data[1], delta_angle), theta_0)
    if hg:
        delta_min = decimal_deg(data[2], data[3], np.full_like(data[1],
                                                               delta_angle),
                                theta_0)  # (grad, minuten, unsicherheit in min) → (grad, unsicherheit in grad)
    print(f'\nLampe: {lamp}')
    if lamp == 'I':
        lamp = '?'

    return prism.get_spectrum_of_minimum_deflection(lambda_of_n, delta_min, lamp=lamp)


data_dir = '_2/V20_Prismenspektrometer/daten/'
theta_0 = 261, 25, 10  # grad, minuten, unsicherheit in min

# Prisma 1
_ = Hg_prism(data_dir, 1, theta_0)

# Prisma 2
n_of_lambda, lambda_of_n = Hg_prism(data_dir, 3, theta_0)

# Small sanity test:
# l, dl = lambda_of_n((1.56, 0.002))
# l, dl = sci_round(l, dl)
# print(f'Test: λ(1.560(2)) = {l} ± {dl} nm')

Hg = make_spectrum(data_dir, lambda_of_n, 'Hg', 3, theta_0, hg=True)
He = make_spectrum(data_dir, lambda_of_n, 'He', 3, theta_0)
Uk = make_spectrum(data_dir, lambda_of_n, 'I', 3, theta_0)

#print_array(Hg, He, Uk)

plt.show()
