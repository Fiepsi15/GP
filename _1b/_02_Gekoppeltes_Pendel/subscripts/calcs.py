import numpy as np


# We got any Uncertainty here?
def get_k_statisch(m: float, g: float, L_S: float, x_1: float, x_2: float, L_K: float, L: float, delta_m, delta_L_S,
                   delta_X1, delta_x2, delta_L_K, delta_L) -> tuple[float, float]:
    """
    Berechnet die Federkonstante k für das gekoppelte Pendel.

    :param m: Masse des Pendels
    :param g: Erdbeschleunigung
    :param L_S: Länge bis zum Schwerpunkt des Pendels
    :param x_1: Auslenkung des ersten Pendels
    :param x_2: Auslenkung des zweiten Pendels
    :param L_K: Kopplungslänge
    :param L: Länge des Pendels
    :return: (Federkonstante k, Fehler in k)
    """
    return (m * g * L_S * x_2) / (L_K * x_1 * L), np.sqrt(
        ((g * L_S * x_2 / (L_K * x_1 * L)) * delta_m) ** 2 +
        ((m * g * x_2 / (L_K * x_1 * L)) * delta_L_S) ** 2 +
        ((m * g * L_S / (L_K * x_1 * L)) * delta_x2) ** 2 +
        ((m * g * L_S * x_2 / (L_K ** 2 * x_1 * L)) * delta_L_K) ** 2 +
        ((m * g * L_S * x_2 / (L_K * x_1 ** 2 * L)) * delta_X1) ** 2 +
        ((m * g * L_S * x_2 / (L_K * x_1 * L ** 2)) * delta_L) ** 2
    )


def get_Schwerpunktslaenge(I: float, m: float, omega: float, g: float, delta_I: float, delta_m: float,
                           delta_omega: float) -> tuple[float, float]:
    """
    Berechnet die Länge bis zum Schwerpunkt des Pendels.

    :param I: Trägheitsmoment des Pendels
    :param m: Masse des Pendels
    :param omega: Winkelgeschwindigkeit
    :param g: Erdbeschleunigung
    :return: (L_S, Fehler in L_S)
    """
    return (I * omega ** 2) / (m * g), np.sqrt((omega ** 2 / (m * g) * delta_I) ** 2
                                               + (I * omega ** 2 / (g * m ** 2) * delta_m) ** 2
                                               + (2 * I * omega / (m * g) * delta_omega) ** 2)


def get_Schwerpunktslaenge_from_Parameters(m_Z: float, L_Z: float, rho: float, L: float, R: float, m_K: float,
                                           L_K: float, m_M: float, L_M: float, ) -> float:
    """
    Berechnet die Länge bis zum Schwerpunkt des Pendels basierend auf den gegebenen Parametern.

    :param M_Z: Masse des Zylinders
    :param L_Z: Länge bis zum Zylinder
    :param L: Länge des Pendels
    :param R: Radius der Stange
    :param rho: Dichte des Materials
    :return: Schwerpunktslänge L_S
    """
    m = rho * np.pi * R ** 2 * L
    M = m_Z + m + m_K + m_M

    return (m_Z * L_Z + m * (L / 2) + m_K * L_K + m_M * L_M) / M


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
    return (M_Z * (1 / 12 * h ** 2 + 1 / 4 * (R2 ** 2 - R1 ** 2) + L_Z**2)
            + M_st * (1 / 3 * L ** 2 + 1 / 4 * R ** 2) + M_K * L_K ** 2 + M_M * L_M ** 2)


