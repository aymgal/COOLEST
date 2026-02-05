__author__ = 'aymgal'

from typing import Tuple

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.lensing_entity import LensingEntity
from coolest.template.classes.parameter import Parameter
from coolest.template.classes import util
from astropy.cosmology import FlatLambdaCDM


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
    multiplane_betas : list of beta values between entities
    """

    def __init__(self, *entities: Tuple[LensingEntity], multiplane_betas=None):
        list.__init__(self, entities)
        APIBaseObject.__init__(self)

        self._create_all_ids()

        # NEW
        self.multiplane_betas = multiplane_betas or MultiPlaneBetaList()
        # self.multiplane_betas = multiplane_betas or MultiPlaneBetaList()

    def get_parameters(self, with_name=None, with_fixed=True):
        """Returns the list of either all parameters in the model, 
        or only a subset of them for parameters with a specific name.

        Parameters
        ----------
        with_name : str, optional
            Parameter for which we want to get all corresponding IDs (default: None).
        with_fixed : bool, optional
            If True, includes also fixed parameters (default: True).

        Returns
        -------
        list
            List of parameter instances
        """
        def _selected(param_name, param):
            # below we check that `param` is a Parameter instance because Grid-like parameters
            # do not have (yet) the possibility to be fixed (no fixed attribute).
            is_fixed = False if not isinstance(param, Parameter) else param.fixed
            ignored_if_fixed = not with_fixed and is_fixed
            if (with_name is None) or (param_name == with_name):
                return False if ignored_if_fixed else True
            else:
                return False
        param_list = []
        for entity in self:
            for model_type in ('light', 'mass'):
                model = getattr(entity, f'{model_type}_model', None)
                if model is not None:
                    for profile in model:
                        for param_name, param in profile.parameters.items():
                            if _selected(param_name, param):
                                param_list.append(param)
        return param_list
    
    def get_parameter_ids(self, with_name=None, with_fixed=True):
        """Returns the list of either all parameter IDs in the model, 
        or only a subset of them for parameters with a specific name.

        Parameters
        ----------
        with_name : str, optional
            Parameter for which we want to get all corresponding IDs (default: None).
        with_fixed : bool, optional
            If True, includes also fixed parameters (default: True).

        Returns
        -------
        list
            List of IDs (strings)
        """
        return [p.id for p in self.get_parameters(with_name=with_name, with_fixed=with_fixed)]
    
    def get_parameter_from_id(self, param_id):
        """Returns the Parameter instance that has the given parameter ID, or None.

        Parameters
        ----------
        param_id : str
            Parameter ID

        Returns
        -------
        coolest.template.classes.parameters.Parameter or None
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
        return None
        #raise ValueError("Parameter with ID '{param_id}' not found in any lensing entity.")

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
                        for param_name, parameter in profile.parameters.items():
                            param_id = util.parameter_to_id(param_name, profile.id)
                            parameter.id = param_id
                            
    def add_beta(self, from_entity_id, to_entity_id, beta):
        self.multiplane_betas.append(
            MultiPlaneBeta(from_entity_id, to_entity_id, beta)
        )

    def get_beta(self, from_entity_id, to_entity_id):
        entry = self.multiplane_betas.get(from_entity_id, to_entity_id)
        if entry is None:
            return None
        return entry.beta

    def resolve_beta(self, from_entity_id, to_entity_id, cosmology):
        entry = self.multiplane_betas.get(from_entity_id, to_entity_id)
    
        if entry is None or entry.beta == "auto":
            return self._compute_beta_from_redshifts(from_entity_id, to_entity_id, cosmology)
    
        beta = entry.beta
    
        if hasattr(beta, "point_estimate"):
            return beta.point_estimate.value
    
        return float(beta)

    def get_entity_by_name(self, entity_id):
        for e in self:
            if getattr(e, "name", None) == entity_id:
                return e
        raise KeyError(f"Entity ID not found: {entity_id}")

    def _compute_beta_from_redshifts(self, from_id, to_id, cosmology):
        e_i = self.get_entity_by_name(from_id)
        e_j = self.get_entity_by_name(to_id)
    
        z_i = e_i.redshift
        z_j = e_j.redshift
    
        if z_j <= z_i:
            raise ValueError("Beta requires increasing redshift ordering")
    
        if cosmology.astropy_name != "FlatLambdaCDM":
                raise NotImplementedError(
                    f"Astropy cosmology '{self.astropy_name}' not supported"
                )
    
        cm = FlatLambdaCDM(
                H0=cosmology.H0,
                Om0=cosmology.Om0)
        z_n = max(e.redshift for e in self)
    
        D_n  = cm.angular_diameter_distance(z_n)
        D_ij = cm.angular_diameter_distance_z1z2(z_i, z_j)
        D_in = cm.angular_diameter_distance_z1z2(z_i, z_n)
        D_j = cm.angular_diameter_distance(z_j)
    
        return (D_ij * D_n) / (D_in * D_j)

class MultiPlaneBeta(APIBaseObject):
    """
    Defines the lensing coupling coefficient beta between two lensing entities
    in a multi-plane lens system.

    Parameters
    ----------
    from_id : str
        ID of the foreground lensing entity.
    to_id : str
        ID of the background lensing entity (or source).
    beta : str, float, or Parameter
        Either:
        - "auto" to compute from cosmology and redshifts
        - a fixed float value
        - a COOLEST Parameter instance
    """

    def __init__(self, from_id: str, to_id: str, beta):
        super().__init__()
        self.from_id = from_id
        self.to_id = to_id
        self.beta = beta


class MultiPlaneBetaList(list, APIBaseObject):
    """
    List of MultiPlaneBeta objects defining all plane-to-plane couplings.
    """

    def __init__(self, betas=None):
        list.__init__(self, betas or [])
        APIBaseObject.__init__(self)

    def get(self, from_id, to_id):
        for b in self:
            if b.from_id == from_id and b.to_id == to_id:
                return b
        return None
