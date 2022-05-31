__author__ = 'aymgal'

from lensmodelapi.api.file import FitsFile
from lensmodelapi.api.base import APIBaseObject


class Noise(APIBaseObject):
    """Defines a Point Spread Function"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 background_rms: float = None,
                 with_poisson_noise: bool = True,
                 noise_map: FitsFile = None) -> None:
        self.background_rms = background_rms
        self.with_poisson_noise = with_poisson_noise
        self.noise_map = noise_map
        super().__init__()
