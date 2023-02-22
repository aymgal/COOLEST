__author__ = 'aymgal'

from typing import Tuple
import numpy as np

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.fits_file import FitsFile


__all__ = [
    'Grid',
    'PixelatedRegularGrid',
    'IrregularGrid',
]

SUPPORTED_CHOICES = [
    'PixelatedRegularGrid',
    'IrregularGrid',
]


class Grid(APIBaseObject):

    def __init__(self,
                 fits_path: str,
                 check_fits_file: bool = False, 
                 fits_file_dir: str = None) -> None:
        self.fits_file = FitsFile(fits_path, 
                                  check_exist=check_fits_file, 
                                  directory=fits_file_dir)
        super().__init__()

    def set_grid(self, fits_path, check_fits_file):
        if fits_path is not None:
            self.fits_file = FitsFile(fits_path, check_exist=check_fits_file)


class PixelatedRegularGrid(Grid):
    
    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix_x: int = 0, num_pix_y: int = 0,
                 **kwargs_grid) -> None:
        super().__init__(fits_path, **kwargs_grid)
        self.set_grid(None, field_of_view_x, field_of_view_y, 
                      num_pix_x, num_pix_y)

    @property
    def shape(self):
        return (self.num_pix_x, self.num_pix_y)

    @property
    def pixel_size(self):
        if self.num_pix_x == 0 or self.num_pix_y == 0:
            return 0.
        pix_size_x = np.abs(self.field_of_view_x[0] - self.field_of_view_x[1]) / self.num_pix_x
        pix_size_y = np.abs(self.field_of_view_y[0] - self.field_of_view_y[1]) / self.num_pix_y
        assert pix_size_x == pix_size_y, "Regular grid must have square pixels"
        return pix_size_x

    def set_grid(self, fits_path, 
                 field_of_view_x, field_of_view_y,
                 num_pix_x=0, num_pix_y=0,
                 check_fits_file=True):
        super().set_grid(fits_path, check_fits_file)
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


class IrregularGrid(Grid):
    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix: int = 0,
                 **kwargs_grid) -> None:
        super().__init__(fits_path, **kwargs_grid)
        self.set_grid(None, 
                      field_of_view_x=field_of_view_x, 
                      field_of_view_y=field_of_view_y, 
                      num_pix=num_pix)

    def read_pixels(self):
        data, header = self.fits_file.read()
        x = data.field(0)
        y = data.field(1)
        z = data.field(2)
        num_pix = len(z)
        #assert self.num_pix == len(z), "Given number of grid points does not match the number of .fits table rows!"
        # Here we may want to check/report the overlap between the given field of view and the square encompassing the irregular grid
        field_of_view_x = (min(x), max(x))
        field_of_view_y = (min(y), max(y))
        return field_of_view_x, field_of_view_y, num_pix

    def set_grid(self, fits_path, 
                 field_of_view_x=(0, 0), field_of_view_y=(0, 0),
                 num_pix=0, check_fits_file=True):
        super().set_grid(fits_path, check_fits_file)
        if self.fits_file.exists():
            self.field_of_view_x, self.field_of_view_y, self.num_pix = self.read_pixels()
            if num_pix != 0 and self.num_pix != num_pix:
                raise ValueError("Given number of pixels is inconsistent with the fits file")
            if field_of_view_x != (0, 0) and field_of_view_x == self.field_of_view_x:
                raise ValueError("Given field of view along x direction is inconsistent with the fits file")
            if field_of_view_y != (0, 0) and field_of_view_y == self.field_of_view_y:
                raise ValueError("Given field of view along y direction is inconsistent with the fits file")

        else:
            self.field_of_view_x = field_of_view_x
            self.field_of_view_y = field_of_view_y
            self.num_pix = num_pix
            
