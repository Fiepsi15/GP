import numpy as np
from scipy.optimize import fsolve


def get_tau(t_u_arr, t_g_arr):
    def func(tau, t_1, t_2):
        return -1 / 2 * t_1 ** 2 + tau * (t_2 - tau * (1 - np.exp(-t_2 / tau)))

    t_u = np.average(t_u_arr)
    t_u_err = np.std(t_u_arr)
    t_g = np.average(t_g_arr)
    t_g_err = np.std(t_g_arr)

    tau = fsolve(func, np.array([0.04]), args=(t_u, t_g))[0]
    tau_pp = fsolve(func, np.array([0.04]), args=(t_u + t_u_err, t_g + t_g_err))[0]
    tau_pm = fsolve(func, np.array([0.04]), args=(t_u + t_u_err, t_g - t_g_err))[0]
    tau_mp = fsolve(func, np.array([0.04]), args=(t_u - t_u_err, t_g + t_g_err))[0]
    tau_mm = fsolve(func, np.array([0.04]), args=(t_u - t_u_err, t_g - t_g_err))[0]
    tau_err = np.max([np.abs(tau_pp - tau), np.abs(tau_pm - tau),
                         np.abs(tau_mp - tau), np.abs(tau_mm - tau)])

    return tau, tau_err