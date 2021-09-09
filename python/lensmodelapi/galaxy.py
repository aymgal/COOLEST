__author__ = 'aymgal'

from typing import List

from lensmodelapi.redshift import Redshift
from lensmodelapi.model import LightModel, MassModel


class Galaxy(object):

    def __init__(self,
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel) -> None:
        self.name = name
        self.redshift = redshift
        self.light_model = light_model
        self._type = None

    def type(self):
        return self._type


class LensGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel,
                 mass_model: MassModel) -> None:
        super().__init__(name, redshift, light_model)
        self.mass_model = mass_model
        self._type = 'lens'


class SourceGalaxy(Galaxy):

    def __init__(self, 
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel) -> None:
        super().__init__(name, redshift, light_model)
        self._type = 'source'
        