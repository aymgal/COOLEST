__author__ = 'aymgal'


import pytest
import numpy as np
import numpy.testing as npt

from coolest.api.profiles.mass import PEMD, ExternalShear

from lenstronomy.Util import param_util
from lenstronomy.LensModel.lens_model import LensModel


class TestPEMD(object):

    def test_potential(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        theta_E = 1.1
        gamma = 1.9
        q = 1. #0.9
        phi = 22.
        center_x = 0.1
        center_y = -0.15
        
        # COOLEST
        psi = PEMD().potential(x, y,
                                    theta_E=theta_E, gamma=gamma, phi=phi, q=q,
                                    center_x=center_x, center_y=center_y)

        # reference
        ref = LensModel(['EPL'])
        e1, e2 = param_util.phi_q2_ellipticity((phi-90.)*np.pi/180., q)
        kwargs = {
            'gamma': gamma, 
            'theta_E': theta_E, 
            'e1': e1, 'e2': e2,
            'center_x': center_x,
            'center_y': center_y,
        }
        psi_ref = ref.potential(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(psi, psi_ref, decimal=8)

    def test_deflection(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        theta_E = 1.1
        gamma = 1.9
        q = 1. #0.9
        phi = 22.
        center_x = 0.1
        center_y = -0.15
        
        # COOLEST
        alpha_x, alpha_y = PEMD().deflection(x, y,
                                    theta_E=theta_E, gamma=gamma, phi=phi, q=q,
                                    center_x=center_x, center_y=center_y)

        # reference
        ref = LensModel(['EPL'])
        e1, e2 = param_util.phi_q2_ellipticity((phi-90.)*np.pi/180., q)
        kwargs = {
            'gamma': gamma, 
            'theta_E': theta_E, 
            'e1': e1, 'e2': e2,
            'center_x': center_x,
            'center_y': center_y,
        }
        alpha_x_ref, alpha_y_ref = ref.alpha(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(alpha_x, alpha_x_ref, decimal=8)
        npt.assert_almost_equal(alpha_y, alpha_y_ref, decimal=8)


    def test_hessian(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        theta_E = 1.1
        gamma = 1.9
        q = 1. #0.9
        phi = 22.
        center_x = 0.1
        center_y = -0.15
        
        # COOLEST
        H_xx, H_xy, _, H_yy = PEMD().hessian(x, y,
                                    theta_E=theta_E, gamma=gamma, phi=phi, q=q,
                                    center_x=center_x, center_y=center_y)

        # reference
        ref = LensModel(['EPL'])
        e1, e2 = param_util.phi_q2_ellipticity((phi-90.)*np.pi/180., q)
        kwargs = {
            'gamma': gamma, 
            'theta_E': theta_E, 
            'e1': e1, 'e2': e2,
            'center_x': center_x,
            'center_y': center_y,
        }
        H_xx_ref, H_xy_ref, _, H_yy_ref = ref.hessian(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(H_xx, H_xx_ref, decimal=8)
        npt.assert_almost_equal(H_yy, H_yy_ref, decimal=8)
        npt.assert_almost_equal(H_xy, H_xy_ref, decimal=8)


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
        result = PEMD().convergence(x, y,
                                    theta_E=theta_E, gamma=gamma, phi=phi, q=q,
                                    center_x=center_x, center_y=center_y)

        # reference
        ref = LensModel(['EPL'])
        e1, e2 = param_util.phi_q2_ellipticity((phi-90.)*np.pi/180., q)
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



class TestExternalShear(object):

    def test_potential(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        phi_ext = 22.
        gamma_ext = 0.08
        
        # COOLEST
        psi = ExternalShear().potential(x, y, phi_ext=phi_ext, gamma_ext=gamma_ext)

        # reference
        ref = LensModel(['SHEAR_GAMMA_PSI'])
        kwargs = {
            'gamma_ext': gamma_ext, 
            'psi_ext': (phi_ext-90.)*np.pi/180.,
            'ra_0': 0., 'dec_0': 0.,
        }
        psi_ref = ref.potential(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(psi, psi_ref, decimal=8)

    def test_deflection(self):
        # define some coordinates grid
        n_points = 10
        x_, y_ = np.linspace(-0.4, 0.2, n_points), np.linspace(-0.3, 0.5, n_points)
        x, y = np.meshgrid(x_, y_)
        # x, y = x.flatten(), y.flatten()

        # pick some parameter
        phi_ext = 22.
        gamma_ext = 0.08
        
        # COOLEST
        alpha_x, alpha_y = ExternalShear().deflection(x, y,
                                                      phi_ext=phi_ext, 
                                                      gamma_ext=gamma_ext)

        # reference
        ref = LensModel(['SHEAR_GAMMA_PSI'])
        kwargs = {
            'gamma_ext': gamma_ext, 
            'psi_ext': (phi_ext-90.)*np.pi/180.,
            'ra_0': 0., 'dec_0': 0.,
        }
        alpha_x_ref, alpha_y_ref = ref.alpha(x, y, [kwargs])

        # compare
        npt.assert_almost_equal(alpha_x, alpha_x_ref, decimal=8)
        npt.assert_almost_equal(alpha_y, alpha_y_ref, decimal=8)
