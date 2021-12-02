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

    def update_parameter_bounds_with_obs(self, instrument):
        """
        This function is meant to limit the available parameter space
        using simple arguments such as the image field of view, pixel size, etc.
        """
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
