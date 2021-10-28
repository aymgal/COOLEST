# Single parameter of a profile

from lensmodelapi.api.base import APIBaseObject

__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'LinearParameterSet',
    'HyperParameter',
]


class DefinitionRange(APIBaseObject):

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value


class Prior(APIBaseObject):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class GaussianPrior(Prior):

    def __init__(self, mean=None, std_dev=None):
        super().__init__(mean=mean, std_dev=std_dev)


class LogNormalPrior(Prior):

    def __init__(self, mean=None, std_dev=None):
        super().__init__(mean=mean, std_dev=std_dev)


class UniformPrior(Prior):

    def __init__(self, min_value=None, max_value=None):
        super().__init__(min_value=min_value, max_value=max_value)


class Parameter(APIBaseObject):

    def __init__(self, 
                 name: str, 
                 description: str, 
                 definition_range: DefinitionRange,
                 fixed: bool = False,
                 default_value: float = None,
                 initial_value: float = None,
                 prior: Prior = None,
                 latex_name: str = None) -> None:
        self.name = name
        self.description = description
        self.fixed = fixed
        self.value = initial_value
        self.default_value = default_value
        self.definition_range = definition_range
        self.prior = prior
        if latex_name is None:
            latex_name = name
        self.latex_name = latex_name
        self.id = None
        super().__init__()
        
    def set_value(self, value, overwrite=False):
        if self.value is not None and not overwrite:
            raise ValueError(f"A value ({self.value:.2f}) has already been set.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value cannot be smaller than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value cannot be larger than {self.max_value}.")
        self.value = value

    def fix(self):
        if self.value is None:
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


class LinearParameterSet(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, 
                 num_values: int, 
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.num_values = num_values


class HyperParameter(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
