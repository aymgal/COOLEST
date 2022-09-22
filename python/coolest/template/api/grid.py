__author__ = 'aymgal'

from coolest.template.api.base import APIBaseObject
from coolest.template.api.fits_file import FitsFile


class PixelatedRegularGrid(APIBaseObject):
    
    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: float = None,
                 field_of_view_y: float = None):
        documentation = "Pixelated light profile on a pixel grid"
        self.fits_file = FitsFile(fits_path)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists:
            data, header = self.fits_file.read()
            array_shape = array.shape
            assert array_shape == (header['NAXIS1'], header['NAXIS2'])
            self.num_pix_x, self.num_pix_y = array_shape
        else:
            self.num_pix_x, self.num_pix_y = None, None
        super().__init__()

    @property
    def shape(self):
        return (self.num_pix_x, self.num_pix_y)

    @property
    def pixel_size(self):
        return self.field_of_view_x / (num_pix_x + 1)
