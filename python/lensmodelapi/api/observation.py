__author__ = 'aymgal'

from astropy.io import fits
import numpy as np

from lensmodelapi.api.fits_file import FitsFile
from lensmodelapi.api.noise import Noise
from lensmodelapi.api.base import APIBaseObject


class Observation(APIBaseObject):
    """Defines a data image, as a simple FITS file"""
    def __init__(self, 

                 image: FitsFile = None,  # can be None for mock generation
                 field_of_view_ra: float = None,
                 field_of_view_dec: float = None,

                 exposure_time: float = None,
                 wht_map: FitsFile = None,

                 noise: Noise = None,

                 mag_zero_point: float = None,
                 mag_sky_brightness: float = None,

                 arc_mask: FitsFile = None,
                 likelihood_mask: FitsFile = None,
                 
                 time_delays: list = None,
                 magnification_ratios: list = None) -> None:
        if image is None:
            image = FitsFile(None)
        if wht_map is None:
            wht_map = FitsFile(None)
        if arc_mask is None:
            arc_mask = FitsFile(None)
        if likelihood_mask is None:
            likelihood_mask = FitsFile(None)
        self.image = image
        self.field_of_view_ra = field_of_view_ra
        self.field_of_view_dec = field_of_view_dec
        self.exposure_time = exposure_time
        self.mag_zero_point = mag_zero_point          # magnitude zero-point (corresponds to 1 count per second on the detector)
        self.mag_sky_brightness = mag_sky_brightness  # sky brightness (magnitude per arcsec^2)
        self.noise = noise
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

    def update_fov_with_instrument(self, instrument):
        if self.image.exists:
            num_pix_x, num_pix_y = self.image.shape
            self.field_of_view_ra  = instrument.pixel_size * num_pix_x
            self.field_of_view_dec = instrument.pixel_size * num_pix_y

    def _check_images(self):
        self._check_positive(self.wht_map, "WHT map")
        self._check_binary(self.arc_mask, "Arc mask")
        self._check_binary(self.likelihood_mask, "Likelihood mask")

    @staticmethod
    def _check_positive(fits_file, fits_name):
        if not fits_file.exists:
            return
        pixels, _ = fits_file.read()
        if not np.all(pixels > 0):
            raise ValueError(f"{fits_name} pixels should all be positive.")

    @staticmethod
    def _check_binary(fits_file, fits_name):
        if not fits_file.exists:
            return
        pixels, _ = fits_file.read()
        if not np.array_equal(pixels, pixels.astype(bool)):
            raise ValueError(f"{fits_name} pixels should be either 0 or 1.")
