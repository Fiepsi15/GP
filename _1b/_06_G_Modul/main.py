import numpy as np
from _1b._06_G_Modul.subscripts import GReg as sub
from _1b._06_G_Modul.subscripts import Moment_of_Inertia as MoI
from scrips.array_to_tex import array_to_tex as a2t


def unwrap_and_mean(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    data_bar = np.mean(data, axis=1) / 3
    delta_data = np.std(data, axis=1) / 3
    return data_bar, delta_data


dm = 0.1e-3  # Uncertainty in mass (kg)
dR = 0.5e-3 / 2  # Uncertainty in radius (m)
dl = 1e-3  # Uncertainty in length of the Wire(m)
dr = 0.01e-3 / 2 # Uncertainty in radius of the Wire(m)

# Calculate the moments of inertia for the rings
rings = np.loadtxt('_1b/_06_G_Modul/daten/ring_data.csv', skiprows=1, delimiter=',').transpose()[1:4, :] * 1e-3  # Load data and convert to kg and meters
rings[1] = rings[1] / 2  # Convert diameter to radius
rings[2] = rings[2] / 2  # Convert diameter to radius
moments_of_inertia, Delta_moments_of_inertia = MoI.get_moment_of_inertia(rings[0], dm, rings[1], dR, rings[2], dR)
print(rings, '\n')
rings = rings.tolist()
rings.append(moments_of_inertia.tolist())

# Create a LaTeX table for the moments of inertia
a2t(np.array(rings),
    np.array([[dR for _ in range(len(rings[0]))], [dR for _ in range(len(rings[0]))], [dm for _ in range(len(rings[0]))], Delta_moments_of_inertia]),
    [['$R_1$', '$R_2$', '$m$', '$I$'], ['m', 'm', 'kg', 'kgm$^2$']],
    'Moment_of_Inertia', 'Moment of Inertia of the Rings')

# Calculate the G-Modulus from the torsion oscillation of the aluminum wire
print()
alu = np.loadtxt('_1b/_06_G_Modul/daten/alu_times.csv', skiprows=1, delimiter=',')[:, 1:6]  # Load data and convert to kg and meters
alu_bar, delta_alu = unwrap_and_mean(alu)
G_alu, dG_alu = sub.g_mod_regression(alu_bar, delta_alu, moments_of_inertia, Delta_moments_of_inertia, length=0.957, dl=dl, radius=1e-3, dr=dr)
print(G_alu, dG_alu)
print('abweichung tabellenwert', G_alu / 26e9)

# Steel
print()
steel = np.loadtxt('_1b/_06_G_Modul/daten/stahl_times.csv', skiprows=1, delimiter=',')[:, 1:6]  # Load data and convert to kg and meters
steel_bar, delta_steel = unwrap_and_mean(steel)
G_steel, dG_steel = sub.g_mod_regression(steel_bar, delta_steel, moments_of_inertia, Delta_moments_of_inertia, length=0.961, dl=dl, radius=1.58e-3 / 2, dr=dr)
print(G_steel, dG_steel)
print('abweichung tabellenwert', G_steel / 75e9)

# Brass
print()
brass = np.loadtxt('_1b/_06_G_Modul/daten/messing_times.csv', skiprows=1, delimiter=',')[:, 1:6]  # Load data and convert to kg and meters
brass_bar, delta_brass = unwrap_and_mean(brass)
G_brass, dG_brass = sub.g_mod_regression(brass_bar, delta_brass, moments_of_inertia, Delta_moments_of_inertia, length=0.962, dl=dl, radius=1.93e-3 / 2, dr=dr)
print(G_brass, dG_brass)
print('abweichung tabellenwert', G_brass / 35e9)

