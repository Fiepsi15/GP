import numpy as np
from scipy import signal
from scipy import optimize
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


def calculate_evolution(data, peak_g, peak_r):
    data = data.transpose()
    def model(t,I, b, c):
        return I * np.exp(b * t) + c

    I_0_g = data[peak_g][0]
    y_g = data[peak_g] #/ I_0_g
    t = np.arange(len(y_g))
    popt, pcov = optimize.curve_fit(model, t, y_g, p0=(I_0_g - 3000, -0.08, 5000))
    I_g, b_g, c_g = popt
    delta_I_g, delta_b_g, delta_c_g = np.sqrt(np.diag(pcov))

    #I_0_r = data[peak_r][0]
    y_r = data[peak_r][0] #/ I_0_r
    popt, pcov = optimize.curve_fit(model, t, y_r, p0=(-I_0_g, -0.05, I_0_g))
    I_r, b_r, c_r = popt
    delta_I_r, delta_b_r, delta_c_r = np.sqrt(np.diag(pcov))

    b_g_r, d_b_g_r = sci_round(b_g, delta_b_g)
    b_r_r, d_b_r_r = sci_round(b_r, delta_b_r)
    print(f'\nGrün: b ={b_g_r} pm {d_b_g_r}')
    print(f'Rot: b ={b_r_r} pm {d_b_r_r}')

    fig, ax = plt.subplots()
    ax.errorbar(t, data[peak_g], label='Messwerte grüne Spezies', fmt='.', color='green')
    ax.plot(t, model(t, I_g, b_g, c_g), label='Exponentieller Fit', color='green')
    ax.errorbar(t, data[peak_r][0], label='Messwerte rote Spezies', fmt='.', color='red')
    ax.plot(t, model(t, I_r, b_r, c_r), label='Exponentieller Fit', color='red')
    ax.set(xlabel='Zeit in $\\mathrm{s}$', ylabel='Intensität', ylim=[0, 40e3])
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    return


def run_pc(data_directory):
    pattern = [f'{data_directory}/sub Rng3__{i}__{180 + i}.txt' for i in range(1, 60)]
    first_spec = np.loadtxt(pattern[1], skiprows=find_start(pattern[1]), delimiter='\t').transpose()
    data = np.zeros((59, first_spec.shape[1]))
    for i in range(len(data)):
        data[i] = np.loadtxt(pattern[i], skiprows=find_start(pattern[i]), delimiter='\t').transpose()[1]
    wavelength = first_spec[0]

    peaks_g, _ = signal.find_peaks(data[0], prominence=100)
    print('\nPeak wavelengths green type: ')
    for peak in peaks_g:
        print(f'lambda = {wavelength[peak]}')

    peaks_r, _ = signal.find_peaks(data[-1], prominence=10000)
    print('\nPeak wavelengths red type: ')
    for peak in peaks_r:
        print(f'lambda = {wavelength[peak]}')

    calculate_evolution(data, peaks_g[1], peaks_r)

    fig, ax = plt.subplots(2,2, figsize=(12, 8), sharex=True, sharey=True)
    fig.subplots_adjust(left = 0.1, hspace=0.2, wspace=0.1, right=0.95)
    fig.suptitle('Zeitentwicklung des Emissionsspektrums', fontsize=20, weight='semibold')

    ax[0,0].plot(wavelength, data[0], label='Gemessenes Spektrum', color='blue')
    ax[0,0].set(title='$t = 0 \\mathrm{s}$')
    ax[0,1].plot(wavelength, data[5], label='Gemessenes Spektrum', color='blue')
    ax[0,1].set(title='$t = 5 \\mathrm{s}$')
    ax[1,0].plot(wavelength, data[11], label='Gemessenes Spektrum', color='blue')
    ax[1,0].set(title='$t = 11 \\mathrm{s}$')
    ax[1,1].plot(wavelength, data[-1], label='Gemessenes Spektrum', color='blue')
    ax[1,1].set(title='$t = 59 \\mathrm{s}$')
    for a in ax:
        for ax in a:
            ax.plot([wavelength[peaks_g[1]], wavelength[peaks_g[1]]], [0, 35e3], label='Grüne Variante', color='green', ls=':')
            ax.plot([wavelength[peaks_r], wavelength[peaks_r]], [0, 35e3], label='Rote Variante', color='red', ls=':')
            ax.set(xlabel='Wellenlänge in $\\mathrm{nm}$', ylabel='Intensität')
            ax.tick_params(axis='both', which='both', direction='in')
            ax.minorticks_on()
            ax.legend()
            ax.grid()

    return