import numpy as np


def logarithmic_decrement(x, x_plus_T):
    return np.log(x) - np.log(x_plus_T)


def prep_y(data):
    return logarithmic_decrement(data[1][0], data[1])  # Formel aus der Ausarbeitung hat doch gepasst


def eigenfrequenz(gamma, dgamma, omega, domega):
    omega0 = np.sqrt(omega ** 2 + gamma ** 2)
    domega0 = np.sqrt((omega * domega / np.sqrt(omega ** 2 + gamma ** 2)) ** 2
                      + (gamma * dgamma / np.sqrt(omega ** 2 + gamma ** 2)) ** 2)
    print(f"omega0 = {omega0} ± {domega0}")
    return omega0, domega0


def resonanzfrequenz(gamma, dgamma, omega, domega):
    omega_max = np.sqrt(omega ** 2 - gamma ** 2)
    domega_max = np.sqrt((omega * domega / np.sqrt(omega ** 2 - gamma ** 2)) ** 2
                         + (gamma * dgamma / np.sqrt(omega ** 2 - gamma ** 2)) ** 2)
    print(f"omega_max = {omega_max} ± {domega_max}")
    return omega_max, domega_max

def resonanzfrequenz_omega0(gamma, dgamma, omega0, domega0):
    omega_max = np.sqrt(omega0 ** 2 - 2*gamma ** 2)
    domega_max = np.sqrt((omega0 * domega0 / np.sqrt(omega0 ** 2 - 2 * gamma ** 2)) ** 2
                         + (2*gamma * dgamma / np.sqrt(omega0 ** 2 -2 * gamma ** 2)) ** 2)
    print(f"omega_max = {omega_max} ± {domega_max}")
    return omega_max, domega_max
