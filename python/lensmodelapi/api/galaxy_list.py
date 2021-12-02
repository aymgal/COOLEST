__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.galaxy import Galaxy
from lensmodelapi.api import util


class GalaxyList(list, APIBaseObject):

    def __init__(self,
                 *galaxies: Tuple[Galaxy]):
        list.__init__(self, galaxies)
        self._create_all_ids()

    def num_sources():
        raise NotImplementedError("Couting number of source galaxies is not yet implemented.")

    def num_lenses():
        raise NotImplementedError("Couting number of source galaxies is not yet implemented.")

    def update_parameter_bounds_with_obs(self, instrument):
        for galaxy in self:
            for light_profile in galaxy.light_model.profiles:
                light_profile.update_parameter_bounds_with_obs(instrument)
            for mass_profile in galaxy.mass_model.profiles:
                mass_profile.update_parameter_bounds_with_obs(instrument)

    def _create_all_ids(self):
        for i, galaxy in enumerate(self):
            for model_type in ['light', 'mass']:
                for j, profile in enumerate(getattr(galaxy, f'{model_type}_model').profiles):
                    profile_id = util.profile_to_id(model_type, profile.name, j, i)
                    profile.id = profile_id
                    for param_name, parameter in profile.parameters.items():
                        param_id = f'{profile.id}_{param_name}'
                        parameter.id = param_id
