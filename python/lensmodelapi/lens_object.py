__author__ = 'aymgal'

from typing import List

from lensmodelapi.base import LensModelAPIObject
from lensmodelapi.galaxy_list import GalaxyList
from lensmodelapi.galaxy import Galaxy
from lensmodelapi.coordinates import Coordinates
from lensmodelapi.observation import Observation


class LensObject(LensModelAPIObject):
    """
    Global model for a given system
    which may be defined by multiple Galaxies
    each defined by several mass models and light models 
    """
    def __init__(self,
                 galaxies: List[Galaxy],
                 coordinates: Coordinates,
                 observation: Observation = None) -> None:
        self.galaxies = GalaxyList(galaxies)
        self.coordinates = coordinates
        self.observation = observation
        super().__init__()
        