__author__ = 'aymgal'


from coolest.template.classes.base import APIBaseObject

__all__ = [
    'PosteriorStatistics',
    'Prior', 
    'GaussianPrior', 
    'LogNormalPrior',
    'UniformPrior',
]


class PosteriorStatistics(APIBaseObject):

    def __init__(self, mean=None, median=None, 
                 percentile_16th=None, percentile_84th=None):
        self.mean = mean
        self.median = median
        self.percentile_16th = percentile_16th
        self.percentile_84th = percentile_84th


class Prior(APIBaseObject):

    def __init__(self, ptype=None, **kwargs):
        self.type = ptype
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class GaussianPrior(Prior):

    def __init__(self, mean=None, width=None):
        super().__init__(self.__class__.__name__, 
                         mean=mean, width=width)


class LogNormalPrior(Prior):

    def __init__(self, mean=None, width=None):
        super().__init__(self.__class__.__name__, 
                         mean=mean, width=width)


class UniformPrior(Prior):

    def __init__(self, min_value=None, max_value=None):
        super().__init__(self.__class__.__name__, 
                         min_value=min_value, max_value=max_value)
