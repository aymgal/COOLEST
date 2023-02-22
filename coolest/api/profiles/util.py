__author__ = 'aymgal'


import numpy as np
from scipy import ndimage


def shift_rotate_elliptical(x, y, phi, q, center_x, center_y):
    phi_rad = phi * np.pi / 180.
    x_shift = x - center_x
    y_shift = y - center_y
    cos_phi = np.cos(phi_rad)
    sin_phi = np.sin(phi_rad)
    x_trans = cos_phi * x_shift + sin_phi * y_shift
    y_trans = -sin_phi * x_shift + cos_phi * y_shift
    return x_trans * np.sqrt(q), y_trans / np.sqrt(q)


class CartesianGridInterpolator(object):
    """
    Regular grid spline interpolator
    https://docs.scipy.org/doc/scipy/tutorial/interpolate/ND_regular_grid.html#uniformly-spaced-data
    """
    
    def __init__(self, points, values, method='linear', fill_value=0.):
        self.limits = np.array([[min(x), max(x)] for x in points])
        self.values = np.asarray(values, dtype=float)
        self.order = {'linear': 1, 'cubic': 3, 'quintic': 5}[method]
        self.fill_value = fill_value

    def __call__(self, xi):
        """
        `xi` here is an array-like (an array or a list) of points.

        Each "point" is an ndim-dimensional array_like, representing
        the coordinates of a point in ndim-dimensional space.
        """
        # transpose the xi array into the ``map_coordinates`` convention
        # which takes coordinates of a point along columns of a 2D array.
        xi = np.asarray(xi).T

        # convert from data coordinates to pixel coordinates
        ns = self.values.shape
        coords = [(n-1)*(val - lo) / (hi - lo) 
                  for val, n, (lo, hi) in zip(xi, ns, self.limits)]

        # interpolate
        return ndimage.map_coordinates(self.values, coords,
                                       order=self.order,
                                       mode='constant',
                                       cval=self.fill_value,
                                       prefilter=False)
