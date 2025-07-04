import numpy as np
import matplotlib.pyplot as plt
from scrips.tools import sci_round

def run():
    data = np.loadtxt('_1b/_10_Adiabatenexponent/daten/V_01.csv', skiprows=1, delimiter=',')/1e2

    gamma = []
    for h in data:
        gamma.append(h[0]/(h[0] - h[1]))

    gamma_bar = np.mean(gamma)
    sigma = np.std(gamma)

    print(gamma_bar, sigma)
    gamma_bar_r, sigma_r = sci_round(gamma_bar, sigma)
    print(f'γ = {gamma_bar_r} ± {sigma_r}')

    #Just the values
    i = np.arange(len(data))
    plt.scatter(i, data[:, 0], label='$h_1$', color='blue')
    plt.scatter(i, data[:, 1], label='$h_2$', color='red')
    plt.legend()
    plt.xlabel('$i$')
    plt.ylabel('$h\\text{ in m} $')
    plt.grid(True)
    plt.show()


    #Plot the gamma values with averages
    plt.title("Clément-Désormes Method")
    plt.scatter(i, gamma, label='$\\gamma$', color='green')

    plt.plot([0, len(data)], [gamma_bar, gamma_bar], color='black', label='$\\bar{\\gamma} = $' + str(gamma_bar_r) + ' ± ' + str(sigma_r))
    plt.plot([0, len(data)], [gamma_bar + sigma, gamma_bar + sigma], color='black', label='$\\sigma$', linestyle='--')
    plt.plot([0, len(data)], [gamma_bar - sigma, gamma_bar - sigma], color='black', linestyle='--')

    plt.xlabel('$i$')
    plt.ylabel('$\\gamma$')
    plt.legend()
    plt.grid(True)
    plt.show()