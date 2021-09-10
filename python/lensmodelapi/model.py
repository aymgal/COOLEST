__author__ = 'aymgal'

from typing import List

from lensmodelapi.base import LensModelAPIObject
from lensmodelapi.profile_list import ProfileList, MassProfileList, LightProfileList


class Model(LensModelAPIObject):

    def __init__(self, 
                 profiles: ProfileList) -> None:
        self.profiles = profiles
        super().__init__()


class MassModel(Model):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        profiles = MassProfileList(profile_names)
        super().__init__(profiles)
        

class LightModel(Model):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        profiles = LightProfileList(profile_names)
        super().__init__(profiles)
        