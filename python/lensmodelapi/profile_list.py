__author__ = 'aymgal'

from types import ModuleType
from typing import List

from lensmodelapi.profiles import mass as mass_profiles_module
from lensmodelapi.profiles import light as light_profiles_module


class ProfileList(list):

    def __init__(self, 
                 profiles_module: ModuleType,
                 profile_names: List[str]) -> None:
        profiles = []
        for name in profile_names:
            if name not in profiles_module.SUPPORTED_PROFILES:
                raise ValueError(f"Profile '{name}' of type '{self._type}' is not supported.")
            profile_class = getattr(profiles_module, name)
            profiles.append(profile_class())
        list.__init__(self, profiles)
        self._type = None

    def type(self):
        return self._type

    def num_pixelated_profiles(self):
        pass  #TODO


class MassProfileList(ProfileList):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        super().__init__(mass_profiles_module, profile_names)
        self._type = 'mass'


class LightProfileList(ProfileList):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        super().__init__(light_profiles_module, profile_names)
        self._type = 'light'
