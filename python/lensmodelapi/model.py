# Generic model, as an ensemble of profiles

from lensmodelapi.profile_base import ProfileList
from lensmodelapi import mass_profile as mass_module
from lensmodelapi import light_profile as light_module


class Model(object):

    def __init__(self, 
                 profile_module,
                 profile_names: list[str]) -> None:
        self.profiles = ProfileList(profile_module, profile_names)
        self._type = None
        self._id = None

    def set_id(self, unique_id: str) -> None:
        self._id = unique_id

    def model_type(self):
        return self._type


class MassModel(Model):

    def __init__(self, 
                 profile_names: list) -> None:
        super().__init__(mass_module, profile_names)
        self._type = 'mass'
        

class LightModel(Model):

    def __init__(self, 
                 profile_names: list) -> None:
        super().__init__(light_module, profile_names)
        self._type = 'light'
        