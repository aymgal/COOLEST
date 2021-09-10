__author__ = 'aymgal'

from lensmodelapi.base import LensModelAPIObject


class Cosmology(LensModelAPIObject):

    def __init__(self, 
                 H0: float,
                 Om0: float,
                 model_name: str = 'FlatLambdaCDM') -> None:
        self.model_name = model_name
        self.H0 = H0
        self.Om0 = Om0
        super().__init__()
