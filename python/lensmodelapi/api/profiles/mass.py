__author__ = 'aymgal'

from lensmodelapi.api.profile import MassProfile
from lensmodelapi.api.parameter import NonLinearParameter, PixelParameterSet
from lensmodelapi.api.parameter import DefinitionRange


__all__ = [
    'SIE', 
    'NIE',
    'PEMD',
    'SPEMD',
    'NFWElliptical',
    'Chameleon',
    'ExternalShearEllipticity', 
    'ExternalShearAngleStrength',
    'PixelatedPotential',
    'PixelatedConvergence',
]
SUPPORTED_CHOICES = __all__


class SIE(MassProfile):
    
    def __init__(self):
        description = "Singular isothermal sphere"
        parameters = {
            'theta_E': NonLinearParameter("Einstein radius",
                                          DefinitionRange(min_value=0.0),
                                          latex_str=r"$\theta_{\rm E}$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                                     DefinitionRange(min_value=-1.0, max_value=1.0),
                                     latex_str=r"$e_1$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                                     DefinitionRange(min_value=-1.0, max_value=1.0),
                                     latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                                           DefinitionRange(),
                                           latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                                           DefinitionRange(),
                                           latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class NIE(MassProfile):
    
    def __init__(self):
        description = "Non-singular isothermal sphere"
        parameters = {
            'theta_E': NonLinearParameter("Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\theta_{\rm E}$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_1$"),
            'r_core': NonLinearParameter("Core radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm c}$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class PEMD(MassProfile):
    
    def __init__(self):
        description = "Powerlaw elliptical mass distribution"
        parameters = {
            'gamma': NonLinearParameter("Mass density slope at Einstein radius",
                               DefinitionRange(min_value=1.0, max_value=3.0),
                               latex_str=r"$\gamma$"),
            'theta_E': NonLinearParameter("Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\theta_{\rm E}$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_1$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class SPEMD(MassProfile):
    
    def __init__(self):
        description = "Softened powerlaw elliptical mass distribution"
        parameters = {
            'gamma': NonLinearParameter("Mass density slope at Einstein radius",
                               DefinitionRange(min_value=1.0, max_value=3.0),
                               latex_str=r"$\gamma$"),
            'theta_E': NonLinearParameter("Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\theta_{\rm E}$"),
            'r_core': NonLinearParameter("Core radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm c}$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_1$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class NFWElliptical(MassProfile):
    
    def __init__(self):
        description = "NFW with ellipticity introduced in the mass"
        parameters = {
            'r_s': NonLinearParameter("Radius at which the mass density profile slope transitions from -1 to -3",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm s}$"),
            'rho_0': NonLinearParameter("Characteristic mass density",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\rho_0$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_1$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class Chameleon(MassProfile):
    
    def __init__(self):
        description = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = {
            'alpha_1': NonLinearParameter("Deflection angle at 1 (in coordinates units) from the center",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\alpha_1$"),
            'w_c': NonLinearParameter("Core radius of inner NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm c}$"),
            'w_t': NonLinearParameter("Core radius of outer NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm t}$"),
            'e1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_1$"),
            'e2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$e_2$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class ExternalShearEllipticity(MassProfile):
    
    def __init__(self):
        description = "External shear defined with ellipticity"
        parameters = {
            'gamma1': NonLinearParameter("Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$\gamma_1$"),
            'gamma2': NonLinearParameter("Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$\gamma_2$"),
            'center_x': NonLinearParameter("Shear origin along x coordinates",
                               DefinitionRange(),
                               fixed=True,
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Shear origin along y coordinates",
                               DefinitionRange(),
                               fixed=True,
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class ExternalShearAngleStrength(MassProfile):
    
    def __init__(self):
        description = "External shear defined with ellipticity"
        parameters = {
            'gamma_ext': NonLinearParameter("Strength of external shear",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$\gamma_{\rm ext}$"),
            'phi_ext': NonLinearParameter("Orientation of external shear",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_str=r"$\phi_{\rm ext}$"),
            'center_x': NonLinearParameter("Shear origin along x coordinates",
                               DefinitionRange(),
                               fixed=True,
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Shear origin along y coordinates",
                               DefinitionRange(),
                               fixed=True,
                               latex_str=r"$y_0$")
        }
        super().__init__(description, parameters)


class PixelatedPotential(MassProfile):
    
    def __init__(self):
        description = "Pixelated lensing potential on a pixel grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(description, parameters)


class PixelatedConvergence(MassProfile):
    
    def __init__(self):
        description = "Pixelated convergence on a pixel grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(description, parameters)
