__author__ = 'aymgal'

from coolest.template.classes.profile import Profile, AnalyticalProfile
from coolest.template.classes.parameter import (NonLinearParameter, 
                                                LinearParameter, 
                                                LinearParameterSet, 
                                                NonLinearParameterSet,
                                                PixelatedRegularGridParameter,
                                                IrregularGridParameter)
from coolest.template.classes.parameter import DefinitionRange


__all__ = [
    'Sersic',
    'Chameleon',
    'Uniform',
    'Shapelets',
    'LensedPS',
    'PixelatedRegularGrid',
    'IrregularGrid',
]
SUPPORTED_CHOICES = __all__


class Sersic(AnalyticalProfile):
    """Surface brightness described by an elliptical Sérsic profile.

    This profile is described by the following parameters:
    
    - 'I_eff': amplitude at the effective radius
    - 'theta_eff': effective radius, a.k.a. Sersic radius, equal to the half-light radius
    - 'n': Sersic index
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
        parameters = {
            'I_eff': LinearParameter("Amplitude at the Sersic radius",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$I_{\rm Sersic}$"),
            'theta_eff': NonLinearParameter("Sersic (half-light) radius",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$R_{\rm Sersic}$"),
            'n': NonLinearParameter("Sersic index",
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
        super().__init__(parameters)


class Chameleon(AnalyticalProfile):
    """Surface brightness described by an elliptical Chameleon profile,
    defined as the difference between two NIE profiles.

    This profile is described by the following parameters:
    
    - 'A': normalization of the profile
    - 's_c': core radius of the innver NIE
    - 's_t': core radius of the outer NIE
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
        parameters = {
            'A': LinearParameter("Normalization of the profile",
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
        super().__init__(parameters)


class Shapelets(AnalyticalProfile):
    """Surface brightness described by a shapelet basis set.
    """
    
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
        super().__init__(parameters)

        
class LensedPS(AnalyticalProfile):
    """Surface brightness of a set of point sources after being lensed. 

    This profile is described by the following parameters:
    
    - 'ra_list': list of coordinates along the x axis
    - 'dec_list': list of coordinates along the y axis
    - 'amps': list of amplitudes
    """

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
        super().__init__(parameters)


class Uniform(AnalyticalProfile):
    """Uniform surface brightness profile.

    This profile is described by the following parameters:
    
    - 'A': amplitude
    """
    
    def __init__(self):
        documentation = "Uniform sheet of light"
        parameters = {
            'A': LinearParameter("Central amplitude",
                            DefinitionRange(min_value=0.0),
                            latex_str=r"$A$"),
        }
        super().__init__(parameters)


class PixelatedRegularGrid(Profile):
    """Surface brightness described on a regular grid of pixels.

    This profile is described by the following parameters:
    
    - 'pixels': 2D array of pixel values
    """

    def __init__(self):
        parameters = {
            'pixels': PixelatedRegularGridParameter("Pixel values")
        }
        super().__init__(parameters)


class IrregularGrid(Profile):
    """Surface brightness described on an irregular grid of pixels.

    This profile is described by the following parameters:
    
    - 'pixels': set of 2D coordinates and associated pixel values (x, y, z)
    """

    def __init__(self):
        parameters = {
            'pixels': IrregularGridParameter("Pixel positions and values")
        }
        super().__init__(parameters)
