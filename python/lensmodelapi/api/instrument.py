__author__ = 'aymgal'

from lensmodelapi.api.file import FitsFile
from lensmodelapi.api.base import APIBaseObject


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
