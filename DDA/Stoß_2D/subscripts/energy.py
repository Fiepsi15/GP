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


def rotational_energy(ri1, ri2, vi1, vi2, m, pre, post, vs3=0):
    R_puck = 38e-3 / 2  # m
    d_pucks = 64e-3  # m
    I = (1 / 2 * m / 2 * R_puck ** 2 + m / 2 * (d_pucks / 2) ** 2) * 2
    ri1 = ri1.transpose()
    ri2 = ri2.transpose()
    vi1 = vi1.transpose()
    vi2 = vi2.transpose()
    rs = (ri1 + ri2) / 2
    vs = (vi1 + vi2) / 2
    r1 = ri1 - rs
    v1 = vi1 - vs

    omega = np.cross(r1, v1) / np.array([r1[i, 0] ** 2 + r1[i, 1] ** 2 for i in range(len(r1))])
    omega_pre = omega[pre[0]:pre[1]]
    omega_post = omega[post[0]:post[1]]

    vs = vs - vs3

    K_trans = 1 / 2 * m * np.array([vs[i, 0] ** 2 + vs[i, 1] ** 2 for i in range(len(vs))])
    K_trans_pre = K_trans[pre[0]:pre[1]]
    K_trans_post = K_trans[post[0]:post[1]]

    K_pre = I * np.abs(omega_pre) ** 2
    K_post = I * np.abs(omega_post) ** 2

    K_pre_m, K_pre_std = mean_std(K_pre)
    K_post_m, K_post_std = mean_std(K_post)

    print('rotation')
    testprint(K_pre_m, K_pre_std, K_post_m, K_post_std)

    return K_pre, K_post, K_trans_pre, K_trans_post


def energy_with_rotation2(r1, r2, v1, v2, m1, m2, pre, post):
    K_rot_pre, K_rot_post, K_trans_pre, K_trans_post = rotational_energy(r1, r2, v1, v2, m1 + m2, pre, post)
    K_pre = K_rot_pre + K_trans_pre
    K_post = K_rot_post + K_trans_post

    K_trans_pre_m, K_trans_pre_std = mean_std(K_trans_pre)
    K_trans_post_m, K_trans_post_std = mean_std(K_trans_post)
    print('translation')
    testprint(K_trans_pre_m, K_trans_pre_std, K_trans_post_m, K_trans_post_std)

    K_pre_m, K_pre_std = mean_std(K_pre)
    K_post_m, K_post_std = mean_std(K_post)

    print('sum')
    testprint(K_pre_m, K_pre_std, K_post_m, K_post_std)
    print()


def energy_with_rotation3(r1, r2, r3, v1, v2, v3, m1, m2, m3, pre, post):
    vs = ((v1 * m1 + v2 * m2 + v3 * m3) / (m1 + m2 + m3)).transpose()
    v3 = v3.transpose()
    K_rot_pre, K_rot_post, K_trans_pre, K_trans_post = rotational_energy(r1, r2, v1, v2, m1 + m2, pre, post, vs)

    vs3 = v3 - vs
    K_puck = 1/2 * m3 * (vs3[:,0] ** 2 + vs3[:,1] ** 2)

    K_puck_pre = K_puck[pre[0]:pre[1]]
    K_puck_post = K_puck[post[0]:post[1]]

    K_trans_pre = K_trans_pre + K_puck_pre
    K_trans_post = K_trans_post + K_puck_post

    K_trans_pre_m, K_trans_pre_std = mean_std(K_trans_pre)
    K_trans_post_m, K_trans_post_std = mean_std(K_trans_post)
    print('translation')
    testprint(K_trans_pre_m, K_trans_pre_std, K_trans_post_m, K_trans_post_std)

    K_pre = K_rot_pre + K_trans_pre
    K_post = K_rot_post + K_trans_post

    K_pre_m, K_pre_std = mean_std(K_pre)
    K_post_m, K_post_std = mean_std(K_post)

    print('sum')
    testprint(K_pre_m, K_pre_std, K_post_m, K_post_std)
    print()


def test_energy(v1, v2, m1, m2, pre, post, v3=None, m3=None):
    v1_pre, v1_post = v1[:, pre[0]:pre[1]], v1[:, post[0]:post[1]]
    v2_pre, v2_post = v2[:, pre[0]:pre[1]], v2[:, post[0]:post[1]]
    v3_pre, v3_post = None, None
    if v3 is not None:
        v3_pre, v3_post = v3[:, pre[0]:pre[1]], v3[:, post[0]:post[1]]

    v_pre_m = np.mean(v1_pre, axis=1) * m1 + np.mean(v2_pre, axis=1) * m2
    M = m1 + m2
    if v3 is not None:
        v_pre_m += np.mean(v3_pre, axis=1) * m3
        M += m3

    v_pre_m = v_pre_m / M
    v1_pre = v1_pre.transpose() - v_pre_m
    v1_post = v1_post.transpose() - v_pre_m
    v2_pre = v2_pre.transpose() - v_pre_m
    v2_post = v2_post.transpose() - v_pre_m
    if v3 is not None:
        v3_pre = v3_pre.transpose() - v_pre_m
        v3_post = v3_post.transpose() - v_pre_m

    K1_pre = 1 / 2 * m1 * (v1_pre[:, 0] ** 2 + v1_pre[:, 1] ** 2)
    K1_post = 1 / 2 * m1 * (v1_post[:, 0] ** 2 + v1_post[:, 1] ** 2)
    K2_pre = 1 / 2 * m2 * (v2_pre[:, 0] ** 2 + v2_pre[:, 1] ** 2)
    K2_post = 1 / 2 * m2 * (v2_post[:, 0] ** 2 + v2_post[:, 1] ** 2)
    K3_pre, K3_post = None, None
    if v3 is not None:
        K3_pre = 1 / 2 * m3 * (v3_pre[:, 0] ** 2 + v3_pre[:, 1] ** 2)
        K3_post = 1 / 2 * m3 * (v3_post[:, 0] ** 2 + v3_post[:, 1] ** 2)

    K_pre = K1_pre + K2_pre
    K_post = K1_post + K2_post
    if v3 is not None:
        K_pre += K3_pre
        K_post += K3_post

    K_pre_m, K_pre_std = mean_std(K_pre)
    K_post_m, K_post_std = mean_std(K_post)

    testprint(K_pre_m, K_pre_std, K_post_m, K_post_std)
