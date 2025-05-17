import numpy as np
import matplotlib.pyplot as plt

def get_cum_std(array):
    std_array = [0]
    for i in range(1, len(array)):
        std_array.append(np.std(array[0:(i + 1)]))
    std_array = np.array(std_array)

    return std_array


def wurf(p, x0, theta):
    m = 1
    g = 9.81
    auftreff = x0 + (p / m) ** 2 * np.sin(2 * theta) / g
    return auftreff


def error(arr, std):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i][j] = arr[i][j] + np.random.normal(0, std)
    return arr



p = 10 + np.zeros((1000, 1000))
x0 = 0 + np.zeros((1000, 1000))
theta = 45 + np.zeros((1000, 1000))

p = error(p, 0.01)
x0 = error(x0, 0.01)
theta = error(theta, 1)

arr = wurf(p, x0, np.deg2rad(theta))

arr_mean = np.mean(arr)
arr_std = np.std(arr)

plt.hist(arr[0], bins='auto')
plt.show()

print(arr)
