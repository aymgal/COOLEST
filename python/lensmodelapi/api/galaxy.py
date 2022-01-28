__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.mass_light_model import MassModel, LightModel


class Galaxy(APIBaseObject):

    def __init__(self,
                 name: str,
                 redshift: float,
                 light_model: LightModel = None,
                 mass_model: MassModel = None) -> None:
        self.name = name
        if redshift is not None and redshift < 0:
            raise ValueError("Redshift cannot be negative.")
        self.redshift = redshift
        if light_model is None:
            light_model = LightModel()
        self.light_model = light_model
        if mass_model is None:
            mass_model = MassModel()
        self.mass_model = mass_model
        super().__init__()
