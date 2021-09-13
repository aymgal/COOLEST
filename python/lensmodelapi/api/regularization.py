__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter_list import ParameterList


class Regularization(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: ParameterList,
                 applied_to_profile_id: str = None) -> None:
        self.description = description
        self.parameters = parameters
        self.applied_to_profile_id = applied_to_profile_id
        super().__init__()
