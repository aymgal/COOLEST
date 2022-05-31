__author__ = 'aymgal'


import inspect
import json
from copy import deepcopy


def get_class_names(instance):
    class_names = [c.__name__ for c in inspect.getmro(instance.__class__)]
    return class_names[0], ' < '.join(class_names[:-1])


def filter_dict(dictionary, exclude_keys=None):
    if exclude_keys is None:
        return dictionary
    dictionary_ = deepcopy(dictionary)
    for key in dictionary.keys():
        if key in exclude_keys or key[0] == '_':
            del dictionary_[key]
        elif isinstance(dictionary[key], dict):
            dictionary_[key] = filter_dict(dictionary_[key], exclude_keys)
    return dictionary_


class APIBaseObject(object):
    """Base class for all API objects"""

    def __init__(self):
        #self.type, self._api_inheritance = get_class_names(self)
        pass
        
    def to_JSON(self, indent=2, exclude_keys=None):
        return json.dumps(self, default=lambda o: filter_dict(o.__dict__, exclude_keys), 
                          sort_keys=True, indent=indent)
