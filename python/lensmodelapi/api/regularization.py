__author__ = 'aymgal'

from typing import Dict

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter import Parameter


class Regularization(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: Dict[str, Parameter],
                 applied_to_profile_id: str = None) -> None:
        self.name = self.__class__.__name__  # name of children class
        self.description = description
        self.parameters = parameters
        self.applied_to_profile_id = applied_to_profile_id
        super().__init__()
