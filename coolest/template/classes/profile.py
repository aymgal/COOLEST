__author__ = 'aymgal'

import numpy as np
from typing import Dict

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.parameter import (Parameter, 
                                                LinearParameter, LinearParameterSet,
                                                NonLinearParameter, HyperParameter)


__all__ = ['Profile' ,'AnalyticalProfile']


class Profile(APIBaseObject):
    """Abstract class for any light or mass profile.

    Parameters
    ----------
    parameters : Dict[(str, Parameter)]
        Dictionary of Parameters objects keyed by parameter name.
    """

    def __init__(self, parameters: Dict[(str, Parameter)]) -> None:
        self.type = self.__class__.__name__  # name of children class
        self.parameters = parameters
        self.id = None
        super().__init__()


class AnalyticalProfile(Profile):
    """Abstract class for an light or mass profile described 
    by one or several analytical functions.

    Parameters
    ----------
    parameters : Dict[(str, Parameter)]
        Dictionary of Parameters objects keyed by parameter name.
    """

    def __init__(self, parameters: Dict[(str, Parameter)]) -> None:
        """"""
        super().__init__(parameters)
        
    def total_num_params(self, include_fixed=False, include_hyper=True):
        """Compute the number of parameter of the profile.

        Parameters
        ----------
        include_fixed : bool, optional
            Include fixed parameters in the count, by default False
        include_hyper : bool, optional
            Include the hyper-parameters in the count, by default True

        Returns
        -------
        int
            Number of parameters
        """
        count = 0
        for name, parameter in self.parameters.items():
            if isinstance(parameter, (NonLinearParameter, LinearParameter)):
                if not parameter.fixed or include_fixed:
                    count += 1
            elif isinstance(parameter, LinearParameterSet):
                if not parameter.fixed or include_fixed:
                    count += parameter.num_values
            elif isinstance(parameter, HyperParameter) and include_hyper:
                if not parameter.fixed or include_fixed:
                    count += 1
        return count
