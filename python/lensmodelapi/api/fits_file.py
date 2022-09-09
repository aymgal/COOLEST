__author__ = 'aymgal'

import os
from astropy.io import fits

from lensmodelapi.api.base import APIBaseObject



class FitsFile(APIBaseObject):
    """A .fits file object"""
    def __init__(self, fits_path: str = None) -> None:
        self.fits_path = fits_path
        super().__init__()

    @property
    def exists(self):
        return self.fits_path is not None and os.path.exists(self.fits_path)

    def read(self):
        return fits.getdata(self.fits_path, header=True)


class PixelFitsFile(FitsFile):
    """A .fits file object holding a 2D image"""
    def __init__(self,
                 fits_path: str = None,
                 pixel_size: float = None) -> None:
        super().__init__(fits_path)
        self.pixel_size = pixel_size
        if self.exists:
            pixels, header = self.read()
            array_shape = pixels.shape
            assert array_shape == (header['NAXIS1'], header['NAXIS2'])
            self.num_pix_x, self.num_pix_y = array_shape
        else:
            self.num_pix_x, self.num_pix_y = None, None

    @property
    def shape(self):
        return (self.num_pix_x, self.num_pix_y)


class MultiExtFitsFile(FitsFile):
    """A multi-extension .fits file object"""
    def __init__(self,
                 fits_path: str = None) -> None:
        super().__init__(fits_path)
