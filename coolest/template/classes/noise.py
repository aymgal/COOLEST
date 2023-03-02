__author__ = 'aymgal'

from coolest.template.classes.grid import PixelatedRegularGrid
from coolest.template.classes.base import APIBaseObject


__all__ = [
    'Noise',
    'UniformGaussianNoise',
    'NoiseMap',
    'NoiseRealization',
    'InstrumentalNoise',
    'DrizzledNoise',
]

SUPPORTED_CHOICES = [
    'UniformGaussianNoise',
    'NoiseMap',
    'NoiseRealization',
    'InstrumentalNoise',
    'DrizzledNoise'
]


class Noise(APIBaseObject):
    """
    Generic class for characterizing the noise of an Observation
    All supported noise types correspond to the classes below
    """

    def __init__(self, ntype: str = None, **kwargs) -> None:
        self.type = ntype
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


 # types:
 #      - NoiseMap w description
 #      - NoiseRealization w description
 #      - UniformGaussian
 #      - IntrumentalUniformGaussian


class UniformGaussianNoise(Noise):
    """Uniform gaussian noise given a standard deviation, with 0 mean"""

    def __init__(self, std_dev: float = 0.) -> None:
        ntype = self.__class__.__name__
        super().__init__(ntype, std_dev=std_dev)

class NoiseMap(Noise):
    """Noise characterized by a noise map, which contains diagonal elements of the data covariance matrix"""

    def __init__(self, noise_map: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if noise_map is None:
            noise_map = PixelatedRegularGrid()
        super().__init__(ntype, noise_map=noise_map)

class NoiseRealization(Noise):
    """Fixed realization of the noise"""

    def __init__(self, noise_realization: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if noise_realization is None:
            noise_realization = PixelatedRegularGrid()
        super().__init__(ntype, noise_realization=noise_realization)

class InstrumentalNoise(Noise):
    """
    The noise properties will be computed directly based 
    on the Instrument (i.e. readout noise) and Observation (e.g. exposure time, sky brightness, etc.)
    """

    def __init__(self, 
                 with_readout_noise: bool = True, 
                 with_sky_shot_noise: bool = True,
                 with_target_shot_noise: bool = True) -> None:
        ntype = self.__class__.__name__
        super().__init__(ntype, 
                         with_readout_noise=with_readout_noise,
                         with_sky_shot_noise=with_sky_shot_noise,
                         with_target_shot_noise=with_target_shot_noise)

class DrizzledNoise(Noise):
    """Provide an exposure map (.wht extension) as output by e.g. astrodrizzle, typically for HST images"""

    def __init__(self, background_rms: float = 0.0, 
                 wht_map: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if wht_map is None:
            wht_map = PixelatedRegularGrid()
        super().__init__(ntype, background_rms=background_rms, wht_map=wht_map)
