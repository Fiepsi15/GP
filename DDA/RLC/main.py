import numpy as np
import matplotlib.pyplot as plt
from DDA.RLC.subscripts.sweep_calcs import sweep

data_directory = 'DDA/RLC/data/'


def square_wave():
    square_waveform_data = np.loadtxt(data_directory + 'Square_220µF_10Hz_Aqui_2000Hz_12052026.csv', skiprows=4,
                                      delimiter='\t').transpose()
    print(square_waveform_data.shape)
    time = square_waveform_data[0]
    Ue = square_waveform_data[1] - 2.5
    U_R = square_waveform_data[2] - 2.5

    R = 5  # Ohm

    I = U_R / R

    fig, ax = plt.subplots()

    plrange = 200

    ax.plot(time[:plrange], Ue[:plrange])
    ax.plot(time[:plrange], U_R[:plrange])
    plt.show()




sweep(150, 2000, data_directory)
