# container for data-related things


class Data(object):

    def __init__(self, 
                 data_fits_path: str,
                 psf_fits_path: str,
                 data_pixel_size: float,
                 psf_pixel_size: float = None) -> None:
        self.data_fits_path = data_fits_path
        self.psf_fits_path = psf_fits_path
        self.data_pixel_size = data_pixel_size
        if psf_pixel_size is None:
            psf_pixel_size = data_pixel_size
        self.psf_pixel_size = psf_pixel_size
