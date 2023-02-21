__author__ = 'aymgal'

import os
from astropy.io import fits


class FitsFile(object):
    """A .fits file object"""
    def __init__(self, path: str, check_exist: bool = False, directory: str = None) -> None:
        if (path is not None) and (directory is not None) and (not os.path.isabs(path)):
            self.path = os.path.join(directory, path)
        else:
            self.path = path
        if not self.exists() and check_exist:
            raise RuntimeError(f"FITS file located at '{self.path}' does not exist")

    def exists(self):
        if self.path is None:
            return False
        return os.path.exists(self.path)

    def read(self):
        return fits.getdata(self.path, header=True)
