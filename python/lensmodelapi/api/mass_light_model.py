__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.profile_list import MassProfileList, LightProfileList


class MassModel(APIBaseObject):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        self.profiles = MassProfileList(*profile_names)
        super().__init__()
        

class LightModel(APIBaseObject):

    def __init__(self, 
                 *profile_names: Tuple[str]) -> None:
        self.profiles = LightProfileList(*profile_names)
        super().__init__()
        