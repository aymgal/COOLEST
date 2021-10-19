__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.galaxy import Galaxy, SourceGalaxy, LensGalaxy


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

    def _create_all_ids(self):
        for i, galaxy in enumerate(self):
            for model_type in ['light', 'mass']:
                for j, profile in enumerate(getattr(galaxy, f'{model_type}_model').profiles):
                    profile_id = self.profile_to_id(model_type, profile.type, j, i)
                    profile.id = profile_id
                    for parameter in profile.parameters:
                        param_id = f'{profile.id}_{parameter.name}'
                        parameter.id = param_id

    @staticmethod
    def profile_to_id(model_type, profile_name, profile_idx, galaxy_idx):
        return f'galaxy-{galaxy_idx}_{model_type}-model_{profile_name}-{profile_idx}'

    @staticmethod
    def id_to_profile(id_str):
        galaxy_str, model_str, profile_str = id_str.split('_')
        galaxy_idx = int(galaxy_str.split('-')[1])
        profile_name, profile_idx = profile_str.split('-')
        profile_idx = int(profile_idx)
        model_type = model_str.split('-')[0]
        return model_type, profile_name, profile_idx, galaxy_idx
