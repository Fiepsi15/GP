import numpy as np
import matplotlib.pyplot as plt
from _2.V20_Prismenspektrometer.subscripts import prism_calculation as prism
from scrips.tools import sci_round


def decimal_deg(deg, min, delta_min):
    angle = deg + min / 60
    delta_angle = delta_min / 60

    return angle, delta_angle


def Hg_prism(dir, i):
    prism1 = np.loadtxt(dir + f'Hg_prism{i}.csv', delimiter=',', skiprows=1).transpose()

    wavelength = prism1[1]
    delta_angle = 10  # Bogenminuten
    delta_min = decimal_deg(prism1[2], prism1[3], np.full_like(wavelength,
                                                               delta_angle))  # (grad, minuten, unsicherheit in min) → (grad, unsicherheit in grad)

    return prism.get_lambda_of_n(wavelength, delta_min)

def make_spectrum(dir, lambda_of_n, lamp, prism_num, hg=False):
    data = np.loadtxt(dir + f'{lamp}_prism{prism_num}.csv', delimiter=',', skiprows=1).transpose()

    delta_angle = 10
    delta_min = decimal_deg(data[1], data[2], np.full_like(data[1], delta_angle))
    if hg:
        delta_min = decimal_deg(data[2], data[3], np.full_like(data[1],
                                                               delta_angle))  # (grad, minuten, unsicherheit in min) → (grad, unsicherheit in grad)
    print(f'\nLampe: {lamp}')
    if lamp == 'I':
        lamp = '?'
    prism.get_spectrum_of_minimum_deflection(lambda_of_n, delta_min, lamp=lamp)
    return


data_dir = '_2/V20_Prismenspektrometer/daten/'

# Prisma 1
_ = Hg_prism(data_dir, 1)

# Prisma 2
n_of_lambda, lambda_of_n = Hg_prism(data_dir, 3)

# Small sanity test:
#l, dl = lambda_of_n((1.56, 0.002))
#l, dl = sci_round(l, dl)
#print(f'Test: λ(1.560(2)) = {l} ± {dl} nm')

make_spectrum(data_dir, lambda_of_n, 'Hg', 3, hg=True)
make_spectrum(data_dir, lambda_of_n, 'He', 3)
make_spectrum(data_dir, lambda_of_n, 'I', 3)

plt.show()