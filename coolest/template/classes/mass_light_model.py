__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.profile_list import ProfileList
from coolest.template.classes.profiles import mass as mass_profiles_module
from coolest.template.classes.profiles import light as light_profiles_module


class MassModel(ProfileList):
    """Describes a mass model of a lensing entity as a list of (mass) profiles
    """

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(mass_profiles_module, *profile_names)
        

class LightModel(ProfileList):
    """Describes a light model of a lensing entity as a list of (light) profiles
    """

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(light_profiles_module, *profile_names)
