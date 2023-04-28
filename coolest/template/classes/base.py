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


# class Fields(object):
#     """Essentially a wrapper of inspect.signature
#     to store argument names and default value in a readable json format.
#     This is mainly for the documentation website"""
#     def __init__(self, func):
#         signature = inspect.signature(func)
#         for key, parameter in signature.parameters.items():
#             setattr(self, str(parameter.name), str(parameter.default))


class APIBaseObject(object):
    """Abstract class on which all COOLEST template classes are based.
    This handles the filtering of attributes and automatic documentation attributes.

    
    """

    def __init__(self):
        """Creates a `documentation` attribute based on the docstring 
        of the child class.
        """
        #self.type, self._api_inheritance = get_class_names(self)
        if not hasattr(self, 'documentation') or self.documentation is None:
            if self.__doc__ is not None:
                self.documentation = self.__doc__.strip()
            else:
                self.documentation = ""
        # self.fields = Fields(self.__init__)
        
    def to_JSON(self, indent=2, exclude_keys=None):
        """Returns a JSON representation of `self`, filtering out specific attributes
        based on their name.

        Parameters
        ----------
        indent : int, optional
            Indentation to be used in the JSON representation, by default 2
        exclude_keys : list, optional
            List of attribute names to be excluded from the JSON representation
            (see `standard` submodule for examples), by default None
        """
        return json.dumps(self, default=lambda o: filter_dict(o.__dict__, exclude_keys), 
                          sort_keys=True, indent=indent)
