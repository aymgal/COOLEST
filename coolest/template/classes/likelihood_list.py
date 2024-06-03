__author__ = 'aymgal'

from copy import deepcopy
from typing import Tuple

from coolest.template.classes.likelihood import Likelihood, SUPPORTED_CHOICES
from coolest.template.classes.base import APIBaseObject

class DataLikelihoodList(list, APIBaseObject):

    """
    A list all likelihood terms used during lens model parameters optimization. 
    Only applicable in the 'MAP' mode.
    """

    def __init__(self, *likelihoods: Tuple[Likelihood]) -> None:
        # check that there is no duplicate likelihood type
        unique_choices = deepcopy(SUPPORTED_CHOICES)
        for ll in likelihoods:
            if ll.type in unique_choices:
                unique_choices.remove(ll.type)
            else:
                raise ValueError(f"There cannot be more than one likelihood type '{ll.type}'.")
        list.__init__(self, likelihoods)
        APIBaseObject.__init__(self)
    
    def index(self, likelihood_type):
        """Override the parent class to look for a likelihood from its string type.

        Parameters
        ----------
        likelihood_type : string
            Type of likelihood
        """
        found = False
        for i, ll in enumerate(self):
            if ll.type == likelihood_type:
                return i
        raise ValueError(f"Likelihood '{likelihood_type}' is not in the likelihood list.")

    def check_consistency_with_observation(self, observation):
        for ll in self:
            ll.check_consistency_with_observation(observation)
        