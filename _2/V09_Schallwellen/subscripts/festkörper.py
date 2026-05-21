import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def rod(frequencies, rule):
    def model(x, c):
        return c * x

    l = 1.138


    selected = find_valid_frequencies(frequencies, rule=rule)

    for i in range(len(selected)):
        fset = np.array(selected[i]).transpose()
        x = rule(fset[0]) / l
        y = fset[1]
        y_err = np.full_like(y, 50)
        y_err = np.array([(50 if (y[i] < 11e3) else 100) for i in range(len(y))])
        popt, pcov = curve_fit(model, x, y, sigma=y_err, absolute_sigma=True)
        c_val = popt[0]
        delta_c_val = np.sqrt(np.diag(pcov))[0]
        c_r, dc_r = sci_round(c_val, delta_c_val)

        print(f'Value for c = {c_r} pm {dc_r}, with {len(selected[i])} frequencies and lowest order {fset[0][0]} at {fset[1][0]} Hz')

        if i != 2 and frequencies[0] != 4.3e3:
            continue
        print(f'Serie:\n {fset.transpose()}')

        fit, ax = plt.subplots()
        ax.scatter(x, y, label='Messdaten', color='blue')
        ax.plot(x, model(x, c_val), label=f'Fit: $c = {c_r} \\pm {dc_r}$', color='red')
        ax.set_xlabel('$\\frac{n + 1/2}{L} / \\mathrm{m}^{-1}$')
        ax.set_ylabel('$\\nu / \\mathrm{Hz}$')
        ax.legend()
        ax.grid()

    plt.show()
    return selected


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
