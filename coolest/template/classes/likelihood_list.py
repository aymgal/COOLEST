__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.likelihood import Likelihood
from coolest.template.classes.base import APIBaseObject

class DataLikelihoodList(list, APIBaseObject):

    """
    A list all likelihood terms used during lens model parameters optimization. 
    Only applicable in the 'MAP' mode.
    """

    def __init__(self, *likelihoods: Tuple[Likelihood]) -> None:
        list.__init__(self, likelihoods)
        APIBaseObject.__init__(self)
