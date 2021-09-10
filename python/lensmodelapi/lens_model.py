__author__ = 'aymgal'

from typing import List

from lensmodelapi.base import APIBaseObject
from lensmodelapi.galaxy_list import GalaxyList
from lensmodelapi.galaxy import Galaxy, LensGalaxy, SourceGalaxy
from lensmodelapi.regularization_list import RegularizationList
from lensmodelapi.coordinates import Coordinates


class LensModel(APIBaseObject):

    def __init__(self, 
                 galaxies: List[Galaxy],
                 regularizations: List[str],
                 coordinates: Coordinates) -> None:
        self.galaxies = GalaxyList(galaxies)
        self.regularizations = RegularizationList(regularizations)
        super().__init__()
        self._create_unique_ids()

    def _create_unique_ids(self):
        for i, galaxy in enumerate(self.galaxies):
            for model in ['light', 'mass']:
                for j, profile in enumerate(getattr(galaxy, f'{model}_model').profiles):
                    for parameter in profile.parameters:
                        parameter.id = f'galaxy{i}_{model}_{profile.object.lower()}{j}_{parameter.name}'
