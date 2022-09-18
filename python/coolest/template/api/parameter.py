# Single parameter of a profile

from typing import List

from coolest.template.api.base import APIBaseObject
from coolest.template.api.probabilities import Prior, PosteriorStatistics

import numpy as np


__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'HyperParameter',
    'LinearParameterSet',
    'NonLinearParameterSet',
    # 'PixelParameterSet',
]


class DefinitionRange(APIBaseObject):

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value


class PointEstimate(APIBaseObject):

    def __init__(self, value=None):
        self.value = value


class Parameter(APIBaseObject):

    def __init__(self, 
                 documentation: str, 
                 definition_range: DefinitionRange,
                 units: str = None,
                 fixed: bool = False,
                 point_estimate: PointEstimate = None,
                 posterior_stats: PosteriorStatistics = None,
                 prior: Prior = None,
                 latex_str: str = None) -> None:
        self.documentation = documentation
        self.units = units
        self.definition_range = definition_range
        self.fixed = fixed
        if not isinstance(point_estimate, PointEstimate):
            self.point_estimate = PointEstimate(point_estimate)
        else:
            self.point_estimate = point_estimate
        if posterior_stats is None:
            posterior_stats = PosteriorStatistics()
        self.posterior_stats = posterior_stats
        if prior is None:
            prior = Prior()
        self.prior = prior
        self.latex_str = latex_str
        self.id = None
        super().__init__()
        
    def set_point_estimate(self, point_estimate):
        if isinstance(point_estimate, (float, int, list)):
            self.point_estimate = PointEstimate(value=point_estimate)
        elif isinstance(point_estimate, tuple):
            self.point_estimate = PointEstimate(value=list(point_estimate))
        elif isinstance(point_estimate, np.ndarray):
            self.point_estimate = PointEstimate(value=point_estimate.tolist())
        elif isinstance(point_estimate, PointEstimate):
            self.point_estimate = point_estimate
        else:
            raise ValueError("Parameter prior must be either a PointEstimate instance "
                             "or a single number (float or int) or an array (tuple, list or ndarray).")
        val = self.point_estimate.value
        min_val = self.definition_range.min_value
        max_val = self.definition_range.max_value
        if min_val is not None and np.any(np.asarray(val) < np.asarray(min_val)):
            raise ValueError(f"Value cannot be smaller than {self.definition_range.min_value}.")
        if max_val is not None and np.any(np.asarray(val) > np.asarray(max_val)):
            raise ValueError(f"Value cannot be larger than {self.definition_range.max_value}.")

    def remove_point_estimate(self):
        self.point_estimate = PointEstimate()

    def set_posterior(self, posterior_stats):
        if not isinstance(posterior_stats, PosteriorStatistics):
            raise ValueError("Parameter prior must be a PosteriorStatistics instance.")
        self.posterior_stats = posterior_stats

    def remove_posterior(self):
        self.posterior_stats = PosteriorStatistics()

    def set_prior(self, prior):
        if not isinstance(prior, Prior):
            raise ValueError("Parameter prior must be a Prior instance.")
        self.prior = prior

    def remove_prior(self):
        self.prior = Prior()

    def fix(self):
        if self.point_estimate.value is None:
            raise ValueError("Cannot fix parameter as no point estimate value has been set.")
        self.fixed = True

    def unfix(self):
        self.fixed = False


class NonLinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HyperParameter(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        


class ParameterSet(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs) -> None:
        if 'point_estimate' not in kwargs or kwargs['point_estimate'] is None:
            kwargs['point_estimate'] = []
        if not isinstance(kwargs['point_estimate'], list):
            raise ValueError("For any ParameterSet, `point_estimate` must be a list of values.")
        super().__init__(*args, **kwargs)
        self.num_values = len(self.point_estimate.value)


class LinearParameterSet(ParameterSet):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        
class NonLinearParameterSet(ParameterSet):
    """Typically for position of point sources"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


# class PixelParameterSet(ParameterSet):
#     """Typically for pixelated profiles"""

#     def __init__(self, 
#                  *args,
#                  x_coords: List[float] = [],
#                  y_coords: List[float] = [],
#                  order_in_memory: str = 'C',
#                  **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         if (len(x_coords) != len(self.point_estimate.value) or 
#             len(y_coords) != len(self.point_estimate.value)):
#             raise ValueError("List of coordinates must have the same length as pixel values in `value`.")
#         self.x_coords = x_coords
#         self.y_coords = y_coords

#         # see https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flatten.html
#         self.order_in_memory = order_in_memory
