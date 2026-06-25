import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from scrips.tools import sci_round


def wavelength_to_rgb(wavelength, gamma=0.8):
    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).
    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    #R *= 255
    #G *= 255
    #B *= 255
    return (R, G, B)


def calculate_n(delta_min, epsilon=60):
    epsilon = np.deg2rad(epsilon)
    delta_min = np.deg2rad(delta_min)

    n = np.sin((delta_min[0] + epsilon) / 2) / np.sin(epsilon / 2)
    delta_n = np.abs(np.cos((delta_min[0] + epsilon) / 2) / np.sin(epsilon / 2) * 1 / 2 * delta_min[1])

    return n, delta_n


def print_ab(a, b):
    ar = sci_round(a[0], a[1])
    br = sci_round(b[0], b[1])
    print(f'a = {ar[0]} ± {ar[1]}')
    print(f'b = {br[0]} ± {br[1]}')


def get_lambda_of_n(wavelength, delta_min, epsilon=60):
    def model(x, a, b):
        return a + b / x ** 2

    n = calculate_n(delta_min, epsilon)
    popt, pcov = optimize.curve_fit(model, wavelength, n[0], sigma=n[1], absolute_sigma=True)
    a, b = zip(popt, np.sqrt(np.diag(pcov)))
    print_ab(a, b)

    def n_of(wavelength):
        n = a[0] + b[0] / wavelength ** 2
        delta_n = np.sqrt((a[1] ** 2) + (b[1] / wavelength ** 2) ** 2)
        return n, delta_n

    def lambda_of_n(n):
        wavelength = np.sqrt(b[0] / (n[0] - a[0]))
        delta_wavelength = np.abs(1 / (2 * wavelength) * b[0] / (n[0] - a[0]) ** 2 * n[1])
        return wavelength, delta_wavelength

    x = np.linspace(wavelength[0], wavelength[-1], 100)
    fig, ax = plt.subplots()
    ax.errorbar(wavelength, delta_min[0], yerr=delta_min[1], label='delta_min', color='blue', fmt='o', capsize=2)
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    fig, ax = plt.subplots()
    ax.errorbar(wavelength, n[0], yerr=n[1], label='Messwerte $n_{\\lambda}$', color='blue', fmt='o', capsize=2)
    ax.plot(x, n_of(x)[0], label='Ausgleichskurve $n(\\lambda)$', color='red')
    ax.fill_between(x, n_of(x)[0] + n_of(x)[1], n_of(x)[0] - n_of(x)[1], label='Unsicherheit', color='red', alpha=0.2)
    ax.set(xlabel='Wellenlänge $\\lambda\\,[\\mathrm{nm}]$', ylabel='Brechungsindex $n\\,(\\lambda)$',
           title='Brechungsindex in Abhängigkeit der Wellenlänge')
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return n_of, lambda_of_n


def get_spectrum_of_minimum_deflection(lambda_of_n, delta_min, epsilon=60, lamp = ''):
    n = calculate_n(delta_min, epsilon)
    wavelength = lambda_of_n(n)

    print('Spektrallinien:')

    fig, ax = plt.subplots(figsize=(6, 1.5))
    fig.subplots_adjust(bottom=0.3, top=0.82)

    for wavelength_s, delta_wavelength in np.array(wavelength).transpose():
        ax.plot([wavelength_s, wavelength_s], [0, 1], color=wavelength_to_rgb(wavelength_s)) #plt.get_cmap('Spectral')(1 - (wavelength - 400) / (700 - 400)))
        ax.fill_betweenx([0, 1], [wavelength_s - delta_wavelength, wavelength_s - delta_wavelength], [wavelength_s + delta_wavelength, wavelength_s + delta_wavelength], color=wavelength_to_rgb(wavelength_s), alpha=0.2)
        w_r, dw_r = sci_round(wavelength_s, delta_wavelength)
        print(f'lambda = {w_r} +- {dw_r}')

    ax.plot([], [], label='Spektrallinien', color='orange')
    ax.fill_between([], [], [], label='Unsicherheit', color='orange', alpha=0.2)
    ax.set(xlabel='Wellenlänge $\\lambda\\,[\\mathrm{nm}]$', ylabel=lamp, title='Spektrum', xlim=(380, 750), ylim=(0, 1))
    ax.tick_params(axis='x', which='both', direction='in')
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)
    ax.minorticks_on()
    ax.legend(loc='upper right')

    return wavelength