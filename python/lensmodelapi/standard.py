__author__ = 'aymgal'


from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.observation import Observation
from lensmodelapi.api.instrument import Instrument
from lensmodelapi.api.lensing_entity_list import LensingEntityList
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.coordinates import CoordinatesOrigin
from lensmodelapi.api.cosmology import Cosmology



# TODO: excluded keys should depend on the mode: 'MOCK', 'MAP', etc...
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
                 coordinates_origin: CoordinatesOrigin,
                 lensing_entities: LensingEntityList,
                 observation: Observation,
                 instrument: Instrument,
                 cosmology: Cosmology = None,
                 likelihoods: LikelihoodList = None,
                 regularizations: RegularizationList = None,
                 metadata: dict = None):
        if coordinates_origin is None:
            coordinates_origin = CoordinatesOrigin('0', '0')
        self.coordinates_origin = coordinates_origin
        self.lensing_entities = lensing_entities
        self.observation = observation
        self.instrument  = instrument
        self.cosmology   = cosmology
        self.likelihoods = likelihoods
        self.regularizations = regularizations

        self.standard = 'coolest'
        if metadata is None:
            metadata = {}
        self.meta = metadata
        if observation.image.exists:
            mode = 'MAP'
        else:
            mode = 'MOCK'
        self.meta.update({'mode': mode})
        