from DDA.RLC.subscripts.sweep_calcs import sweep
from DDA.RLC.subscripts.square_calcs import square_wave

data_directory = 'DDA/RLC/data/'


square_wave(data_directory)
sweep(150, 2000, data_directory)
