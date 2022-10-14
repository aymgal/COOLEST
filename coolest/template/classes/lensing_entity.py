__author__ = 'aymgal'

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.mass_light_model import MassModel


class LensingEntity(APIBaseObject):

    def __init__(self,
                 type_: str,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        self.type = type_
        self.name = name
        if redshift is not None and redshift < 0:
            raise ValueError("Redshift cannot be negative.")
        self.redshift = redshift
        if mass_model is None:
            mass_model = MassModel()
        self.mass_model = mass_model
        super().__init__()
