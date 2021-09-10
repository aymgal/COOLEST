__author__ = 'aymgal'


import inspect


def get_class_names(instance):
    class_names = [c.__name__ for c in inspect.getmro(instance.__class__)]
    return class_names[0], ' < '.join(class_names)


class LensModelAPIObject(object):
    """Base class for all API objects"""

    def __init__(self):
        self.api_type, self.api_inheritance = get_class_names(self)
