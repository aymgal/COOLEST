__author__ = 'aymgal'

from astropy.io import fits
import numpy as np

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


class Instrument(APIBaseObject):
    """Defines an telescope+camera setup"""
    # TODO: support for general pixel shape (using pixel to angle matrix)
    def __init__(self,
                 name: str,
                 psf: FitsFile,
                 pixel_size: float, 
                 field_of_view_ra: float = None,
                 field_of_view_dec: float = None,
                 background_rms: float = None,
                 exposure_time: float = None,
                 psf_pixel_size: float = None) -> None:
        self.name = name
        self.psf = psf
        self.pixel_size = pixel_size
        self.field_of_view_ra = field_of_view_ra
        self.field_of_view_dec = field_of_view_dec
        self.background_rms = background_rms
        self.exposure_time = exposure_time
        if psf_pixel_size is None:
            self.psf_pixel_size = pixel_size
        super().__init__()

    def set_background_rms(self, sigma_bkg):
        self.background_rms = sigma_bkg

    def update_fov_with_data(self, data):
        self.field_of_view_ra = self.pixel_size * data.image.num_pix_ra
        self.field_of_view_dec = self.pixel_size * data.image.num_pix_dec


class Data(APIBaseObject):
    """Defines a data image, as a simple FITS file"""
    def __init__(self, 
                 image: FitsFile, 
                 noise_map: FitsFile = None,
                 wht_map: FitsFile = None) -> None:
        self.image = image
        self.noise_map = noise_map
        self.wht_map = wht_map
        super().__init__()

    def check_consistency_with_instrument(self, instrument):
        """Checks that the data image is consistent with instrument properties"""
        num_pix_ra = int(instrument.field_of_view_ra / instrument.pixel_size)
        error_ra = f"Field-of-view along RA is inconsistent (data: {self.image.num_pix_ra}, instrument: {num_pix_ra})."
        assert self.image.num_pix_ra  == num_pix_ra, error_ra
        num_pix_dec = int(instrument.field_of_view_dec / instrument.pixel_size)
        error_dec = f"Field-of-view along Dec is inconsistent (data: {self.image.num_pix_dec}, instrument: {num_pix_dec})."
        assert self.image.num_pix_dec  == num_pix_dec, error_dec
        # TODO: check pixel size value?

    def estimate_background_noise(self):
        # TODO: this is a VERY crude estimation
        pixels, _ = self.image.read()
        sigma_bkg = np.median(np.abs(pixels - np.median(pixels)))
        return float(sigma_bkg)
