__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.regularizations import pixelated as regularization_module
from coolest.template.classes import util


class RegularizationList(list, APIBaseObject):

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
                raise ValueError(f"Regularization '{name}' is not supported.")
            profile_class = getattr(regularization_module, name)
            profiles.append(profile_class(applied_to_profile_id=profile.id))
        list.__init__(self, profiles)
        APIBaseObject.__init__(self)
        self._create_all_ids()

    def _create_all_ids(self):
        for j, regularization in enumerate(self):
            regularization_id = util.regul_to_id(regularization.type, j)
            regularization.id = regularization_id
            for name, parameter in regularization.parameters.items():
                param_id = f'{regularization.id}_{name}'
                parameter.id = param_id
