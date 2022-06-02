__author__ = 'aymgal'

from lensmodelapi.api.lensing_entity import LensingEntity
from lensmodelapi.api.mass_light_model import MassModel
from lensmodelapi.api import util


class ExternalShear(LensingEntity):

    def __init__(self,
                 name: str,
                 redshift: float,
                 mass_model: MassModel = None) -> None:
        super().__init__('external_shear', name, redshift, 
                         mass_model=mass_model)
    #     self._create_all_ids()

    # def _create_all_ids(self):
    #     for j, profile in enumerate(self.mass_model.profiles):
    #         profile_id = util.ext_shear_profile_to_id(profile.name, j)
    #         profile.id = profile_id
    #         for param_name, parameter in profile.parameters.items():
    #             param_id = f'{profile.id}-{param_name}'
    #             parameter.id = param_id
