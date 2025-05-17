import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def get_cum_mean(array):
    mu_array = np.cumsum(array)
    for i in range(len(array)):
        mu_array[i] = mu_array[i] / (i + 1)

    return mu_array


def get_cum_std(array):
    std_array = [0]
    for i in range(1, len(array)):
        std_array.append(np.std(array[0:(i + 1)]))
    std_array = np.array(std_array)

    return std_array


def get_cum_kurtosis(array):
    kurtosis_array = [1]
    for i in range(1, len(array)):
        kurtosis_array.append(stats.kurtosis(array[0:i], fisher=False))
    kurtosis_array = np.array(kurtosis_array)

    return kurtosis_array





#Startwerte:
n = 1000
mu = 0
sigma = 1

arr = np.random.randn(n, n)

#i initialisieren
i = np.arange(1, n + 1, 1)

#Y bauen
Y = [sigma]
for ies in i[1:n]:
    Y.append(sigma / np.sqrt(ies - 1))
Y = np.array(Y)


#Plotting zum test der FKTN
'''
for k in range(5):
    plt.plot(i, (get_cum_mean(arr[:, k])))
plt.plot(i, [mu for _ in range(len(i))])

for k in range(5):
    plt.plot(i, (get_cum_std(arr[:, k])))
plt.plot(i, [sigma for _ in range(len(i))])

for k in range(5):
    plt.plot(i, (get_cum_kurtosis(arr[:, k])))
plt.plot(i, [3 for _ in range(len(i))])

plt.show()
'''


#Histogramm
plt.hist(arr[:,0], bins='auto', density=True)
x_min, x_max = plt.xlim()
x = np.linspace(x_min, x_max, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.show()


#Komulatives Mittel mit Y
plt.plot(i, mu + Y, color='black')
plt.plot(i, mu - Y, color='black')
for k in range(5):
    plt.plot(i, (get_cum_mean(arr[:, k])))
plt.semilogx()
plt.show()


#Komulative Std mit Y
plt.plot(i, sigma + Y, color='black')
plt.plot(i, sigma - Y, color='black')
for k in range(5):
    plt.plot(i, (get_cum_std(arr[:, k])))
plt.semilogx()
plt.show()


#Kurtosis
cum_stds = [get_cum_std(arr[k, :]) for k in range(np.shape(arr)[1])]
cum_stds = np.array(cum_stds)

plt.plot(i, [np.std(cum_stds[:, k]) for k in range(np.shape(arr)[0])])
plt.xscale('log')
plt.yscale('log')

for k in range(5):
    plt.plot(i, np.power((get_cum_kurtosis(arr[k, :])), 1/4))

plt.show()
