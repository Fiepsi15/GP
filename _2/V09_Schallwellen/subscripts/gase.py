import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def get_sonic_speed_reg(nu, d, N, plot_axis, d_nu, d_d, d_N, plot_title=''):
    def  model(x, c):
        return x * c

    x = N / (2 * d)
    y = nu
    y_err = d_nu
    x_err = np.sqrt((d_N / (2 * d)) ** 2
                    + (N / (2 * d ** 2) * d_d) ** 2)

    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    c = popt[0]
    d_c = np.sqrt(np.diag(pcov))
    c_r, dc_r = sci_round(c, d_c)

    plot_axis.errorbar(x, y, yerr=y_err, xerr=x_err, fmt='.', capsize=5, color='blue', label='Messdaten')
    plot_axis.plot(x, model(x, c), color='red', label=f'Fit: $c = {c_r} \\pm {dc_r}$')
    plot_axis.set_title(plot_title)
    plot_axis.set_xlabel('$\\frac{N}{2d}/(\\mathrm{m})^{-1}$')
    plot_axis.set_ylabel('$\\nu/\\mathrm{Hz}$ ')
    plot_axis.grid(True)
    plot_axis.legend()

    return c, d_c