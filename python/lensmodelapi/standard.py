__author__ = 'aymgal'


from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lens_model import LensModel
from lensmodelapi.api.observation import Observation
from lensmodelapi.api.instrument import Instrument
from lensmodelapi.api.cosmology import Cosmology


EXCLUDE_KEYS = [
    'documentation',
    'id',
    'latex_str',
    'units',
    'fixed',
    'definition_range',
]


class CoolestStandard(APIBaseObject):

    _exclude_keys = EXCLUDE_KEYS

    def __init__(self,
                 lens_model: LensModel,
                 observation: Observation,
                 instrument: Instrument,
                 cosmology: Cosmology = None):
        self.lens_model  = lens_model
        self.observation = observation
        self.instrument  = instrument
        self.cosmology   = cosmology
        self.standard = 'coolest'
        if observation.image.exists:
            mode = 'MODEL'
        else:
            mode = 'MOCK'
        self.meta = {
            'mode': mode,
        }
        