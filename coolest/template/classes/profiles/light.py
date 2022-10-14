__author__ = 'aymgal'

from coolest.template.classes.profile import Profile, AnalyticalLightProfile
from coolest.template.classes.parameter import (NonLinearParameter, 
                                            LinearParameter, 
                                            LinearParameterSet, 
                                            NonLinearParameterSet,
                                            PixelatedRegularGridParameter)
from coolest.template.classes.parameter import DefinitionRange


__all__ = [
    'Sersic',
    'Chameleon',
    'Uniform',
    'Shapelets',
    'LensedPS',
    'PixelatedRegularGrid',
    # 'PixelatedIrregularGrid',
    # 'PixelatedDelaunayGrid',
    # 'PixelatedVoronoiGrid',
]
SUPPORTED_CHOICES = __all__


class Sersic(AnalyticalLightProfile):
    
    def __init__(self):
        documentation = "Elliptical Sersic"
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


class Chameleon(AnalyticalLightProfile):
    
    def __init__(self):
        documentation = ("Chameleon profile defined as the difference between two NIE profiles"
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


class Shapelets(AnalyticalLightProfile):
    
    def __init__(self):
        documentation = "Set of shapelet functions"
        parameters = {
            'n_max': NonLinearParameter("Maximum order of the Shapelet decomposition",
                               DefinitionRange(min_value=0),
                               latex_str=r"$\n_{\rm max}$", fixed=True),
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
        super().__init__(documentation, parameters)

        
class LensedPS(AnalyticalLightProfile):

    def __init__(self):
        documentation = "Set of lensed point sources"
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
        super().__init__(documentation, parameters)


class Uniform(AnalyticalLightProfile):
    
    def __init__(self):
        documentation = "Uniform sheet of light"
        parameters = {
            'A': LinearParameter("Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$A$"),
        }
        super().__init__(documentation, parameters)


class PixelatedRegularGrid(Profile):

    def __init__(self):
        documentation = "A pixelated profile defined on a regular Cartesian grid"
        self.pixels = PixelatedRegularGridParameter("Pixel values")
        super().__init__(documentation)
