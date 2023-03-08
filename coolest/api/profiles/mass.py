__author__ = 'aymgal'


import numpy as np
from scipy import special

from coolest.template.classes.profiles.mass import (PEMD as TemplatePEMD,
                                                    ExternalShear as TemplateExternalShear)
from coolest.api.profiles import util


class PEMD(TemplatePEMD):

    """
    Power-law Elliptical Mass Distribution (a.k.a. Elliptical Power-law)
    Implementations from lenstronomy (Birrer et al.) and Tessore et al. 2015 were used.
    """


    def param_conv(self, theta_E, q, gamma):
        theta_E_conv = theta_E / (np.sqrt((1. + q**2) / (2. * q)))
        b = theta_E_conv * np.sqrt((1. + q**2) / 2.)
        t = gamma - 1.
        return b, t

    def deflection(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        b, t = self.param_conv(theta_E, q, gamma)
        # shift and rotate
        phi_ = util.eastofnorth2normalradians(phi)
        x_, y_ = util.shift(x, y, center_x, center_y)
        #print("COOL-a", phi, x_[:3, 0], y_[:3, 0])
        x_, y_ = util.rotate(x_, y_, phi_)
        #print("COOL-b", x_[:3, 0], y_[:3, 0])

        a_x_, a_y_ = self._defl_major_axis(x_, y_, b, t, q)

        # rotate back
        #print("COOL-c", phi, a_x[:3, 0], a_y[:3, 0])
        a_x, a_y = util.rotate(a_x_, a_y_, - phi_)
        #print("COOL-d", phi, a_x[:3, 0], a_y[:3, 0])
        return a_x, a_y

    @staticmethod
    def _defl_major_axis(x_, y_, b, t, q):
        # evaluate the profile following to Tessore et al. 2015
        Z = np.empty(np.shape(x_), dtype=complex)
        Z.real = q * x_
        Z.imag = y_
        R = np.abs(Z)
        R = np.maximum(R, 1e-9)
        R_omega = Z * special.hyp2f1(1, t/2, 2-t/2, -(1-q)/(1+q)*(Z/Z.conj()))
        alpha = 2. / (1+q) * (b/R)**t * R_omega
        a_x_ = np.nan_to_num(alpha.real, neginf=-1e10, posinf=1e10)
        a_y_ = np.nan_to_num(alpha.imag, neginf=-1e10, posinf=1e10)
        return a_x_, a_y_

    def convergence(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the convergence (kappa) at the given position (x, y)"""
        phi_ = util.eastofnorth2normalradians(phi)
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi_, q, center_x, center_y)
        return (3.-gamma)/2. * (theta_E / np.sqrt(x_t**2+y_t**2)) ** (gamma-1.)

    @staticmethod
    def _conv_major_axis(x_, y_, b, t, q):
        R = np.hypot(q*x_, y_)
        R = np.maximum(R, 1e-9)
        return (2 - t)/2. * (b/R)**t

    def hessian(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        b, t = self.param_conv(theta_E, q, gamma)
        phi_ = util.eastofnorth2normalradians(phi)
        x_, y_ = util.shift(x, y, center_x, center_y)
        x_, y_ = util.rotate(x_, y_, phi_)

        # convergence
        kappa_ = self._conv_major_axis(x_, y_, b, t, q)
        kappa_ = np.nan_to_num(kappa_, neginf=-1e10, posinf=1e10)

        # deflection
        alpha_x_, alpha_y_ = self._defl_major_axis(x_, y_, b, t, q)

        #R = np.hypot(q*x, y)
        #R = np.maximum(R, 1e-9)
        r = np.hypot(x_, y_)
        cos, sin = x_/r, y_/r

        # shear
        gamma_1_ = (1-t)*(alpha_x_*cos - alpha_y_*sin)/r - kappa_*(cos*cos*2 - 1)
        gamma_2_ = (1-t)*(alpha_y_*cos + alpha_x_*sin)/r - kappa_*(sin*cos*2)
        gamma_1_ = np.nan_to_num(gamma_1_, neginf=-1e10, posinf=1e10)
        gamma_2_ = np.nan_to_num(gamma_2_, neginf=-1e10, posinf=1e10)

        # hessian derivatives, still oriented along major axis?
        #H_xx = kappa + gamma_1_
        #H_yy = kappa - gamma_1_
        #H_xy = gamma_2_
        #H_yx = H_xy

        kappa = kappa_
        gamma_1 = np.cos(2 * phi_) * gamma_1_ - np.sin(2 * phi_) * gamma_2_
        gamma_2 = np.sin(2 * phi_) * gamma_1_ + np.cos(2 * phi_) * gamma_2_

        H_xx = kappa + gamma_1
        H_yy = kappa - gamma_1
        H_xy = gamma_2
        H_yx = H_xy

        return H_xx, H_xy, H_yx, H_yy


class ExternalShear(TemplateExternalShear):

    def deflection(self, x, y, gamma_ext=0., phi_ext=0.):
        """coordinates of the origin for the external shear profile assumed to be (0., 0.)""" 
        phi_ext_ = util.eastofnorth2normalradians(phi_ext)
        gamma1 = gamma_ext * np.cos(2.*phi_ext_)
        gamma2 = gamma_ext * np.sin(2.*phi_ext_)
        x_ = x # no shift
        y_ = y # no shift
        a_x = gamma1 * x_ + gamma2 * y_
        a_y = gamma2 * x_ - gamma1 * y_
        return a_x, a_y

    def convergence(self, x, y, gamma_ext=0., phi_ext=0.):
        return np.zeros_like(x)

    def hessian(self, x, y, gamma_ext=0., phi_ext=0.):
        kappa = 0.
        phi_ext_ = util.eastofnorth2normalradians(phi_ext)
        gamma1 = gamma_ext * np.cos(2.*phi_ext_)
        gamma2 = gamma_ext * np.sin(2.*phi_ext_)
        H_xx = kappa + gamma1
        H_yy = kappa - gamma1
        H_xy = gamma2
        H_yx = H_xy
        return H_xx, H_xy, H_yx, H_yy
