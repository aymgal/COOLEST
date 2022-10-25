__author__ = 'aymgal'

from coolest.template.classes.base import APIBaseObject


class Cosmology(APIBaseObject):

    """Defines the cosmological model. 
    Currently, only FlatLambdaCDM from astropy is supported, based on H0 and Omega_m.
    """

    def __init__(self, 
                 H0: float,
                 Om0: float,
                 astropy_name: str = 'FlatLambdaCDM') -> None:
        self.H0 = H0
        self.Om0 = Om0
        self.astropy_name = astropy_name
        super().__init__()
