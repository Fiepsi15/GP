import math
import numpy as np

def round_up(n, decimals=0):
    n = n * 10 ** decimals
    n = math.ceil(n)
    return np.round(n * 10 ** -decimals, decimals + 2)


def find_first_nonzero_digit(n):
    n_s = str(n)
    pre_decimals = 0
    for i in range(len(n_s)):
        if n_s[-i-1] == 'e':
            pre_decimals = int(n_s[-i+1:])
            position = pre_decimals
            return pre_decimals, position
    for i in range(len(n_s)):
        if n_s[i] == '.':
            pre_decimals = i
            break
    position = 0
    for i in range(len(n_s)):
        if n_s[i] == '.':
            continue
        if n_s[i] != '0':
            position = i if pre_decimals == 0 else i - pre_decimals
            break
    return pre_decimals, position


def sci_round(n, delta_n, delta_delta_n=1/3):
    dpre_decimals, dposition = find_first_nonzero_digit(delta_n * delta_delta_n)

    if dposition < 0:
        dposition += 1
    return np.round(n, dposition), round_up(delta_n, dposition)


