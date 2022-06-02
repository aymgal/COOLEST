__author__ = 'aymgal'

from lensmodelapi.api.fits_file import PixelFitsFile
from lensmodelapi.api.base import APIBaseObject


class PSF(APIBaseObject):
    """Defines a Point Spread Function"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 image: PixelFitsFile,
                 description: str = None) -> None:
        self.image = image
        self.description = description
        super().__init__()
