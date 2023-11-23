__author__ = 'aymgal', 'lynevdv', 'Giorgos Vernardos'


import numpy as np
from scipy import interpolate

from coolest.template.classes.profiles.light import (Sersic as TemplateSersic,
                                                     Shapelets as TemplateShapelets,
                                                     PixelatedRegularGrid as TemplatePixelatedRegularGrid,
                                                     IrregularGrid as TemplateIrregularGrid)
from coolest.api.profiles import util


class BaseLightProfile(object):

    _template_class = None
    _units = None

    def surface_brightness(self, **params):
        raise NotImplementedError(f"The method surface_brightness() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def evaluate_surface_brightness(self, **params):
        raise NotImplementedError(f"The method evaluate_surface_brightness() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def get_extent(self):
        return None

    def get_coordinates(self):
        return None

    @property
    def units(self):
        if not hasattr(self, '_units'):
            raise ValueError(f"Units for profile {self.__class__.__name__} must be specified")
        if self._units not in ('per_pix', 'per_ang'):
            raise ValueError(f"Unsupported units type {self._units}")
        return self._units

    @property
    def template_class(self):
        if self._template_class is None:
            raise RuntimeError("No template class has been set by light profile class")
        return self._template_class

    @property
    def type(self):
        return self.template_class.type

    @property
    def parameter_names(self):
        return list(self.template_class.parameters.keys())


class Sersic(BaseLightProfile):

    """Elliptical Sersic"""

    _units = 'per_ang'
    _template_class = TemplateSersic()

    def surface_brightness(self, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        raise ValueError("Sersic surface brightness can only be evaluated")

    def evaluate_surface_brightness(self, x, y, I_eff=1., theta_eff=2., n=4., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the surface brightness at the given position (x, y)"""
        phi_ = util.eastofnorth2normalradians(phi)
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi_, q, center_x, center_y)
        bn = 1.9992*n - 0.3271
        return I_eff * np.exp( - bn * ( (np.sqrt(x_t**2+y_t**2) / theta_eff )**(1./n) -1. ) )


class Shapelets(BaseLightProfile):

    """Elliptical Sersic
    
    The implementation uses functions from `lenstronomy` (:cite:t:`lenstronomy2018`, :cite:t:`lenstronomy2021`), based on the developments of :cite:t:`Refregier2003`.
    """

    _units = 'per_ang'
    _template_class = TemplateShapelets()

    def __init__(self):
        from lenstronomy.LightModel.Profiles.shapelets import ShapeletSet
        self._backend = ShapeletSet()

    def surface_brightness(self, amps=0, n_max=0, beta=0, center_x=0, center_y=0):
        raise ValueError("Surface brightness of a set of shapelets can only be evaluated")

    def evaluate_surface_brightness(self, x, y, amps=0, n_max=0, beta=0, center_x=0, center_y=0):
        """Returns the surface brightness at the given position (x, y)"""
        x_, y_ = x.flatten(), y.flatten()
        flux = self._backend.function(x_, y_, amps, n_max, beta, center_x=center_x, center_y=center_y)
        return flux.reshape(*x.shape)


class PixelatedRegularGrid(BaseLightProfile):

    """Pixelated profile on a regular grid"""

    _units = 'per_pix'
    _template_class = TemplatePixelatedRegularGrid()

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
        coordinates = self.get_coordinates()
        points = coordinates.pixel_axes
        interp = util.CartesianGridInterpolator(points, pixels, method=self._interp_method)
        points_eval = np.array([y.ravel(), x.ravel()]).T
        pixels_eval = interp(points_eval).reshape(*x.shape)
        return pixels_eval

    def get_extent(self):
        coordinates = self.get_coordinates()
        return coordinates.plt_extent

    def get_coordinates(self):
        from coolest.api.util import get_coordinates_from_regular_grid
        return get_coordinates_from_regular_grid(self._fov_x, self._fov_y, self._nx, self._ny)


class IrregularGrid(BaseLightProfile):

    """Pixelated profile on an irregular grid of points {x, y, z}"""

    _units = 'per_pix'
    _template_class = TemplateIrregularGrid()

    def __init__(self, field_of_view_x, field_of_view_y, num_pix,
                 interpolation_method='cubic'):
        self._fov_x = field_of_view_x
        self._fov_y = field_of_view_y
        self._n = num_pix
        self._interp_method = interpolation_method

    def surface_brightness(self, x=None, y=None, z=None):
        """Returns the surface brightness pixels"""
        if x is None or y is None or z is None:
            return np.zeros(self._n), np.zeros(self._n), np.zeros(self._n)
        return x, y, z

    def evaluate_surface_brightness(self, x_eval, y_eval, x=None, y=None, z=None):
        z_eval = interpolate.griddata((x, y), z, (x_eval, y_eval), 
                                      method=self._interp_method)
        return z_eval

    def get_extent(self):
        return [
            self._fov_x[0], 
            self._fov_x[1], 
            self._fov_y[0], 
            self._fov_y[1]
        ]
