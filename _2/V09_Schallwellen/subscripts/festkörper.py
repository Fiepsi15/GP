import numpy as np
import matplotlib.pyplot as plt

l = 1.138

frequency = np.array([[2.150, 6], [4.300, 6], [6.450, 6], [8.600, 5], [9.950, 2], [10.750, 5], [12.9, 2], [15.1, 3], [17.2, 2], [19.4, 2], [21.5, 3]]).transpose()

fig, ax = plt.subplots()

ax.scatter(frequency[0], frequency[1])
ax.set_xlabel('Frequency (kHz)')
ax.set_ylabel('Occurrences')
ax.set_title('Occurrences of Frequencies')
ax.grid()
plt.show()
