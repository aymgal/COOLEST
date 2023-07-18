__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.profile import AnalyticalProfile
from coolest.template.classes import util


class LensingEntityList(list, APIBaseObject):
    """The list of components that define the lensing system.
    In COOLEST, a `LensingEntity` is an instance Galaxy or a MassField.

    Note that unique identifiers (IDs) for each profile and parameters will be 
    generated at instantiation time.

    - A given profile has a unique IDs with the following pattern:

    `{entity index}-{{massfield} or {galaxy}}-{{mass} or {light}}-{profile index}_{profile name}`

    - A given parameter has the same ID as above, just with the parameter name at the end:

    `{entity index}-{{massfield} or {galaxy}}-{{mass} or {light}}-{profile index}_{profile name}-{parameter name}`

    Parameters
    ----------
    *entities : LensingEntity instances
        As many LensingEntity instances as required
    """

    def __init__(self, *entities: Tuple[LensingEntity]):
        list.__init__(self, entities)
        APIBaseObject.__init__(self)
        self._create_all_ids()

    def get_parameter_ids(self, with_name=None):
        """Returns the list of either all parameter IDs in the model.
        or a subset of them for parameters with a specific name.

        Parameters
        ----------
        with_name : str, optional
            Parameter for which we want to get all corresponding IDs, by default None
        """
        def _selected(param_name):
            return ((with_name is None) or 
                    (with_name is not None and param_name == with_name))
        id_list = []
        for entity in self:
            for model_type in ('light', 'mass'):
                model = getattr(entity, f'{model_type}_model', None)
                if model is not None:
                    for profile in model:
                        for param_name, param in profile.parameters.items():
                            if _selected(param_name):
                                id_list.append(param.id)
        return id_list
    
    def get_parameter_from_id(self, param_id):
        """Returns the Parameter instance that has the given parameter ID. 

        Parameters
        ----------
        param_id : str
            Parameter ID

        Returns
        -------
        coolest.template.classes.parameters.Parameter
            Instance of a Parameter with ID equal to `param_ID`
        """
        # NOTE: it can be very inefficient for a large number of lensing entities
        for entity in self:
            for model_type in ('light', 'mass'):
                model = getattr(entity, f'{model_type}_model', None)
                if model is not None:
                    for profile in model:
                        for param in profile.parameters.values():
                            if param.id == param_id:
                                return param
        # if the following line is reached, then no ID has been found
        raise ValueError("Parameter with ID '{param_id}' not found in any lensing entity.")

    def _create_all_ids(self):
        for i, entity in enumerate(self):
            for model_type in ('light', 'mass'):
                model = getattr(entity, f'{model_type}_model', None)
                if model is not None:
                    for j, profile in enumerate(model):
                        if entity.type == 'Galaxy':
                            profile_id = util.galaxy_profile_to_id(model_type, profile.type, j, i)
                        elif entity.type == 'MassField':
                            profile_id = util.mass_field_profile_to_id(profile.type, j, i)
                        profile.id = profile_id
                        # if isinstance(profile, AnalyticalProfile):
                        for param_name, parameter in profile.parameters.items():
                            param_id = util.parameter_to_id(param_name, profile.id)
                            parameter.id = param_id
