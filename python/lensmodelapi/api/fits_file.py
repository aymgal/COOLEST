__author__ = 'aymgal'

import os
from astropy.io import fits

from lensmodelapi.api.base import APIBaseObject


class FitsFile(APIBaseObject):
    """A simple FITS file"""
    def __init__(self,
                 fits_path: str) -> None:
        self.fits_path = fits_path
        if self.exists:
            pixels, header = self.read()
            array_shape = pixels.shape
            assert array_shape == (header['NAXIS1'], header['NAXIS2'])
            self._array_shape = array_shape
        else:
            self._array_shape = (None, None)
        # self.num_pix_x, self.num_pix_y = self.image.shape
        super().__init__()

    @property
    def exists(self):
        return self.fits_path is not None and os.path.exists(self.fits_path)

    @property
    def shape(self):
        return self._array_shape
    
    def read(self):
        return fits.getdata(self.fits_path, header=True)
