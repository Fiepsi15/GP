import numpy as np

def get_moment_of_inertia(mass, dm, inner_radius, dri, outer_radius, dro):
    """
    Calculate the moment of inertia for a hollow cylinder.

    :param mass: Mass of the cylinder.
    :param dm: Uncertainty in mass.
    :param inner_radius: Inner radius of the cylinder.
    :param dri: Uncertainty in inner radius.
    :param outer_radius: Outer radius of the cylinder.
    :param dro: Uncertainty in outer radius.
    :return: Moment of inertia and its uncertainty.
    """
    # Moment of inertia for a hollow cylinder
    I = (1/2) * mass * (inner_radius**2 + outer_radius**2)

    # Uncertainty calculation
    dI = I * np.sqrt(((1/2) * (inner_radius**2 + outer_radius**2) * dm) ** 2
                     + (mass * inner_radius * dri) ** 2
                     + (mass * outer_radius * dro) ** 2)
    return I, dI
