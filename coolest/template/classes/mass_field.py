__author__ = 'aymgal'

from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.mass_light_model import MassModel
from coolest.template.classes import util


class MassField(LensingEntity):
    """Generic field of massive objects, for instance an external shear field.

    Parameters
    ----------
    name : str
        Name associated to that shear component.
    redshift : float
        Redshift associated to that shear component, if needed.
    mass_model : MassModel, optional
        Mass model of the field, by default None
    """

    def __init__(self,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        super().__init__(name, redshift, mass_model=mass_model)
        