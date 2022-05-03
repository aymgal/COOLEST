__author__ = 'aymgal'

from astropy.io import fits

from lensmodelapi.api.base import APIBaseObject


class FitsFile(APIBaseObject):
    """A simple FITS file"""
    def __init__(self,
                 fits_path: str) -> None:
        self.fits_path = fits_path
        pixels, header = self.read()
        array_shape = pixels.shape
        assert array_shape == (header['NAXIS1'], header['NAXIS2'])
        self.num_pix_ra, self.num_pix_dec = array_shape
        super().__init__()

    def read(self):
        return fits.getdata(self.fits_path, header=True)
