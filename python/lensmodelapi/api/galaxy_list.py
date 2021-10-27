__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.galaxy import Galaxy, SourceGalaxy, LensGalaxy
from lensmodelapi.api import util


class GalaxyList(list):

    def __init__(self,
                 *galaxies: Tuple[Galaxy]):
        list.__init__(self, galaxies)
        self._create_all_ids()

    def num_sources():
        count = 0
        for g in self:
            if isinstance(g, SourceGalaxy):
                count += 1
        return count

    def num_lenses():
        count = 0
        for g in self:
            if isinstance(g, LensGalaxy):
                count += 1
        return count

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
                    profile_id = util.profile_to_id(model_type, profile.type, j, i)
                    profile.id = profile_id
                    for parameter in profile.parameters:
                        param_id = f'{profile.id}_{parameter.name}'
                        parameter.id = param_id
