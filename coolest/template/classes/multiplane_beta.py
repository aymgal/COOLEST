# Multiplane beta classes for multi-plane lensing systems

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.parameter import Parameter
from astropy.cosmology import FlatLambdaCDM


__all__ = [
    'MultiPlaneBeta',
    'MultiPlaneBetaList',
]


class MultiPlaneBeta(APIBaseObject):
    """
    Defines the lensing coupling coefficient beta between two lensing planes
    in a multi-plane lens system.

    Parameters
    ----------
    from_id : str
        ID of the foreground lensing plane (typically redshift as string).
    to_id : str
        ID of the background lensing plane or source (typically redshift as string).
    beta : str, float, or Parameter
        Either:
        - "auto" to compute from cosmology and redshifts
        - a fixed float value
        - a COOLEST Parameter instance with point estimate and posterior statistics
    """

    def __init__(self, from_id: str, to_id: str, beta):
        super().__init__()
        # from_id / to_id should be redshift-based identifiers (stringified floats)
        self.from_id = from_id
        self.to_id = to_id
        # wrap numeric betas into Parameter instances so they behave like other params
        if isinstance(beta, (int, float)):
            p = Parameter(documentation=f"beta {from_id}->{to_id}", point_estimate=beta)
            p.id = f"beta-{from_id}-{to_id}"
            self.beta = p
        elif isinstance(beta, Parameter):
            # ensure id is set
            if beta.id is None:
                beta.id = f"beta-{from_id}-{to_id}"
            self.beta = beta
            beta.latex_str = f"$\\beta-{from_id}-{to_id}$"
        else:
            # keep strings such as 'auto' as-is
            self.beta = beta

    def set_beta_parameter_id(self):
        """Ensure parameter ID is set if beta is a Parameter instance."""
        bp = getattr(self, 'beta', None)
        if isinstance(bp, Parameter) and bp.id is None:
            bp.id = f"beta-{self.from_id}-{self.to_id}"


class MultiPlaneBetaList(list, APIBaseObject):
    """
    List of MultiPlaneBeta objects defining all plane-to-plane couplings
    in a multi-plane lens system.
    """

    def __init__(self, betas=None):
        list.__init__(self, betas or [])
        APIBaseObject.__init__(self)

    def get(self, from_id, to_id):
        """Retrieve a beta entry by from and to plane IDs.
        
        Parameters
        ----------
        from_id : str
            ID of the foreground plane
        to_id : str
            ID of the background plane or source
            
        Returns
        -------
        MultiPlaneBeta or None
            The beta entry if found, otherwise None
        """
        for b in self:
            if b.from_id == from_id and b.to_id == to_id:
                return b
        return None
    
    def get_using_param_id(self, id):
        """Retrieve a beta entry by its parameter ID (if beta is a Parameter).
        
        Parameters
        ----------
        id : str
            Parameter ID to look for
            
        Returns
        -------
        MultiPlaneBeta or None
            The beta entry if found, otherwise None
        """
        for b in self:
            bp = getattr(b, 'beta', None)
            if isinstance(bp, Parameter) and bp.id == id:
                return b
        return None

    
    def get_all_beta_ids(self):
        """Returns all beta ids from list

        Returns
        -------
        param_id_list
            List of parameter ids corresponding to the betas in the list
        """
        param_id_list = [b.beta.id for b in self]
        return param_id_list

    def normalize(self):
        """Ensure all beta entries have their parameter IDs set."""
        for b in self:
            if hasattr(b, 'set_beta_parameter_id'):
                b.set_beta_parameter_id()

    def resolve_beta(self, from_id, to_id, lensing_entities, cosmology):
        """Retrieve or compute a beta value between two planes.
        
        Parameters
        ----------
        from_id : str
            ID of the foreground plane (redshift-based)
        to_id : str
            ID of the background plane (redshift-based)
        lensing_entities : LensingEntityList
            List of lensing entities to look up redshifts
        cosmology : Cosmology
            Cosmology object for beta computation
            
        Returns
        -------
        float
            The computed or stored beta value
        """
        entry = self.get(from_id, to_id)
        
        if entry is None or entry.beta == "auto":
            return self._compute_beta_from_redshifts(from_id, to_id, lensing_entities, cosmology)
        
        beta = entry.beta
        
        if hasattr(beta, "point_estimate"):
            return beta.point_estimate.value
        
        return float(beta)

    @staticmethod
    def _compute_beta_from_redshifts(from_id, to_id, lensing_entities, cosmology):
        """Compute beta from redshifts using cosmology.
        
        Parameters
        ----------
        from_id : str
            Redshift ID of foreground plane
        to_id : str
            Redshift ID of background plane
        lensing_entities : LensingEntityList
            List of entities (for reference, though not used here)
        cosmology : Cosmology
            Cosmology object
            
        Returns
        -------
        float
            Computed beta value
        """
        # Parse redshifts from IDs
        try:
            z_i = float(from_id)
            z_j = float(to_id)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot parse redshifts from IDs: {from_id}, {to_id}")
        
        if z_j <= z_i:
            raise ValueError("Beta requires increasing redshift ordering")
        
        if cosmology.astropy_name != "FlatLambdaCDM":
            raise NotImplementedError(
                f"Astropy cosmology '{cosmology.astropy_name}' not supported"
            )
        
        cm = FlatLambdaCDM(H0=cosmology.H0, Om0=cosmology.Om0)
        
        # Get maximum redshift from entities
        z_n = max(e.redshift for e in lensing_entities)
        
        D_n = cm.angular_diameter_distance(z_n)
        D_ij = cm.angular_diameter_distance_z1z2(z_i, z_j)
        D_in = cm.angular_diameter_distance_z1z2(z_i, z_n)
        D_j = cm.angular_diameter_distance(z_j)
        
        return float((D_ij * D_n) / (D_in * D_j))
