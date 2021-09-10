__author__ = 'aymgal'

from lensmodelapi.base import LensModelAPIObject
from lensmodelapi.redshift import Redshift
from lensmodelapi.model import LightModel, MassModel


class Galaxy(LensModelAPIObject):

    def __init__(self,
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel,
                 mass_model: MassModel = None) -> None:
        self.name = name
        self.redshift = redshift
        self.light_model = light_model
        self.mass_model = mass_model
        super().__init__()


class LensGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel,
                 mass_model: MassModel) -> None:
        super().__init__(name, redshift, light_model, mass_model=mass_model)
        


class SourceGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel) -> None:
        super().__init__(name, redshift, light_model, mass_model=None)
        