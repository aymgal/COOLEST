__author__ = 'aymgal'


import numpy as np

from coolest.template.classes.profiles.mass import PEMD as TemplatePEMD
from coolest.api.profiles import util


class PEMD(TemplatePEMD):

    """Power-law Elliptical Mass Distribution (a.k.a. Elliptical Power-law)"""

    def convergence(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the convergence (kappa) at the given position (x, y)"""
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi, q, center_x, center_y)
        return (3.-gamma)/2. * (theta_E / np.sqrt(x_t**2+y_t**2)) ** (gamma-1)
