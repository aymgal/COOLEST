__author__ = 'aymgal'

from coolest.template.api.fits_file import PixelFitsFile
from coolest.template.api.base import APIBaseObject


class PSF(APIBaseObject):
    """Defines a Point Spread Function"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
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

    def __init__(self, image: PixelFitsFile) -> None:
        psf_type = self.__class__.__name__
        super().__init__(psf_type, image=image)


class GaussianPSF(PSF):

    def __init__(self, std_dev) -> None:
        """
        std_dev will be interpreted as having units of the Instrument pixel size.
        Otherwise it can be describe in the description attribute of the PSF.
        """
        psf_type = self.__class__.__name__
        super().__init__(psf_type, std_dev=std_dev)
