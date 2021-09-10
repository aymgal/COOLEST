__author__ = 'aymgal'

from typing import List

from lensmodelapi.regularizations import pixelated as regularization_module


class RegularizationList(list):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        profiles = []
        for name in profile_names:
            if name not in regularization_module.SUPPORTED_PROFILES:
                raise ValueError(f"Regularization '{name}' of type '{self._type}' is not supported.")
            profile_class = getattr(regularization_module, name)
            profiles.append(profile_class())
        list.__init__(self, profiles)
