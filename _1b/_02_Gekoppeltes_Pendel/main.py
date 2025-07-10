import _1b._02_Gekoppeltes_Pendel.subscripts.calcs as calcs
from scrips import tools, array_to_tex
import numpy as np

m_Z = 284.49e-3  # Masse des Zylinders in kg
L_Z = 48.1e-2  # Länge bis zum Zylinder in m
R1 = 0.61e-2 / 2  # Innenradius des Zylinders in m
R2 = 3e-2 / 2  # Aussenradius des Zylinders in m
h = 5e-2  # Höhe des Zylinders in m
rho = 7.7e3  # Dichte des Materials in kg/m^3
L = 51.7e-2  # Länge des Pendels in m
R = (6.1/2)*1e-3  # Radius der Stange in m
M_st = np.pi * R ** 2 * L * rho  # Masse der Stange in kg
m_K = 30.72e-3  # Masse der Kopplungsmontur in kg
L_K = 44e-2  # Kopplungslänge in m
m_M = 2.09e-3  # Masse der Mutter in kg
L_M = 50.50e-2  # Länge bis zur Mutter in m
m = m_Z + M_st + m_K + m_M  # Gesamtmasse in kg

dL = 0.1e-2  # Unsicherheit in der Länge in m
d_h = 0.05e-3  # Unsicherheit in der genau gemessenen Längen in m
dm = 0.01e-3  # Unsicherheit in der Masse in kg



L_S = calcs.get_Schwerpunktslaenge_from_Parameters(m_Z, L_Z, rho, L, R, m_K, L_K, m_M, L_M)
I_1 = calcs.get_Traegheitsmoment_from_Parameters(m_Z, h, R1, R2, L_Z, M_st, L, R, m_K, L_K, m_M, L_M)
I_2 = calcs.get_Traegheitsmoment_from_Parameters(m_Z, h, R1, R2, L_Z, M_st, L, R, m_K, L_K-4e-2, m_M, L_M)
I_3 = calcs.get_Traegheitsmoment_from_Parameters(m_Z, h, R1, R2, L_Z, M_st, L, R, m_K, L_K-8e-2, m_M, L_M)
dI = calcs.get_Traegheitsmoment_from_Parameters_err(dL, d_h, dm, m_Z, h, R1, R2, L_Z, M_st, L, R, m_K, L_K-4e-2, m_M, L_M)
print(f"Schwerpunktslänge: {L_S} m")
print(f"Trägheitsmoment_1= {I_2:.4f} kg*m^2")
print(f"Trägheitsmoment_2= {I_3:.4f} kg*m^2")
print(f"Trägheitsmoment_3= {I_1:.4f} kg*m^2")
print(f"Unsicherheit im Trägheitsmoment: {dI} kg*m^2")

Is = np.array([[L_K, L_K-4e-2, L_K-8e-2], [I_1, I_2, I_3]])
array_to_tex.array_to_tex(Is, [[1e-3 for _ in range(3)], [dI for _ in range(3)]], [["L_K", "I"], ["m", "kg*m^2"]], "Trägheitsmomente", "träg para")

print("\n\nFederkonstante:")
print(calcs.get_k_statisch(m, 9.81, L_S, 101e-3, 6e-3, L_K, L, dm, dL, dL, dL, dL, dL))
print("\n\nSchwerpunktslänge:")
print(calcs.get_Schwerpunktslaenge(I_1, m, 2*np.pi / 1.356, 9.81, dI, dm, 2*np.pi/ 0.023))
