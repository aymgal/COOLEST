__author__ = 'aymgal'

from coolest.template.api.psf import PSF
from coolest.template.api.base import APIBaseObject


class Instrument(APIBaseObject):
    """Defines an Instrument (detector + PSF) setup"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 name: str,
                 band: str,
                 pixel_size: float, 
                 readout: float = None,
                 psf: PSF = None) -> None:
        self.name = name
        self.band = band
        self.pixel_size = pixel_size
        self.readout = readout
        self.psf = psf
        super().__init__()
