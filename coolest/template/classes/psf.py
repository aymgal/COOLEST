__author__ = 'aymgal'

from coolest.template.classes.grid import PixelatedRegularGrid
from coolest.template.classes.base import APIBaseObject


__all__ = [
    'PSF',
    'PixelatedPSF',
    'GaussianPSF',
]

SUPPORTED_CHOICES = list(set(__all__) - {'PSF'})

#TODO: add support for a Moffat PSF


class PSF(APIBaseObject):
    """Defines the model of the Point Spread Function (PSF) of the instrument.

    Parameters
    ----------
    psf_type : str
        Type of PSF model, as the names of the classes defined in this module.
    description : str, optional
        Any details regarding the way the PSF has been estimated, by default None
    **kwargs : dict, optional
        All the other attributes of the specific PSF model.
    """

    def __init__(self,
                 psf_type: str = None,
                 description: str = None,
                 **kwargs) -> None:
        self.type = psf_type
        self.description = description
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class PixelatedPSF(PSF):
    """PSF modeled as a 2D image.

    Parameters
    ----------
    pixels : PixelatedRegularGrid, optional
        Grid class that holds pixel values and the extent of 
        the PSF kernel, by default None
    description : str, optional
        Any details regarding the way the PSF has been estimated, by default None
    """

    def __init__(self, pixels: PixelatedRegularGrid = None, 
                 description: str = None) -> None:
        psf_type = self.__class__.__name__
        if pixels is None:
            pixels = PixelatedRegularGrid()
        super().__init__(psf_type, description=description, pixels=pixels)


class GaussianPSF(PSF):
    """PSF modeled as a 2D image.

    Parameters
    ----------
    fwhm : float, optional
        Full width at half maximum, in units of the Instrument pixel size, 
        by default 0.0
    description : str, optional
        Any details regarding the way the PSF has been estimated, by default None
    """

    def __init__(self, fwhm: float = 0.0, 
                 description: str = None) -> None:
        psf_type = self.__class__.__name__
        super().__init__(psf_type, description=description, fwhm=fwhm)
