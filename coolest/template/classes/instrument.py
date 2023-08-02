__author__ = 'aymgal'

from coolest.template.classes.psf import PSF
from coolest.template.classes.base import APIBaseObject


class Instrument(APIBaseObject):
    """Defines the instrument used for the observation.
    This includes the name of the telescope and detector, the filter, 
    the pixel size, the readout noise and the point spread function (PSF).

    Parameters
    ----------
    pixel_size : float
        Size in arcseconds of a single detector pixel.
    name : str, optional
        Name of the instrument, by default ""
    band : str, optional
        Name of the filter, by default ""
    readout_noise : float, optional
        Readout noise (in electrons), by default 0.
    psf : PSF, optional
        Instance of PSF object, by default None
    """

    def __init__(self,
                 pixel_size: float,
                 name: str = "",
                 band: str = "",
                 readout_noise: float = 0.,
                 psf: PSF = None) -> None:
        self.name = name
        self.band = band
        self.pixel_size = pixel_size
        self.readout_noise = readout_noise
        if psf is None:
            psf = PSF()
        self.psf = psf
        super().__init__()
