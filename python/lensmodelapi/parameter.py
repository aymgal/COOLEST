# Single parameter of a profile

__all__ = [
    'NonLinearParameter', 
    'LinearParameter', 
    'LinearParameterSet',
    'HyperParameter',
    'ParameterList',
]

class Parameter(object):

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
            self.latex_name = name
        self.value = default_value
        self._type = None
        self._id = None
        
    def set_value(self, value, overwrite=False):
        if self.value is not None and not overwrite:
            raise ValueError(f"A value ({self.value:.2f}) has already been set.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value cannot be smaller than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value cannot be larger than {self.max_value}.")
        self.value = value

    def set_id(self, unique_id: str) -> None:
        self._id = unique_id

    def fix():
        if self.value is None:
            raise ValueError(f"Cannot fix parameter {self.name} as no value has been set.")
        self.fixed = True

    def unfix():
        self.fixed = False

    def param_type():
        return self._type


class ParameterList(list):

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    def total_num_params(self):
        count = 0
        for p in self:
            if isinstance(p, (NonLinearParameter, LinearParameter)):
                count += 1
            elif isinstance(p, LinearParameterSet):
                count += p.num_values
        return count


class NonLinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = 'non_linear'


class LinearParameter(Parameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = 'linear'


class LinearParameterSet(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, num_values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_values = num_values
        self._type = 'linear_set'


class HyperParameter(Parameter):
    """Typically for pixelated profiles"""

    def __init__(self, profile_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_id = profile_id
        self._type = 'hyper'
