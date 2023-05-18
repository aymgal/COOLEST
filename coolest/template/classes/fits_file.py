__author__ = 'aymgal'


import os
from astropy.io import fits


class FitsFile(object):
    """A .fits file object"""
    def __init__(self, path: str, directory: str = None, check_exist: bool = False) -> None:
        self.path = path
        self._directory = directory
        if not self.exists() and check_exist:
            raise RuntimeError(f"FITS file located at '{self.path}' does not exist")

    @property
    def abs_path(self):
        if not hasattr(self, '_directory') or self._directory is None:
            return self.path
        return os.path.join(self._directory, self.path)

    def exists(self):
        if self.path is None:
            return False
        return os.path.exists(self.abs_path)

    def read(self, directory=None):
        """directory must be given when _directory attribute has been set beforehand"""
        if not hasattr(self, '_directory'):
            if directory is None:
                raise ValueError("You must provide a FITS file directory if none has been set")
            abs_path = os.path.join(directory, self.path)
        else:
            abs_path = self.abs_path
        return fits.getdata(abs_path, header=True)
