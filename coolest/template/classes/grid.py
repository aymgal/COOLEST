__author__ = 'aymgal'

from typing import Tuple
import numpy as np

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.fits_file import FitsFile



class PixelatedRegularGrid(APIBaseObject):
    
    def __init__(self, 
                 fits_path: str = "",
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix_x: int = 0,
                 num_pix_y: int = 0) -> None:
        self.fits_file = FitsFile(fits_path)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists():
            self.num_pix_x, self.num_pix_y = self.read_pixels()
        else:
            self.num_pix_x, self.num_pix_y = num_pix_x, num_pix_y
        super().__init__()

    @property
    def shape(self):
        return (self.num_pix_x, self.num_pix_y)

    @property
    def pixel_size(self):
        return np.abs(self.field_of_view_x[0] - self.field_of_view_x[1]) / self.num_pix_x

    def set_grid(self, fits_path, 
                 field_of_view_x=(0, 0), field_of_view_y=(0, 0),
                 num_pix_x=0, num_pix_y=0, check_fits_file=True):
        self.fits_file = FitsFile(fits_path, check_exist=check_fits_file)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists():
            self.num_pix_x, self.num_pix_y = self.read_pixels()
            # if number of pixels is also given, check that it is consistent
            if num_pix_x != 0 and self.num_pix_x != num_pix_x:
                raise ValueError("Given number of pixels in x direction "
                                 "is inconsistent with the fits file")
            if num_pix_y != 0 and self.num_pix_y != num_pix_y:
                raise ValueError("Given number of pixels in y direction "
                                 "is inconsistent with the fits file")
        else:
            self.num_pix_x, self.num_pix_y = num_pix_x, num_pix_y

    def read_pixels(self):
        array, header = self.fits_file.read()
        array_shape = array.shape
        if array_shape != (header['NAXIS1'], header['NAXIS2']):
            raise ValueError("Given dimensions do not match the .fits image!")
        return array_shape


class IrregularGrid(APIBaseObject):
    def __init__(self, 
                 fits_path: str = "",
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix: int = 0) -> None:
        self.fits_file = FitsFile(fits_path)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists():
            self.field_of_view_x, self.field_of_view_y, self.num_pix = self.read_pixels()
        else:
            self.field_of_view_x = field_of_view_x
            self.field_of_view_y = field_of_view_y
            self.num_pix = num_pix
        super().__init__()


    def read_pixels(self):
        data, header = self.fits_file.read()
        x = data.field(0)
        y = data.field(1)
        z = data.field(2)
        num_pix = len(z)
        #assert self.num_pix == len(z), "Given number of grid points does not match the number of .fits table rows!"
        if self.field_of_view_x == (0, 0) and self.field_of_view_y == (0, 0):
            # Here we may want to check/report the overlap between the given field of view and the square encompassing the irregular grid
            self.field_of_view_x = (min(x), max(x))
            self.field_of_view_y = (min(y), max(y))
        return field_of_view_x, field_of_view_y, num_pix

    def set_grid(self, fits_path, 
                 field_of_view_x=(0, 0), field_of_view_y=(0, 0),
                 num_pix=0, check_fits_file=True):
        self.fits_file = FitsFile(fits_path, check_exist=check_fits_file)
        if self.fits_file.exists():
            self.field_of_view_x, self.field_of_view_y, self.num_pix = self.read_pixels()
            if num_pix != 0 and self.num_pix != num_pix_x:
                raise ValueError("Given number of pixels is inconsistent with the fits file")
            if field_of_view_x != (0, 0) and field_of_view_x == self.field_of_view_x:
                raise ValueError("Given field of view along x direction is inconsistent with the fits file")
            if field_of_view_y != (0, 0) and field_of_view_y == self.field_of_view_y:
                raise ValueError("Given field of view along y direction is inconsistent with the fits file")

        else:
            self.field_of_view_x = field_of_view_x
            self.field_of_view_y = field_of_view_y
            self.num_pix = num_pix
            
