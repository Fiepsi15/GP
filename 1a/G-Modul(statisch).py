import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def Auswerten(m, theta, theta_err, R, r, l):
    g = 9.81

    def linmodel(k, m):
        return k * m

    def G_err(R, r, k, L):
        dG = np.sqrt(np.power(L[1] * 2 * g * R[0] / (np.pi * k[0] * np.power(r[0], 4)), 2)
                     + np.power(R[1] * 2 * g * L[0] / (np.pi * k[0] * np.power(r[0], 4)), 2)
                     + np.power(k[1] * 2 * g * L[0] * R[0] / (np.pi * np.power(k[0], 2) * np.power(r[0], 4)), 2)
                     + np.power(r[1] * 8 * g * L[0] * R[0] / (np.pi * k[0] * np.power(r[0], 5)), 2))
        return dG

    popt, pcov = curve_fit(linmodel, m, theta, absolute_sigma=True)
    k = popt[0]
    k_err = np.sqrt(pcov[0][0])
    print(k, k_err)
    plt.figure()
    plt.errorbar(m, theta, yerr=theta_err, fmt='o')
    plt.plot(m, linmodel(m, *popt))
    plt.show()
    G = (2 * g * l[0] * R[0]) / (np.pi * k * np.power(r[0], 4))
    d_G = G_err(R, r, [k, k_err], l)

    print(f"Errechneter G-Modul: {G} +-{d_G}\n={G / 1e9}e9 +-{d_G / 1e9}e9\n")


D_scheibe = [0.16, 0.1]
R_scheibe = np.array(D_scheibe) / 2

drat1_d = [0.002, 0.00005]
drat2_d = [0.001, 0.00005]
drat3_d = [0.001, 0.00005]

drat1_r = np.array(drat1_d) / 2
drat2_r = np.array(drat2_d) / 2
drat3_r = np.array(drat3_d) / 2

drat1_l = [0.978, 0.001]
drat2_l = [0.972, 0.001]
drat3_l = [0.974, 0.001]

drat1_m = np.array([8, 16, 24, 32, 40, 48, 56, 64, 72, 80]) / 1e3
drat2_m = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]) / 1e3
drat3_m = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]) / 1e3

drat1_theta = np.array([8, 15, 27, 32, 44, 54, 61, 73, 80, 92])
drat1_theta_err = 5
drat2_theta = np.array([11, 24, 35, 50, 58, 64, 78, 81, 107, 120])
drat2_theta_err = 6
drat3_theta = np.array([14, 28, 43, 55, 69, 69, 80, 93, 109, 137])
drat3_theta_err = 5

drat1_theta = np.deg2rad(drat1_theta)
drat2_theta = np.deg2rad(drat2_theta)
drat3_theta = np.deg2rad(drat3_theta)
drat1_theta_err = np.deg2rad(drat1_theta_err)
drat2_theta_err = np.deg2rad(drat2_theta_err)
drat3_theta_err = np.deg2rad(drat3_theta_err)

Auswerten(drat1_m, drat1_theta, drat1_theta_err, R_scheibe, drat1_r, drat1_l)
Auswerten(drat2_m, drat2_theta, drat2_theta_err, R_scheibe, drat2_r, drat2_l)
Auswerten(drat3_m, drat3_theta, drat3_theta_err, R_scheibe, drat3_r, drat3_l)
