__author__ = 'aymgal', 'gvernard'

from typing import Tuple
import numpy as np
import warnings

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
    """Generic class that represents a grid of coordinates and values.

    Parameters
    ----------
    fits_path : str
        Path to the FITS file in which the values (and perhaps the coordinates)
        are stored. If meant to be stored within a COOLEST template file, 
        this should just be the name of the FITS file, placed 
        in the same directory as the template.
    check_fits_file : bool, optional
        If True, creating the object will check that the FITS file exists, by default False
    fits_file_dir : str, optional
        Absolute path of the directory containing the FITS file, by default None
    """

    def __init__(self,
                 fits_path: str,
                 check_fits_file: bool = False, 
                 fits_file_dir: str = None) -> None:
        self.fits_file = FitsFile(fits_path, 
                                  check_exist=check_fits_file, 
                                  directory=fits_file_dir)
        super().__init__()

    def set_grid(self, fits_path, check_fits_file):
        """Set / replace the FitsFile object associated with the Grid.
        This is useful to set associate the FITS file after the Grid instance
        has been created.

        Parameters
        ----------
        fits_path : str
            Path to the FITS file
        check_fits_file : _type_
            If True, check the existence of the FITS file at fits_path.
        """
        if fits_path is not None:
            self.fits_file = FitsFile(fits_path, check_exist=check_fits_file)


class PixelatedRegularGrid(Grid):
    """Class that represents a grid of values defined on a regular, Cartesian grid.

    Parameters
    ----------
    fits_path : str
        Path to the FITS file in which the values (and perhaps the coordinates)
        are stored. This should be relative to the final COOLEST template file.
    field_of_view_x : Tuple[float], optional
        2-tuple holding the extremal coordinates of the coordinates grid 
        along the x direction (i.e., left side of the leftmost pixel and 
        rightside of the rightmost pixel), by default (0, 0)
    field_of_view_y : Tuple[float], optional
        2-tuple holding the extremal coordinates of the coordinates grid 
        along the y direction (i.e., bottom side of the lower pixel and 
        top side of the upper pixel), by default (0, 0)
    num_pix_x : int, optional
        Number of pixels along the x direction, by default 0
    num_pix_y : int, optional
        Number of pixels along the y direction, by default 0
    **kwargs_file : dic, optional
        Any remaining keyword arguments for FitsFile
    """
    
    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix_x: int = 0, 
                 num_pix_y: int = 0,
                 **kwargs_file) -> None:
        super().__init__(fits_path, **kwargs_file)
        self.set_grid(None, field_of_view_x, field_of_view_y, 
                      num_pix_x, num_pix_y, 
                      check_fits_file=kwargs_file.get('check_fits_file', True))

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
        """Set / replace the FitsFile object associated with the Grid.
        This is useful to set the FITS file after the Grid instance
        has been created.

        See class constructor for parameter descriptions.
        """
        super().set_grid(fits_path, check_fits_file)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists() and check_fits_file:
            self.num_pix_x, self.num_pix_y = self.read_fits()
            # if number of pixels is also given, check that it is consistent
            if num_pix_x != 0 and self.num_pix_x != num_pix_x:
                raise ValueError("Given number of pixels in x direction "
                                 "is inconsistent with the fits file")
            if num_pix_y != 0 and self.num_pix_y != num_pix_y:
                raise ValueError("Given number of pixels in y direction "
                                 "is inconsistent with the fits file")
        else:
            self.num_pix_x, self.num_pix_y = num_pix_x, num_pix_y

    def read_fits(self):
        """Read the content of the FITS file and extract the necessary Grid attributes.

        Returns
        -------
        (num_pix_x, num_pix_y)
            Number of pixels along each axis.
        """
        array, header = self.fits_file.read()
        array_shape = array.shape
        if array_shape != (header['NAXIS1'], header['NAXIS2']):
            warnings.warn("Image dimensions do not match the FITS header")
        return array_shape

    def get_pixels(self, directory=None):
        """Get the pixel (z) values of the regular grid from the FITS file.
        If the attribute FITS path is a relative one, it needs the absolute
        directory to read the FITS file.

        Parameters
        ----------
        directory : str, optional
            Absolute directory of the FITS file, by default None

        Returns
        -------
        ndarray
            2D array of pixel values associated to the regular grid.
        """
        array, _ = self.fits_file.read(directory=directory)
        return array


class IrregularGrid(Grid):
    """Class that represents an irregular set of values and their coordinates.

    Parameters
    ----------
    fits_path : str
        Path to the FITS file in which the values (and perhaps the coordinates)
        are stored. This should be relative to the final COOLEST template file.
    field_of_view_x : Tuple[float], optional
        2-tuple holding the minimum and maximum values of the x coordinates vector, 
        by default (0, 0)
    field_of_view_y : Tuple[float], optional
         2-tuple holding the minimum and maximum values of the y coordinates vector, 
        by default (0, 0)
    num_pix : int, optional
        Number of coordinates points, by default 0
    **kwargs_file : dic, optional
        Any remaining keyword arguments for FitsFile
    """

    def __init__(self, 
                 fits_path: str = None,
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix: int = 0,
                 **kwargs_file) -> None:
        super().__init__(fits_path, **kwargs_file)
        self.set_grid(None, 
                      field_of_view_x=field_of_view_x, 
                      field_of_view_y=field_of_view_y, 
                      num_pix=num_pix)

    def set_grid(self, fits_path, 
                 field_of_view_x=(0, 0), field_of_view_y=(0, 0),
                 num_pix=0, check_fits_file=True):
        """Set / replace the FitsFile object associated with the Grid.
        This is useful to set associate the FITS file after the Grid instance
        has been created.

        See class constructor for parameter descriptions.
        """
        super().set_grid(fits_path, check_fits_file)
        if self.fits_file.exists():
            self.field_of_view_x, self.field_of_view_y, self.num_pix = self.read_fits()
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

    def read_fits(self):
        """Read the content of the FITS file and extract the necessary Grid attributes.

        Returns
        -------
        field_of_view_x, field_of_view_y, num_pix
            Field of view and number of pxiels.
        """
        x, y, z = self.get_xyz()
        num_pix = len(z)
        #assert self.num_pix == len(z), "Given number of grid points does not match the number of .fits table rows!"
        # Here we may want to check/report the overlap between the given field of view and the square encompassing the irregular grid
        field_of_view_x = (min(x), max(x))
        field_of_view_y = (min(y), max(y))
        return field_of_view_x, field_of_view_y, num_pix

    def get_xyz(self, directory=None):
        """Get the x, y, z values of the irregular grid from the FITS file.
        If the attribute FITS path is a relative one, it needs the absolute
        directory to read the FITS file.

        Parameters
        ----------
        directory : str, optional
            Absolute directory of the FITS file, by default None

        Returns
        -------
        ndarray, ndarray, ndarray
            x, y and z arrays
        """
        data, _ = self.fits_file.read(directory=directory)
        x = data.field(0)
        y = data.field(1)
        z = data.field(2)
        return x, y, z
