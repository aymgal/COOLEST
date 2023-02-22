__author__ = 'lynevdv'


import numpy as np

from coolest.api.profiles import util


class BaseLightProfile(object):

    _units = None

    def surface_brightness(self, **params):
        raise NotImplementedError(f"The method surface_brightness() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def evaluate_surface_brightness(self, **params):
        raise NotImplementedError(f"The method evaluate_surface_brightness() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def get_extent(self):
        return None

    @property
    def units(self):
        if not hasattr(self, '_units'):
            raise NotImplementedError(f"Units for profile {self.__class__.__name__} is not defined")
        if self._units not in ('flux_per_pix', 'flux_per_ang'):
            raise ValueError(f"Unsupported units type {self._units}")
        return self._units


class Sersic(BaseLightProfile):

    """Elliptical Sersic"""

    _units = 'flux_per_ang'

    def surface_brightness(self, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        raise ValueError("Sersic surface brightness can only be evaluated")

    def evaluate_surface_brightness(self, x, y, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the surface brightness at the given position (x, y)"""
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi, q, center_x, center_y)
        bn = 1.9992*n - 0.3271
        return I_eff * np.exp( - bn * ( (np.sqrt(x_t**2+y_t**2) / theta_eff )**(1./n) -1. ) )


class PixelatedRegularGrid(BaseLightProfile):

    """Pixelated profile on a regular grid"""

    _units = 'flux_per_pix'

    def __init__(self, field_of_view_x, field_of_view_y, num_pix_x, num_pix_y,
                 interpolation_method='cubic'):
        if num_pix_x == 0 or num_pix_y == 0:
            raise ValueError("Light profile defined on regular grid has zero pixels")
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y
        self._nx = num_pix_x
        self._ny = num_pix_y
        self._shape = (num_pix_x, num_pix_y)
        self._pix_scl_x = np.abs(self._fov_x[0] - self._fov_x[1]) / self._nx
        self._pix_scl_y = np.abs(self._fov_y[0] - self._fov_y[1]) / self._ny
        self._interp_method = interpolation_method

    def surface_brightness(self, pixels=None):
        """Returns the surface brightness pixels"""
        if pixels is None:
            return np.zeros(self._shape)
        return pixels

    def evaluate_surface_brightness(self, x, y, pixels=None):
        extent = self.get_extent()
        points = (
            np.linspace(extent[2], extent[3], self._ny, endpoint=True),
            np.linspace(extent[0], extent[1], self._nx, endpoint=True),
        )
        values = pixels
        interp = util.CartesianGridInterpolator(points, values, 
                                                method=self._interp_method)
        points_eval = np.array([y.ravel(), x.ravel()]).T
        values_eval = interp(points_eval).reshape(*x.shape)
        return values_eval

    def get_extent(self):
        half_pix_x = self._pix_scl_x / 2.
        half_pix_y = self._pix_scl_y / 2.
        return [
            self._fov_x[0] - half_pix_x, 
            self._fov_x[1] + half_pix_x, 
            self._fov_y[0] - half_pix_y, 
            self._fov_y[1] + half_pix_y
        ]


class IrregularGrid(BaseLightProfile):

    """Pixelated profile on an irregular grid of points {x, y, z}"""

    _units = 'flux_per_pix'

    def __init__(self, field_of_view_x, field_of_view_y, num_pix):
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y
        self._n = num_pix

    def surface_brightness(self, x=None, y=None, z=None):
        """Returns the surface brightness pixels"""
        if x is None or y is None or z is None:
            return 0.
        return x, y, z
