import numpy as np
import _1b._12_Latente_Waerme.subscripts._3_1_script as kalo
import _1b._12_Latente_Waerme.subscripts._3_2_script as eis
import _1b._12_Latente_Waerme.subscripts._3_3_script as dampf

T_h = 45.7
T_c = 24
T_f = 35.2
m_h = 49.88e-3
m_c = 50e-3

print("Calculating heat capacity of the calorimeter...")
C_K1 = kalo.calculate_kalorimeter_heat_capacity([T_h, T_c, T_f, m_h, m_c])

C_K2 = kalo.calculate_kalorimeter_heat_capacity([45.2, 24.5, 35.2, 49.48e-3, 49.41e-3])

C_K = np.mean([C_K1, C_K2])
print("mean C_K:", C_K)

print("\nCalculating latent heat of fusion of ice...")
eis.Eis_Ls(C_K, 44, 0.5, 20, 50e-3, 19.13e-3)
eis.Eis_Ls(C_K, 48.6, 0.4, 18.2, 49.69e-3, 19.24e-3)

print("\nCalculating latent heat of condensation of water...")
dampf.Latentnt_heat_of_condensation(C_K, 98.2, 23.8, 52.6, 7.6e-3, 143.53e-3)
dampf.Latentnt_heat_of_condensation(C_K, 98.2, 19.4, 47.6, 7.55e-3, 159.52e-3)

print("\nCalculating latent heat of boiling water...")
dampf.Latent_heat_of_boiling_water(94, 2, 240, (66.94 - 49.02) * 1e-3)
dampf.Latent_heat_of_boiling_water(85, 1.8, 240, (64.28 - 49.00) * 1e-3)
dampf.Latent_heat_of_boiling_water(70, 1.5, 240, (59.00 - 48.87) * 1e-3)



