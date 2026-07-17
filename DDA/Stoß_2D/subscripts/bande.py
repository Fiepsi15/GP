import numpy as np
from scrips.tools import sci_round


def mean_std(p, axis=0):
    mean = np.mean(p, axis=axis)
    std = np.std(p, axis=axis) / np.sqrt(len(p))
    return mean, std


def testprint(K_pre_m, delta_K_pre, K_post_m, delta_K_post):
    p_pre_x_r, d_p_pre_x_r = sci_round(K_pre_m, delta_K_pre)
    print(f'Pre: K = {p_pre_x_r} +- {d_p_pre_x_r}')
    p_post_x_r, d_p_post_x_r = sci_round(K_post_m, delta_K_post)
    print(f'Post: K = {p_post_x_r} +- {d_p_post_x_r}')


def bande(r, v, p, m, pre, post):
    v_pre, v_post = v[:, pre[0]:pre[1]], v[:, post[0]:post[1]]
    p_pre, p_post = p[:, pre[0]:pre[1]], p[:, post[0]:post[1]]

    theta_in = np.arctan(p_pre[:, 0] / p_pre[:, 1])
    theta_out = np.arctan(p_post[:, 0] / p_post[:, 1])
    theta_in_m, theta_in_std = mean_std(theta_in, axis=0)
    theta_out_m, theta_out_std = mean_std(theta_out, axis=0)
    print('Theta:')
    testprint(theta_in_m, theta_in_std, theta_out_m, theta_out_std)

    p_pre = np.sqrt(p_pre[:, 0] ** 2 + p_pre[:, 1] ** 2)
    p_post = np.sqrt(p_post[:, 0] ** 2 + p_post[:, 1] ** 2)

    p_pre_m, p_pre_std = mean_std(p_pre, 0)
    p_post_m, p_post_std = mean_std(p_post, 0)

    K_pre = 1 / 2 * m * (v_pre[:, 0] ** 2 + v_pre[:, 1] ** 2)
    K_post = 1 / 2 * m * (v_post[:, 0] ** 2 + v_post[:, 1] ** 2)
    K_pre_m, K_pre_std = mean_std(K_pre, axis=0)
    K_post_m, K_post_std = mean_std(K_post, axis=0)

    testprint(K_pre_m, K_pre_std, K_post_m, K_post_std)
    print('p:')
    testprint(p_pre_m, p_pre_std, p_post_m, p_post_std)
