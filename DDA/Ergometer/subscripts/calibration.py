import numpy as np
from scrips.tools import sci_round
from matplotlib import pyplot as plt
from scipy import optimize


def get_average_voltage(voltages):
    value = np.mean(voltages)
    uncertainty = np.std(voltages) / np.sqrt(len(voltages))
    return value, uncertainty


def uncert(p_x, p_a, p_b):
        return np.sqrt((p_b[1]) ** 2
                       + (p_x[0] * p_a[1]) ** 2
                       + (p_x[1] * p_a[0]) ** 2)


def linreg(p_voltage, p_force):
    def model(p_x, p_a, p_b):
        return p_a * p_x + p_b

    x = p_voltage[0]
    y = p_force
    #y_err = p_voltage[1]
    popt, pcov = optimize.curve_fit(model, x, y)#, sigma=y_err, absolute_sigma=True)
    a, b = popt
    delta_a, delta_b = np.sqrt(np.diag(pcov))

    fig, ax = plt.subplots()
    a_r, da_r = sci_round(a, delta_a)
    b_r, db_r = sci_round(b, delta_b)

    plt.errorbar(x, y, xerr=p_voltage[1], fmt='o', capsize=2, color='blue', label='Messwerte')
    ax.plot(x, model(x, a, b), color='red', label=f'Fit: $F = ({a_r}\\pm{da_r})\\,$' + '$\\mathrm{N / V}\\times U$' + f'$ \\;+\\; ({b_r} \\pm {db_r})$' + '$\\mathrm{N}$')
    ax.fill_between(x, model(x, a, b) - uncert(p_voltage, (a, delta_a), (b, delta_b)), model(x, a, b) + uncert(p_voltage, (a, delta_a), (b, delta_b)), label='Unsicherheit', color='red', alpha=0.2)
    ax.set(xlabel='Spannung [V]', ylabel='Kraft [N]', title='Kraft-Spannung')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()


    return (a, delta_a), (b, delta_b)


def calibrate(data_dir, masses, measurement_rate):
    g = 9.81
    voltages = []
    for mass in masses:
        data = np.loadtxt(f'{data_dir}/At_rest_{mass}g_{measurement_rate}Hz.csv', skiprows=4, delimiter='\t', unpack=True)
        voltage_data = data[1]
        voltage = get_average_voltage(voltage_data)
        voltages.append(voltage)

    forces = np.array(masses) * g / 1e3
    voltages = np.array(voltages).transpose()

    factor, offset = linreg(voltages, forces)

    f_r, df_r = sci_round(factor[0], factor[1])
    o_r, do_r = sci_round(offset[0], offset[1])
    print(f'Calibration results:\n F = U * ({f_r} +- {df_r}) N/V + ({o_r} +- {do_r}) N\n')
    return factor, offset
