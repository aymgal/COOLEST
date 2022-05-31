__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.profile_list import ProfileList
from lensmodelapi.api.profiles import mass as mass_profiles_module
from lensmodelapi.api.profiles import light as light_profiles_module


class MassModel(ProfileList):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(mass_profiles_module, *profile_names)
        

class LightModel(ProfileList):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(light_profiles_module, *profile_names)
