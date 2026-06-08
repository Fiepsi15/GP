import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def mean_std(p, axis=0):
    mean = np.mean(p, axis=axis)
    std = np.std(p, axis=axis) / np.sqrt(len(p))
    return mean, std


def testprint(K_pre_m, delta_K_pre, K_post_m, delta_K_post):
    p_pre_x_r, d_p_pre_x_r = sci_round(K_pre_m, delta_K_pre)
    print(f'Pre: K = {p_pre_x_r} +- {d_p_pre_x_r}')
    p_post_x_r, d_p_post_x_r = sci_round(K_post_m, delta_K_post)
    print(f'Post: K = {p_post_x_r} +- {d_p_post_x_r}')


def test_energy(v1, v2, m1, m2, pre, post):
    v1_pre, v1_post = v1[:, pre[0]:pre[1]], v1[:, post[0]:post[1]]
    v2_pre, v2_post = v2[:, pre[0]:pre[1]], v2[:, post[0]:post[1]]

    v_pre_m = np.mean(v1_pre, axis=1) + np.mean(v2_pre, axis=1)
    v1_pre = v1_pre.transpose() - v_pre_m
    v1_post = v1_post.transpose() - v_pre_m
    v2_pre = v2_pre.transpose() - v_pre_m
    v2_post = v2_post.transpose() - v_pre_m

    K1_pre = 1/2 * m1 * (v1_pre[:,0] ** 2 + v1_pre[:,1] ** 2)
    K1_post = 1/2 * m1 * (v1_post[:,0] ** 2 + v1_post[:,1] ** 2)
    K2_pre = 1/2 * m2 * (v2_pre[:,0] ** 2 + v2_pre[:,1] ** 2)
    K2_post = 1/2 * m2 * (v2_post[:,0] ** 2 + v2_post[:,1] ** 2)

    K_pre = K1_pre + K2_pre
    K_post = K1_post + K2_post

    K_pre_m, K_pre_std = mean_std(K_pre)
    K_post_m, K_pre_std = mean_std(K_post)

    testprint(K_pre_m, K_pre_std, K_post_m, K_pre_std)
