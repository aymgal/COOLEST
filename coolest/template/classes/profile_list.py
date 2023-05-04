__author__ = 'aymgal'

from types import ModuleType
from typing import Tuple

from coolest.template.classes.base import APIBaseObject


class ProfileList(list, APIBaseObject):

    def __init__(self, 
                 profiles_module: ModuleType,
                 *profile_names: Tuple[str]) -> None:
        """Generic list of model (mass or light) profile.
        Note that this class is not meant to be instantiated by the user.

        Parameters
        ----------
        profiles_module : mass or light profile submodule
            Submodule in coolest.template.classes.profiles defining 
            the python classes corresponding to each model profile.
        *profile_names: list of profile names, which must be class names
        defined in the profiles_module submodule.

        Raises
        ------
        ValueError
            If profile is not supported.
        """
        profiles = []
        for name in profile_names:
            if name not in profiles_module.SUPPORTED_CHOICES:
                raise ValueError(f"Profile '{name}' is not supported.")
            profile_class = getattr(profiles_module, name)
            profiles.append(profile_class())
        list.__init__(self, profiles)

    def num_pixelated_profiles(self):
        pass  #TODO
