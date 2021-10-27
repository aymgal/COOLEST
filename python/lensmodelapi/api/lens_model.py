__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.galaxy_list import GalaxyList
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.coordinates import Coordinates


class LensModel(APIBaseObject):

    def __init__(self, 
                 galaxies: GalaxyList,
                 regularizations: RegularizationList,
                 likelihoods: LikelihoodList,
                 coordinates: Coordinates) -> None:
        self.galaxies = galaxies
        self.regularizations = regularizations
        self.likelihoods = likelihoods
        self.coordinates = coordinates
        super().__init__()

    def update_parameter_bounds_with_obs(self, instrument):
        self.galaxies.update_parameter_bounds_with_obs(instrument)