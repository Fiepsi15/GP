import numpy as np
from DDA.E_mod.subscripts.dynamisch import alu, stahl, kupfer

data_dir_dyn = 'DDA/E_mod/daten/dynamisch'
data_dir_stat = 'DDA/E_mod/daten/statisch'
Datenbank_statisch = {'Kupfer': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.5e-3, 'm': 27.24e-3},
             'Stahl_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 0.55e-3, 'm': 26.74e-3},
             'Stahl_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 49.13e-3},
             'Alu_dünn': {'l_ges': 200e-3, 'b': 20e-3, 'd': 1e-3, 'm': 15.61e-3},
             'Alu_dick': {'l_ges': 200e-3, 'b': 20e-3, 'd': 2e-3, 'm': 32.08e-3}}




print('Alu')
strk_lng = [[['dünn', 268], ['dünn', 232]], [['dick', 260], ['dick', 233]]]
alu(strk_lng, data_dir_dyn)

print('\nStahl')
strk_lng = [[['dünn', 255], ['dünn', 199], ['dünn', 151]], [['dick', 267], ['dick', 239], ['dick', 208]]]
stahl(strk_lng, data_dir_dyn)

print('\nKupfer')
laengen = [255, 191, 133]
kupfer(laengen, data_dir_dyn)

