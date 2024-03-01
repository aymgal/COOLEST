__author__ = 'aymgal'


import numpy as np
from scipy import ndimage



def degree2radians(phi):
    return phi * np.pi / 180.

def eastofnorth2normalradians(phi_in):
    phi_out = degree2radians(phi_in - 90.)
    return phi_out

def shift(x, y, center_x, center_y):
    x_shift = x - center_x
    y_shift = y - center_y
    return x_shift, y_shift

def rotate(x, y, phi_radians):
    cos_phi = np.cos(phi_radians)
    sin_phi = np.sin(phi_radians)
    x_trans = cos_phi * x + sin_phi * y
    y_trans = -sin_phi * x + cos_phi * y
    return x_trans, y_trans

def shift_rotate_elliptical(x, y, phi_radians, q, center_x, center_y):
    x_shift, y_shift = shift(x, y, center_x, center_y)
    x_trans, y_trans = rotate(x_shift, y_shift, phi_radians)
    return x_trans * np.sqrt(q), y_trans / np.sqrt(q)

def cartesian2polar(x, y):
    r = np.hypot(x, y)
    phi = np.arctan2(y, x)
    return r, phi


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
