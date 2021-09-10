__author__ = 'aymgal'

from astropy.io import fits

from lensmodelapi.base import LensModelAPIObject


class FitsFile(LensModelAPIObject):

    def __init__(self,
                 fits_path: str,
                 pixel_size: float = None,
                 num_pix_ra: int = None,
                 num_pix_dec: int = None,
                 update_with_fits: bool = False) -> None:
        self.fits_path = fits_path
        self.pixel_size = pixel_size
        self.num_pix_ra = num_pix_ra
        self.num_pix_dec = num_pix_dec
        super().__init__()

    def update_with_fits(self):
        array_shape, pixel_size = self.extract_properties()
        if array_shape is not None:
            self.num_pix_ra, self.num_pix_dec = array_shape
        if pixel_size is not None:
            self.pixel_size = pixel_size

    def extract_properties(self):
        pixels, header = self.read(self.fits_path)
        array_shape = pixels.shape
        pixel_size = None  # TODO: extraction of pixel size and other things from the header
        return array_shape, pixel_size

    @staticmethod
    def read(fits_path):
        pixels, header = fits.getdata(fits_path, header=True)
        return pixels, header


class Observation(LensModelAPIObject):

    def __init__(self, 
                 image: FitsFile,
                 psf: FitsFile,
                 update_with_fits: bool = False) -> None:
        self.image = image
        if update_with_fits:
            self.image.update_with_fits()
        self.psf = psf
        if update_with_fits:
            self.psf.update_with_fits()
        super().__init__()
