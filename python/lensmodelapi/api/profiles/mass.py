__author__ = 'aymgal'

from lensmodelapi.api.profile import MassProfile
from lensmodelapi.api.parameter_list import ParameterList
from lensmodelapi.api.parameter import NonLinearParameter, LinearParameterSet
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
        parameters = ParameterList(
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class NIE(MassProfile):
    
    def __init__(self):
        description = "Non-singular isothermal sphere"
        parameters = ParameterList(
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('r_core',
                               "Core radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$r_{\rm c}$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class PEMD(MassProfile):
    
    def __init__(self):
        description = "Powerlaw elliptical mass distribution"
        parameters = ParameterList(
            NonLinearParameter('gamma',
                               "Mass density slope at Einstein radius",
                               DefinitionRange(min_value=1.0, max_value=3.0),
                               latex_name=r"$\gamma$"),
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class SPEMD(MassProfile):
    
    def __init__(self):
        description = "Softened powerlaw elliptical mass distribution"
        parameters = ParameterList(
            NonLinearParameter('gamma',
                               "Mass density slope at Einstein radius",
                               DefinitionRange(min_value=1.0, max_value=3.0),
                               latex_name=r"$\gamma$"),
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('r_core',
                               "Core radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$r_{\rm c}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class NFWElliptical(MassProfile):
    
    def __init__(self):
        description = "NFW with ellipticity introduced in the mass"
        parameters = ParameterList(
            NonLinearParameter('r_s',
                               "Radius at which the mass density profile slope transitions from -1 to -3",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$r_{\rm s}$"),
            NonLinearParameter('rho_0',
                               "Characteristic mass density",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\rho_0$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class Chameleon(MassProfile):
    
    def __init__(self):
        description = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = ParameterList(
            NonLinearParameter('alpha_1',
                               "Deflection angle at 1 (in coordinates units) from the center",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$\alpha_1$"),
            NonLinearParameter('w_c',
                               "Core radius of inner NIE",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$w{\rm c}$"),
            NonLinearParameter('w_t',
                               "Core radius of outer NIE",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$w{\rm t}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class ExternalShearEllipticity(MassProfile):
    
    def __init__(self):
        description = "External shear defined with ellipticity"
        parameters = ParameterList(
            NonLinearParameter('gamma1',
                               "Complex ellipticity component 1",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('gamma2',
                               "Complex ellipticity component 2",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class ExternalShearAngleStrength(MassProfile):
    
    def __init__(self):
        description = "External shear defined with ellipticity"
        parameters = ParameterList(
            NonLinearParameter('gamma',
                               "Strength of external shear",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('phi',
                               "Orientation of external shear",
                               DefinitionRange(min_value=-1.0, max_value=1.0),
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               DefinitionRange(),
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               DefinitionRange(),
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        )
        super().__init__(description, parameters)


class PixelatedPotential(MassProfile):
    
    def __init__(self):
        num_pixels = None # TODO
        description = "Pixelated lensing potential on a pixel grid"
        parameters = ParameterList(
            LinearParameterSet(num_pixels,
                               'pixels',
                               "Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"{\rm pixels}"),
        )
        super().__init__(description, parameters)


class PixelatedConvergence(MassProfile):
    
    def __init__(self):
        num_pixels = None # TODO
        description = "Pixelated convergence on a pixel grid"
        parameters = ParameterList(
            LinearParameterSet(num_pixels,
                               'pixels',
                               "Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"{\rm pixels}"),
        )
        super().__init__(description, parameters)
