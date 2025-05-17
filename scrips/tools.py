import math

def round_up(n, decimals=0):
    n = n * 10 ** decimals
    n = math.ceil(n)
    return n * 10 ** -decimals