import numpy as np
from DDA.E_mod.subscripts import dynamisch as dyn

data_dir_dyn = 'DDA/E_mod/daten/dynamisch'
data_dir_stat = 'DDA/E_mod/daten/statisch'
Datenbank = {'Kupfer': {'l_ges': 319.5e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 27.17e-3},
             'Stahl_dünn': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 0.55e-3, 'm': 26.59e-3},
             'Stahl_dick': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 1e-3, 'm': 46.84e-3},
             'Alu_dünn': {'l_ges': 302e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 8.93e-3},
             'Alu_dick': {'l_ges': 300.5e-3, 'b': 20e-3, 'd': 2e-3, 'm': 32.16e-3}}
Datenbank_statisch = {'Kupfer': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 27.24e-3},
             'Stahl_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.55e-3, 'm': 26.74e-3},
             'Stahl_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 49.13e-3},
             'Alu_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 15.61e-3},
             'Alu_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 2e-3, 'm': 32.08e-3}}


def run(staerke, metall, einspannlaenge):
    mess_daten = np.zeros(0)
    if staerke == 'dünn':
        mess_daten = np.loadtxt(f'{data_dir_dyn}/Duenner-{metall}-{einspannlaenge}.txt', skiprows=4, unpack=True, delimiter='\t')
    elif staerke == 'dick':
        mess_daten = np.loadtxt(f'{data_dir_dyn}/Dicker-{metall}-{einspannlaenge}.txt', skiprows=4, unpack=True, delimiter='\t')
    else:
        mess_daten = np.loadtxt(f'{data_dir_dyn}/{metall}-{einspannlaenge}.txt', skiprows=4, unpack=True, delimiter='\t')

    parameter = Datenbank
    if staerke != '':
        parameter = Datenbank[f'{metall}_{staerke}']
    else:
        parameter = Datenbank[metall]
    L = einspannlaenge / 1e3

    dyn.test(mess_daten[1], masse=parameter['m'], L=L, b=parameter['b'], d=parameter['d'], l_ges=parameter['l_ges'])


run('dünn', 'Alu', 268)

#test_daten = np.loadtxt(f'{data_dir_dyn}/Duenner-Alu-232.txt', skiprows=4, unpack=True, delimiter='\t')
#
#alu = Datenbank['Alu_dünn']
#L = 232e-3
#dyn.test(test_daten[1], masse=alu['m'], L=L, b=alu['b'], d=alu['d'], l_ges=alu['l_ges'])
