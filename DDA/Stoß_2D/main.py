import numpy as np
from matplotlib import pyplot as plt
from subscripts.lin_momentum import test_momentum as lin_momentum
from subscripts.energy import test_energy as energy
from DDA.Stoß_2D.subscripts.xy_plot import plot as xy_plot
from DDA.Stoß_2D.subscripts.ang_momentum import test_momentum as ang_momentum

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
    ret = (time, r1, v1, p1, K1, r2, v2, p2, K2)
    if len(daten) > 15:
        x3 = daten[15]
        y3 = daten[16]
        r3 = np.array([x3, y3])
        vx3 = daten[17]
        vy3 = daten[18]
        v3 = np.array([vx3, vy3])
        px3 = daten[19]
        py3 = daten[20]
        p3 = np.array([px3, py3])
        K3 = daten[21]
        ret = (time, r1, v1, p1, K1, r2, v2, p2, K2, r3, v3, p3, K3)
    return ret


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


def test_range3(r1, r2, r3, pre, post):
    plt.scatter(r1[0][pre[0]:pre[1]], r1[1][pre[0]:pre[1]], label='pre')
    plt.scatter(r1[0][post[0]:post[1]], r1[1][post[0]:post[1]], label='post')
    plt.scatter(r1[0], r1[1], label='r1', marker='.')
    plt.scatter(r2[0][pre[0]:pre[1]], r2[1][pre[0]:pre[1]], label='pre')
    plt.scatter(r2[0][post[0]:post[1]], r2[1][post[0]:post[1]], label='post')
    plt.scatter(r2[0], r2[1], label='r2', marker='.')
    plt.scatter(r3[0][pre[0]:pre[1]], r3[1][pre[0]:pre[1]], label='pre')
    plt.scatter(r3[0][post[0]:post[1]], r3[1][post[0]:post[1]], label='post')
    plt.scatter(r3[0], r3[1], label='r3', marker='.')
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

time, r1, v1, p1, K1, r2, v2, p2, K2 = extract(data[:15])

pre = (12, 23)
post = (24, 38)

#test_range(r1, r2, pre, post)

#lin_momentum(p1, p2, pre, post)

#energy(v1, v2, 18.4, 18.4, pre, post)

#xy_plot(r1, r2, pre, post)

data = np.loadtxt(data_dir + '3-5-2-Puck-Hantel-Stoss1.txt', skiprows=3, delimiter=';', converters=conv).transpose()

time, r1, v1, p1, K1, r2, v2, p2, K2, r3, v3, p3, K3 = extract(data)

pre = (2, 27)
post = (28, 55)

#test_range3(r1, r2, r3, pre, post)

ang_momentum(r3, r1, r2, v1, v2, p3, p1, p2, 18.4, 18.6, 18.6, pre, post)

