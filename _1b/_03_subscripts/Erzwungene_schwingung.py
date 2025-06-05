import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from _1b._03_subscripts.funcs import resonanzfrequenz_omega0


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
    
    F_m = popt[0]
    omega0 = popt[1]
    gamma = popt[2]

    if(np.min(omega)>2):
        omega = np.linspace(2, np.max(omega),200)
    else: omega = np.linspace(2, np.max(omega),200)
    A = model(omega,F_m,omega0,gamma)


    #bestimmung des maximums
    max = np.where(A == np.max(A))
    A_max = A[max]
    omega_max = omega[max]


    #Berechnen der -Wertsbreite
    A_halb = A_max/np.sqrt(2) # unsere Wertsbreite

    omega_halb = whereEquals(omega,A,A_halb)

    print(f"A_max = {A_max}, omega_max = {omega_max}")
    print(f"A_halb = {A_halb}, omega_halb = {omega_halb}")
    print(f"gamma = {(omega_halb[1]-omega_halb[0])/(2)}")

    
    
    plt.scatter(omega_max, A_max, color='red', label = r"$A_\text{max}$", zorder=4)
    plt.scatter(omega_halb, [A_halb,A_halb], color='black', label = r"$\frac{1}{\sqrt{2}} \cdot A_\text{max}$", zorder = 3)
    plt.plot(omega_halb,[A_halb,A_halb], color = 'black', label= r"$\Delta\omega$", zorder = 1)
    plt.plot(omega, A, label = r"Fit an Daten",  zorder = 0)
    
    plt.xlabel(r'$\omega$ (1/s)')
    plt.ylabel(r'$\alpha$ (V)')
    plt.title('Alpha vs Omega')
    plt.grid()
    plt.legend()
    alpha_omega_plot(data,error)
    plt.show()
    return


def phi_fit(data,error):
    def model(omega,omega0,gamma):
        errorcause = np.where(omega> omega0)
        phi = np.arctan((2*gamma*omega)/(omega0**2-omega**2))
        phi[np.where((omega-omega0)> 0)] = phi[np.where((omega-omega0)> 0)] + np.pi
        return(phi)
    
    omega = data[0]
    phi = np.deg2rad(data[2])
    omega_err = error[0]
    phi_err = error[2]
    

    popt, pcov = curve_fit(model, omega, phi, sigma=phi_err, absolute_sigma=True)
    omega0 = popt[0]
    gamma = popt[1]
    dgamma = np.sqrt(pcov[1][1])
    print(f"gamma = {gamma} ± {dgamma}")

    omega_plot = np.linspace(np.min(omega), np.max(omega),200)
    phi_plot = model(omega_plot, omega0, gamma)

    omega_0 = whereEquals(omega_plot, phi_plot, np.pi/2)
    print(f"omega0 = {omega_0}")


    omega_0_where = np.where(omega_0 == omega_plot)

    a= 0
    steigung = (phi_plot[omega_0_where[0]+1+a]-phi_plot[omega_0_where[0]-1+a])/(omega_plot[omega_0_where[0]+1+a]-omega_plot[omega_0_where[0]-1+a])
    plt.scatter([omega_plot[omega_0_where[0]+1+a],omega_plot[omega_0_where[0]-1+a]], np.rad2deg([phi_plot[omega_0_where[0]+1+a],phi_plot[omega_0_where[0]-1+a]]))
    gamma_calc = np.sqrt(1/steigung)
    print(f"gamma = {gamma_calc}")

    omega_max, domega_max = resonanzfrequenz_omega0(gamma_calc,0,omega_0,0)




    plt.plot(omega_plot,np.rad2deg(phi_plot), label = "Fit an Daten")
    plt.scatter(omega,np.rad2deg(phi), label= "Daten")
    
    plt.xlabel(r'$\omega$ (1/s)')
    plt.ylabel(r'$\varphi$ (°)')
    plt.title('Phi vs Omega')
    plt.grid()
    plt.legend()
    plt.show()

    return





def whereEquals(x,y,y_target):
    x_out = np.array([])
    y_delta = y-y_target
    for i in range(len(y)-1):
        if(y_delta[i]*y_delta[i+1]<0):
            if(np.abs(y_delta[i])< np.abs(y_delta[i+1])):
                x_out = np.append(x_out,x[i])
            else: x_out = np.append(x_out,x[i+1])
    return x_out





