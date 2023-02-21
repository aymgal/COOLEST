__author__ = 'lynevdv'


import numpy as np
from coolest.api.profiles import util


class Sersic(object):

    """Elliptical Sersic"""

    def surface_brightness(self):
        raise ValueError("Sersic surface brightness can only be evaluated")

    def evaluate_surface_brightness(self, x, y, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the surface brightness at the given position (x, y)"""
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi, q, center_x, center_y)
        bn = 1.9992*n - 0.3271
        return I_eff * np.exp( - bn * ( (np.sqrt(x_t**2+y_t**2) / theta_eff )**(1./n) -1. ) )


class PixelatedRegularGrid(object):

    """Pixelated profile on a regular grid"""

    def __init__(self, field_of_view_x, field_of_view_y):
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y

    def surface_brightness(self, pixels=None):
        """Returns the surface brightness pixels"""
        if pixels is None:
            return 0., [0, 0, 0, 0]
        extent = [self._fov_x[0], self._fov_x[1], self._fov_y[0], self._fov_y[1]]
        return pixels, extent

    def evaluate_surface_brightness(self, pixels=None):
        """Returns the surface brightness at the given position (x, y)"""
        raise NotImplementedError()


class IrregularGrid(object):

    """Pixelated profile on an irregular grid of points {x, y, z}"""

    def __init__(self, field_of_view_x, field_of_view_y):
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y

    def surface_brightness(self, x=None, y=None, z=None):
        """Returns the surface brightness pixels"""
        if pixels is None:
            return 0., [0, 0, 0, 0]
        extent = [self._fov_x[0], self._fov_x[1], self._fov_y[0], self._fov_y[1]]
        return (x, y, z), extent

    def evaluate_surface_brightness(self, pixels=None):
        """Returns the surface brightness at the given position (x, y)"""
        raise NotImplementedError()

