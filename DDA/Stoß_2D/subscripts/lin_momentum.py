import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def testprint(p_pre_m, delta_p_pre, p_post_m, delta_p_post):
    p_pre_x_r, d_p_pre_x_r = sci_round(p_pre_m[0], delta_p_pre[0])
    p_pre_y_r, d_p_pre_y_r = sci_round(p_pre_m[1], delta_p_pre[1])
    print(f'Pre: px = {p_pre_x_r} +- {d_p_pre_x_r}')
    print(f'Pre: py = {p_pre_y_r} +- {d_p_pre_y_r}')
    p_post_x_r, d_p_post_x_r = sci_round(p_post_m[0], delta_p_post[0])
    p_post_y_r, d_p_post_y_r = sci_round(p_post_m[1], delta_p_post[1])
    print(f'Post: px = {p_post_x_r} +- {d_p_post_x_r}')
    print(f'Post: py = {p_post_y_r} +- {d_p_post_y_r}')

    return


def testprint_s(K_pre_m, delta_K_pre, K_post_m, delta_K_post):
    p_pre_x_r, d_p_pre_x_r = sci_round(K_pre_m, delta_K_pre)
    print(f'Pre: K = {p_pre_x_r} +- {d_p_pre_x_r}')
    p_post_x_r, d_p_post_x_r = sci_round(K_post_m, delta_K_post)
    print(f'Post: K = {p_post_x_r} +- {d_p_post_x_r}')


def mean_std(p, axis=0):
    mean = np.mean(p, axis=axis)
    std = np.std(p, axis=axis) / np.sqrt(len(p))
    return mean, std


def single(p, pre, post):
    p = p.transpose()
    p_abs = np.sqrt(p[:,0] ** 2 + p[:,1] ** 2)
    p_pre, p_post = p_abs[pre[0]:pre[1]], p_abs[post[0]:post[1]]

    p_pre_m, delta_p_pre = mean_std(p_pre, axis=0)
    p_post_m, delta_p_post = mean_std(p_post, axis=0)

    testprint_s(p_pre_m, delta_p_pre, p_post_m, delta_p_post)


def test_momentum(p1, p2, pre, post, p3=None):
    p1_pre, p1_post = p1[:, pre[0]:pre[1]], p1[:, post[0]:post[1]]
    p2_pre, p2_post = p2[:, pre[0]:pre[1]], p2[:, post[0]:post[1]]
    p3_pre, p3_post = None, None
    p3_pre_m, delta_p3_pre = None, None
    p3_post_m, delta_p3_post = None, None
    if p3 is not None:
        p3_pre, p3_post = p3[:, pre[0]:pre[1]], p3[:, post[0]:post[1]]
        p3_pre_m, delta_p3_pre = mean_std(p3_pre, axis=1)
        p3_post_m, delta_p3_post = mean_std(p3_post, axis=1)

    p1_pre_m, delta_p1_pre = mean_std(p1_pre, axis=1)
    p2_pre_m, delta_p2_pre = mean_std(p2_pre, axis=1)
    p1_post_m, delta_p1_post = mean_std(p1_post, axis=1)
    p2_post_m, delta_p2_post = mean_std(p2_post, axis=1)

    p_pre = p1_pre + p2_pre
    p_post = p1_post + p2_post
    if p3 is not None:
        p_pre += p3_pre
        p_post += p3_post

    p_pre_m, delta_p_pre = mean_std(p_pre, axis=1)
    p_post_m, delta_p_post = mean_std(p_post, axis=1)

    # testprint(p_pre_m, delta_p_pre, p_post_m, delta_p_post)

    values = np.array([[p1_pre_m[0], p1_post_m[0]], [p1_pre_m[1], p1_post_m[1]],
                       [p2_pre_m[0], p2_post_m[0]], [p2_pre_m[1], p2_post_m[1]],
                       [p_pre_m[0], p_post_m[0]], [p_pre_m[1], p_post_m[1]]]) * 1e3
    uncert = np.array([[delta_p1_pre[0], delta_p1_post[0]], [delta_p1_pre[1], delta_p1_post[1]],
                       [delta_p2_pre[0], delta_p2_post[0]], [delta_p2_pre[1], delta_p2_post[1]],
                       [delta_p_pre[0], delta_p_post[0]], [delta_p_pre[1], delta_p_post[1]]]) * 1e3
    if p3 is not None:
        values = np.array([[p1_pre_m[0], p1_post_m[0]], [p1_pre_m[1], p1_post_m[1]],
                           [p2_pre_m[0], p2_post_m[0]], [p2_pre_m[1], p2_post_m[1]],
                           [p3_pre_m[0], p3_post_m[0]], [p3_pre_m[1], p3_post_m[1]],
                           [p_pre_m[0], p_post_m[0]], [p_pre_m[1], p_post_m[1]]]) * 1e3
        uncert = np.array([[delta_p1_pre[0], delta_p1_post[0]], [delta_p1_pre[1], delta_p1_post[1]],
                           [delta_p2_pre[0], delta_p2_post[0]], [delta_p2_pre[1], delta_p2_post[1]],
                           [delta_p3_pre[0], delta_p3_post[0]], [delta_p3_pre[1], delta_p3_post[1]],
                           [delta_p_pre[0], delta_p_post[0]], [delta_p_pre[1], delta_p_post[1]]]) * 1e3

    if p3 is not None:
        a2t(values, uncert,
            [['p_{1x}', 'p_{1y}', 'p_{2x}', 'p_{2y}', 'p_{3x}', 'p_{3y}', 'p_x', 'p_y'],
             ['mNs' for _ in range(len(values))]],
            override_row_len=3)
        return

    a2t(values, uncert, [['p_{1x}', 'p_{1y}', 'p_{2x}', 'p_{2y}', 'p_x', 'p_y'], ['mNs' for _ in range(len(values))]],
        override_row_len=2)

    return
