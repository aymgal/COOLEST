# Single parameter of a profile

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.probabilities import Prior, PosteriorStatistics


__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'HyperParameter',
    'LinearParameterSet',
    'PixelParameterSet',
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
                 name: str, 
                 description: str, 
                 definition_range: DefinitionRange,
                 units: str = None,
                 fixed: bool = False,
                 initial_estimate: PointEstimate = None,
                 posterior: PosteriorStatistics = None,
                 prior: Prior = None,
                 latex_name: str = None) -> None:
        self.name = name
        self.description = description
        self.units = units
        self.definition_range = definition_range
        self.fixed = fixed
        if not isinstance(initial_estimate, PointEstimate):
            self.initial_estimate = PointEstimate(initial_estimate)
        else:
            self.initial_estimate = initial_estimate
        self.point_estimate = PointEstimate(value=self.initial_estimate.value)
        if posterior is None:
            posterior = PosteriorStatistics()
        self.posterior = posterior
        if prior is None:
            prior = Prior()
        self.prior = prior
        if latex_name is None:
            latex_name = name
        self.latex_name = latex_name
        self.id = None
        super().__init__()
        
    def set_point_estimate(self, point_estimate):
        if isinstance(point_estimate, (float, int)):
            point_estimate = PointEstimate(value=float(point_estimate))
        elif not isinstance(point_estimate, PointEstimate):
            raise ValueError("Parameter prior must be either a PointEstimate instance "
                             "or a single number (float or int).")
        if (self.definition_range.min_value is not None 
            and point_estimate.value < self.definition_range.min_value):
            raise ValueError(f"Value cannot be smaller than {self.definition_range.min_value}.")
        if (self.definition_range.max_value is not None 
            and point_estimate.value > self.definition_range.max_value):
            raise ValueError(f"Value cannot be larger than {self.definition_range.max_value}.")
        self.point_estimate = point_estimate

    def remove_point_estimate(self):
        self.point_estimate = PointEstimate()

    def set_posterior(self, posterior):
        if not isinstance(posterior, PosteriorStatistics):
            raise ValueError("Parameter prior must be a PosteriorStatistics instance.")
        self.posterior = posterior

    def remove_posterior(self):
        self.posterior = PosteriorStatistics()

    def set_prior(self, prior):
        if not isinstance(prior, Prior):
            raise ValueError("Parameter prior must be a Prior instance.")
        self.prior = prior

    def remove_prior(self):
        self.prior = Prior()

    def fix(self):
        if self.elf.point_estimate.value is None:
            raise ValueError(f"Cannot fix parameter {self.name} as no value has been set.")
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
        if 'initial_estimate' not in kwargs or kwargs['initial_estimate'] is None:
            kwargs['initial_estimate'] = []
        if not isinstance(kwargs['initial_estimate'], list):
            raise ValueError("For any ParameterSet, `initial_estimate` must be a list of values.")
        super().__init__(*args, **kwargs)
        self.num_values = len(self.point_estimate.value)


class LinearParameterSet(ParameterSet):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class PixelParameterSet(ParameterSet):
    """Typically for pixelated profiles"""

    def __init__(self, 
                 *args,
                 x_coords: List[float] = [],
                 y_coords: List[float] = [],
                 order_in_memory: str = 'C',
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if (len(x_coords) != len(self.point_estimate.value) or 
            len(y_coords) != len(self.point_estimate.value)):
            raise ValueError("List of coordinates must have the same length as pixel values in `value`.")
        self.x_coords = x_coords
        self.y_coords = y_coords

        # see https://numpy.org/doc/stable/reference/generated/numpy.ndarray.flatten.html
        self.order_in_memory = order_in_memory
