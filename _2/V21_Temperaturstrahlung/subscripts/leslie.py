import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def emissionsvermoegen(t, schwarz: np.ndarray, weiss: np.ndarray, matt: np.ndarray, verspiegelt: np.ndarray, delta_relative) -> None:
    # Gaus Fehlerfortpflanzung liefert:
    delta_em_rel = np.sqrt(2) * delta_relative

    # Berechnung relativ zu Schwarz
    em_w, em_m, em_v = [np.zeros_like(schwarz) for _ in range(3)]
    for i in range(len(schwarz)):
        em_w[i] = weiss[i] / schwarz[i]
        em_m[i] = matt[i] / schwarz[i]
        em_v[i] = verspiegelt[i] / schwarz[i]

    # Mittelwerte und Runden
    em_w_mean = np.mean(em_w)
    delta_em_w = delta_em_rel / len(em_w) * np.sqrt(np.sum(em_w ** 2))
    em_w_r, d_em_w_r = sci_round(em_w_mean, delta_em_w)

    em_m_mean = np.mean(em_m)
    delta_em_m = delta_em_rel / len(em_m) * np.sqrt(np.sum(em_m ** 2))
    em_m_r, d_em_m_r = sci_round(em_m_mean, delta_em_m)

    em_v_mean = np.mean(em_v)
    delta_em_v = delta_em_rel / len(em_v) * np.sqrt(np.sum(em_v ** 2))
    em_v_r, d_em_v_r = sci_round(em_v_mean, delta_em_v)

    # Ausgabe
    print('\nEmissionsvermögen von:')
    print(f'Weiss = {em_w_r} pm {d_em_w_r}')
    print(f'Matt = {em_m_r} pm {d_em_m_r}')
    print(f'Verspiegelt = {em_v_r} pm {d_em_v_r}\n---')

    #a2t(np.array([t, em_w, em_m, em_v]), np.array([np.full_like(t, 0.1), delta_em_rel * em_w, delta_em_rel * em_m, delta_em_rel * em_v]), [['$T$', '$\\varepsilon_\\mathrm{W}$', '$\\varepsilon_\\mathrm{M}$', '$\\varepsilon_\\mathrm{V}$'],['$\\mathrm{°C}$', '', '', '']], 'leslie.tex')

    return
