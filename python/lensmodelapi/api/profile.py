__author__ = 'aymgal'

import numpy as np
from typing import Dict

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter import Parameter


class Profile(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: Dict[(str, Parameter)]) -> None:
        self.name = self.__class__.__name__  # name of children class
        self.description = description
        self.parameters = parameters
        self.id = None
        super().__init__()

    def total_num_params(self, include_fixed=False, include_hyper=True):
        count = 0
        for name, parameter in self.parameters.items():
            if isinstance(parameter, (NonLinearParameter, LinearParameter)):
                if not parameter.fixed or include_fixed:
                    count += 1
            elif isinstance(parameter, LinearParameterSet):
                if not parameter.fixed or include_fixed:
                    count += p.num_values
            elif isinstance(parameter, HyperParameter) and include_hyper:
                if not parameter.fixed or include_fixed:
                    count += 1
        return count


class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MassProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
