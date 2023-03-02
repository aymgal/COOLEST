__author__ = 'aymgal'

from coolest.template.classes.profile import Profile, AnalyticalProfile
from coolest.template.classes.parameter import NonLinearParameter
from coolest.template.classes.parameter import (DefinitionRange,
                                            PixelatedRegularGridParameter)
from coolest.template.classes.grid import PixelatedRegularGrid


__all__ = [
    'SIE', 
    'NIE',
    'PEMD',
    'SPEMD',
    'NFW',
    'Chameleon',
    'ExternalShear', 
    'PixelatedRegularGridPotential',
]
SUPPORTED_CHOICES = __all__


class SIE(AnalyticalProfile):
    
    def __init__(self):
        documentation = "Singular isothermal sphere"
        parameters = {
            'theta_E': NonLinearParameter("Einstein radius",
                                          DefinitionRange(min_value=0.0),
                                          latex_str=r"$\theta_{\rm E}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                                           DefinitionRange(),
                                           latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                                           DefinitionRange(),
                                           latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class NIE(AnalyticalProfile):
    
    def __init__(self):
        documentation = "Non-singular isothermal sphere"
        parameters = {
            'theta_E': NonLinearParameter("Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\theta_{\rm E}$"),
            'r_core': NonLinearParameter("Core radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm c}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class PEMD(AnalyticalProfile):
    
    def __init__(self):
        documentation = "Powerlaw elliptical mass distribution"
        parameters = {
            'gamma': NonLinearParameter("Mass density slope at Einstein radius",
                               DefinitionRange(min_value=1.0, max_value=3.0),
                               latex_str=r"$\gamma$"),
            'theta_E': NonLinearParameter("Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\theta_{\rm E}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class SPEMD(AnalyticalProfile):
    
    def __init__(self):
        documentation = "Softened powerlaw elliptical mass distribution"
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
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class NFW(AnalyticalProfile):
    
    def __init__(self):
        documentation = "NFW with ellipticity introduced in the mass"
        parameters = {
            'r_s': NonLinearParameter("Radius at which the mass density profile slope transitions from -1 to -3",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm s}$"),
            'rho_0': NonLinearParameter("Characteristic mass density",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\rho_0$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class Chameleon(AnalyticalProfile):
    
    def __init__(self):
        documentation = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = {
            'b': NonLinearParameter("Normalization of the profile",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\alpha_1$"),
            's_c': NonLinearParameter("Core radius of inner NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm c}$"),
            's_t': NonLinearParameter("Core radius of outer NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm t}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$q$"),
            'phi': NonLinearParameter("Position angle",
                                     DefinitionRange(min_value=-90., max_value=90.),
                                     latex_str=r"$\phi$"),
            'center_x': NonLinearParameter("Profile center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Profile center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$")
        }
        super().__init__(documentation, parameters)


class ExternalShear(AnalyticalProfile):
    
    def __init__(self):
        documentation = "External shear defined with a strength and orientation"
        parameters = {
            'gamma_ext': NonLinearParameter("Strength of external shear",
                               DefinitionRange(min_value=0., max_value=1.0),
                               latex_str=r"$\gamma_{\rm ext}$"),
            'phi_ext': NonLinearParameter("Orientation of external shear",
                               DefinitionRange(min_value=-90., max_value=90.),
                               latex_str=r"$\phi_{\rm ext}$"),
        }
        super().__init__(documentation, parameters)


class PixelatedRegularGridPotential(Profile):

    def __init__(self):
        documentation = "A pixelated profile defined on a regular Cartesian grid"
        parameters = {
            'pixels': PixelatedRegularGridParameter("Pixel values")
        }
        super().__init__(documentation, parameters)
