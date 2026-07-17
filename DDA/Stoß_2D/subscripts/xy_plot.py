import numpy as np
from matplotlib import pyplot as plt, figure


def single(r, pre, post, p_label, p_marker, p_color1, p_color2, ax, no_col=False):
    r_pre, r_post = r[:, pre[0]:pre[1] + 1], r[:, post[0] - 1:post[1]]

    ax.plot(r_pre[0], r_pre[1], label=p_label, color=p_color1, marker=p_marker)
    if no_col:
        return
    ax.plot(r_post[0], r_post[1], label=f'{p_label} nach dem Stoß', color=p_color2, marker=p_marker)


def plot(r1, r2, pre, post):
    fig, ax = plt.subplots()
    fig.suptitle('Positionen der Massen')

    label = 'M1'
    marker = 'v'
    color1, color2 = 'red', 'orange'
    single(r1, pre, post, label, marker, color1, color2, ax)

    label = 'M2'
    marker = '^'
    color1, color2 = 'blue', 'green'
    single(r2, pre, post, label, marker, color1, color2, ax)

    ax.tick_params(axis='both', which='major', direction='in')
    ax.set(xlabel='$x/\\mathrm{m}$', ylabel='$y/\\mathrm{m}$')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    plt.show()


def plot1(r, pre, post):
    fig, ax = plt.subplots()
    fig.suptitle('Positionen der Masse')

    label = 'M1'
    marker = 'v'
    color1, color2 = 'red', 'orange'
    single(r, pre, post, label, marker, color1, color2, ax)

    ax.tick_params(axis='both', which='major', direction='in')
    ax.set(xlabel='$x/\\mathrm{m}$', ylabel='$y/\\mathrm{m}$')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    plt.show()


def plot2_hantel(r1, r2, m1, m2, pre, post):
    fig, ax = plt.subplots()
    fig.suptitle('Positionen der Massen und des Schwerpunkts')

    label = 'M1'
    marker = 'v'
    color1, color2 = 'red', 'red'
    single(r1, pre, post, label, marker, color1, color2, ax, no_col=True)

    label = 'M2'
    marker = '^'
    color1, color2 = 'blue', 'blue'
    single(r2, pre, post, label, marker, color1, color2, ax, no_col=True)

    r3 = (r1 * m1 + r2 * m2) / (m1 + m2)

    label = 'Schwerpunkt'
    marker = 'o'
    color1, color2 = 'green', 'green'
    single(r3, pre, post, label, marker, color1, color2, ax, no_col=True)

    ax.tick_params(axis='both', which='major', direction='in')
    ax.set(xlabel='$x/\\mathrm{m}$', ylabel='$y/\\mathrm{m}$')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    plt.show()


def plot3_hantel(r1, r2, r3, m1, m2, pre, post):
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.suptitle('Positionen der Massen und des Schwerpunkts')

    label = 'M1 (Hantel)'
    marker = 'v'
    color1, color2 = 'red', 'orange'
    single(r1, pre, post, label, marker, color1, color2, ax)

    label = 'M2 (Hantel)'
    marker = '^'
    color1, color2 = 'blue', 'purple'
    single(r2, pre, post, label, marker, color1, color2, ax)

    label = 'M3'
    marker = '>'
    color1, color2 = 'green', 'black'
    single(r3, pre, post, label, marker, color1, color2, ax)

    r4 = (r1 * m1 + r2 * m2) / (m1 + m2)

    label = 'Schwerpunkt'
    marker = 'o'
    color1, color2 = 'teal', 'cyan'
    single(r4, pre, post, label, marker, color1, color2, ax)

    ax.tick_params(axis='both', which='major', direction='in')
    ax.set(xlabel='$x/\\mathrm{m}$', ylabel='$y/\\mathrm{m}$')
    ax.minorticks_on()
    ax.legend()
    ax.grid()

    plt.show()
