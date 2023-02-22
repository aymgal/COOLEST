__author__ = 'lynevdv'


import numpy as np
from coolest.api.profiles import util



class BaseLightProfile(object):

    def surface_brightness(self, **params):
        raise NotImplementedError()

    def evaluate_surface_brightness(self, **params):
        raise NotImplementedError()

    def get_extent(self):
        return None


class Sersic(BaseLightProfile):

    """Elliptical Sersic"""

    def surface_brightness(self, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        raise ValueError("Sersic surface brightness can only be evaluated")

    def evaluate_surface_brightness(self, x, y, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the surface brightness at the given position (x, y)"""
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi, q, center_x, center_y)
        bn = 1.9992*n - 0.3271
        return I_eff * np.exp( - bn * ( (np.sqrt(x_t**2+y_t**2) / theta_eff )**(1./n) -1. ) )


class PixelatedRegularGrid(BaseLightProfile):

    """Pixelated profile on a regular grid"""

    def __init__(self, field_of_view_x, field_of_view_y, num_pix_x, num_pix_y):
        if num_pix_x == 0 or num_pix_y == 0:
            raise ValueError("Light profile defined on regular grid has zero pixels")
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y
        self._nx = num_pix_x
        self._ny = num_pix_y
        self._shape = (num_pix_x, num_pix_y)

    def surface_brightness(self, pixels=None):
        """Returns the surface brightness pixels"""
        if pixels is None:
            return np.zeros(self._shape)
        return pixels

    def evaluate_surface_brightness(self, pixels=None):
        """Returns the surface brightness at the given position (x, y)"""
        raise NotImplementedError()

    def get_extent(self):
        half_pix_x = np.abs(self._fov_x[0] - self._fov_x[1]) / self._nx / 2.
        half_pix_y = np.abs(self._fov_y[0] - self._fov_y[1]) / self._ny / 2.
        return [
            self._fov_x[0] - half_pix_x, 
            self._fov_x[1] + half_pix_x, 
            self._fov_y[0] - half_pix_y, 
            self._fov_y[1] + half_pix_y
        ]


class IrregularGrid(BaseLightProfile):

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

