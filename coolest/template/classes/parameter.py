# Single parameter of a profile

from typing import List

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.probabilities import Prior, PosteriorStatistics
from coolest.template.classes.grid import PixelatedRegularGrid, IrregularGrid

import numpy as np


__all__ = [
    'Parameter',
    'NonLinearParameter', 
    'LinearParameter', 
    'HyperParameter',
    'LinearParameterSet',
    'NonLinearParameterSet',
    'PixelatedRegularGridParameter',
    'IrregularGridParameter',
]


class DefinitionRange(APIBaseObject):
    """Defines the interval over which a parameter is defined.

    Parameters
    ----------
    min_value : (int, float), optional
        Lower bound of the interval (inclusive), by default None
    max_value : (int, float), optional
        Upper bound of the interval (inclusive), by default None
    """
    
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value


class PointEstimate(APIBaseObject):
    """Define a point in the parameter space.

    Parameters
    ----------
    value : float, optional
        Value of the parameter, by default None
    """
    
    def __init__(self, value=None):
        self.value = value


class Parameter(APIBaseObject):
    """Base class of a generic model parameter.

    Parameters
    ----------
    documentation : str
        Short description of the parameter.
    definition_range : DefinitionRange, optional
        Interval over which the parameter is defined, by default None
    units : str, optional
        Unit of the parameter, if any, by default None
    fixed : bool, optional
        If True, the parameter is considered fixed 
        (i.e. should not be, or has not be optimized), by default False
    point_estimate : PointEstimate, optional
        Point-estimate value of the parameter, by default None
    posterior_stats : PosteriorStatistics, optional
        Summary statistics of the marginalized posterior 
        distribution of the parameter, by default None
    prior : Prior, optional
        Prior assigned the parameter, if any, by default None
    latex_str : str, optional
        LaTeX representation of the parameter, by default None
    
    #TODO: for parameters like orientation / axis ratio, add a class method to compute
                 related quantities like ellipticity parameters.
    """
    def __init__(self, 
                 documentation: str, 
                 definition_range: DefinitionRange = None,
                 units: str = None,
                 fixed: bool = False,
                 point_estimate: PointEstimate = None,
                 posterior_stats: PosteriorStatistics = None,
                 prior: Prior = None,
                 latex_str: str = None) -> None:
        self.documentation = documentation
        self.units = units
        self.definition_range = definition_range
        self.fixed = fixed
        if not isinstance(point_estimate, PointEstimate):
            self.point_estimate = PointEstimate(point_estimate)
        else:
            self.point_estimate = point_estimate
        if posterior_stats is None:
            posterior_stats = PosteriorStatistics()
        self.posterior_stats = posterior_stats
        if prior is None:
            prior = Prior()
        self.prior = prior
        self.latex_str = latex_str
        self.id = None
        super().__init__()
        
    def set_point_estimate(self, point_estimate):
        """Set the point estimate value of the parameter.

        Parameters
        ----------
        point_estimate : int, float, list, PointEstimate
            Parameter value, or directly a PointEstimate instance.

        Raises
        ------
        ValueError
            If the provided point_estimate has not a supported type.
        ValueError
            If the parameter value is below its minimum allowed value.
        ValueError
            If the parameter value is above its maximum allowed value.
        """
        if isinstance(point_estimate, (float, int, list)):
            self.point_estimate = PointEstimate(value=point_estimate)
        elif isinstance(point_estimate, tuple):
            self.point_estimate = PointEstimate(value=list(point_estimate))
        elif isinstance(point_estimate, np.ndarray):
            self.point_estimate = PointEstimate(value=point_estimate.tolist())
        elif isinstance(point_estimate, PointEstimate):
            self.point_estimate = point_estimate
        else:
            raise ValueError("Parameter prior must be either a PointEstimate instance "
                             "or a single number (float or int) or an array (tuple, list or ndarray).")
        if self.point_estimate.value is not None:
            val = self.point_estimate.value
            min_val = self.definition_range.min_value
            max_val = self.definition_range.max_value
            if min_val is not None and np.any(np.asarray(val) < np.asarray(min_val)):
                raise ValueError(f"Value cannot be smaller than {self.definition_range.min_value}.")
            if max_val is not None and np.any(np.asarray(val) > np.asarray(max_val)):
                raise ValueError(f"Value cannot be larger than {self.definition_range.max_value}.")

    def remove_point_estimate(self):
        """Remove the current point estimate of the parameter.
        """
        self.point_estimate = PointEstimate()

    def set_posterior(self, posterior_stats):
        """Set the posterior statistics of the parameter.

        Parameters
        ----------
        posterior_stats : PosteriorStatistics
            Instance of the PosteriorStatistics object.

        Raises
        ------
        ValueError
            If the argument is not a PosteriorStatistics instance.
        """
        if not isinstance(posterior_stats, PosteriorStatistics):
            raise ValueError("Parameter prior must be a PosteriorStatistics instance.")
        self.posterior_stats = posterior_stats

    def remove_posterior(self):
        """Remove the current posterior statistics of the parameter.
        """
        self.posterior_stats = PosteriorStatistics()

    def set_prior(self, prior):
        """Associate a prior distribution to the parameter.

        Parameters
        ----------
        prior : Prior
            Instance of Prior object.

        Raises
        ------
        ValueError
            If the argument is not a Prior instance.
        """
        if not isinstance(prior, Prior):
            raise ValueError("Parameter prior must be a Prior instance.")
        self.prior = prior

    def remove_prior(self):
        """Remove the current posterior statistics of the parameter.
        """
        self.prior = Prior()

    def fix(self):
        """Set the fixed attribute to True, marking it as fixed."""
        if self.point_estimate.value is None:
            raise ValueError("Cannot fix parameter as no point estimate value has been set.")
        self.fixed = True

    def unfix(self):
        """Set the fixed attribute to False, marking as free to vary"""
        self.fixed = False


class NonLinearParameter(Parameter):
    """Define a non-linear parameter of a lens model
    
    Warning: this class may be removed in the future.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinearParameter(Parameter):
    """Define a hyper-parameter of a lens model
    
    Warning: this class may be removed in the future, as it has adds unncessary abstraction level.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HyperParameter(Parameter):
    """Define a hyper-parameter of a model"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        


class ParameterSet(Parameter):
    """Typically for analytical basis sets"""

    def __init__(self, *args, **kwargs) -> None:
        if 'point_estimate' not in kwargs or kwargs['point_estimate'] is None:
            kwargs['point_estimate'] = []
        if not isinstance(kwargs['point_estimate'], list):
            raise ValueError("For any ParameterSet, `point_estimate` must be a list of values.")
        super().__init__(*args, **kwargs)
        self.num_values = len(self.point_estimate.value)


class LinearParameterSet(ParameterSet):
    """Typically for analytical basis sets.

    Warning: this class may be removed in the future, as it has adds unncessary abstraction level.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        
class NonLinearParameterSet(ParameterSet):
    """Typically for position of point sources.
    
    Warning: this class may be removed in the future, as it has adds unncessary abstraction level."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class PixelatedRegularGridParameter(PixelatedRegularGrid):
    """Typically for pixelated profiles"""
    # TODO: implement .fixed attribute following the analytical Parameter interface

    def __init__(self, documentation, **kwargs_grid) -> None:
        self.documentation = documentation
        super().__init__(**kwargs_grid)


class IrregularGridParameter(IrregularGrid):
    """Typically for pixelated profiles"""
    # TODO: implement .fixed attribute following the analytical Parameter interface

    def __init__(self, documentation, **kwargs_grid) -> None:
        self.documentation = documentation
        super().__init__(**kwargs_grid)
        