import numpy as np


def Schnittpunkt(m1, dm1, b1, db1, m2, dm2, b2, db2):
    x = (b1 - b2) / (m2 - m1)
    y = m1 * x + b1

    dx = np.sqrt(
        (dm1 * (b1 - b2) / (m2 - m1) ** 2) ** 2
        + (dm2 * (b2 - b1) / (m2 - m1) ** 2) ** 2
        + (db1 / (m1 - m2)) ** 2
        + (db2 / (m2 - m1)) ** 2
    )
    dy = np.sqrt(
        (dm1 * m2(b1 - b2) / (m2 - m1) ** 2) ** 2
        + (dm2 * m1 * (b2 - b1) / (m2 - m1) ** 2) ** 2
        + (db1 * (m1 / (m2 - m1) + 1)) ** 2
        + (db2 * (m1 / (m1 - m2) + 1)) ** 2
    )

    return [x, y, dx, dy]
