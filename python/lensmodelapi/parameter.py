# Single parameter of a profile

class ParameterBase(object):

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
        
    def set_value(self, value, overwrite=False):
        if self.value is not None and not overwrite:
            raise ValueError(f"A value ({self.value:.2f}) has already been set.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value cannot be smaller than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value cannot be smaller than {self.max_value}.")
        self.value = value

    def fix():
        self.fixed = True

    def unfix():
        self.fixed = False

    def param_type():
        return self._type


class NonLinearParameter(ParameterBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = 'non_linear'


class LinearParameter(ParameterBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = 'linear'


class LinearParameterSet(ParameterBase):

    def __init__(self, num_values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_values = num_values
        self._type = 'non_linear'
