__author__ = 'lynevdv'

import pytest
import numpy as np
import numpy.testing as npt

from coolest.api.profiles.light import Sersic

from lenstronomy.Util import param_util
from lenstronomy.LightModel.light_model import LightModel


class TestSersic(object):

    def test_surface_brightness(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        I_eff = 10.
        theta_eff = 2.
        n = 3.5
        q = 0.9
        phi = 22.
        center_x = 0.1
        center_y = -0.15

        # COOLEST
        result = Sersic().evaluate_surface_brightness(x, y, I_eff=I_eff, theta_eff=theta_eff, n=n, phi=phi, q=q,
                                                      center_x=center_x, center_y=center_y)

        # reference
        ref = LightModel(['SERSIC_ELLIPSE'])
        e1, e2 = param_util.phi_q2_ellipticity(phi * np.pi / 180., q)
        kwargs = {
            'amp': I_eff,
            'R_sersic': theta_eff,
            'n_sersic': n,
            'e1': e1, 'e2': e2,
            'center_x': center_x,
            'center_y': center_y,
        }
        result_ref = ref.surface_brightness(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(result, result_ref, decimal=8)
