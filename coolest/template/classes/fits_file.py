__author__ = 'aymgal'

import os
from astropy.io import fits


class FitsFile(object):
    """A .fits file object"""
    def __init__(self, path: str) -> None:
        self.path = path

    @property
    def exists(self):
        return os.path.exists(self.path)

    def read(self):
        return fits.getdata(self.path, header=True)
