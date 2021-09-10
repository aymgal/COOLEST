__author__ = 'aymgal'

from lensmodelapi.base import APIBaseObject
from lensmodelapi.lens_model import LensModel
from lensmodelapi.coordinates import Coordinates
from lensmodelapi.observation import Data, Instrument


class LensObject(APIBaseObject):
    """
    Global model for a given system
    which may be defined by multiple Galaxies
    each defined by several mass models and light models 
    """
    def __init__(self,
                 instrument: Instrument,
                 coordinates: Coordinates,
                 lens_model: LensModel,
                 data: Data = None) -> None:
        self.lens_model = lens_model
        self.instrument = instrument
        self.coordinates = coordinates
        self.data = data
        super().__init__()
        