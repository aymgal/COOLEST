__author__ = 'aymgal'


from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.observation import Observation
from coolest.template.classes.instrument import Instrument
from coolest.template.classes.lensing_entity_list import LensingEntityList
from coolest.template.classes.regularization_list import RegularizationList
from coolest.template.classes.likelihood_list import DataLikelihoodList
from coolest.template.classes.coordinates import CoordinatesOrigin
from coolest.template.classes.cosmology import Cosmology


__all__ = ['COOLEST']


SUPPORTED_MODES = ['MOCK', 'MAP', 'DOC']

MOCK_EXCLUDE_KEYS = [
    'documentation',
    'latex_str',
    'units',
    'fixed',
    'posterior_stats',
    'definition_range',
    'likelihoods',
    'regularizations',
]

MAP_EXCLUDE_KEYS = [
    'documentation',
    'latex_str',
    'units',
    'definition_range',
]

DOC_EXCLUDE_KEYS = [
    'posterior_stats',
    'prior',
    'fixed',
    'id',
]


class COOLEST(APIBaseObject):
    """Main component of COOLEST. This object stores all relevant quantities
    to a given lens model, as a hierarchy of python objects whose attributes 
    describe the Observation, Instrument, Coordinates, Lens models, etc.

    Parameters
    ----------
    mode : str
        Mode of the stored lens model described in the COOLEST object.
        Should be one of the following:

        - `'MOCK'`: the object describes a mock observation of a lens;

        - `'MAP'`: the object describes a maximum a posteriori point estimates 
        (best-fit values) lens model, possibly including statistics 
        regarding the posterior distribution of lens model parameters;

        - `'DOC'`: the object contains all description of profiles and parameters,
        (only relevant for generating documentation products).

        The mode affects which attributes a stored in the JSON representation 
        of the COOLEST object.
        
    coordinates_origin : CoordinatesOrigin
        Instance of a CoordinatesOrigin object.
    lensing_entities : LensingEntityList
        Instance of a LensingEntityList object.
    observation : Observation
        Instance of a Observation object.
    instrument : Instrument
        Instance of a Instrument object.
    cosmology : Cosmology, optional
        Instance of a Cosmology object, by default None
    metadata : dict, optional
        Any additional data to be stored in the COOLEST format, by default None

    Raises
    ------
    ValueError
        If the provided mode is not supported.
    """

    def __init__(self,
                 mode: str,
                 coordinates_origin: CoordinatesOrigin,
                 lensing_entities: LensingEntityList,
                 observation: Observation,
                 instrument: Instrument,
                 cosmology: Cosmology = None,
                 likelihoods: DataLikelihoodList = None,
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

        self.standard = 'COOLEST'
        if metadata is None:
            metadata = {}
        self.meta = metadata

    @property
    def exclude_keys(self):
        if self.mode == 'MOCK':
            return MOCK_EXCLUDE_KEYS
        elif self.mode == 'MAP':
            return MAP_EXCLUDE_KEYS
        elif self.mode == 'DOC':
            return DOC_EXCLUDE_KEYS
        else:
            return []
