from scrips.tools import round_up
import numpy as np
from _03_subscripts.reg_gamma import reg_gamma
from _03_subscripts.log_dec_gamma import log_dec_gamma
from _03_subscripts import Erzwungene_schwingung
import _03_subscripts.funcs

# Air dampened pendulum
print("Just air dampening:\n--------------------\n")
thingy = np.loadtxt('_03_daten/Free_Airdampened.csv', skiprows=1, delimiter=',').transpose()  # read the .csv
thingy[1] = thingy[1] / 2  # Peak \\Delta to Amplitude
err = np.array([[round_up(0.1 * np.sqrt(2), 2) for _ in range(thingy.shape[1])],
                [round_up(np.sqrt(8), 1) for _ in range(thingy.shape[1])]])
TA, dTA = 1.992, 0.001

gammaAir, dgammaAir = reg_gamma(thingy, err)
LambdaAir, dLambdaAir = log_dec_gamma(thingy, TA, err, dTA)


# 300mA eddy current Brake dampening
print('\n\n300mA eddy current Brake:\n--------------------\n')
thingy_300mA = np.loadtxt('_03_daten/Free_300_mA.csv', skiprows=1, delimiter=',').transpose()
err_300 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_300mA.shape[1])],
                [round_up(np.sqrt(32), 0) for _ in range(thingy_300mA.shape[1])]])
T3, dT3 = 1.925, 0.001

gamma3, dgamma3 = reg_gamma(thingy_300mA, err_300)
log_dec_gamma(thingy_300mA, T3, err_300, dT3)


# 600mA eddy current Brake dampening
print('\n\n600mA eddy current Brake:\n--------------------\n')
thingy_600mA = np.loadtxt('_03_daten/Free_600_mA.csv', skiprows=1, delimiter=',').transpose()
err_600 = np.array([[round_up(0.04 * np.sqrt(2), 2) for _ in range(thingy_600mA.shape[1])],
                    [round_up(np.sqrt(32), 0) for _ in range(thingy_600mA.shape[1])]])
T6, dT6 = 2.03, 0.01

gamma6, dgamma6 = reg_gamma(thingy_600mA, err_600)
Lambda6, dLambda6 = log_dec_gamma(thingy_600mA, T6, err_600, dT6)


forced_300mA = np.loadtxt('_03_daten/Erzwungen_300_mA.csv', skiprows=1, delimiter=',').transpose()
forced_300mA[1] = forced_300mA[1] / 1e-3  # mA to A
forced_300mA[0] = forced_300mA[0] * 2 * np.pi #F to omega
err_f_300 = np.array([[0.001 for _ in range(forced_300mA.shape[1])],
                    [0.001 for _ in range(forced_300mA.shape[1])]])
Erzwungene_schwingung.alpha_omega_plot([forced_300mA[0], forced_300mA[1]], err_f_300)


