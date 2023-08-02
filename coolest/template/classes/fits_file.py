__author__ = 'aymgal'


import os
from astropy.io import fits


class FitsFile(object):
    """Class that represents a FITS file on the disk.

    Parameters
    ----------
    path : str
        Path to the FITS file, depending on usage either relative or absolute.
    directory : str, optional
        Absolute directory containing the FITS file, 
        in case `path` is a relative, by default None
    check_exist : bool, optional
        If True, will check if the FITS file exists when the object is 
        instantiated, by default False

    Raises
    ------
    RuntimeError
        If the FITS file does not exist on the disk.
    """

    def __init__(self, path: str, 
                 directory: str = None, 
                 check_exist: bool = False) -> None:
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
        """Read the data and header content of the FITS file, using astropy.io.fits.

        A directory must be given typically when it has not been set at 
        the initialization of the object.

        Parameters
        ----------
        directory : str, optional
            Absolute directory containing the FITS file, by default None

        Returns
        -------
        ndarray or recarray or Group
            (data, header) content of the FITS file (as returned by fits.getdata())

        Raises
        ------
        ValueError
            If no directory is provided and no directory has been set beforehand.
        """
        if not hasattr(self, '_directory'):
            if directory is None:
                raise ValueError("You must provide a FITS file directory if none has been set")
            abs_path = os.path.join(directory, self.path)
        else:
            abs_path = self.abs_path
        return fits.getdata(abs_path, header=True)
