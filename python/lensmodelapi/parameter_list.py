__author__ = 'aymgal'

from typing import List

from lensmodelapi.parameter import (Parameter,
                                    NonLinearParameter,
                                    LinearParameter,
                                    LinearParameterSet,
                                    HyperParameter)


class ParameterList(list):

    def __init__(self,
                 parameters: List[Parameter]) -> None:
        list.__init__(self, parameters)

    def total_num_params(self, include_fixed=False, include_hyper=True):
        count = 0
        for p in self:
            if isinstance(p, (NonLinearParameter, LinearParameter)):
                if not p.fixed or include_fixed:
                    count += 1
            elif isinstance(p, LinearParameterSet):
                if not p.fixed or include_fixed:
                    count += p.num_values
            elif isinstance(p, HyperParameter) and include_hyper:
                if not p.fixed or include_fixed:
                    count += 1
        return count
