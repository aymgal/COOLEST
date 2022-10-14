__author__ = 'aymgal'

from astropy.io import fits
import numpy as np
from typing import Tuple

from coolest.template.api.grid import PixelatedRegularGrid
from coolest.template.api.noise import Noise
from coolest.template.api.base import APIBaseObject


class Observation(APIBaseObject):
    """Defines a data image, as a simple FITS file"""
    def __init__(self, 
                 pixels: PixelatedRegularGrid = None,  # can be None for mock generation
                 exposure_time: float = None,
                 noise: Noise = None,
                 mag_zero_point: float = None,
                 mag_sky_brightness: float = None,
                 # time_delays: list = None,
                 # magnification_ratios: list = None
                 ) -> None:
        if pixels is None:
            pixels = PixelatedRegularGrid()
        self.pixels = pixels
        self.exposure_time = exposure_time
        self.mag_zero_point = mag_zero_point          # magnitude zero-point (corresponds to 1 count per second on the detector)
        self.mag_sky_brightness = mag_sky_brightness  # sky brightness (magnitude per arcsec^2)
        self.noise = noise
        # self.time_delays = time_delays
        # self.magnification_ratios = magnification_ratios
        super().__init__()

    def check_consistency_with_instrument(self, instrument):
        """Checks that the data image is consistent with instrument properties"""
        width  = abs(self.pixels.field_of_view_x[1]  - self.pixels.field_of_view_x[0])
        height = abs(self.pixels.field_of_view_y[1] - self.pixels.field_of_view_y[0])
        num_pix_ra = int(width / instrument.pixel_size)
        error_message_ra = f"Field-of-view along RA is inconsistent (data: {self.pixels.num_pix_x}, instrument: {num_pix_ra})."
        assert self.pixels.num_pix_x  == num_pix_ra, error_message_ra
        num_pix_dec = int(height / instrument.pixel_size)
        error_message_dec = f"Field-of-view along Dec is inconsistent (data: {self.pixels.num_pix_y}, instrument: {num_pix_dec})."
        assert self.pixels.num_pix_y  == num_pix_dec, error_message_dec
        # TODO: check pixel size value?

    # def set_default_field_of_view(self, instrument):
    #     if not self.pixels.exists:
    #         return
    #     pixel_size = self.pixels.pixel_size
    #     num_pix_x, num_pix_y = self.pixels.shape
    #     self.field_of_view  = ( num_pix_x*pixel_size/2, -num_pix_x*pixel_size/2)  # RA is opposite to x
    #     self.field_of_view_dec = (-num_pix_y*pixel_size/2,  num_pix_y*pixel_size/2)

    # def _check_images(self):
    #     self._check_positive(self.wht_map, "WHT map")
    #     self._check_binary(self.arc_mask, "Arc mask")
    #     self._check_binary(self.likelihood_mask, "Likelihood mask")

    # @staticmethod
    # def _check_positive(fits_file, fits_name):
    #     if not fits_file.exists:
    #         return
    #     pixels, _ = fits_file.read()
    #     if not np.all(pixels > 0):
    #         raise ValueError(f"{fits_name} pixels should all be positive.")

    # @staticmethod
    # def _check_binary(fits_file, fits_name):
    #     if not fits_file.exists:
    #         return
    #     pixels, _ = fits_file.read()
    #     if not np.array_equal(pixels, pixels.astype(bool)):
    #         raise ValueError(f"{fits_name} pixels should be either 0 or 1.")
