__author__ = 'aymgal'


import pytest
import numpy as np
import numpy.testing as npt


class TestPEMD(object):

    def test_convergence(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        theta_E = 1.1
        gamma = 1.9
        q = 0.9
        phi = 22.
        center_x = 0.1
        center_y = -0.15
        
        # COOLEST
        from coolest.api.profiles.mass import PEMD
        result = PEMD().convergence(x, y,
                                    theta_E=theta_E, gamma=gamma, phi=phi, q=q,
                                    center_x=center_x, center_y=center_y)

        # reference
        from lenstronomy.Util import param_util
        from lenstronomy.LensModel.lens_model import LensModel
        ref = LensModel(['EPL'])
        e1, e2 = param_util.phi_q2_ellipticity(phi*np.pi/180., q)
        kwargs = {
            'gamma': gamma, 
            'theta_E': theta_E, 
            'e1': e1, 'e2': e2,
            'center_x': center_x,
            'center_y': center_y,
        }
        result_ref = ref.kappa(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(result, result_ref, decimal=8)
