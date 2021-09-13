__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.galaxy_list import GalaxyList
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.regularization import Regularization
from lensmodelapi.api.coordinates import Coordinates


class LensModel(APIBaseObject):

    def __init__(self, 
                 galaxies: GalaxyList,
                 regularizations: RegularizationList,
                 coordinates: Coordinates) -> None:
        self.galaxies = galaxies
        self.regularizations = regularizations
        super().__init__()

    # def _check_regul(self):
    #     for regularization in self.regularizations:
    #         profile_id = regularization.applied_to_profile
    #         if profile_id is not None and profile_id not in self._profile_ids:
    #             raise ValueError(f"Profile ID '{profile_id}' does not correspond "
    #                              f"to any profile for regularization {regularization.object_name}.")
