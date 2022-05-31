__author__ = 'aymgal'

from lensmodelapi.api.file import FitsFile
from lensmodelapi.api.base import APIBaseObject


class PSF(APIBaseObject):
    """Defines a Point Spread Function"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 image: FitsFile,
                 pixel_size: float = None,
                 description: str = None) -> None:
        self.image = image
        self.pixel_size = pixel_size
        self.description = description
        super().__init__()
