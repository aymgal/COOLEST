__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lensing_entity_list import LensingEntityList
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.coordinates import CoordinatesOrigin
from lensmodelapi.api.cosmology import Cosmology


class LensModel(APIBaseObject):

    def __init__(self, 
                 name: str,
                 lensing_entities: LensingEntityList,
                 coordinates_origin: CoordinatesOrigin = None,
                 likelihoods: LikelihoodList = None,
                 regularizations: RegularizationList = None,
                 cosmology: Cosmology = None) -> None:
        self.name = name
        self.lensing_entities = lensing_entities
        if coordinates_origin is None:
            coordinates_origin = CoordinatesOrigin('0', '0')
        self.coordinates_origin = coordinates_origin
        self.likelihoods = likelihoods
        self.regularizations = regularizations
        self.cosmology = cosmology
        super().__init__()
