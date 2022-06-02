__author__ = 'aymgal'


from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.observation import Observation
from lensmodelapi.api.instrument import Instrument
from lensmodelapi.api.lensing_entity_list import LensingEntityList
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.coordinates import CoordinatesOrigin
from lensmodelapi.api.cosmology import Cosmology



SUPPORTED_MODES = ['MOCK', 'MAP']

MOCK_EXCLUDE_KEYS = [
    'exclude_keys',
    'documentation',
    'id',
    'latex_str',
    'units',
    'fixed',
    'definition_range',
    'likelihoods',
    'regularizations',
]

MAP_EXCLUDE_KEYS = [
    'exclude_keys',
    'documentation',
    'id',
    'latex_str',
    'units',
    'definition_range',
]


class CoolestStandard(APIBaseObject):

    def __init__(self,
                 mode: str,
                 coordinates_origin: CoordinatesOrigin,
                 lensing_entities: LensingEntityList,
                 observation: Observation,
                 instrument: Instrument,
                 cosmology: Cosmology = None,
                 likelihoods: LikelihoodList = None,
                 # regularizations: RegularizationList = None,
                 metadata: dict = None):
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"COOLEST mode '{mode}' must be in {SUPPORTED_MODES}")
        self.mode = mode
        if coordinates_origin is None:
            coordinates_origin = CoordinatesOrigin('0', '0')
        self.coordinates_origin = coordinates_origin
        self.lensing_entities = lensing_entities
        self.observation = observation
        self.instrument  = instrument
        self.cosmology   = cosmology
        self.likelihoods = likelihoods
        # self.regularizations = regularizations

        self.standard = 'coolest'
        if metadata is None:
            metadata = {}
        self.meta = metadata
        if self.mode != 'MOCK' and not observation.image.exists:
            raise ValueError("The mode is not 'MOCK' but the imaging data is not provided!")
        self.meta.update({'mode': mode})

        if self.mode == 'MOCK':
            self.exclude_keys = MOCK_EXCLUDE_KEYS
        elif self.mode == 'MAP':
            self.exclude_keys = MAP_EXCLUDE_KEYS
        else:
            self.exclude_keys = []
