from scrips.tools import round_up
import numpy as np
from _1b._03_Drehpendel.subscripts import reg_gamma, Erzwungene_schwingung
from _1b._03_Drehpendel.subscripts import log_dec_gamma
import _1b._03_Drehpendel.subscripts.funcs as funcs
from scrips import array_to_tex as a2t

# Air dampened pendulum
print("Just air dampening:\n--------------------\n")
thingy = np.loadtxt('_1b/daten/Free_Airdampened.csv', skiprows=1, delimiter=',').transpose()  # read the .csv
thingy[1] = thingy[1] / 2  # Peak \\Delta to Amplitude
err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(thingy.shape[1])],
                [round_up(np.sqrt(8), 1) for _ in range(thingy.shape[1])]])
TA, dTA = 1.992, 0.001

omegaAir, domegaAir = 3.1532, 0.0016

gammaAir, dgammaAir = reg_gamma(thingy, err)
LambdaAir, dLambdaAir = log_dec_gamma(thingy, TA, err, dTA)
omega0Air, domega0Air = funcs.eigenfrequenz(gammaAir, dgammaAir, omegaAir, domegaAir)
omega_maxAir, domega_maxAir = funcs.resonanzfrequenz(gammaAir, dgammaAir, omegaAir, domegaAir)


# 300mA eddy current Brake dampening
print('\n\n300mA eddy current Brake:\n--------------------\n')
thingy_300mA = np.loadtxt('_1b/daten/Free_300_mA.csv', skiprows=1, delimiter=',').transpose()
err_300 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_300mA.shape[1])],
                [round_up(np.sqrt(32), 0) for _ in range(thingy_300mA.shape[1])]])
T3, dT3 = 1.925, 0.001

omega300 , domega300 = 3.263992367 , 0.001659558

a2t.csv_to_tex("_1b/daten/Free_300_mA.csv", err_300, [['$t$', '$U$'], ['s', 'mV']], 'Amplitude bei 300mA', 'tab:300mA_free')

gamma3, dgamma3 = reg_gamma(thingy_300mA, err_300)
log_dec_gamma(thingy_300mA, T3, err_300, dT3)
omega0300, domega0300 = funcs.eigenfrequenz(gamma3, dgamma3, omega300, domega300)
omega_max300, domega_max300 = funcs.resonanzfrequenz(gamma3, dgamma3, omega300, domega300)



# 600mA eddy current Brake dampening
print('\n\n600mA eddy current Brake:\n--------------------\n')
thingy_600mA = np.loadtxt('_1b/daten/Free_600_mA.csv', skiprows=1, delimiter=',').transpose()
err_600 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_600mA.shape[1])],
                    [round_up(np.sqrt(32), 0) for _ in range(thingy_600mA.shape[1])]])
T6, dT6 = 2.03, 0.01

omega600 , domega600 = 3.095165176, 0.01524711909

a2t.csv_to_tex("_1b/daten/Free_600_mA.csv", err_600, [['$t$', '$U$'], ['s', 'mV']], 'Amplitude bei 600mA', 'tab:600mA_free')

gamma6, dgamma6 = reg_gamma(thingy_600mA, err_600)
Lambda6, dLambda6 = log_dec_gamma(thingy_600mA, T6, err_600, dT6)
omega0300, domega0300 = funcs.eigenfrequenz(gamma6, dgamma6, omega600, domega600)
omega_max300, domega_max300 = funcs.resonanzfrequenz(gamma6, dgamma6, omega600, domega600)

print("Erzwungene Schwingung:\n--------------------\n")

print("300mA: \n--------------------\n")
forced_300mA = np.loadtxt('_1b/daten/Erzwungen_300_mA.csv', skiprows=1, delimiter=',').transpose()
forced_300mA[1] = forced_300mA[1] * 1e-3  # mA to A
forced_300mA[0] = forced_300mA[0] * 2 * np.pi #F to omega
err_f_300 = np.array([[0.001 for _ in range(forced_300mA.shape[1])],
                    [0.001 for _ in range(forced_300mA.shape[1])],
                    [1 for _ in range(forced_300mA.shape[1])]])

a2t.array_to_tex(np.array([np.round(forced_300mA[i], 5) for i in range(3)]), err_f_300, [['$\\omega$', '$A$', '$\\phi$'], ['rad/s', 'mV', '°']], 'Erzwungene Schwingung bei 300mA', 'tab:300mA_forced')

Erzwungene_schwingung.alpha_fit([forced_300mA[0], forced_300mA[1]], err_f_300)
Erzwungene_schwingung.phi_fit(forced_300mA, err_f_300)


print("\n600mA: \n--------------------\n")
forced_600mA = np.loadtxt('_1b/daten/Erzwungen_600_mA.csv', skiprows=1, delimiter=',').transpose()
forced_600mA[1] = forced_600mA[1] * 1e-3  # mA to A
forced_600mA[0] = forced_600mA[0] * 2 * np.pi * 1e-3 #F to omega
err_f_600 = np.array([[0.001 for _ in range(forced_600mA.shape[1])],
                    [0.001 for _ in range(forced_600mA.shape[1])],
                    [1 for _ in range(forced_600mA.shape[1])]])

a2t.array_to_tex(np.array([np.round(forced_600mA[i], 5) for i in range(3)]), err_f_600, [['$\\omega$', '$A$', '$\\phi$'], ['rad/s', 'mV', '°']], 'Erzwungene Schwingung bei 600mA', 'tab:600mA_forced')

Erzwungene_schwingung.alpha_fit([forced_600mA[0], forced_600mA[1]], err_f_600)
Erzwungene_schwingung.phi_fit(forced_600mA, err_f_600)