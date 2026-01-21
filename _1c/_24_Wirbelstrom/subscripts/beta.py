import numpy as np

def beta_bestimmung(m, m_err, g, sigma, sigma_err, B0, B0_err, r, r_err, d, d_err, k, k_err):
    # Berechnung von beta
    pi = np.pi
    numerator = m * g
    denominator = k * sigma * B0**2 * pi * r**2 * d
    beta = numerator / denominator

    # Fehlerfortpflanzung nach Gauß
    dbeta_dm = g / denominator
    dbeta_dk = -m * g / (k**2 * sigma * B0**2 * pi * r**2 * d)
    dbeta_dsigma = -m * g / (k * sigma**2 * B0**2 * pi * r**2 * d)
    dbeta_dB0 = -2 * m * g / (k * sigma * B0**3 * pi * r**2 * d)
    dbeta_dr = -2 * m * g / (k * sigma * B0**2 * pi * r**3 * d)
    dbeta_dd = -m * g / (k * sigma * B0**2 * pi * r**2 * d**2)

    beta_err = np.sqrt(
        (dbeta_dm * m_err) ** 2 +
        (dbeta_dk * k_err) ** 2 +
        (dbeta_dsigma * sigma_err) ** 2 +
        (dbeta_dB0 * B0_err) ** 2 +
        (dbeta_dr * r_err) ** 2 +
        (dbeta_dd * d_err) ** 2
    )
    return beta, beta_err

