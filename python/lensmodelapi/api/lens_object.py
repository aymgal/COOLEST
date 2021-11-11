__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lens_model import LensModel
from lensmodelapi.api.observation import Data, Instrument


class LensObject(APIBaseObject):
    """
    Global model for a given system
    which may be defined by multiple Galaxies
    each defined by several mass models and light models 
    """
    def __init__(self,
                 name: str,
                 lens_model: LensModel,
                 instrument: Instrument = None,
                 data: Data = None) -> None:
        self.name = name
        self.lens_model = lens_model
        self.instrument = instrument
        self.data = data
        super().__init__()
        
    def update_parameter_bounds(self):
        """
        Based on the e.g. field-of-view, will update the allowed range
        for certain parameters
        """
        self.lens_model.update_parameter_bounds_with_obs(self.instrument)
        