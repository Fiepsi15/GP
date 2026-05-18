import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scrips.tools import sci_round


def rod():
    def model(x, c):
        return c * x

    l = 1.138

    frequency = np.array(
        [[2.150, 6], [4.300, 6], [6.450, 6], [8.600, 5], [9.950, 2], [10.750, 5], [12.9, 2], [15.1, 3], [17.2, 2],
         [19.4, 2], [21.5, 3]]).transpose() * 1e3

    def rule1(i):
        return i + 1 / 2

    selected = find_valid_frequencies(frequency[0], rule=rule1)

    for i in range(len(selected)):
        fset = np.array(selected[i]).transpose()
        x = (fset[0] + 1 / 2) / l
        y = fset[1]
        popt, pcov = curve_fit(model, x, y)
        c_val = popt[0]
        delta_c_val = np.sqrt(np.diag(pcov))[0]
        c_r, dc_r = sci_round(c_val, delta_c_val)

        print(f'Value for c = {c_r} pm {dc_r}')

        if i != 2:
            continue

        fit, ax = plt.subplots()
        ax.scatter(x, y, label='Messdaten', color='blue')
        ax.plot(x, model(x, c_val), label=f'Fit: $c = {c_r} \\pm {dc_r}$', color='red')
        ax.set_xlabel('$\\frac{n + 1/2}{L} / \\mathrm{m}^{-1}$')
        ax.set_ylabel('$\\nu / \\mathrm{Hz}$')
        ax.legend()
        ax.grid()

    plt.show()
    return


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
