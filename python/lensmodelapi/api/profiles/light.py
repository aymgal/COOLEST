__author__ = 'aymgal'

from lensmodelapi.api.profile import LightProfile
from lensmodelapi.api.parameter_list import ParameterList
from lensmodelapi.api.parameter import (NonLinearParameter, 
                                        LinearParameter, 
                                        LinearParameterSet)
from lensmodelapi.api.parameter import DefinitionRange


__all__ = [
    'SersicElliptical',
    'Chameleon',
    'Uniform',
    'PixelatedRegularGrid',
    'PixelatedAdaptiveGrid',
]
SUPPORTED_CHOICES = __all__


class SersicElliptical(LightProfile):
    
    def __init__(self):
        description = "Elliptical Sersic"
        parameters = ParameterList(
            LinearParameter('A',
                            "Amplitude at origin",
                            DefinitionRange(min_value=0.0),
                            latex_name=r"$A$"),
            NonLinearParameter('R_sersic',
                               "Sersic radius",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"$R_{\rm Sersic}$"),
            NonLinearParameter('n_sersic',
                               "Sersic index",
                               DefinitionRange(min_value=0.5, max_value=10.0),
                               latex_name=r"$n_{\rm Sersic}$"),
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


class Chameleon(LightProfile):
    
    def __init__(self):
        description = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = ParameterList(
            LinearParameter('A',
                            "Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_name=r"$A$"),
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


class Uniform(LightProfile):
    
    def __init__(self):
        description = "Uniform sheet of light"
        parameters = ParameterList(
            LinearParameter('A',
                            "Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_name=r"$A$"),
        )
        super().__init__(description, parameters)


class PixelatedRegularGrid(LightProfile):
    
    def __init__(self):
        num_pixels = None # TODO
        description = "Pixelated light profile on a pixel grid"
        parameters = ParameterList(
            LinearParameterSet(num_pixels,
                               'pixels',
                               "Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"{\rm pixels}"),
        )
        super().__init__(description, parameters)


class PixelatedAdaptiveGrid(LightProfile):
    
    def __init__(self):
        num_pixels = None # TODO
        description = "Pixelated light profile on an adaptive (thus irregular) grid"
        parameters = ParameterList(
            LinearParameterSet(num_pixels,
                               'pixels',
                               "Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_name=r"{\rm pixels}"),
        )
        super().__init__(description, parameters)
