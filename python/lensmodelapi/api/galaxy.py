__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.model import LightModel, MassModel


class Galaxy(APIBaseObject):

    def __init__(self,
                 name: str,
                 redshift: float,
                 light_model: LightModel,
                 mass_model: MassModel = None) -> None:
        self.name = name
        if redshift < 0:
            raise ValueError("Redshift cannot be negative.")
        self.redshift = redshift
        self.light_model = light_model
        if mass_model is None:
            mass_model = MassModel([])
        self.mass_model = mass_model
        super().__init__()


class LensGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: float,
                 light_model: LightModel,
                 mass_model: MassModel) -> None:
        super().__init__(name, redshift, light_model, mass_model=mass_model)
        


class SourceGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: float,
                 light_model: LightModel) -> None:
        super().__init__(name, redshift, light_model, mass_model=None)
        