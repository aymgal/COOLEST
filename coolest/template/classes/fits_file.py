__author__ = 'aymgal'

import os
import warnings
from astropy.io import fits


class FitsFile(object):
    """A .fits file object"""
    def __init__(self, path: str, check_exist: bool = False) -> None:
        self.path = path
        if not self.exists():
            message = f"Fits file located at '{self.path}' does not exist"
            if check_exist:
                raise RuntimeError(message)
            else:
                warnings.warn(message)

    def exists(self):
        if self.path is None: return False
        return os.path.exists(self.path)

    def read(self):
        return fits.getdata(self.path, header=True)
