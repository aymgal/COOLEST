__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.profile_list import ProfileList
from coolest.template.classes.profiles import mass as mass_profiles_module
from coolest.template.classes.profiles import light as light_profiles_module


class MassModel(ProfileList):
    """Describes a mass model of a lensing entity as a list of (mass) profiles
    
    Parameters
    ----------
    *profile_names : str
        Names of the mass profiles, following corresponding class names in
        the coolest.template.classes.profiles.mass submodule.
    """

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(mass_profiles_module, *profile_names)
        

class LightModel(ProfileList):
    """Describes a light model of a lensing entity as a list of (light) profiles

    Parameters
    ----------
    *profile_names : str
        Names of the light profiles, following corresponding class names in
        the coolest.template.classes.profiles.light submodule.
    """

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        super().__init__(light_profiles_module, *profile_names)
