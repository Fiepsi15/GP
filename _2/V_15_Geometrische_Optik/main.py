import numpy as np
from _2.V_15_Geometrische_Optik.subscripts import brennweite_abbildung as abb
from _2.V_15_Geometrische_Optik.subscripts import brennweite_bessel as bess
from _2.V_15_Geometrische_Optik.subscripts import mikroskop as mikr
from scrips.tools import sci_round

# 3.1.1
print("Brennweite Abbildungsverfahren:")

# Linse 1: f = 60mm

g1 = np.array([8.2, 9.0, 7.5, 10.0]) / 1e2
b1 = np.array([23, 18, 33, 14.4]) / 1e2
dg = np.full_like(g1, 1e-3)
db = np.full_like(g1, 1e-3)

_ = abb.calculate_f(g1, b1, dg, db, name="f1")

# Linsensystem: f1= 60mm, f2 = -150mm

g2 = np.array([14.5, 15, 16, 17]) / 1e2
b2 = np.array([26.5, 25.8, 21.6, 21.5]) / 1e2

f, df = abb.calculate_f(g2, b2, dg, db, name="f2")
d, dd = abb.calculate_d(60, -150, f * 1e3, df * 1e3)

print(f"therefore, d must be about {d} ± {dd} mm")

# 3.1.2
print("\nBrennweite Besselverfahren:")

d1 = np.array([50, 48, 46, 44]) / 1e2
s1 = np.array([14.3, 15, 15.2, 16.1]) / 1e2
s2 = np.array([36.4, 33.9, 31.2, 28.4]) / 1e2
a1 = np.abs(s2 - s1)
delta_d = np.float64(1e-3)
delta_a = np.sqrt(2) * delta_d

_ = bess.calculate_f(d1, a1, dd=np.full_like(d1, delta_d), da=np.full_like(d1, delta_a), name="f1")

d2 = np.array([50, 48, 46, 44]) / 1e2
s1 = np.array([11.9, 12.1, 12.5, 13.6]) / 1e2
s2 = np.array([37.9, 34.4, 32, 29.9]) / 1e2
a2 = np.abs(s2 - s1)

f, df = bess.calculate_f(d2, a2, dd=np.full_like(d2, delta_d), da=np.full_like(d2, delta_a), name="f2")
d, dd = abb.calculate_d(60, -150, f * 1e3, df * 1e3)

print(f"therefore, d must be about {d} ± {dd} mm")

# 3.4 Mikroskop


s1 = np.array([20, 20, 20])
s2 = np.array([2.4, 2.2, 3.3])
ds1 = 1
ds2 = 0.1

V_Obj, dV_Obj = mikr.get_vergroesserung_obj(s1, s2, ds1, ds2)
V_Objr, dV_Objr = np.zeros_like(V_Obj), np.zeros_like(V_Obj)
for i in range(len(V_Obj)):
    V_Objr[i], dV_Objr[i] = sci_round(V_Obj[i], dV_Obj[i])
print(f'\n Obj. Vergrößerung: {V_Objr} ± {dV_Objr}')

s = 0.25
d = np.array([18.3, 19, 14]) * 1e-2
dd = np.full_like(d, 1e-3)
f_Obj = 16 * 1e-3
f_Ok = 25 * 1e-3

V, dV = mikr.get_vergroesserung(s, d, f_Obj, f_Ok, dd)
Vr, dVr = np.zeros_like(V), np.zeros_like(V)
for i in range(len(V_Obj)):
    Vr[i], dVr[i] = sci_round(V[i], dV[i])
print(f'Gesamtvergrößerung: {Vr} ± {dVr}')

Vm, dVm = mikr.get_ges_meas(V_Obj, f_Ok, s, dV_Obj)
Vmr, dVmr = np.zeros_like(V), np.zeros_like(V)
for i in range(len(V_Obj)):
    Vmr[i], dVmr[i] = sci_round(Vm[i], dVm[i])
print(f'Gesamtvergrößerung (gemessen): {Vmr} ± {dVmr}')