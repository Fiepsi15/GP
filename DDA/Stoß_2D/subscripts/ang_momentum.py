import numpy as np
from scrips.tools import sci_round
from scrips.array_to_tex import array_to_tex as a2t


def mean_std(p, axis=0):
    mean = np.mean(p, axis=axis)
    std = np.std(p, axis=axis) / np.sqrt(len(p))
    return mean, std


def testprint(K_pre_m, delta_K_pre, K_post_m, delta_K_post):
    p_pre_x_r, d_p_pre_x_r = sci_round(K_pre_m, delta_K_pre)
    print(f'Pre: l = {p_pre_x_r} +- {d_p_pre_x_r}')
    p_post_x_r, d_p_post_x_r = sci_round(K_post_m, delta_K_post)
    print(f'Post: l = {p_post_x_r} +- {d_p_post_x_r}')


def test_momentum(r1, r2, r3, v2, v3, p1, p2, p3, m1, m2, m3, pre, post):
    r1_pre, r1_post = r1.transpose()[pre[0]:pre[1]], r1.transpose()[post[0]:post[1]]
    r2_pre, r2_post = r2.transpose()[pre[0]:pre[1]], r2.transpose()[post[0]:post[1]]
    r3_pre, r3_post = r3.transpose()[pre[0]:pre[1]], r3.transpose()[post[0]:post[1]]

    v2_pre, v2_post = v2.transpose()[pre[0]:pre[1]], v2.transpose()[post[0]:post[1]]
    v3_pre, v3_post = v3.transpose()[pre[0]:pre[1]], v3.transpose()[post[0]:post[1]]

    p1_pre, p1_post = p1.transpose()[pre[0]:pre[1]], p1.transpose()[post[0]:post[1]]
    p2_pre, p2_post = p2.transpose()[pre[0]:pre[1]], p2.transpose()[post[0]:post[1]]
    p3_pre, p3_post = p3.transpose()[pre[0]:pre[1]], p3.transpose()[post[0]:post[1]]


    l1_pre = np.cross(r1_pre, p1_pre)
    l1_post = np.cross(r1_post, p1_post)

    l2_pre = np.cross(r2_pre, p2_pre)
    l2_post = np.cross(r2_post, p2_post)

    l3_pre = np.cross(r3_pre, p3_pre)
    l3_post = np.cross(r3_post, p3_post)

    #rh_pre, rh_post = r2_pre * m2 + r3_pre * m3 / (m2 + m3), r2_post * m2 + r3_post * m3 / (m2 + m3)
    #vh_pre, vh_post = v2_pre + v3_pre, v2_post + v3_post

    #ph_pre, ph_post = p2_pre + p3_pre, p2_post + p3_post
    #lhb_pre = np.cross(rh_pre, ph_pre)
    #lhb_post = np.cross(rh_post, ph_post)

    #lh_pre = np.cross(r2_pre - rh_pre, v2_pre - vh_pre) * m2 + np.cross(r3_pre - rh_pre, v3_pre - vh_pre) * m3
    #lh_post = np.cross(r2_post - rh_post, v2_post - vh_post) * m2 + np.cross(r3_post - rh_post, v3_post - vh_post) * m3


    l_pre = l1_pre + l2_pre + l3_pre
    l_post = l1_post + l2_post + l3_post

    l_pre_m, l_pre_std = mean_std(l_pre, axis=0)
    l_post_m, l_post_std = mean_std(l_post, axis=0)
    l1_pre_m, l1_pre_std = mean_std(l1_pre, axis=0)
    l1_post_m, l1_post_std = mean_std(l1_post, axis=0)
    l2_pre_m, l2_pre_std = mean_std(l2_pre, axis=0)
    l2_post_m, l2_post_std = mean_std(l2_post, axis=0)
    l3_pre_m, l3_pre_std = mean_std(l3_pre, axis=0)
    l3_post_m, l3_post_std = mean_std(l3_post, axis=0)

    testprint(l_pre_m, l_pre_std, l_post_m, l_post_std)

    values = np.array([[l1_pre_m[0], l1_post_m[0]], [l1_pre_m[1], l1_post_m[1]],
                       [l2_pre_m[0], l2_post_m[0]], [l2_pre_m[1], l2_post_m[1]],
                       [l3_pre_m[0], l3_post_m[0]], [l3_pre_m[1], l3_post_m[1]],
                       [l_pre_m[0], l_post_m[0]], [l_pre_m[1], l_post_m[1]]]) * 1e3
    uncert = np.array([[l1_pre_std[0], l1_post_std[0]], [l1_pre_std[1], l1_post_std[1]],
                       [l2_pre_std[0], l2_post_std[0]], [l2_pre_std[1], l2_post_std[1]],
                       [l3_pre_std[0], l3_post_std[0]], [l3_pre_std[1], l3_post_std[1]],
                       [l_pre_std[0], l_post_std[0]], [l_pre_std[1], l_post_std[1]]]) * 1e3

    a2t(values, uncert, [['l_{1x}', 'l_{1y}', 'l_{2x}', 'l_{2y}', 'l_{3x}', 'l_{3y}', 'l_x', 'l_y'], ['mNms' for _ in range(len(values))]], override_row_len=3)
