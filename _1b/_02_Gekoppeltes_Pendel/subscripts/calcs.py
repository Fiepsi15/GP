import numpy as np


def get_k_statisch(m: float, g: float, L_S: float, x_1: float, x_2: float, L_K: float, L: float) -> float:
    """
    Berechnet die statische Federkonstante k für das gekoppelte Pendel.

    :param m: Masse des Pendels
    :param g: Erdbeschleunigung
    :param L_S: Länge bis zum Schwerpunkt des Pendels
    :param x_1: Auslenkung des ersten Pendels
    :param x_2: Auslenkung des zweiten Pendels
    :param L_K: Kopplungslänge
    :param L: Länge des Pendels
    :return: Federkonstante k
    """
    return (m * g * L_S * x_2) / (L_K * x_1 * L)


def get_Schwerpunktslaenge(I: float, m: float, omega: float, g: float, delta_I: float, delta_m: float, delta_omega: float) -> tuple[float, float]:
    """
    Berechnet die Länge bis zum Schwerpunkt des Pendels.

    :param I: Trägheitsmoment des Pendels
    :param m: Masse des Pendels
    :param omega: Winkelgeschwindigkeit
    :param g: Erdbeschleunigung
    :return: L_S
    """
    return (I * omega ** 2) / (m * g), np.sqrt((omega ** 2 /(m * g) * delta_I) ** 2
                                               + (I * omega ** 2 / (g * m ** 2) * delta_m) ** 2
                                               + (2 * I * omega / (m * g) * delta_omega) ** 2)


def get_Traegheitsmoment_from_Parameters(M_Z: float, h: float, R1: float, R2: float, L_Z: float, M_st: float, L: float,
                                         R: float, M_K: float, L_K: float, M_M: float, L_M: float) -> float:
    """
    Berechnet das Trägheitsmoment des Pendels basierend auf den gegebenen Parametern.

    :param M_Z: Masse des Zylinders
    :param h: Höhe des Zylinders
    :param R1: Innenradius des Zylinders
    :param R2: Aussenradius des Zylinders
    :param L_Z: Länge bis zum Zylinders
    :param M_st: Masse der Stange
    :param L: Länge des Pendels
    :param R: Radius der Stange
    :param M_K: Masse der Kopplungsmontur
    :param L_K: Kopplungslänge
    :param M_M: Masse der Mutter
    :param L_M: Länge bis zur Mutter
    :return: Trägheitsmoment I
    """
    return (M_Z * (1 / 12 * h ** 2 + 1 / 4 * (R2 ** 2 - R1 ** 2) + L_Z)
            + M_st * (1 / 3 * L ** 2 + 1 / 4 * R) + M_K * L_K ** 2 + M_M * L_M ** 2)


def get_kopplungsgrad_from_Eigenfrequenzen(Periode_0: float, Periode_180: float) -> float:
    """
    Berechnet den Kopplungsgrad basierend auf den Eigenfrequenzen.

    :param Periode_0: Periode bei 0 Grad
    :param Periode_180: Periode bei gegenphasiger Schwingung (180 Grad)
    :return: Kopplungsgrad
    """
    return (Periode_0 ** 2 - Periode_180 ** 2) / (Periode_0 ** 2 + Periode_180 ** 2)

def get_kopplungsgrad_from_Schwebung(Phasenperiode: float, Gruppenperiode: float) -> float:
    """
    Berechnet den Kopplungsgrad basierend auf der Schwebung.

    :param Phasenperiode: Periode der Phasenverschiebung
    :param Gruppenperiode: Periode der Gruppengeschwindigkeit
    :return: Kopplungsgrad
    """
    return 2 * (Phasenperiode * Gruppenperiode) / (Phasenperiode ** 2 + Gruppenperiode ** 2)
