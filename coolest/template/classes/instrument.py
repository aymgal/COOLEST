__author__ = 'aymgal'

from coolest.template.classes.psf import PSF, UnspecifiedPSF
from coolest.template.classes.base import APIBaseObject


class Instrument(APIBaseObject):
    """Defines the instrument used for the observation.
    This includes the name of the telescope and detector, the filter, 
    the pixel size, the readout noise and the point spread function (PSF).

    Parameters
    ----------
    pixel_size : float
        Size in arcseconds of a single detector pixel, by default None.
    name : str, optional
        Name of the instrument, by default ""
    band : str, optional
        Name of the filter, by default ""
    readout_noise : float, optional
        Readout noise (in electrons) when it is relevant to the instrument, 
        by default None.
    psf : PSF, optional
        Instance of PSF object, by default None (i.e. UnspecifiedPSF).
    """

    def __init__(self,
                 pixel_size: float = None,
                 name: str = "",
                 band: str = "",
                 readout_noise: float = None,
                 psf: PSF = None) -> None:
        self.name = name
        self.band = band
        self.pixel_size = pixel_size
        self.readout_noise = readout_noise
        if psf is None:
            psf = UnspecifiedPSF()
        self.psf = psf
        super().__init__()
