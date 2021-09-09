__author__ = 'aymgal'


class Cosmology(object):

    def __init__(self, 
                 H0: float,
                 Om0: float,
                 model_name: str = 'FlatLambdaCDM') -> None:
        self.H0 = H0
        self.Om0 = Om0
        self.model_name = model_name
