# Single parameter of a profile

from lensmodelapi.base import APIBaseObject

__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'LinearParameterSet',
    'HyperParameter',
]

class Parameter(APIBaseObject):

    def __init__(self, 
                 name: str, 
                 description: str, 
                 fixed: bool = False,
                 default_value: float = None,
                 min_value: float = None, 
                 max_value: float = None,
                 latex_name: str = None) -> None:
        self.name = name
        self.description = description
        self.fixed = fixed
        self.min_value = min_value
        self.max_value = max_value
        if latex_name is None:
            latex_name = name
        self.latex_name = latex_name
        self.value = default_value
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
        