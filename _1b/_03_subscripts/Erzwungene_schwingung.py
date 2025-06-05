import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def alpha_omega_plot(data, error):
    """
    Plots the relationship between alpha and omega with error bars.
    :param data: [omega, alpha]
    :param error: [omega_err, alpha_err]
    :return:
    """
    omega = data[0]
    alpha = data[1]
    omega_err = error[0]
    alpha_err = error[1]
    # Plotting the data
    plt.errorbar(omega, alpha, xerr=omega_err, yerr=alpha_err, fmt='o', capsize=5, label='Data', color='blue')
    plt.xlabel(r'$\omega$ (1/s)')
    plt.ylabel(r'$\alpha$ (V)')
    plt.title('Alpha vs Omega')
    plt.grid()
    plt.legend()
    plt.show()
    return


def alpha_fit(data, error):
    def model(omega,F_m, omega0,gamma):
        return F_m/np.sqrt((omega0**2 -omega**2)**2 +(2*gamma*omega)**2)

    omega = data[0]
    alpha = data[1]
    omega_err = error[0]
    alpha_err = error[1]

    popt, pcov = curve_fit(model, omega, alpha, sigma=alpha_err, absolute_sigma=True)
    dgamma = np.sqrt(pcov[0][0])


    omega = np.linspace(0, np.max(omega),2000)
    A = model(omega,popt[0],popt[1],popt[2])


    #bestimmung des maximums
    max = np.where(A == np.max(A))
    A_max = A[max]
    omega_max = omega[max]

    A_halb = A_max/np.sqrt(2) # unsere Wertsbreite
    halb = np.where(A == A_halb)
    A_halb = A[halb]
    omega_halb = omega[halb]
    print(A_halb)
    

    print(f"A_max = {A_max}, omega_max = {omega_max}")


    plt.scatter(omega_max, A_max, color='red', label = r"$A_\text{max}$")
    plt.scatter(omega_halb, A_halb, color='red', label = r"$\frac{1}{\sqrt{2}} \cdot A_\text{max}$")
    plt.plot(omega_halb,A_halb, color = 'red', label= r"Halbwertsbreite")
    plt.plot(omega, A, label = r"Fit an Daten")
    plt.xlabel(r'$\omega$ (1/s)')
    plt.ylabel(r'$\alpha$ (V)')
    plt.title('Alpha vs Omega')
    plt.grid()
    plt.legend()
    alpha_omega_plot(data,error)
    plt.show()
    return



forced_300mA = np.loadtxt("_1b\_03_daten\Erzwungen_300_mA.csv", skiprows=1, delimiter=',').transpose()
forced_300mA[1] = forced_300mA[1] / 1e-3  # mA to A
forced_300mA[0] = forced_300mA[0] * 2 * np.pi #F to omega
err_f_300 = np.array([[0.001 for _ in range(forced_300mA.shape[1])],
                    [0.001 for _ in range(forced_300mA.shape[1])]])

#alpha_omega_plot(forced_300mA, err_f_300)
popt = alpha_fit(forced_300mA, err_f_300)

