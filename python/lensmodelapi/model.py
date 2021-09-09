__author__ = 'aymgal'

from typing import List

from lensmodelapi.profile_list import ProfileList, MassProfileList, LightProfileList


class Model(object):

    def __init__(self, 
                 profiles: ProfileList) -> None:
        self.profiles = profiles
        self._type = None
        
    def type(self):
        return self._type


class MassModel(Model):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        profiles = MassProfileList(profile_names)
        super().__init__(profiles)
        self._type = 'mass'
        

class LightModel(Model):

    def __init__(self, 
                 profile_names: List[str]) -> None:
        profiles = LightProfileList(profile_names)
        super().__init__(profiles)
        self._type = 'light'
        