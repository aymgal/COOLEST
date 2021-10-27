__author__ = 'aymgal'

import numpy as np

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter_list import ParameterList


class Profile(APIBaseObject):

    def __init__(self,
                 description: str, 
                 parameters: ParameterList) -> None:
        self.description = description
        self.parameters = parameters
        self.id = None
        super().__init__()

    def update_parameter_bounds_with_obs(self, instrument):
        fov_ra, fov_dec = instrument.field_of_view_ra, instrument.field_of_view_dec
        # Einstein radius cannot be more than half the FOV
        max_theta_E = max(fov_ra, fov_dec) / 2.
        for param in self.parameters:
            if param.name == 'theta_E':
                param.max_value = max_theta_E

class LightProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MassProfile(Profile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
