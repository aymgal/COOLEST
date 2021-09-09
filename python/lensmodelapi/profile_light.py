# Single light profile

from lensmodelapi.profile_base import LightProfile
from lensmodelapi.parameter import (ParameterList,
                                    NonLinearParameter, 
                                    LinearParameter, 
                                    LinearParameterSet)


__all__ = ['SersicElliptical', 'PixelatedRegularGrid']
SUPPORTED_PROFILES = __all__


class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = 'light'


class SersicElliptical(LightProfile):
    
    def __init__(self):
        name = 'sersic_elliptical'
        description = "Elliptical Sersic"
        parameters = ParameterList([
            LinearParameter('A',
                            "Amplitude at origin",
                            min_value=0.0,
                            latex_name=r"$A$"),
            NonLinearParameter('R_sersic',
                               "Sersic radius",
                               min_value=0.0,
                               latex_name=r"$R_{\rm Sersic}$"),
            NonLinearParameter('n_sersic',
                               "Sersic index",
                               min_value=0.5,
                               max_value=10.0,
                               latex_name=r"$n_{\rm Sersic}$"),
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
        super(name, description, parameters)


class Uniform(LightProfile):
    
    def __init__(self):
        name = 'uniform'
        description = "Uniform sheet of light"
        parameters = ParameterList([
            LinearParameter('A',
                            "Central amplitude",
                            min_value=0.0,
                            latex_name=r"$A$"),
        ])
        super(name, description, parameters)


class PixelatedRegularGrid(LightProfile):
    
    def __init__(self, num_pixels):
        name = 'pixelated_regular'
        description = "Pixelated light profile on a grid pixel grid"
        parameters = ParameterList([
            LinearParameterSet('pixels',
                               "Set of pixel values",
                               num_pixels,
                               min_value=0.0,
                               latex_name=r"{\rm pixels}"),
        ])
        super(name, description, parameters)
