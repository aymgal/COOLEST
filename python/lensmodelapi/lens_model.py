__author__ = 'aymgal'

from typing import List

from lensmodelapi.base import APIBaseObject
from lensmodelapi.galaxy_list import GalaxyList
from lensmodelapi.galaxy import Galaxy
from lensmodelapi.regularization_list import RegularizationList


class LensModel(APIBaseObject):

    def __init__(self, 
                 galaxies: List[Galaxy],
                 regularizations: List[str]) -> None:
        self.galaxies = GalaxyList(galaxies)
        self.regularizations = RegularizationList(regularizations)
        super().__init__()
