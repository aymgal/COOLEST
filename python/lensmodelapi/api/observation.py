__author__ = 'aymgal'

from lensmodelapi.api.data import Data
from lensmodelapi.api.instrument import Instrument
from lensmodelapi.api.base import APIBaseObject


class Observation(APIBaseObject):
    """Contains imaging data and instrument properties"""
    def __init__(self,
                 data: Data,
                 instrument: Instrument) -> None:
        self.data = data
        self.instrument = instrument
        super().__init__()
