import numpy as np
from matplotlib import pyplot as plt


def plot(r1, r2, pre, post):

    r1_pre, r1_post = r1[:, pre[0]:pre[1]+1], r1[:, post[0]-1:post[1]]
    r2_pre, r2_post = r2[:, pre[0]:pre[1]+1], r2[:, post[0]-1:post[1]]

    fig, ax = plt.subplots()
    fig.suptitle('Positionen der Massen')

    ax.plot(r1_pre[0], r1_pre[1], label='M1 vor dem Stoß', color='red', marker='v')
    ax.plot(r2_pre[0], r2_pre[1], label='M2 vor dem Stoß', color='blue', marker='^')
    ax.plot(r1_post[0], r1_post[1], label='M1 nach dem Stoß', color='orange', marker='v')
    ax.plot(r2_post[0], r2_post[1], label='M2 nach dem Stoß', color='green', marker='^')
    ax.tick_params(axis='both', which='major', direction='in')
    ax.set(xlabel='$x/\\mathrm{m}$', ylabel='$y/\\mathrm{m}$')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    plt.show()

