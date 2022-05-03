__author__ = 'aymgal'

from astropy.io import fits
import numpy as np

from lensmodelapi.api.file import FitsFile
from lensmodelapi.api.base import APIBaseObject


class Data(APIBaseObject):
    """Defines a data image, as a simple FITS file"""
    def __init__(self, 
                 image: FitsFile, 
                 noise_map: FitsFile = None,
                 wht_map: FitsFile = None,
                 arc_mask: FitsFile = None,
                 likelihood_mask: FitsFile = None,
                 time_delays: list = None,
                 magnification_ratios: list = None) -> None:
        self.image = image
        self.noise_map = noise_map
        self.wht_map = wht_map
        self.arc_mask = arc_mask
        self.likelihood_mask = likelihood_mask
        self._check_images()
        self.time_delays = time_delays
        self.magnification_ratios = magnification_ratios
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

    def _check_images(self):
        self._check_positive(self.wht_map, "WHT map")
        self._check_binary(self.arc_mask, "Arc mask")
        self._check_binary(self.likelihood_mask, "Likelihood mask")

    @staticmethod
    def _check_positive(fits_file, fits_name):
        if fits_file is None:
            return
        pixels, _ = fits_file.read()
        if not np.all(pixels > 0):
            raise ValueError(f"{fits_name} pixels should all be positive.")

    @staticmethod
    def _check_binary(fits_file, fits_name):
        if fits_file is None:
            return
        pixels, _ = fits_file.read()
        if not np.array_equal(pixels, pixels.astype(bool)):
            raise ValueError(f"{fits_name} pixels should be either 0 or 1.")
