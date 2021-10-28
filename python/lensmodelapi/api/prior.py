__author__ = 'aymgal'


from lensmodelapi.api.base import APIBaseObject


class Prior(APIBaseObject):

    def __init__(self, prior_type=None, **kwargs):
        self.prior_type = prior_type
        for key, value in kwargs.items():
            setattr(self, key, value)


class GaussianPrior(Prior):

    def __init__(self, mean=None, width=None):
        super().__init__(prior_type='gaussian', 
                         mean=mean, width=width)


class LogNormalPrior(Prior):

    def __init__(self, mean=None, width=None):
        super().__init__(prior_type='log-normal', 
                         mean=mean, width=width)


class UniformPrior(Prior):

    def __init__(self, min_value=None, max_value=None):
        super().__init__(prior_type='uniform', 
                         min_value=min_value, max_value=max_value)