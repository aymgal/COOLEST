__author__ = 'aymgal'

from lensmodelapi.api.profile import MassProfile
from lensmodelapi.api.parameter import NonLinearParameter, PixelParameterSet
from lensmodelapi.api.parameter import DefinitionRange


__all__ = [
    'SIE', 
    'NIE',
    'PEMD',
    'SPEMD',
    'NFW',
    'Chameleon',
    'ExternalShear', 
    'PixelatedPotential',
    'PixelatedConvergence',
]
SUPPORTED_CHOICES = __all__


class SIE(MassProfile):
    
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


class NIE(MassProfile):
    
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


class PEMD(MassProfile):
    
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


class SPEMD(MassProfile):
    
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


class NFW(MassProfile):
    
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


class Chameleon(MassProfile):
    
    def __init__(self):
        documentation = ("Chameleon profile defined as the difference between two NIE profiles"
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


class ExternalShear(MassProfile):
    
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


class PixelatedPotential(MassProfile):
    
    def __init__(self):
        documentation = "Pixelated lensing potential on a pixel grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(documentation, parameters)


class PixelatedConvergence(MassProfile):
    
    def __init__(self):
        documentation = "Pixelated convergence on a pixel grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(documentation, parameters)
