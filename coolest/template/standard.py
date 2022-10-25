__author__ = 'aymgal'


from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.observation import Observation
from coolest.template.classes.instrument import Instrument
from coolest.template.classes.lensing_entity_list import LensingEntityList
from coolest.template.classes.regularization_list import RegularizationList
from coolest.template.classes.likelihood_list import LikelihoodList
from coolest.template.classes.coordinates import CoordinatesOrigin
from coolest.template.classes.cosmology import Cosmology


__all__ = ['COOLEST']


SUPPORTED_MODES = ['MOCK', 'MAP', 'DOC']

MOCK_EXCLUDE_KEYS = [
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
    'documentation',
    'id',
    'latex_str',
    'units',
    'definition_range',
]

DOC_EXCLUDE_KEYS = [
    'posterior_stats',
    'prior',
    'id',
    'units',
    'fixed',
    'definition_range',
]


class COOLEST(APIBaseObject):
    """
    Defines the COOLEST file.
    """

    def __init__(self,
                 mode: str,
                 coordinates_origin: CoordinatesOrigin,
                 lensing_entities: LensingEntityList,
                 observation: Observation,
                 instrument: Instrument,
                 cosmology: Cosmology = None,
                 # likelihoods: LikelihoodList = None,
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
        # self.likelihoods = likelihoods
        # self.regularizations = regularizations

        self.standard = 'COOLEST'
        if metadata is None:
            metadata = {}
        self.meta = metadata

        if self.mode == 'MOCK':
            self.exclude_keys = MOCK_EXCLUDE_KEYS
        elif self.mode == 'MAP':
            self.exclude_keys = MAP_EXCLUDE_KEYS
        elif self.mode == 'DOC':
            self.exclude_keys = DOC_EXCLUDE_KEYS
        else:
            self.exclude_keys = []
        self.exclude_keys += ['exclude_keys']
