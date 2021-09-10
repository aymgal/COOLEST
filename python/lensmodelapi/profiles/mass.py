__author__ = 'aymgal'

from lensmodelapi.profile import MassProfile
from lensmodelapi.parameter_list import ParameterList
from lensmodelapi.parameter import NonLinearParameter


__all__ = [
    'SIE', 
    'PEMD',
    'SPEMD',
    'NFWElliptical',
    'Chameleon',
    'ExternalShearEllipticity', 
    'ExternalShearAngleStrength',
]
SUPPORTED_PROFILES = __all__


class SIE(MassProfile):
    
    def __init__(self):
        name = 'SIE'
        description = "Singular isothermal sphere"
        parameters = ParameterList([
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               min_value=0.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class PEMD(MassProfile):
    
    def __init__(self):
        name = 'PEMD'
        description = "Powerlaw elliptical mass distribution"
        parameters = ParameterList([
            NonLinearParameter('gamma',
                               "Mass density slope at Einstein radius",
                               min_value=1.0,
                               latex_name=r"$\gamma$"),
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               min_value=0.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class SPEMD(MassProfile):
    
    def __init__(self):
        name = 'SPEMD'
        description = "Softened powerlaw elliptical mass distribution"
        parameters = ParameterList([
            NonLinearParameter('gamma',
                               "Mass density slope at Einstein radius",
                               min_value=1.0,
                               max_value=3.0,
                               latex_name=r"$\gamma$"),
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               min_value=0.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('r_core',
                               "Core radius",
                               min_value=0.0,
                               latex_name=r"$r_{\rm c}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class NFWElliptical(MassProfile):
    
    def __init__(self):
        name = 'NFW_elliptical'
        description = "NFW with ellipticity introduced in the mass"
        parameters = ParameterList([
            NonLinearParameter('r_s',
                               "Radius at which the mass density profile slope transitions from -1 to -3",
                               min_value=0.0,
                               latex_name=r"$r_{\rm s}$"),
            NonLinearParameter('rho_0',
                               "Characteristic mass density",
                               min_value=0.0,
                               latex_name=r"$\rho_0$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class Chameleon(MassProfile):
    
    def __init__(self):
        name = 'chameleon'
        description = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = ParameterList([
            NonLinearParameter('alpha_1',
                               "Deflection angle at 1 (in coordinates units) from the center",
                               min_value=0.0,
                               latex_name=r"$\alpha_1$"),
            NonLinearParameter('w_c',
                               "Core radius of inner NIE",
                               min_value=0.0,
                               latex_name=r"$w{\rm c}$"),
            NonLinearParameter('w_t',
                               "Core radius of outer NIE",
                               min_value=0.0,
                               latex_name=r"$w{\rm t}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class ExternalShearEllipticity(MassProfile):
    
    def __init__(self):
        name = 'ext_shear_gamma1gamma2'
        description = "External shear defined with ellipticity"
        parameters = ParameterList([
            NonLinearParameter('gamma1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('gamma2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)


class ExternalShearAngleStrength(MassProfile):
    
    def __init__(self):
        name = 'ext_shear_gamma_psi'
        description = "External shear defined with ellipticity"
        parameters = ParameterList([
            NonLinearParameter('gamma',
                               "Strength of external shear",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('phi',
                               "Orientation of external shear",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        ])
        super().__init__(name, description, parameters)
