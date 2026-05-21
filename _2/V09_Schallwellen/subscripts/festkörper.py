import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.optimize import curve_fit
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def rod(frequencies, rule, ax, title):
    def model(x, c):
        return c * x

    l = 1.138
    dl = 1e-3
    c, dc = 0, 0

    selected = find_valid_frequencies(frequencies, rule=rule)

    for i in range(len(selected)):
        fset = np.array(selected[i]).transpose()
        x = rule(fset[0]) / l
        x_err = rule(fset[0]) / l ** 2 * dl
        y = fset[1]
        y_err = np.array([(50 if (y[i] < 11e3) else 100) for i in range(len(y))])
        popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
        c_val = popt[0]
        delta_c_val = np.sqrt(np.diag(pcov))[0]
        c_r, dc_r = sci_round(c_val, delta_c_val)

        print(
            f'Value for c = {c_r} pm {dc_r}, with {len(selected[i])} frequencies and lowest order {fset[0][0]} at {fset[1][0]} Hz')

        if i != 2 and frequencies[0] != 4.3e3:
            continue

        #a2t(np.array([x, y]), np.array([x_err, y_err]), [['$(2n + 1)/l$', '$\\nu$'], ['$\\mathrm{m}^{-1}$', '$\\mathrm{Hz}$']], override_row_len=3)
        c, dc = c_val, delta_c_val

        ax.grid()
        ax.yaxis.minorticks_on()
        ax.tick_params(direction='in', which='both')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.errorbar(fset[0], y, yerr=y_err, label='Messdaten', color='blue', capsize=5, fmt='.')
        ax.plot(fset[0], model(x, c_val), label=f'lineare Regression liefert:\n$c = ({c_r} \\pm {dc_r})\\; \\mathrm{'{'}m{'}'}/ \\mathrm{'{'}s{'}'}$', color='red')
        ax.plot(fset[0], model(x, c_val + delta_c_val), label=f'$\\pm\\delta c$', color='grey', linestyle='dashed')
        ax.plot(fset[0], model(x, c_val - delta_c_val), color='grey', linestyle='dashed')
        ax.set_xlabel('$n$')
        ax.set_ylabel('$\\nu / \\mathrm{Hz}$')
        ax.legend()
        ax.set_title(title)

    return c, dc


def find_valid_frequencies(frequencies, rule):
    n = np.array([i for i in range(len(frequencies))])
    possible = []
    for i in range(len(frequencies)):
        for j in range(10):
            valid = []
            pred_freq = (rule(n)) / (rule(j)) * frequencies[i]
            for f in frequencies:
                for k in range(len(pred_freq)):
                    if abs(pred_freq[k] - f) < 0.01 * pred_freq[k]:
                        valid.append((k, f))
            if len(valid) > 2:
                for k in range(len(possible)):
                    if possible[k][0][0] == valid[0][0] and possible[k][0][1] == valid[0][1]:
                        possible.pop(k)
                        break
                possible.append(valid)

    return possible
