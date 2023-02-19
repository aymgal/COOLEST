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
