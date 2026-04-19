import numpy as np

delta_x = np.array([[0.8, 0.83], [0.82, 0.83], [0.84, 0.86]]) / 1e3
N = 200
lambda_Laser = 532e-9

kappa = (lambda_Laser * N) / (2 * np.mean(delta_x))
print(kappa)

delta_x_unknown = np.array([[0.96], [0.99], [0.97]]) / 1e3
lambda_unknown = (2 * kappa * np.mean(delta_x_unknown)) / N
print(lambda_unknown)
