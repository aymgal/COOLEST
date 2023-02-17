__author__ = 'aymgal'

from coolest.template.classes.grid import PixelatedRegularGrid
from coolest.template.classes.base import APIBaseObject


__all__ = [
    'PSF',
    'PixelatedPSF',
    'GaussianPSF',
]

SUPPORTED_CHOICES = __all__


class PSF(APIBaseObject):
    """Defines a Point Spread Function"""
    def __init__(self,
                 psf_type: str,
                 description: str = None,
                 **kwargs) -> None:
        self.type = psf_type
        self.description = description
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class PixelatedPSF(PSF):

    def __init__(self, description: str = None, pixels: PixelatedRegularGrid = None) -> None:
        psf_type = self.__class__.__name__
        super().__init__(psf_type, description=description, pixels=pixels)


class GaussianPSF(PSF):

    def __init__(self, description: str = None, std_dev: float = 0.0) -> None:
        """
        std_dev will be interpreted as having units of the Instrument pixel size.
        Otherwise it can be describe in the description attribute of the PSF.
        """
        psf_type = self.__class__.__name__
        super().__init__(psf_type, description=description, std_dev=std_dev)
