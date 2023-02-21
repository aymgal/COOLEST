__author__ = 'aymgal, Giorgos Vernardos'

from typing import Tuple
import numpy as np
from scipy.interpolate import griddata

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.fits_file import FitsFile


class PixelatedRegularGrid(APIBaseObject):
    
    def __init__(self, 
                 fits_path: str = "",
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix_x: int = 0,
                 num_pix_y: int = 0):
        documentation = "Pixelated light profile on a pixel grid"
        self.fits_file = FitsFile(fits_path)
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        if self.fits_file.exists:
            array, header = self.fits_file.read()
            array_shape = array.shape
            assert array_shape == (header['NAXIS1'], header['NAXIS2']), "Given dimensions do not match the .fits image!"
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



    
class IrregularGrid(APIBaseObject):
    def __init__(self, 
                 fits_path: str = "",
                 field_of_view_x: Tuple[float] = (0, 0),
                 field_of_view_y: Tuple[float] = (0, 0),
                 num_pix: int = 0):
        documentation = "Irregular light profile, a list of (x,y,z) values"
        self.field_of_view_x = field_of_view_x
        self.field_of_view_y = field_of_view_y
        self.num_pix = num_pix
        self.fits_file = FitsFile(fits_path)

        try:
            self.set_fits(self.fits_path)
        except Exception as e:
            print(e) # We may want something different here
    
        super().__init__()


    def set_fits(self,fits_path):
        self.fits_file = FitsFile(fits_path)
        if self.fits_file.exists:
            x,y,z = self.get_xyz()
            self.num_pix = len(z)
            #assert self.num_pix == len(z), "Given number of grid points does not match the number of .fits table rows!"
            if self.field_of_view_x == (0,0) and self.field_of_view_y == (0,0):
                # Here we may want to check/report the overlap between the given field of view and the square encompassing the irregular grid
                self.field_of_view_x = (min(x),max(x))
                self.field_of_view_y = (min(y),max(y))
        else:
            self.num_pix = 0
            #raise Exception("Input .fits file does not exist!")

            
    def get_xyz(self):
        if self.fits_file.exists:
            data, header = self.fits_file.read()
            x = data.field(0)
            y = data.field(1)
            z = data.field(2)
            return x,y,z
        else:
            raise Exception("Input .fits file does not exist!")
        

    def get_on_grid(self,xg,yg,**kwargs):
        x,y,z = self.get_xyz()

        #print(len(x))
        #print(xg.shape,yg.shape)

        zg = griddata((x,y),z,(xg,yg),method=kwargs["method"])

        return zg

        
