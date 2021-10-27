__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.regularizations import pixelated as regularization_module
from lensmodelapi.api import util


class RegularizationList(list):

    def __init__(self, 
                 *regularization_profile_pairs: Tuple[Tuple]) -> None:
        """
        regularization_profile_pairs is a tuple of tuple with the following syntax:
        (
            ('regularization method 1', specific Profile (light or mass) instance),
            ('regularization method 2', specific Profile (light or mass) instance),
            ...
        )
        """
        profiles = []
        for name, profile in regularization_profile_pairs:
            if name not in regularization_module.SUPPORTED_CHOICES:
                raise ValueError(f"Regularization '{name}' of type '{self._type}' is not supported.")
            profile_class = getattr(regularization_module, name)
            profiles.append(profile_class(applied_to_profile_id=profile.id))
        list.__init__(self, profiles)
        self._create_all_ids()

    def _create_all_ids(self):
        for j, regularization in enumerate(self):
            regularization_id = util.regul_to_id(regularization.type, j)
            regularization.id = regularization_id
            for parameter in regularization.parameters:
                param_id = f'{regularization.id}_{parameter.name}'
                parameter.id = param_id
