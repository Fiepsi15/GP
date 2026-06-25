import numpy as np
import matplotlib.pyplot as plt
from _2.V20_Prismenspektrometer.subscripts import prism_calculation as prism


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

    return prism.get_n_of_lambda(wavelength, delta_min)


data_dir = '_2/V20_Prismenspektrometer/daten/'

# Prisma 1
_ = Hg_prism(data_dir, 1)

# Prisma 2
n_of_lambda = Hg_prism(data_dir, 3)



plt.show()