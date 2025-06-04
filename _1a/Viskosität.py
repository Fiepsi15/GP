import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def Auswertung(X,Y,Paras,Korrektur = False):
   def linear_model(A, B, C):
       return [B * xl + C for xl in A]
   if Korrektur == False:
       x = [1/(np.mean(xl)**2) for xl in X]
   else:
       x = [(1+2.1*np.mean(xl)/Paras[0])/(np.mean(xl)**2) for xl in X]
   y = [np.mean(xl) for xl in Y ]
   popt, pcov = curve_fit(linear_model, x,y, absolute_sigma=True)
   m_fit, c_fit = popt
   m_err, c_err = np.sqrt(np.diag(pcov))
   Y_err = [np.std(xl) for xl in Y]
   X_err = [np.std([1/xi for xi in xl]) for xl in X]
   plt.figure()
   if Korrektur == False:
       plt.title('Regression ohne Korrektur')
       plt.xlabel(r'$\frac{1}{r^2}$ in $\frac{1}{m^2}$')
   else:
       plt.title('Regression mit Korrektur')
       plt.xlabel(r'$\frac{\lambda}{r^2}$ in $\frac{1}{m^2}$')
   plt.errorbar(x,y, yerr=Y_err,xerr = X_err, fmt='x', label='Messdaten mit Fehlerbalken',capsize=5)
   plt.plot(x,linear_model(x,m_fit,c_fit),label = 'Regressionsgerade')
   plt.ylabel('t in s')
   plt.legend()
   plt.show()
   nu = m_fit*Paras[2]*2*(Paras[3]-Paras[4])/(9*Paras[5])
   dnu = np.sqrt((m_err*Paras[2]*2*(Paras[3]-Paras[4])/(9*Paras[5]))**2+(Paras[6]*m_fit*Paras[2]*2*(Paras[3]-Paras[4])/(9*Paras[5])**2)**2)
   print(f"Viskosität mit Korrektur: {nu:.3f} ± {dnu:.3f}")

ds = 7850  # Dichte Stahl
dö = 860  # Dichte Öl
g = 9.81
Rz = 0.0583  # Radius des Messzylinders
DRz = 0.00005  # Fehler Radius des Messzylinders
s = 0.3  # Fallstrecke
Ds = 0.001  # Fehler Fallstrecke
Paras = [Rz, DRz, g, ds, dö, s, Ds]
X = [[0.00399, 0.00399, 0.00399, 0.00399, 0.00399], [0.00299, 0.00299, 0.00299, 0.00299, 0.00299], [0.00199, 0.00199, 0.00199, 0.00199, 0.00199], [0.005, 0.00499, 0.00499, 0.00499, 0.00499]]
for i in range(len(X)):
    for j in range(len(X[i])):
        X[i][j] = X[i][j]/2
Y = [[9.82, 9.76, 9.71, 9.92, 9.72], [16.44, 16.40, 16.62, 16.71, 16.18], [35.55, 35.56, 35.20, 35.51, 36.50], [6.27, 6.23, 6.31, 6.27, 6.30]]
Auswertung(X, Y, Paras, Korrektur=True)