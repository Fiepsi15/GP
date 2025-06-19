import math
import numpy as np

def round_up(n, decimals=0):
    n = n * 10 ** decimals
    n = math.ceil(n)
    return np.round(n * 10 ** -decimals, decimals + 2)


# TODO Make entire funktion for scientific rounding
def round_to_any_digit(n, decimals=0):
    n = n * 10 ** decimals
    n = np.round(n, 0)
    return np.round(n * 10 ** -decimals, decimals + 2)


def find_first_nonzero_digit(n):
    n_s = str(n)
    position = 0
    pre_decimals = 0
    for i in range(len(n_s)):
        if n_s[i] == '.':
            pre_decimals = i
            continue
        if n_s[i] != '0':
            position = i if pre_decimals == 0 else i - 1
            break
    return pre_decimals, position


def sci_round(n, delta_n, delta_delta_n=1/3):
    delta_n_s = str(delta_n)
    print(delta_n_s)
    print(delta_n * delta_delta_n)
    pre_decimals, position = find_first_nonzero_digit(delta_n * delta_delta_n)

    print(position, pre_decimals)
    try:
        print(delta_n_s[position + pre_decimals])
    except IndexError:
        print("Uncertainty * Uncertainty**2 is to close to one, floating point math. ..")
        return


