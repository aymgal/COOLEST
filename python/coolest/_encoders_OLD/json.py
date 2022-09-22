__author__ = 'aymgal'

from json import JSONEncoder

from lensmodelapi.profile import Profile
from lensmodelapi.parameter import Parameter


def check_type(obj):
    def decorator(func):
        def wrapper_func(*args, **kwargs):
            inst = args[1]
            if not isinstance(inst, obj):
                raise TypeError(f"Unexpected type {inst} (should be {obj}).")
            return func(*args, **kwargs)
        return wrapper_func
    return decorator


class JSONProfile(JSONEncoder):
    @check_type(Profile)
    def default(self, p):
        return {
            'name': p.name,
            'description': p.description,
            'parameters': str(p.parameters),
        }

class JSONParameter(JSONEncoder):
    @check_type(Parameter)
    def default(self, p):
        return {
            'type': p.__class__.__name__,
            'name': p.name,
            'value': p.value,
            'description': p.description,
            'fixed': p.fixed,
            'min_value': p.min_value,
            'max_value': p.max_value, 
            'id': p.get_id(),
        }
