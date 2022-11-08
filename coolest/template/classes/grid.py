__author__ = 'aymgal'

from typing import Tuple
import numpy as np

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.fits_file import FitsFile


class PixelatedRegularGrid(APIBaseObject):
    
    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: Tuple[float] = [None, None],
                 field_of_view_y: Tuple[float] = [None, None],
                 num_pix_x: int = None,
                 num_pix_y: int = None):
        documentation = "Pixelated light profile on a pixel grid"
        self.fits_file = FitsFile(fits_path)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists:
            array, header = self.fits_file.read()
            array_shape = array.shape
            assert array_shape == (header['NAXIS1'], header['NAXIS2'])
            self.num_pix_x, self.num_pix_y = array_shape
        else:
            self.num_pix_x, self.num_pix_y = num_pix_x, num_pix_y
        super().__init__()

    @property
    def shape(self):
        return (self.num_pix_x, self.num_pix_y)

    @property
    def pixel_size(self):
        return np.abs(self.field_of_view_x[0]- self.field_of_view_x[1])/self.num_pix_x
