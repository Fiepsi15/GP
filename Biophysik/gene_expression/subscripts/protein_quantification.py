import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def absorption_quantification(Baseline, Sample):
    fig, ax = plt.subplots()
    Sample[1] = Sample[1] - Baseline[1]

    peaks, _ = signal.find_peaks(Sample[1], prominence=0.1)
    print('\nPeak wavelengths: ')
    for peak in peaks:
        print(f'lambda = {Sample[0][peak]}')

    ax.plot(Sample[0], Sample[1], label='Absorption Spectrum Sample', color='red')
    ax.plot([Sample[0][peaks[0]], Sample[0][peaks[0]]], [0, 1], label='peaks', color='blue', ls='--')
    ax.plot([Sample[0][peaks[1]], Sample[0][peaks[1]]], [0, 1], color='blue', ls='--')
    ax.set(xlabel='Wellenlänge in $\\mathrm{nm}$', ylabel='$\\mathrm{Absorbanz}$')
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.grid(True)
    ax.legend()

    molecular_weight_Eos = 25.8e3  # Da
    yield_volume = 1e-3  # L

    concentration_506 = Sample[1][peaks[0]] / 72e3 * (1600 / 300)
    concentration_278 = Sample[1][peaks[1]] / 23.515e3 * (1600 / 300)
    concentration_Eos = concentration_506
    concentration_others = concentration_278 - concentration_506
    con_Eos_r, _ = sci_round(concentration_Eos, 0.1 * concentration_Eos)
    con_oth_r, _ = sci_round(concentration_others, 0.1 * concentration_others)
    print(f'\nAchieved concentration of EosFP: {con_Eos_r} mol/L')
    print(f'Concentration of other proteins: {con_oth_r} mol/L')

    mass_Eos = concentration_Eos * molecular_weight_Eos * yield_volume * 1e-3  # kg
    mass_Eos_r, _ = sci_round(mass_Eos, 0.1 * mass_Eos)
    print(f'Achieved mass of EosFP: {mass_Eos_r} kg = {mass_Eos_r * 1e6} mg')

    return
