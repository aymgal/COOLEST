__author__ = 'aymgal'

from lensmodelapi.base import APIBaseObject
from lensmodelapi.parameter_list import ParameterList
from lensmodelapi.profile import Profile


class Regularization(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: ParameterList) -> None:
        self.description = description
        self.parameters = parameters
        super().__init__()
