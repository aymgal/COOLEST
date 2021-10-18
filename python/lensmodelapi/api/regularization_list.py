__author__ = 'aymgal'

from typing import List, Tuple

from lensmodelapi.api.regularizations import pixelated as regularization_module


class RegularizationList(list):

    def __init__(self, 
                 regularization_profile_pairs: List[Tuple]) -> None:
        profiles = []
        for name, profile in regularization_profile_pairs:
            if name not in regularization_module.SUPPORTED_CHOICES:
                raise ValueError(f"Regularization '{name}' of type '{self._type}' is not supported.")
            profile_class = getattr(regularization_module, name)
            profiles.append(profile_class(applied_to_profile_id=profile.id))
        list.__init__(self, profiles)
        self._create_all_ids()

    def _create_all_ids(self):
        # TODO: define IDs for hyper-parameters as well
        pass
        