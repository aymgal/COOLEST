__author__ = 'aymgal'

from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.mass_light_model import MassModel
from coolest.template.classes import util


class ExternalShear(LensingEntity):

    def __init__(self,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        super().__init__(name, redshift, mass_model=mass_model)
        