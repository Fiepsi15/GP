import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def get_sonic_speed_reg(nu, d, N, plot_axis, d_nu, d_d, d_N, plot_title=''):
    def  model(x, c):
        return x * c

    x = N / (2 * d)
    y = nu
    y_err = np.full_like(y, d_nu)
    x_err = np.sqrt((d_N / (2 * d)) ** 2
                    + (N / (2 * d ** 2) * d_d) ** 2)

    #a2t(np.array([x, y]), np.array([x_err, y_err]), [['$n/2d$', '$\\nu$'], ['$\\mathrm{m}^{-1}$', '$\\mathrm{Hz}$']], caption='Luft')

    popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
    c = popt[0]
    d_c = np.sqrt(np.diag(pcov))[0]
    c_r, dc_r = sci_round(c, d_c)
    print(c_r, dc_r)

    plot_axis.errorbar(x, y, yerr=y_err, xerr=x_err, fmt='.', capsize=5, color='blue', label='Messdaten')
    plot_axis.plot(x, model(x, c), color='red', label=f'lineare Regression liefert:\n$c = ({c_r} \\pm {dc_r})\\; \\mathrm{'{'}m{'}'}/ \\mathrm{'{'}s{'}'}$')
    plot_axis.plot(x, model(x, c + d_c), color='grey', linestyle='dashed', label='$\\pm \\delta c $')
    plot_axis.plot(x, model(x, c - d_c), color='grey', linestyle='dashed')
    plot_axis.set_title(plot_title)
    plot_axis.set_xlabel('$\\frac{n}{2d}/\\mathrm{m}^{-1}$')
    plot_axis.set_ylabel('$\\nu/\\mathrm{Hz}$ ')
    plot_axis.minorticks_on()
    plot_axis.tick_params(direction='in', which='both')
    plot_axis.grid(True)
    plot_axis.legend()

    return c, d_c