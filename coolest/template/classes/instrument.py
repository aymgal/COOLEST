__author__ = 'aymgal'

from coolest.template.classes.psf import PSF
from coolest.template.classes.base import APIBaseObject


class Instrument(APIBaseObject):
    """Defines an Instrument (detector + PSF) setup"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 name: str,
                 band: str,
                 pixel_size: float, 
                 readout_noise: float = None,
                 psf: PSF = None) -> None:
        self.name = name
        self.band = band
        self.pixel_size = pixel_size
        self.readout_noise = readout_noise
        self.psf = psf
        super().__init__()
