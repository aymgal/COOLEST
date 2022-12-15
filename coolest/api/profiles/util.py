__author__ = 'aymgal'


import numpy as np


def shift_rotate_elliptical(x, y, phi, q, center_x, center_y):
    phi_rad = phi * np.pi / 180.
    x_shift = x - center_x
    y_shift = y - center_y
    cos_phi = np.cos(phi_rad)
    sin_phi = np.sin(phi_rad)
    x_trans = cos_phi * x_shift + sin_phi * y_shift
    y_trans = -sin_phi * x_shift + cos_phi * y_shift
    return x_trans * np.sqrt(q), y_trans / np.sqrt(q)
