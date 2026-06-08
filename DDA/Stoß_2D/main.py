import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from subscripts.lin_momentum import test_momentum as lin_momentum

# t;x;y;r;vx;vy;v;px;py;p;K;x;y;r;vx;vy;v;px;py;p;K;
data_dir = 'daten/'


def conv(str: str):
    if str == '':
        return '0'
    for i in range(len(str)):
        if str[i] == ',':
            str = str[:i] + '.' + str[i + 1:]
    return str


def extract(daten):
    time = daten[0]
    x1 = daten[1]
    y1 = daten[2]
    r1 = np.array([x1, y1])
    vx1 = daten[3]
    vy1 = daten[4]
    v1 = np.array([vx1, vy1])
    px1 = daten[5]
    py1 = daten[6]
    p1 = np.array([px1, py1])
    K1 = daten[7]
    x2 = daten[8]
    y2 = daten[9]
    r2 = np.array([x2, y2])
    vx2 = daten[10]
    vy2 = daten[11]
    v2 = np.array([vx2, vy2])
    px2 = daten[12]
    py2 = daten[13]
    p2 = np.array([px2, py2])
    K2 = daten[14]
    return time, r1, v1, p1, K1, r2, v2, p2, K2


def test_range(r1, r2, pre, post):
    plt.scatter(r1[0][pre[0]:pre[1]], r1[1][pre[0]:pre[1]], label='pre')
    plt.scatter(r1[0][post[0]:post[1]], r1[1][post[0]:post[1]], label='post')
    plt.scatter(r1[0], r1[1], label='r1', marker='.')
    plt.scatter(r2[0][pre[0]:pre[1]], r2[1][pre[0]:pre[1]], label='pre')
    plt.scatter(r2[0][post[0]:post[1]], r2[1][post[0]:post[1]], label='post')
    plt.scatter(r2[0], r2[1], label='r2', marker='.')
    plt.legend()
    plt.show()
    return


data = np.loadtxt(data_dir + 'ruhend-stoss-gleiche-Masse1.txt', skiprows=3, delimiter=';', converters=conv).transpose()
data[3:5] = data[4:6]
data[5:7] = data[7:9]
data[7:10] = data[10:13]
data[10:12] = data[14:16]
data[12:14] = data[17:19]
data[14] = data[-1]

time, r1, v1, p1, K1, r2, v2, p2, K2 = extract(data)

pre = (12, 23)
post = (24, 38)

#test_range(r1, r2, pre, post)

lin_momentum(p1, p2, pre, post)
