__author__ = 'aymgal'

from types import ModuleType
from typing import Tuple

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.profiles import mass as mass_profiles_module
from lensmodelapi.api.profiles import light as light_profiles_module


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


class MassProfileList(ProfileList):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(mass_profiles_module, *profile_names)


class LightProfileList(ProfileList):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(light_profiles_module, *profile_names)
