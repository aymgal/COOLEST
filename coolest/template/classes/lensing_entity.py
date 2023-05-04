__author__ = 'aymgal'

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.mass_light_model import MassModel


__all__ = [
    'LensingEntity',
]

SUPPORTED_CHOICES = ['Galaxy', 'MassField']


class LensingEntity(APIBaseObject):
    """Abstract lensing entity, typically a Galaxy or an MassField object.

    Parameters
    ----------
    name : str
        Name of the entity (e.g., the name of the galaxy)
    redshift : float
        Redshift of the entity, if known / assumed
    mass_model : MassModel, optional
        Mass model (i.e., a set of mass profiles), by default None

    Raises
    ------
    ValueError
        If the provided redshift is negative.
    """

    def __init__(self,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        self.type = self.__class__.__name__  # name of the children class
        self.name = name
        if redshift is not None and redshift < 0:
            raise ValueError("Redshift cannot be negative.")
        self.redshift = redshift
        if mass_model is None:
            mass_model = MassModel()
        self.mass_model = mass_model
        super().__init__()
