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

    def _create_all_ids(self):
        for i, galaxy in enumerate(self):
            for model_type in ['light', 'mass']:
                for j, profile in enumerate(getattr(galaxy, f'{model_type}_model').profiles):
                    profile_id = util.galaxy_profile_to_id(model_type, profile.name, j, i)
                    profile.id = profile_id
                    for param_name, parameter in profile.parameters.items():
                        param_id = f'{profile.id}-{param_name}'
                        parameter.id = param_id
