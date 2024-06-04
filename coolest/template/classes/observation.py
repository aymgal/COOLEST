__author__ = 'aymgal'

from typing import Union

from coolest.template.classes.grid import PixelatedRegularGrid
from coolest.template.classes.noise import Noise
from coolest.template.classes.base import APIBaseObject


class Observation(APIBaseObject):
    """Defines the observation itself, that is the image pixels, 
    the exposure time, the noise model and/or properties, the magnitude 
    zero-point and sky brightness.

    Parameters
    ----------
    pixels : PixelatedRegularGrid, optional
        Regular 2D Grid instance for the observed / mock data pixels, by default None
    noise : Noise, optional
        Instance of a Noise object associated with the modeling 
        of the data pixels, by default None
    mag_zero_point : float, optional
        Zero-point magnitude, which corresponds to the 1 electron per second
        hitting the detector (given in mag), by default None
    mag_sky_brightness : float, optional
        Magnitude due to sky brightness (given in mag per arcsec^2), 
        by default None
    """
    
    def __init__(self, 
                 pixels: PixelatedRegularGrid = None,  # can be None for mock generation
                 exposure_time: Union[float, PixelatedRegularGrid] = None,
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
        self.mag_zero_point = mag_zero_point          # magnitude zero-point (corresponds to 1 electron per second on the detector)
        self.mag_sky_brightness = mag_sky_brightness  # sky brightness (magnitude per arcsec^2)
        if noise is None:
            noise = Noise()
        self.noise = noise
        # self.time_delays = time_delays
        # self.magnification_ratios = magnification_ratios
        super().__init__()

    def check_consistency_with_instrument(self, instrument):
        """Checks that the data image is consistent with instrument properties"""
        width  = abs(self.pixels.field_of_view_x[1] - self.pixels.field_of_view_x[0])
        height = abs(self.pixels.field_of_view_y[1] - self.pixels.field_of_view_y[0])
        num_pix_ra = round(width / instrument.pixel_size)
        error_message_ra = f"Number of pixels along x is inconsistent (data: {self.pixels.num_pix_x}, instrument: {num_pix_ra})."
        assert self.pixels.num_pix_x  == num_pix_ra, error_message_ra
        num_pix_dec = round(height / instrument.pixel_size)
        error_message_dec = f"Number of pixels along y is inconsistent (data: {self.pixels.num_pix_y}, instrument: {num_pix_dec})."
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
