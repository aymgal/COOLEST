__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.galaxy_list import GalaxyList
from lensmodelapi.api.external_shear import ExternalShear
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.coordinates import Coordinates


class LensModel(APIBaseObject):

    def __init__(self, 
                 galaxies: GalaxyList,
                 likelihoods: LikelihoodList = None,
                 external_shear: ExternalShear = None,
                 regularizations: RegularizationList = None) -> None:
        self.galaxies = galaxies
        if likelihoods is None:
            likelihoods = LikelihoodList('imaging_data')
        self.likelihoods = likelihoods
        self.external_shear = external_shear
        self.regularizations = regularizations
        super().__init__()
