__author__ = 'aymgal'

import numpy as np
from typing import Dict

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.parameter import Parameter
from lensmodelapi.api.fits_file import MultiExtFitsFile



class Profile(APIBaseObject):
    """Base class for all mass and light profiles"""

    def __init__(self, documentation: str) -> None:
        self.type = self.__class__.__name__  # name of children class
        self.documentation = documentation
        self.id = None
        super().__init__()



class AnalyticalProfile(Profile):

    def __init__(self,
                 documentation: str, 
                 parameters: Dict[(str, Parameter)]) -> None:
        super().__init__(documentation)
        self.parameters = parameters
        
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


class AnalyticalLightProfile(AnalyticalProfile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AnalyticalMassProfile(AnalyticalProfile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class PixelatedProfile(Profile):

    def __init__(self,
                 documentation: str, 
                 pixels: MultiExtFitsFile) -> None:
        super().__init__(documentation)
        self.pixels = pixels

    def total_num_params(self, include_fixed=False, include_hyper=True):
        raise NotImplementedError("Number of parameters for pixelated profile is not yet implemented.")


class PixelatedLightProfile(PixelatedProfile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PixelatedMassProfile(PixelatedProfile):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
