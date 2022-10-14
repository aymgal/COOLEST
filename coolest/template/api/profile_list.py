__author__ = 'aymgal'

from types import ModuleType
from typing import Tuple

from coolest.template.api.base import APIBaseObject


class ProfileList(list, APIBaseObject):

    def __init__(self, 
                 profiles_module: ModuleType,
                 *profile_names: Tuple[str]) -> None:
        profiles = []
        for name in profile_names:
            if name not in profiles_module.SUPPORTED_CHOICES:
                raise ValueError(f"Profile '{name}' is not supported.")
            profile_class = getattr(profiles_module, name)
            profiles.append(profile_class())
        list.__init__(self, profiles)

    def num_pixelated_profiles(self):
        pass  #TODO
