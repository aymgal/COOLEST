__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.mass_light_model import MassModel
from lensmodelapi.api import util


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
        self._create_all_ids()

    def _create_all_ids(self):
        for j, profile in enumerate(self.mass_model.profiles):
            profile_id = util.ext_shear_profile_to_id(profile.name, j)
            profile.id = profile_id
            for param_name, parameter in profile.parameters.items():
                param_id = f'{profile.id}-{param_name}'
                parameter.id = param_id
