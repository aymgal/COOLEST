__author__ = 'aymgal'


from coolest.template.classes.base import APIBaseObject

__all__ = [
    'PosteriorStatistics',
    'Prior', 
    'GaussianPrior', 
    'LogNormalPrior',
    'UniformPrior',
]

PRIOR_SUPPORTED_CHOICES = [
    'GaussianPrior', 
    'LogNormalPrior',
    'UniformPrior',
]


class PosteriorStatistics(APIBaseObject):
    """Object that holds low order statistics of the posterior distribution 
    of the parameter.

    Parameters
    ----------
    mean : float, optional
        Mean of the distribution, by default None
    median : float, optional
        Median of the distribution, by default None
    percentile_16th : float, optional
        16th percentile of the distribution, by default None
    percentile_84th : float, optional
        84th percentile of the distribution, by default None
    """
    
    def __init__(self, mean=None, median=None, 
                 percentile_16th=None, percentile_84th=None):
        self.mean = mean
        self.median = median
        self.percentile_16th = percentile_16th
        self.percentile_84th = percentile_84th


class Prior(APIBaseObject):
    """Generic class for a prior distribution that can be assigned
    to a parameter.

    Parameters
    ----------
    ptype : str, optional
        Type of prior, typically class name of one of the Prior class defined
        in this module, by default None
    """
    
    def __init__(self, ptype=None, **kwargs):
        self.type = ptype
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class GaussianPrior(Prior):
    """Gaussian prior.

    Parameters
    ----------
    mean : float, optional
        Mean value, by default None
    width : float, optional
        Width (standard deviation), by default None
    """
    
    def __init__(self, mean=None, width=None):
        super().__init__(self.__class__.__name__, 
                         mean=mean, width=width)


class LogNormalPrior(Prior):
    """Log-Normal prior.

    Parameters
    ----------
    mean : float, optional
        Mean value, by default None
    width : float, optional
        Width, by default None
    """
    
    def __init__(self, mean=None, width=None):
        super().__init__(self.__class__.__name__, 
                         mean=mean, width=width)


class UniformPrior(Prior):
    """Uniform prior.

    Parameters
    ----------
    min_value : float, optional
        Lower bound, by default None
    max_value : float, optional
        Upper bound, by default None
    """
    
    def __init__(self, min_value=None, max_value=None):
        super().__init__(self.__class__.__name__, 
                         min_value=min_value, max_value=max_value)
