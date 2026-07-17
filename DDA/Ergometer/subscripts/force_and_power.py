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
        omegas.append(1 / (time[flanks[i]] - time[flanks[i - mags_per_cycle]]) * 1/mags_per_cycle)

    angular_velocity = np.mean(omegas)
    angular_velocity_err = np.std(omegas) / np.sqrt(len(omegas))
    return angular_velocity, angular_velocity_err


def calculate_force(data, p_cal_factor, p_cal_offset):
    voltage = np.mean(data[2])
    delta_voltage = np.std(data[2]) / np.sqrt(len(data[2]))

    force = p_cal_offset[0] + p_cal_factor[0] * voltage
    return force


def analyze_student(data_dir, cal_factor, cal_offset, student_number):
    data = []
    for i in range(4):
        data_set = np.loadtxt(f'{data_dir}/{student_number}Measurement{i + 1}.csv', skiprows=4, delimiter='\t', unpack=True)
        data.append(data_set)
        print(data_set.shape)
        continue

    angular_vel = []
    force = []
    for data_set in data:
        ang_vel = calculate_angular_velocity(data_set)
        f = calculate_force(data_set, cal_factor, cal_offset)
        f = f, 0.01 * f
        force.append(f)
        w_r, dw_r = sci_round(ang_vel[0], ang_vel[1])
        f_r, df_r = sci_round(f[0], f[1])
        print(f'Angular velocity: {w_r} +- {dw_r}')
        print(f'Force: {f_r} +- {df_r}')
        angular_vel.append(ang_vel)

    angular_velocity = np.array(angular_vel).transpose()
    force = np.array(force).transpose()

    # Plotting
    fig, ax = plt.subplots()
    for data_set in data:
        ax.plot(data_set[0], data_set[2])

    fig, ax = plt.subplots()
    for data_set in data:
        ax.scatter(angular_velocity[0], force[0])

    plt.show()
