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
array_to_tex.array_to_tex(Is, [[1e-3 for _ in range(3)], [dI for _ in range(3)]], [["$L_K$", "$I$"], ["\\text{m}", "\\text{kg}\\cdot\\text{m}^2"]], "Trägheitsmomente", "träg para")

print("\n\nFederkonstante:")
k = calcs.get_k_statisch(m, 9.81, L_S, 101e-3, 6e-3, L_K, L, dm, dL, dL, dL, dL, dL)
print(k)
print("\n\nSchwerpunktslänge:")

T_0 = np.array([1.350, 1.356, 1.340]) #In Phase
dT_0 = np.array([0.028, 0.023, 0.020])

T_1 = np.array([1.275, 1.280, 1.283]) # Gegenphase
dT_1 = np.array([0.025, 0.025, 0.028])

T_P = np.array([1.343, 1.51, 1.352]) # Phase
dT_P = np.array([0.030, 0.03, 0.028])

T_G = np.array([45.7, 60.5, 94]) # Gruppe
dT_G = np.array([1.3, 2, 4])

print(calcs.get_Schwerpunktslaenge(calcs.get_Traegheitsmoment_from_oscillation(k[0], L_K, 2 * np.pi / T_0[0], 2 * np.pi / T_1[0])[0], m, 2*np.pi / 1.350, 9.81, 0.036, dm, 2*np.pi/(1.35 ** 2) * 0.023))
print("\n\nKopplungsgrad:")
kappa, dkappa = calcs.get_kopplungsgrad_from_Eigenfrequenzen(T_0, T_1, dT_0, dT_1)
array_to_tex.array_to_tex(np.array([[L_K, L_K-4e-2, L_K-8e-2], kappa]), [[dL for _ in range(3)], dkappa], [["L_K", "\\kappa"], ["m", ""]], "Kopplungsgrad", "kopplungsgrad")

print("\n\nKopplungsgrad schwebung:")
kappa_s, dkappa_s = calcs.get_kopplungsgrad_from_Schwebung(T_P, T_G, dT_P, dT_G)
array_to_tex.array_to_tex(np.array([[L_K, L_K-4e-2, L_K-8e-2], kappa_s]), [[dL for _ in range(3)], dkappa_s], [["L_K", "\\kappa"], ["m", ""]], "Kopplungsgrad Schwebung", "kopplungsgrad_schwebung")

print("\n\nTrägheitsmoment aus Schwingung:")
print(calcs.get_Traegheitsmoment_from_oscillation(k[0], L_K, 2 * np.pi / T_0, 2 * np.pi / T_1, k[1], dL, 2 * np.pi/(T_0 ** 2) * dT_0, 2 * np.pi/(T_1 ** 2) * dT_1))

'''
omega_P = 2 * np.pi / T_P
omega_G = 2 * np.pi / T_G

domega_P = 2 * np.pi / (T_P ** 2) * dT_P
domega_G = 2 * np.pi / (T_G ** 2) * dT_G

domega = domega_G + domega_P

omega_1 = omega_P + omega_G
omega_2 = omega_P - omega_G
print(calcs.get_Traegheitsmoment_from_oscillation(k[0], L_K, omega_2, omega_1, k[1], dL, domega, domega))
'''

print("\n\nKopplungsgrad aus Parametern:")
kappa, dkappa = calcs.get_kopplungsgrad_from_parameters(m, dm, k[0], k[1], L_S, dL, np.array([L_K, L_K-4e-2, L_K-8e-2]), dL)
array_to_tex.array_to_tex(np.array([[L_K, L_K-4e-2, L_K-8e-2], kappa]), [[dL for _ in range(3)], dkappa], [["L_K", "\\kappa"], ["m", ""]], "Kopplungsgrad aus Parametern", "kopplungsgrad_param")
print(f"kappa {kappa}{dkappa}")




#Die Einzelnen Trägheitsmomente Tabelle muss noch erstellt werden
I_Zylinder = m_Z * (1 / 12 * h**2 + 1 / 4 * (R2**2 - R1**2) + L_Z**2)
I_Zylinder_err = np.sqrt(
    ((1 / 12 * h**2 + 1 / 4 * (R2**2 - R1**2) + L_Z**2) * dm) ** 2
    + (1 / 6 * m_Z * h * d_h) ** 2
    + (1 / 2 * m_Z * R2 * d_h) ** 2
    + (1 / 2 * m_Z * R1 * d_h) ** 2
    + (m_Z * dL) ** 2
)
I_stange = M_st * (1 / 3 * L**2 + 1 / 4 * R**2)
I_stange_err = np.sqrt(
    ((1 / 3 * L**2 + 1 / 4 * R) * dm) ** 2
    + (2 / 3 * M_st * L * dL) ** 2
    + (1 / 4 * M_st * d_h) ** 2
)
I_Mutter = m_M * L_M**2
I_Mutter_err = np.sqrt((L_M**2 * dm) ** 2 + (2 * m_M * L_K * dL) ** 2)
I_Federmontur = np.zeros(3)
I_Federmontur_err = np.zeros(3)
for i in range(3):
    I_Federmontur[i] = m_K * (L_K - i * 4e-2) ** 2
    I_Federmontur_err[i] = np.sqrt(
        ((L_K - i * 4e-2) ** 2 * dm) ** 2 + (2 * m_K * (L_K - i * 4e-2) * dL) ** 2
    )

arr = np.array([I_Zylinder, I_stange, I_Mutter])
arr_err = np.array([I_Zylinder_err, I_stange_err, I_Mutter_err])
print(arr)
print(arr_err)
