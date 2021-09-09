__author__ = 'aymgal'

from typing import List

from lensmodelapi.parameter import (Parameter,
                                    NonLinearParameter,
                                    LinearParameter,
                                    LinearParameterSet)


class ParameterList(list):

    def __init__(self,
                 parameters: List[Parameter]) -> None:
        list.__init__(self, parameters)

    def total_num_params(self, include_fixed=False):
        count = 0
        for p in self:
            if isinstance(p, (NonLinearParameter, LinearParameter)) and not p.fixed:
                if p.fixed or not include_fixed:
                    count += 1
            elif isinstance(p, LinearParameterSet) and not p.fixed:
                if p.fixed or not include_fixed:
                    count += p.num_values
        return count
