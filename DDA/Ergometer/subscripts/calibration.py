import numpy as np
from scrips.tools import sci_round
from scipy import optimize


def get_average_voltage(voltages):
    value = np.mean(voltages)
    uncertainty = np.std(voltages) / np.sqrt(len(voltages))
    return value, uncertainty


def linreg(p_voltage, p_force):
    def model(p_x, p_a, p_b):
        return p_a * p_x + p_b

    x = p_voltage[0]
    y = p_force
    #y_err = p_voltage[1]
    popt, pcov = optimize.curve_fit(model, x, y)#, sigma=y_err, absolute_sigma=True)
    a, b = popt
    delta_a, delta_b = np.sqrt(np.diag(pcov))
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
