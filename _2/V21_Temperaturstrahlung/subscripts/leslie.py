import numpy as np
from scrips.tools import sci_round


def emissionsvermoegen(schwarz: np.ndarray, weiss: np.ndarray, matt: np.ndarray, verspiegelt: np.ndarray) -> None:
    # Berechnung relativ zu Schwarz
    em_w, em_m, em_v = [np.zeros_like(schwarz) for _ in range(3)]
    for i in range(len(schwarz)):
        em_w[i] = weiss[i] / schwarz[i]
        em_m[i] = matt[i] / schwarz[i]
        em_v[i] = verspiegelt[i] / schwarz[i]

    # Mittelwerte und Runden
    em_w_mean = np.mean(em_w)
    delta_em_w = np.std(em_w) / np.sqrt(len(em_w))
    em_w_r, d_em_w_r = sci_round(em_w_mean, delta_em_w)

    em_m_mean = np.mean(em_m)
    delta_em_m = np.std(em_m) / np.sqrt(len(em_m))
    em_m_r, d_em_m_r = sci_round(em_m_mean, delta_em_m)

    em_v_mean = np.mean(em_v)
    delta_em_v = np.std(em_v) / np.sqrt(len(em_v))
    em_v_r, d_em_v_r = sci_round(em_v_mean, delta_em_v)

    # Ausgabe
    print('\nEmissionsvermögen von:')
    print(f'Weiss = {em_w_r} pm {d_em_w_r}')
    print(f'Matt = {em_m_r} pm {d_em_m_r}')
    print(f'Verspiegelt = {em_v_r} pm {d_em_v_r}\n---')

    return
