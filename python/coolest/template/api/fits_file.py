__author__ = 'aymgal'

import os
from astropy.io import fits


class FitsFile(str):
    """A .fits file object"""
    def __new__(cls, fits_path: str = None) -> str:
        return str.__new__(cls, fits_path)

    @property
    def exists(self):
        return os.path.exists(self)

    def read(self):
        return fits.getdata(self, header=True)
