# Global model for a given system
# which may be defined by multiple Galaxies
# each defined by several mass models and light models 


from lensmodelapi.galaxy_list import GalaxyList
# from lensmodelapi.coordinates import Coordinates
from lensmodelapi.data import Data


class LensObject(object):

    def __init__(self,
                 galaxies: GalaxyList,
                 # coordinates: Coordinates,
                 data: Data = None) -> None:
        self.galaxies = galaxies
        # self.coordinates = coordinates
        self.data = data
        