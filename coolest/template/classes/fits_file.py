__author__ = 'aymgal'

import os
from astropy.io import fits


class FitsFile(object):
    """A .fits file object"""
    def __init__(self, path: str, check_exist: bool = False) -> None:
        self.path = path
        if not self.exists() and check_exist:
            raise ValueError(f"Fits file '{self.path}' does not exist!")

    def exists(self):
        return os.path.exists(self.path)

    def read(self):
        return fits.getdata(self.path, header=True)
