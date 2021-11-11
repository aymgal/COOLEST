__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.mass_light_model import MassModel


class ExternalShear(APIBaseObject):

    def __init__(self,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        self.name = name
        if redshift < 0:
            raise ValueError("Redshift cannot be negative.")
        self.redshift = redshift
        if mass_model is None:
            mass_model = MassModel()
        self.mass_model = mass_model
        super().__init__()
