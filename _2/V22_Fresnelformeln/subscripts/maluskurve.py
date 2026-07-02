import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from scrips.tools import sci_round


def print_round(value, label='Value', unit=''):
    val, err = sci_round(value[0], value[1])
    print(f'{label} = {val} +- {err} {unit}')
    return


def model(theta, I_0, theta_0, degree_of_polarisation):
    I_pol = degree_of_polarisation * I_0
    I_un_pol = I_0 - I_pol
    return I_pol * (np.cos(theta - theta_0)) ** 2 + I_un_pol


def delta_model(theta, I_0, theta_0, degree_of_polarisation):
    delta_1 = (np.cos(theta - theta_0[0]) ** 2 - 1) * I_0[0] * degree_of_polarisation[1]
    delta_2 = ((np.cos(theta - theta_0[0]) ** 2 - 1) * degree_of_polarisation[0] + 1) * I_0[1]
    delta_3 = (2 * degree_of_polarisation[0] * I_0[0] * np.cos(theta - theta_0[0]) * np.sin(theta - theta_0[0])
               * theta_0[1])
    delta_I = np.sqrt(delta_1 ** 2 + delta_2 ** 2 + delta_3 ** 2)

    return delta_I


def calculate_polarization(theta, I):
    theta = np.deg2rad(theta)
    popt, pcov = optimize.curve_fit(model, theta[0], I[0], sigma=I[1], absolute_sigma=True, p0=[800, 3 * np.pi / 4, 0.9])
    I_0, theta_0, degree_of_polarisation = popt
    I_0_err, theta_0_err, degree_of_polarisation_err = np.sqrt(np.diag(pcov))
    I_0 = I_0, I_0_err
    theta_0 = theta_0, theta_0_err
    degree_of_polarisation = degree_of_polarisation, degree_of_polarisation_err
    print_round(I_0, 'Intensität I_0', 'mV')
    print_round(np.rad2deg(theta_0), 'Polarisationsrichtung θ_0', '°')
    print_round(degree_of_polarisation, 'Polarisationsgrad')

    fig, ax = plt.subplots()

    theta = np.rad2deg(theta)
    x = np.linspace(0, 2 * np.pi, 100)
    model_I = model(x, I_0[0], theta_0[0], degree_of_polarisation[0])
    delta_I = delta_model(x, I_0, theta_0, degree_of_polarisation)

    ax.errorbar(theta[0], I[0], xerr=theta[1], yerr=I[1], label='Messwerte', color='blue', fmt='o', capsize=2)
    ax.plot(np.rad2deg(x), model_I, label='Fit', color='red')
    ax.fill_between(np.rad2deg(x), model_I - delta_I, model_I + delta_I, label='Unsicherheit', color='red', alpha=0.2)
    ax.set(xlabel='Polfilter Winkel $\\mathrm{[°]}$', ylabel='Photospannung $\\mathrm{[mV]}$', ylim=(0, 900))
    ax.tick_params(axis='both', which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()
