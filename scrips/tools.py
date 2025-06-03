import math
import numpy as np

def round_up(n, decimals=0):
    n = n * 10 ** decimals
    n = math.ceil(n)
    return np.round(n * 10 ** -decimals, decimals + 2)

#TODO Make entire funktion for scientific rounding