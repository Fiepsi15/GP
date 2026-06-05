import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from scrips.tools import sci_round


def find_start(file):
    preamble_length = 0
    with open(file, 'r') as f:
        i = 0
        while preamble_length == 0 and i < 500:
            line = f.readline()
            if i == 2 and not line.startswith('D'):
                preamble_length = 2
            if line == '>>>>>Begin Spectral Data<<<<<\n':
                preamble_length = i + 1
            i += 1
    return preamble_length


def run_pc(data_directory):
    pattern = [f'{data_directory}/sub Rng3__{i}__{180 + i}.txt' for i in range(60)]
    first_spec = np.loadtxt(pattern[0], skiprows=find_start(pattern[0]), delimiter='\t').transpose()
    data = np.zeros((60, first_spec.shape[1]))
    for i in range(len(data)):
        data[i] = np.loadtxt(pattern[i], skiprows=find_start(pattern[i]), delimiter='\t').transpose()[1]
    wavelength = first_spec[0]

    fig, ax = plt.subplots()
    ax.plot(wavelength, data[0], label='initial Spectrum', color='red')
    ax.set(xlabel='Wavelength [nm]', ylabel='Intensität [a.u.]')
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return