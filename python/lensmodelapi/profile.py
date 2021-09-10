__author__ = 'aymgal'

from lensmodelapi.base import APIBaseObject
from lensmodelapi.parameter_list import ParameterList


class Profile(APIBaseObject):

    def __init__(self,
                 name: str, 
                 description: str, 
                 parameters: ParameterList) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters
        super().__init__()
        

class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MassProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
