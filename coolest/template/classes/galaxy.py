__author__ = 'aymgal'

from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.mass_light_model import MassModel, LightModel


class Galaxy(LensingEntity):
    """Class that defines a Galaxy entity (lens galaxy and/or source galaxy).

    Parameters
    ----------
    name : str
        Name associated to the galaxy.
    redshift : float
        Redshift of the galaxy, if any.
    light_model : LightModel, optional
        Light model instance describing the surface brightness of the galaxy, by default None
    mass_model : MassModel, optional
        Mass model instance describing the mass distribution of the galaxy, by default None
    """

    def __init__(self,
                 name: str,
                 redshift: float,
                 light_model: LightModel = None,
                 mass_model: MassModel = None) -> None:
        super().__init__(name, redshift, mass_model=mass_model)
        if light_model is None:
            light_model = LightModel()
        self.light_model = light_model
