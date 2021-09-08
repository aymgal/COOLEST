# Single light profile

from lensmodelapi.parameter import NonLinearParameter, LinearParameter, LinearParameterSet


__all__ = ['SersicElliptical', 'PixelatedRegularGrid']
SUPPORTED_PROFILES = __all__


class _LightProfileBase(object):

    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def num_params(self):
        count = 0
        for p in self.parameters:
            if isinstance(p, (NonLinearParameter, LinearParameter)):
                count += 1
            elif isinstance(p, LinearParameterSet):
                count += p.num_values
        return count


class SersicElliptical(_LightProfileBase):
    
    def __init__(self):
        name = 'sersic_ell'
        description = "Elliptical Sersic"
        parameters = [
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
        ]
        super(name, description, parameters)


class Uniform(_LightProfileBase):
    
    def __init__(self):
        name = 'uniform'
        description = "Uniform sheet of light"
        parameters = [
            LinearParameter('A',
                            "Amplitude at origin",
                            min_value=0.0,
                            latex_name=r"$A$"),
        ]
        super(name, description, parameters)


class PixelatedRegularGrid(_LightProfileBase):
    
    def __init__(self, num_pixels):
        name = 'pixelated_regular'
        description = "Pixelated light profile on a grid pixel grid"
        parameters = [
            LinearParameterSet('pixels',
                               "Set of pixel values",
                               num_pixels,
                               min_value=0.0,
                               latex_name=r"{\rm pixels}"),
        ]
        super(name, description, parameters)
