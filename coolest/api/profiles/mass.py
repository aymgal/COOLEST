__author__ = 'aymgal'


import numpy as np
from scipy import special

from coolest.template.classes.profiles.mass import (PEMD as TemplatePEMD,
                                                    SIE as TemplateSIE,
                                                    ExternalShear as TemplateExternalShear,
                                                    ConvergenceSheet as TemplateConvergenceSheet,
                                                    PixelatedRegularGridFullyDefined as TemplatePixRegGridFD)
from coolest.api.profiles import util



class BaseMassProfile(object):
    """Base class to define a mass profile to compute lensing quantities.
    Each specific class must be consistent with the equivalent class from the
    coolest.template submodule.

    NOTE: in the future, a new coolest.profiles submodule will merge
    profile definitions that are currently split between coolest.template and coolest.api. 
    """

    _units = None
    _template_class = None

    def evaluate_potential(self, **params):
        raise NotImplementedError(f"The method evaluate_potential() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def evaluate_deflection(self, **params):
        raise NotImplementedError(f"The method evaluate_deflection() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def evaluate_convergence(self, **params):
        raise NotImplementedError(f"The method evaluate_convergence() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    def evaluate_hessian(self, **params):
        raise NotImplementedError(f"The method evaluate_hessian() is not defined "
                                  f"for profile '{self.__class__.__name__}'")

    @property
    def template_class(self):
        if self._template_class is None:
            raise RuntimeError("No template class has been set by mass profile class")
        return self._template_class

    @property
    def type(self):
        return self.template_class.type

    @property
    def parameter_names(self):
        return list(self.template_class.parameters.keys())


class PEMD(BaseMassProfile):

    """
    Power-law Elliptical Mass Distribution (a.k.a. Elliptical Power-law)
    This follows implementations in lenstronomy (:cite:t:`lenstronomy2018`:, :cite:t:`lenstronomy2021`:) based on the formulae :cite:p:`Tessore2015`:.
    """

    # TODO: use parameter values (point estimates, prior, etc...) contained in the template?
    _units = 'per_ang'
    _template_class = TemplatePEMD()

    def param_conv(self, theta_E, q, gamma):
        theta_E_conv = theta_E / (np.sqrt((1. + q**2) / (2. * q)))
        b = theta_E_conv * np.sqrt((1. + q**2) / 2.)
        t = gamma - 1.
        return b, t

    def evaluate_potential(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        b, t = self.param_conv(theta_E, q, gamma)
        # shift and rotate
        phi_ = util.eastofnorth2normalradians(phi)
        x_, y_ = util.shift(x, y, center_x, center_y)
        x_, y_ = util.rotate(x_, y_, phi_)
        # deflection angle
        a_x_, a_y_ = self._defl_major_axis(x_, y_, b, t, q)
        # potential
        return (x_ * a_x_ + y_ * a_y_) / (2 - t)

    def evaluate_deflection(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        b, t = self.param_conv(theta_E, q, gamma)
        # shift and rotate
        phi_ = util.eastofnorth2normalradians(phi)
        x_, y_ = util.shift(x, y, center_x, center_y)
        x_, y_ = util.rotate(x_, y_, phi_)
        # deflection angle
        a_x_, a_y_ = self._defl_major_axis(x_, y_, b, t, q)
        # rotate back
        a_x, a_y = util.rotate(a_x_, a_y_, - phi_)
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

    def evaluate_convergence(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
        """Returns the convergence (kappa) at the given position (x, y)"""
        phi_ = util.eastofnorth2normalradians(phi)
        x_t, y_t = util.shift_rotate_elliptical(x, y, phi_, q, center_x, center_y)
        return (3.-gamma)/2. * (theta_E / np.sqrt(x_t**2+y_t**2)) ** (gamma-1.)

    @staticmethod
    def _conv_major_axis(x_, y_, b, t, q):
        R = np.hypot(q*x_, y_)
        R = np.maximum(R, 1e-9)
        return (2 - t)/2. * (b/R)**t

    def evaluate_hessian(self, x, y, theta_E=1., gamma=2., phi=0., q=1., center_x=0., center_y=0.):
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


class SIE(BaseMassProfile):
    """
    Singular Isothermal Elliptical mass profile.
    """

    _gamma = 2.  # isothermal slope
    _template_class = TemplateSIE
    _backend = PEMD()

    def evaluate_potential(self, x, y, theta_E=1., phi=0., q=1., center_x=0., center_y=0.):
        return self._backend.evaluate_potential(x, y, theta_E=theta_E, gamma=self._gamma, phi=phi, q=q, center_x=center_x, center_y=center_y)
    
    def evaluate_deflection(self, x, y, theta_E=1., phi=0., q=1., center_x=0., center_y=0.):
        return self._backend.evaluate_deflection(x, y, theta_E=theta_E, gamma=self._gamma, phi=phi, q=q, center_x=center_x, center_y=center_y)

    def evaluate_convergence(self, x, y, theta_E=1., phi=0., q=1., center_x=0., center_y=0.):
        return self._backend.evaluate_convergence(x, y, theta_E=theta_E, gamma=self._gamma, phi=phi, q=q, center_x=center_x, center_y=center_y)
    
    def evaluate_hessian(self, x, y, theta_E=1., phi=0., q=1., center_x=0., center_y=0.):
        return self._backend.evaluate_hessian(x, y, theta_E=theta_E, gamma=self._gamma, phi=phi, q=q, center_x=center_x, center_y=center_y)
    

class ExternalShear(BaseMassProfile):
    """
    Coordinates of the origin for the external shear profile are assumed to be (0., 0.).
    """ 

    _units = 'per_ang'
    _template_class = TemplateExternalShear()

    def evaluate_potential(self, x, y, gamma_ext=0., phi_ext=0.):
        phi_ext_ = util.eastofnorth2normalradians(phi_ext)
        r, phi = util.cartesian2polar(x, y)
        return 1. / 2 * gamma_ext * r**2 * np.cos(2. * (phi - phi_ext_))

    def evaluate_deflection(self, x, y, gamma_ext=0., phi_ext=0.):
        phi_ext_ = util.eastofnorth2normalradians(phi_ext)
        gamma1 = gamma_ext * np.cos(2.*phi_ext_)
        gamma2 = gamma_ext * np.sin(2.*phi_ext_)
        x_ = x # no shift
        y_ = y # no shift
        a_x = gamma1 * x_ + gamma2 * y_
        a_y = gamma2 * x_ - gamma1 * y_
        return a_x, a_y

    def evaluate_convergence(self, x, y, gamma_ext=0., phi_ext=0.):
        return np.zeros_like(x)

    def evaluate_hessian(self, x, y, gamma_ext=0., phi_ext=0.):
        kappa = 0.
        phi_ext_ = util.eastofnorth2normalradians(phi_ext)
        gamma1 = gamma_ext * np.cos(2.*phi_ext_)
        gamma2 = gamma_ext * np.sin(2.*phi_ext_)
        H_xx = kappa + gamma1
        H_yy = kappa - gamma1
        H_xy = gamma2
        H_yx = H_xy
        return H_xx, H_xy, H_yx, H_yy
    

class ConvergenceSheet(BaseMassProfile):
    """
    Coordinates of the origin for the convergence sheet are assumed to be (0., 0.).
    """

    _units = 'per_ang'
    _template_class = TemplateConvergenceSheet()

    def evaluate_potential(self, x, y, kappa_s=0.):
        x_ = x # no shift
        y_ = y # no shift
        r_ = np.hypot(x_, y_)
        return 0.5 * kappa_s * r_**2
    
    def evaluate_deflection(self, x, y, kappa_s=0.):
        x_ = x # no shift
        y_ = y # no shift
        return x_ * kappa_s, y_ * kappa_s

    def evaluate_convergence(self, x, y, kappa_s=0.):
        return np.full_like(x, kappa_s)

    def evaluate_hessian(self, x, y, kappa_s=0.):
        kappa = np.full_like(x, kappa_s)
        gamma1 = 0.
        gamma2 = 0.
        H_xx = kappa + gamma1
        H_yy = kappa - gamma1
        H_xy = gamma2
        H_yx = H_xy
        return H_xx, H_xy, H_yx, H_yy


class PixelatedRegularGridFullyDefined(BaseMassProfile):

    """Pixelated lens mass model defined a regular grid by its potential, derivatives and hessian arrays."""

    _units = 'per_pix'
    _template_class = TemplatePixRegGridFD()

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

    def potantial(self, pixels=None, pixels_derivative=None, pixels_hessian=None):
        """Returns the lensing potential"""
        if pixels is None:
            return np.zeros(self._shape)
        return pixels
    
    def evaluate_potential(self, x, y, pixels=None, pixels_derivative=None, pixels_hessian=None):
        return self._evaluate_pixels(x, y, pixels=pixels)
    
    def deflection(self, pixels=None, pixels_derivative=None, pixels_hessian=None):
        """Returns the deflection angles"""
        if pixels_derivative is None:
            return np.zeros(self._shape)
        return pixels_derivative
    
    def evaluate_deflection(self, x, y, pixels=None, pixels_derivative=None, pixels_hessian=None):
        a_x = self._evaluate_pixels(x, y, pixels=pixels_derivative[0])
        a_y = self._evaluate_pixels(x, y, pixels=pixels_derivative[1])
        return a_x, a_y
    
    def convergence(self, pixels=None, pixels_derivative=None, pixels_hessian=None):
        """Returns the deflection angles"""
        if pixels_hessian is None:
            return np.zeros(self._shape)
        return 0.5 * (pixels_hessian[0] + pixels_hessian[2])
    
    def evaluate_convergence(self, x, y, pixels=None, pixels_derivative=None, pixels_hessian=None):
        """Returns the deflection angles"""
        H = self.evaluate_hessian(x, y, pixels=pixels, pixels_derivative=pixels_derivative, pixels_hessian=pixels_hessian)
        return 0.5 * (H[0] + H[3])
    
    def hessian(self, pixels_hessian=None):
        """Returns the deflection angles"""
        if pixels_hessian is None:
            return np.zeros(self._shape)
        return pixels_hessian
    
    def evaluate_hessian(self, x, y, pixels=None, pixels_derivative=None, pixels_hessian=None):
        H_xx = self._evaluate_pixels(x, y, pixels=pixels_hessian[0])
        H_yy = self._evaluate_pixels(x, y, pixels=pixels_hessian[1])
        H_xy = self._evaluate_pixels(x, y, pixels=pixels_hessian[2])
        H_yx = H_xy
        return H_xx, H_xy, H_yx, H_yy

    def get_extent(self):
        coordinates = self.get_coordinates()
        return coordinates.plt_extent

    def get_coordinates(self):
        # NOTE: could be made a property to avoid re-doing the intanciation several times
        from coolest.api.util import get_coordinates_from_regular_grid
        return get_coordinates_from_regular_grid(self._fov_x, self._fov_y, self._nx, self._ny)
    
    def _evaluate_pixels(self, x, y, pixels=None):
        coordinates = self.get_coordinates()
        points = coordinates.pixel_axes
        interp = util.CartesianGridInterpolator(points, pixels, method=self._interp_method)
        points_eval = np.array([y.ravel(), x.ravel()]).T
        pixels_eval = interp(points_eval).reshape(*x.shape)
        return pixels_eval
    