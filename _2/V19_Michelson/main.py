import numpy as np
from scrips.tools import sci_round


def get_kappa(delta_x, lambda_Laser, N, delta_lambda=0.0, delta_delta_x=0, delta_N=0):
    kappa = (lambda_Laser * N) / (2 * delta_x)
    delta_kappa = np.sqrt((N / (2 * delta_x) * delta_lambda) ** 2
                          + (lambda_Laser / (2 * delta_x) * delta_N) ** 2
                          + (lambda_Laser * N / (2 * delta_x ** 2) * delta_delta_x) ** 2)
    return kappa, delta_kappa


def get_lambda(kappa, delta_x, N, delta_kappa=0, delta_delta_x=0, delta_N=0):
    lambda_ = (2 * kappa * delta_x) / N
    delta_lambda = np.sqrt((2 * delta_x / N * delta_kappa) ** 2
                           + (2 * kappa / N * delta_delta_x) ** 2
                           + (2 * kappa * delta_x / N ** 2 * delta_N) ** 2)
    return lambda_, delta_lambda


delta_x_meas = np.array([[0.8, 0.83], [0.82, 0.83], [0.84, 0.86]]) / 1e3
N = 200
lambda_Laser = 532e-9
delta_x = np.mean(delta_x_meas, axis=1)
delta_x_m = np.mean(delta_x)
delta_delta_x = np.std(delta_x) / np.sqrt(len(delta_x))

kappa, delta_kappa = get_kappa(np.mean(delta_x_m), lambda_Laser, N, delta_lambda=1e-9, delta_delta_x=delta_delta_x, delta_N=10)
kappa_r, delta_kappa_r = sci_round(kappa, delta_kappa)

print(kappa_r, delta_kappa_r)

delta_x_unknown = np.array([[0.96], [0.99], [0.97]]) / 1e3
delta_x_um = np.mean(delta_x_unknown)
delta_delta_x_u = np.std(delta_x_unknown) / np.sqrt(len(delta_x_unknown))
lambda_unknown, delta_lambda = get_lambda(kappa, np.mean(delta_x_unknown), N, delta_kappa=delta_kappa, delta_delta_x=delta_delta_x_u, delta_N=10)
lambda_r, delta_lambda_r = sci_round(lambda_unknown, delta_lambda)

print(lambda_r, delta_lambda_r)
