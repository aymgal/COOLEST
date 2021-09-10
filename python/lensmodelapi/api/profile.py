__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter_list import ParameterList


class Profile(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: ParameterList) -> None:
        self.description = description
        self.parameters = parameters
        super().__init__()
        

class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MassProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
