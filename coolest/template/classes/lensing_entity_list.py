__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.profile import AnalyticalProfile
from coolest.template.classes import util


class LensingEntityList(list, APIBaseObject):

    """
    The list of components that define the lensing system.
    In COOLEST, a "lensing entity" means either a galaxy, or an external shear component.
    """

    def __init__(self, *entities: Tuple[LensingEntity]):
        list.__init__(self, entities)
        APIBaseObject.__init__(self)
        self._create_all_ids()

    def num_sources():
        raise NotImplementedError("Couting number of source galaxies is not yet implemented.")

    def num_lenses():
        raise NotImplementedError("Couting number of source galaxies is not yet implemented.")

    def num_external_shear():
        raise NotImplementedError("Couting number of external shear is not yet implemented.")

    def _create_all_ids(self):
        for i, entity in enumerate(self):
            for model_type in ['light', 'mass']:
                model = getattr(entity, f'{model_type}_model', None)
                if model is not None:
                    for j, profile in enumerate(model):
                        if entity.type == 'Galaxy':
                            profile_id = util.galaxy_profile_to_id(model_type, profile.type, j, i)
                        elif entity.type == 'ExternalShear':
                            profile_id = util.ext_shear_profile_to_id(profile.type, j, i)
                        profile.id = profile_id
                        if isinstance(profile, AnalyticalProfile):
                            for param_name, parameter in profile.parameters.items():
                                param_id = f'{profile.id}-{param_name}'
                                parameter.id = param_id
