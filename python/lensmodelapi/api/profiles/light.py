__author__ = 'aymgal'

from lensmodelapi.api.profile import LightProfile
from lensmodelapi.api.parameter import (NonLinearParameter, 
                                        LinearParameter, 
                                        LinearParameterSet, 
                                        NonLinearParameterSet, 
                                        PixelParameterSet)
from lensmodelapi.api.parameter import DefinitionRange


__all__ = [
    'Sersic',
    'Chameleon',
    'Uniform',
    'Shapelets',
    'LensedPS',
    'PixelatedRegularGrid',
    'PixelatedAdaptiveGrid',
]
SUPPORTED_CHOICES = __all__


class Sersic(LightProfile):
    
    def __init__(self):
        description = "Elliptical Sersic"
        parameters = {
            'A': LinearParameter("Amplitude at origin",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$A$"),
            'R_sersic': NonLinearParameter("Sersic radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$R_{\rm Sersic}$"),
            'n_sersic': NonLinearParameter("Sersic index",
                               DefinitionRange(min_value=0.5, max_value=10.0),
                               latex_str=r"$n_{\rm Sersic}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$e_1$"),
            'phi': NonLinearParameter("Position angle",
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


class Chameleon(LightProfile):
    
    def __init__(self):
        description = ("Chameleon profile defined as the difference between two NIE profiles"
                       " (elliptical truncated double isothermal profile)")
        parameters = {
            'A': LinearParameter("Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$A$"),
            'w_c': NonLinearParameter("Core radius of inner NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm c}$"),
            'w_t': NonLinearParameter("Core radius of outer NIE",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$w{\rm t}$"),
            'q': NonLinearParameter("Axis ratio, semi-minor axis / semi-major axis",
                                     DefinitionRange(min_value=0.0, max_value=1.0),
                                     latex_str=r"$e_1$"),
            'phi': NonLinearParameter("Position angle",
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


class Shapelets(LightProfile):
    
    def __init__(self):
        self.n_max = None # TODO
        num_coeffs = None # (self.n_max+1)*(self.n_max+2) / 2
        description = "Set of shapelet functions"
        parameters = {
            'beta': NonLinearParameter("Shapelet characteristic scale",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\beta$"),
            'center_x': NonLinearParameter("Shapelets center along x coordinates",
                               DefinitionRange(),
                               latex_str=r"$x_0$"),
            'center_y': NonLinearParameter("Shapelets center along y coordinates",
                               DefinitionRange(),
                               latex_str=r"$y_0$"),
            'amps': LinearParameterSet("Set of amplitude values for each shapelet function",
                               DefinitionRange(),
                               latex_str=r"$A$"),
        }
        super().__init__(description, parameters)

        
class LensedPS(LightProfile):
    def __init__(self):
        description = "Set of lensed point sources"
        parameters = {
            'ra_list': NonLinearParameterSet("RA positions of the lensed point sources",
                               DefinitionRange(),
                               latex_str=r"$ra$"),
            'dec_list': NonLinearParameterSet("DEC positions of the lensed point sources",
                               DefinitionRange(),
                               latex_str=r"$dec$"),
            'amps': LinearParameterSet("Set of amplitude values for the lensed point sources",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$A$"),
        }
        super().__init__(description, parameters)


class Uniform(LightProfile):
    
    def __init__(self):
        description = "Uniform sheet of light"
        parameters = {
            'A': LinearParameter("Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$A$"),
        }
        super().__init__(description, parameters)


class PixelatedRegularGrid(LightProfile):
    
    def __init__(self):
        description = "Pixelated light profile on a pixel grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(description, parameters)


class PixelatedAdaptiveGrid(LightProfile):
    
    def __init__(self):
        description = "Pixelated light profile on an adaptive (thus irregular) grid"
        parameters = {
            'pixels': PixelParameterSet("Set of pixel values",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"{\rm pixels}"),
        }
        super().__init__(description, parameters)