def get_Traegheitsmoment_from_Parameters_err(dL: float, dh: float, dm: float, M_Z: float, h: float, R1: float,
                                             R2: float, L_Z: float, M_st: float, L: float,
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

    return np.sqrt(
        ((1 / 12 * h ** 2 + 1 / 4 * (R2 ** 2 - R1 ** 2) + L_Z**2 ) * dm) ** 2
        + (1 / 6 * M_Z * h * dh) ** 2
        + (1 / 2 * M_Z * R2 * dh) ** 2
        + (1 / 2 * M_Z * R1 * dh) ** 2
        + (M_Z * dL) ** 2
        + ((1 / 3 * L ** 2 + 1 / 4 * R) * dm) ** 2
        + (2 / 3 * M_st * L * dL) ** 2
        + (1 / 4 * M_st * dh) ** 2
        + (L_K ** 2 * dm) ** 2
        + (2 * M_K * L_K * dL) ** 2
        + (L_M ** 2 * dm) ** 2
        + (2 * M_M * L_K * dL) ** 2
    )


def get_Traegheitsmoment_from_oscillation(k: float, L_K: float, Periode_0: float, Periode_180: float, delta_k=0,
                                          delta_L_K=0, delta_Periode_0=0, delta_Periode_180=0) -> tuple[float, float]:
    """
    :param k: Federkonstante der Kopplungsfeder
    :param L_K: Länge bis zur Kopplungsmontur
    :param Periode_0: Gleichphasig
    :param Periode_180: Gegenphasig
    :return: (Trägheitsmoment I, Fehler)
    """
    return (2 * k * L_K ** 2) / (Periode_180 ** 2 - Periode_0 ** 2), np.sqrt(
        ((2 * L_K ** 2) / (Periode_180 ** 2 - Periode_0 ** 2) * delta_k) ** 2 +
        ((4 * k * L_K) / (Periode_180 ** 2 - Periode_0 ** 2) * delta_L_K) ** 2 +
        ((4 * k * L_K ** 2 * Periode_0) / (Periode_180 ** 2 - Periode_0 ** 2) ** 2 * delta_Periode_0) ** 2 +
        ((4 * k * L_K ** 2 * Periode_180) / (Periode_180 ** 2 - Periode_0 ** 2) ** 2 * delta_Periode_180) ** 2
    )

def get_kopplungsgrad_from_parameters(m: float, delta_m: float, k: float, delta_k: float, L_S: float, delta_L_S:  float, L_K: float, delta_L_K: float):
    """
    Berechnet kappa aus Parametern.
    
    Parameter:
    m -- Masse
    k -- Federkonstante
    L_K -- Kopplungslänge
    g -- Erdbeschleunigung
    L_S -- Schwerpunktslänge
    """
    g= 9.81  # Erdbeschleunigung in m/s^2

    D = m * g * L_S + k * L_K**2
    
    # Partielle Ableitungen
    d_k =     (m * g * L_S * L_K**2) / D**2
    d_L_K = 2 * (k * m * g * L_S * L_K) / D**2
    d_m =   (k * L_K**2 * g * L_S)    / D**2
    d_L_S =   (k * L_K**2 * m * g)    / D**2
  
    return k * L_K**2 / (m * g * L_S + k * L_K**2), np.sqrt(
        (d_k * delta_k)**2 +
        (d_L_K * delta_L_K)**2 +
        (d_m * delta_m)**2 +
        (d_L_S * delta_L_S)**2
    )   
    

def get_kopplungsgrad_from_Eigenfrequenzen(Periode_0: float, Periode_180: float, delta_Periode_0: float,
                                           delta_Periode_180: float) -> tuple[float, float]:
    """
    Berechnet den Kopplungsgrad basierend auf den Eigenfrequenzen.

    :param Periode_0: Periode bei 0 Grad
    :param Periode_180: Periode bei gegenphasiger Schwingung (180 Grad)
    :return: (Kopplungsgrad, Fehler in Kopplungsgrad)
    """
    return (Periode_0 ** 2 - Periode_180 ** 2) / (Periode_0 ** 2 + Periode_180 ** 2), np.sqrt(
        (4 * Periode_0 * Periode_180 ** 2 / (Periode_0 ** 2 + Periode_180 ** 2) ** 2 * delta_Periode_0) ** 2
        + (4 * Periode_0 ** 2 * Periode_180 / (Periode_0 ** 2 + Periode_180 ** 2) ** 2 * delta_Periode_180) ** 2)


def get_kopplungsgrad_from_Schwebung(Phasenperiode: float, Gruppenperiode: float, delta_Phasenperiode: float,
                                     delta_Gruppenperiode: float) -> tuple[float, float]:
    """
    Berechnet den Kopplungsgrad basierend auf der Schwebung.

    :param Phasenperiode: Periode der Phasenverschiebung
    :param Gruppenperiode: Periode der Gruppengeschwindigkeit
    :return: (Kopplungsgrad, Fehler in Kopplungsgrad)
    """
    return 2 * (Phasenperiode * Gruppenperiode) / (Phasenperiode ** 2 + Gruppenperiode ** 2), np.sqrt(((
                                                                                                                   2 * Gruppenperiode * (
                                                                                                                       Phasenperiode ** 2 - Gruppenperiode ** 2)) / (
                                                                                                                   Phasenperiode ** 2 + Gruppenperiode ** 2) ** 2 * delta_Phasenperiode) ** 2
                                                                                                      + ((
                                                                                                                     2 * Phasenperiode * (
                                                                                                                         Gruppenperiode ** 2 - Phasenperiode ** 2)) / (
                                                                                                                     Gruppenperiode ** 2 + Phasenperiode ** 2) ** 2 * delta_Gruppenperiode) ** 2)
