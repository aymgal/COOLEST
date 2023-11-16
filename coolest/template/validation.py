__author__ = 'aymgal'

import math

from coolest.template.classes.galaxy import Galaxy
from coolest.api.composable_models import ComposableMassModel

# This submodule defines routines that validate the consistency of a COOLEST instance,
# *after* it has been successfully initialized using the `json` submodule.


class Validator(object):
    """Classes that checks self-consistency of a COOLEST object.

    Parameters
    ----------
    coolest : COOLEST
        `COOLEST` instance
    coolest_dir : _type_
        Directory containing the `COOLEST` instance
    """

    def __init__(self, coolest, coolest_dir):
        self.coolest = coolest
        self.dir = coolest_dir

    def validate(self, check_point_sources=True, source_plane_tolerance=1e-3):
        """Performs consistency checks regarding some key properties of the COOLEST object.
        For instance, it checks that the pixel size of both the observation and
        the instrument are consistent.
        The checks performed here are those that cannot be handled by individual 
        class constructors called during instantiation of the COOLEST object.

        Parameters
        ----------
        check_point_sources : bool, optional
            _description_, by default True
        source_plane_tolerance : _type_, optional
            _description_, by default 1e-3
        """
        # PIXEL SIZE
        self.validate_pix_size(self.coolest)

        # LENSED vs INTRINSIC POINT SOURCE POSITIONS
        if check_point_sources:
            self.validate_point_sources(self.coolest, self.dir, source_plane_tolerance)


    @staticmethod
    def validate_pix_size(coolest):
        """Checks that the Instrument and Observation pixel sizes are consistent.

        Raises
        ------
        ValueError
            If pixel sizes are inconsistent.
        """
        instru_pix_size = coolest.instrument.pixel_size
        obs_pix_size = coolest.observation.pixels.pixel_size
        isclose_bool = math.isclose(instru_pix_size, obs_pix_size,
                                    rel_tol=1e-09, abs_tol=0.0)
        if obs_pix_size not in (0, None) and not isclose_bool:
            raise ValueError(f"Pixel size of observation ({obs_pix_size}) is inconsistent with "
                            f"the instrument pixel size ({instru_pix_size})")
        
    @staticmethod
    def validate_point_sources(coolest, coolest_dir, source_plane_tol):
        """Checks that the PointSource light profiles, if any, are self-consistent
        in terms of their point-estimate values of intrinsic and lensed positions and fluxes.

        Raises
        ------
        ValueError
            If point source lensed and intrinsic parameters are inconsistent.
        """
        # we first decide which mass model we will use to check point source consistency
        # TODO: the user may need to choose which mass model to use
        # NOTE: this routine assumes single-lens plane
        # here we select all entities that have mass profiles
        entity_selection = [i for i, entity in enumerate(coolest.lensing_entities) if len(entity.mass_model) > 0]
        mass_model = ComposableMassModel(coolest, coolest_directory=coolest_dir, 
                                         entity_selection=entity_selection,
                                         profile_selection='all')
        
        # loop over all entities to find all point source light profiles
        for i, entity in enumerate(coolest.lensing_entities):
            if not isinstance(entity, Galaxy):
                # point sources can only be in Galaxy entities
                continue
            for j, profile in enumerate(entity.light_model):
                if profile.type != 'PointSource':
                    # nothing to do if not a point source
                    continue
                elif profile.flag_contains != 'both':
                    # nothing to do if the point source does not contain
                    # both intrinsic and lensed parameters
                    continue
                
                # get lensed positions in image plane
                x_img_all = profile.parameters['x_lensed'].point_estimate.value
                y_img_all = profile.parameters['y_lensed'].point_estimate.value

                # compute corresponding position in source plane
                x_src_all, y_src_all = mass_model.ray_shooting(x_img_all, y_img_all)

                # get intrinsic position in source plane
                x_src = profile.parameters['x_intrinsic'].point_estimate.value
                y_src = profile.parameters['y_intrinsic'].point_estimate.value

                # compute the differences in source plane
                delta_x = x_src - x_src_all
                delta_y = y_src - y_src_all
                
                # check that it does not exceed the tolerance
                if delta_x**2 + delta_y**2 > source_plane_tol**2:
                    raise ValueError(f"Point source profile {j} of entity {i} "
                                     f"with both intrinsic and lensed positions "
                                     f"do not meet tolerance requirements in source plane.")
                