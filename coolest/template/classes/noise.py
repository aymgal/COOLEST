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

SUPPORTED_CHOICES = list(set(__all__) - {'Noise'})


class Noise(APIBaseObject):
    """Generic class for characterizing the noise of an Observation.
    Supported noise types correspond to the specific classes defined in this module.

    Parameters
    ----------
    ntype : str, optional
        Noise type, as the name of the corresponding class, by default None
    """
    
    def __init__(self, ntype: str = None, **kwargs) -> None:
        self.type = ntype
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class UniformGaussianNoise(Noise):
    """Uniform gaussian noise given a standard deviation and zero mean.

    Parameters
    ----------
    std_dev : float, optional
        Standard deviation (RMS value, since mean = 0), by default 0.
    """
    
    def __init__(self, std_dev: float = 0.) -> None:
        ntype = self.__class__.__name__
        super().__init__(ntype, std_dev=std_dev)


class NoiseMap(Noise):
    """Noise characterized by a noise map, which contains diagonal elements of the data covariance matrix.

    Parameters
    ----------
    noise_map : PixelatedRegularGrid, optional
        Regular 2D Grid instance for the standard deviation of the noise per pixel, by default None
    """

    def __init__(self, noise_map: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if noise_map is None:
            noise_map = PixelatedRegularGrid()
        super().__init__(ntype, noise_map=noise_map)


class NoiseRealization(Noise):
    """A single realization of the noise.

    Parameters
    ----------
    noise_realization : PixelatedRegularGrid, optional
        Regular 2D Grid instance for the noise value per pixel, by default None
    """
    
    def __init__(self, noise_realization: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if noise_realization is None:
            noise_realization = PixelatedRegularGrid()
        super().__init__(ntype, noise_realization=noise_realization)


class InstrumentalNoise(Noise):
    """Noise properties are computed directly based on the observed 
    or modeled flux, and on the Instrument (e.g., readout noise) and 
    Observation (e.g., exposure time, sky brightness, etc.) properties.

    Parameters
    ----------
    with_readout_noise : bool, optional
        If True, the noise includes readout noise from the detector, by default True
    with_sky_shot_noise : bool, optional
        If True, the noise includes shot noise from sky background flux 
        (as the Gaussian approximation of the Poisson noise), by default True
    with_target_shot_noise : bool, optional
        If True, the noise includes shot noise from the target flux 
        (as the Gaussian approximation of the Poisson noise), by default True
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
    """Provide an exposure map as output by e.g., astrodrizzle with HST images (typically with '_wht' prefix).

    Parameters
    ----------
    background_rms : float, optional
        Noise standard deviation (RMS value, since mean = 0), by default 0.0
    wht_map : PixelatedRegularGrid, optional
        Regular 2D Grid instance for the effective exposure time per pixel, by default None
    """

    def __init__(self, background_rms: float = 0.0, 
                 wht_map: PixelatedRegularGrid = None) -> None:
        ntype = self.__class__.__name__
        if wht_map is None:
            wht_map = PixelatedRegularGrid()
        super().__init__(ntype, background_rms=background_rms, wht_map=wht_map)
