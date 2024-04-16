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
    'ConvergenceSheet', 
    'PixelatedRegularGridPotential',
]
SUPPORTED_CHOICES = __all__


class SIE(AnalyticalProfile):
    """Singular isothermal ellipsoidal profile.

    This profile is described by the following parameters:

    - 'theta_E': Einstein radius
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate

    """
    
    def __init__(self):
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
        super().__init__(parameters)


class NIE(AnalyticalProfile):
    """Non-singular isothermal ellipsoidal profile.

    This profile is described by the following parameters:

    - 'theta_E': Einstein radius
    - 'r_core: core radius
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate

    """
    
    def __init__(self):
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
        super().__init__(parameters)


class PEMD(AnalyticalProfile):
    """Power-law elliptical mass density profile, 
    also called the Elliptical Power-law profile (EPL).

    This profile is described by the following parameters:

    - 'gamma': logarithmic radial slope
    - 'theta_E': Einstein radius
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
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
        super().__init__(parameters)


class SPEMD(AnalyticalProfile):
    """Softened power-law elliptical mass density profile.

    This profile is described by the following parameters:

    - 'gamma': negative logarithmic radial slope
    - 'theta_E': Einstein radius
    - 'r_core': core radius
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
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
        super().__init__(parameters)


class NFW(AnalyticalProfile):
    """Navarro-Frenk-White mass profile.

    This profile is described by the following parameters:

    - 'r_s': transition radis from logarithmic radial slope -1 to -3 
    - 'rho_c': characteristic mass density
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
        parameters = {
            'r_s': NonLinearParameter("Radius at which the mass density profile slope transitions from -1 to -3",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$r_{\rm s}$"),
            'rho_c': NonLinearParameter("Characteristic mass density",
                               DefinitionRange(min_value=0.0),
                               latex_str=r"$\rho_c$"),
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
    """'Chameleon' mass profile defined as the difference between 
    two concentric NIE profiles.

    This profile is described by the following parameters:
    
    - 'b': normalization of the profile
    - 's_c': core radius of the innver NIE
    - 's_t': core radius of the outer NIE
    - 'q': axis ratio (semi-major axis / semi-minor axis)
    - 'phi': position angle
    - 'center_x': position along the x coordinate
    - 'center_y': position along the y coordinate
    """
    
    def __init__(self):
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
        super().__init__(parameters)


class ExternalShear(AnalyticalProfile):
    """External shear defined with a strength and orientation.
    The 'origin' of the external shear is by convention fixed to coordinates (0, 0).
    
    This profile is described by the following parameters:

    - 'gamma_ext': strength of the shear field
    - 'phi_ext': orientation of the shear field
    """
    
    def __init__(self):
        parameters = {
            'gamma_ext': NonLinearParameter("Strength of external shear",
                               DefinitionRange(min_value=0., max_value=1.0),
                               latex_str=r"$\gamma_{\rm ext}$"),
            'phi_ext': NonLinearParameter("Orientation of external shear",
                               DefinitionRange(min_value=-90., max_value=90.),
                               latex_str=r"$\phi_{\rm ext}$"),
        }
        super().__init__(parameters)


class ConvergenceSheet(AnalyticalProfile):
    """Convergence 'sheet', infinite and uniform mass density profile.
    The 'origin' of the convergence sheet is by convention fixed to coordinates (0, 0).
    The sheet is allowed to be negative, e.g. can describe an arbitrary 
    mass-sheet transformation.
    
    This profile is described by the following parameters:

    - 'kappa_s': convergence of the uniform mass density sheet
    """
    
    def __init__(self):
        parameters = {
            'kappa_s': NonLinearParameter(
                "Convergence value of the uniform mass density sheet",
                DefinitionRange(min_value=-1e8, max_value=1e8),
                latex_str=r"$\kappa_{\rm s}$"
            ),
        }
        super().__init__(parameters)


class PixelatedRegularGridPotential(Profile):
    """Lens potential defined on a grid of regular pixels.

    This profile is described by the following parameters:

    - 'pixels': 2D array of pixel values
    """

    def __init__(self):
        parameters = {
            'pixels': PixelatedRegularGridParameter("Pixel values")
        }
        super().__init__(parameters)
