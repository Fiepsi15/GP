import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from scrips.tools import sci_round


def calculate_angular_velocity(data):
    mags_per_cycle = 8
    time = data[0]
    reed_switch = data[1]
    flanks = []
    for i in range(5, len(time), 5):
        delta = reed_switch[i] - reed_switch[i - 5]
        if delta > 1:
            flanks.append(i)

    omegas = []
    for i in range(mags_per_cycle, len(flanks), mags_per_cycle):
        omegas.append(2 * np.pi / (time[flanks[i]] - time[flanks[i - mags_per_cycle]]))

    angular_velocity = np.mean(omegas)
    angular_velocity_err = np.std(omegas) / np.sqrt(len(omegas))
    return angular_velocity, angular_velocity_err


def calculate_force(data, p_cal_factor, p_cal_offset):
    voltage = np.mean(data[2])
    delta_voltage = np.std(data[2]) / np.sqrt(len(data[2]))

    force = p_cal_offset[0] + p_cal_factor[0] * voltage
    delta_force = np.sqrt((p_cal_offset[1]) ** 2
                          + (voltage * p_cal_factor[1]) ** 2
                          + (p_cal_factor[0] * delta_voltage) ** 2)
    return force, delta_force


def calculate_power(omega, force, r1, r2, d):
    omega_2 = omega[0] * r1 / r2
    delta_omega_2 = omega[1] * r1 / r2
    torque = force[0] * d

    power = torque * omega_2
    delta_power = np.sqrt((d * omega_2 * force[1]) ** 2
                          + (force[0] * d * delta_omega_2) ** 2)
    return power, delta_power


def force_regression(ang_vel, force):
    def model(p_x, p_a):
        return p_a * p_x

    x = ang_vel[0]
    y = force[0]
    y_err = force[1]
    popt, pcov = optimize.curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    a = popt[0]
    delta_a = np.sqrt(np.diag(pcov))[0]

    ar, dar = sci_round(a, delta_a)
    t = np.linspace(np.min(x), np.max(x), 100)
    res = y - model(x, a)
    fig, (ax, ax_res) = plt.subplots(2, 1, sharex=True, height_ratios=(4, 1), figsize=(6, 5))
    fig.subplots_adjust(hspace=0.1)
    ax.errorbar(x, y, xerr=ang_vel[1], yerr=y_err, fmt='o', capsize=2, color='blue', label='Messwerte')
    ax.plot(t, model(t, a), color='red', label=f'Fit: $F = ({ar}\\pm{dar})\\,$' + '$\\mathrm{N s}\\times \\omega$')
    ax.fill_between(t, model(t, a - delta_a), model(t, a + delta_a), color='red', alpha=0.2, label='Unsicherheit')
    ax.set(ylabel='Kraft [N]', title='Kraft-Winkelgeschwindigkeit')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    max_res = np.max(abs(res))
    ax_res.errorbar(x, y - model(x, a), xerr=ang_vel[1], yerr=y_err, fmt='o', capsize=2, color='green', label='Residuen')
    ax_res.set(xlabel='Winkelgeschwindigkeit [1/s]', ylabel='Residuen [N]', ylim=(-max_res * 1.5, max_res * 1.5))
    ax_res.tick_params(which='both', direction='in')
    ax_res.minorticks_on()
    ax_res.legend()
    ax_res.grid()


    return a, delta_a


def power_regression(ang_vel, power):
    def model(p_x, p_a):
        return p_a * p_x ** 2

    x = ang_vel[0]
    y = power[0]
    y_err = power[1]
    popt, pcov = optimize.curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    a = popt[0]
    delta_a = np.sqrt(np.diag(pcov))[0]

    ar, dar = sci_round(a, delta_a)
    t = np.linspace(np.min(x), np.max(x), 100)
    res = y - model(x, a)
    fig, (ax, ax_res) = plt.subplots(2, 1, sharex=True, height_ratios=(4, 1), figsize=(6, 5))
    fig.subplots_adjust(hspace=0.1)
    ax.errorbar(x, y, xerr=ang_vel[1], yerr=y_err, fmt='o', capsize=2, color='blue', label='Messwerte')
    ax.plot(t, model(t, a), color='red', label=f'Fit: $P = ({ar}\\pm{dar})\\,$' + '$\\mathrm{W s^2}\\times \\omega^2$')
    ax.fill_between(t, model(t, a - delta_a), model(t, a + delta_a), color='red', alpha=0.2, label='Unsicherheit')
    ax.set(ylabel='Leistung [W]', title='Leistung-Winkelgeschwindigkeit')
    ax.tick_params(which='both', direction='in')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    max_res = np.max(abs(res))
    ax_res.errorbar(x, res, xerr=ang_vel[1], yerr=y_err, fmt='o', capsize=2, color='green', label='Residuen')
    ax_res.tick_params(which='both', direction='in')
    ax_res.set(xlabel='Winkelgeschwindigkeit [1/s]', ylabel='Residuen [W]', ylim=(-max_res * 1.5, max_res * 1.5))
    ax_res.minorticks_on()
    ax_res.legend()
    ax_res.grid()

    return a, delta_a


def analyze_student(data_dir, cal_factor, cal_offset, student_numbers):
    r1 = 200e-3 # m
    r2 = 63e-3 # m
    d = 145e-3 # m

    data = []
    for student_number in student_numbers:
        for i in range(4):
            data_set = np.loadtxt(f'{data_dir}/{student_number}Measurement{i + 1}.csv', skiprows=4, delimiter='\t', unpack=True)
            data.append(data_set)
            continue

    angular_vel = []
    force = []
    power = []
    for data_set in data:
        ang_vel = calculate_angular_velocity(data_set)
        angular_vel.append(ang_vel)
        f = calculate_force(data_set, cal_factor, cal_offset)
        force.append(f)
        pw = calculate_power(ang_vel, f, r1, r2, d)
        power.append(pw)
        w_r, dw_r = sci_round(ang_vel[0], ang_vel[1])
        f_r, df_r = sci_round(f[0], f[1])
        p_r, dp_r = sci_round(pw[0], pw[1])
        print(f'Angular velocity: {w_r} +- {dw_r}')
        print(f'Force: {f_r} +- {df_r}')
        print(f'Power: {p_r} +- {dp_r}\n')

    angular_velocity = np.array(angular_vel).transpose()
    force = np.array(force).transpose()
    power = np.array(power).transpose()

    ## Plotting
    #fig, ax = plt.subplots()
    #for data_set in data:
    #    ax.plot(data_set[0], data_set[2])

    beta = force_regression(angular_velocity, force)

    gamma = power_regression(angular_velocity, power)

    gamma_2 = beta[0] * d * r1 / r2, beta[1] * d * r1 / r2
    gamma_r = sci_round(gamma[0], gamma[1])
    gamma_2_r = sci_round(gamma_2[0], gamma_2[1])
    print(f'Gamma = {gamma_r[0]} +- {gamma_r[1]}, \nGamma aus beta = {gamma_2_r[0]} +- {gamma_2_r[1]}')

    plt.show()
