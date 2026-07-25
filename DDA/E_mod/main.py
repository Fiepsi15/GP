import numpy as np
from DDA.E_mod.subscripts import dynamisch
from DDA.E_mod.subscripts import statisch

data_dir_dyn = 'DDA/E_mod/daten/dynamisch'
data_dir_stat = 'DDA/E_mod/daten/statisch'


#print('Alu')
#strk_lng = [[['dünn', 268], ['dünn', 232]], [['dick', 260], ['dick', 233]]]
#alu(strk_lng, data_dir_dyn)
#
#print('\nStahl')
#strk_lng = [[['dünn', 255], ['dünn', 199], ['dünn', 151]], [['dick', 267], ['dick', 239], ['dick', 208]]]
#stahl(strk_lng, data_dir_dyn)
#
#print('\nKupfer')
#laengen = [255, 191, 133]
#kupfer(laengen, data_dir_dyn)

strength_list = [1, 2] # mm
statisch.analyze(data_dir_stat, 'Alu', strength_list)
strength_list = [550, 1000] # mu m
statisch.analyze(data_dir_stat, 'Stahl', strength_list)
statisch.analyze(data_dir_stat, 'Kupfer', [])
