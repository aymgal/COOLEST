__author__ = 'aymgal'


import numpy as np
import warnings
from astropy.io import fits

from coolest.api.profiles import light


class CompositeLightModel(object):
    """
    Given a COOLEST object, evaluates a selection of light profiles.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 entity_selection=[0], profile_selection='all'):
        entities = coolest_object.lensing_entities
        self.profile_list = []
        self.param_list = []
        self.info_list = []
        for i, entity in enumerate(entities):
            if self._selected(i, entity_selection):
                if entity.type == 'external_shear':
                    raise ValueError(f"External shear (entity index {i}) has no light model")
                for j, profile in enumerate(entity.light_model):
                    if self._selected(j, profile_selection):
                        if 'Grid' in profile.type:
                            if coolest_directory is None:
                                raise ValueError("The directory in which the COOLEST file is located "
                                                 "must be provided for loading FITS files")
                            params, fixed = self._get_grid_params(profile, coolest_directory)
                            self.profile_list.append(self._get_api_profile(profile, *fixed))
                            self.param_list.append(params)
                        else:
                            self.profile_list.append(self._get_api_profile(profile))
                            self.param_list.append(self._get_point_estimates(profile))
                        self.info_list.append((entity.name, entity.redshift))
        self.num_profiles = len(self.profile_list)
        if self.num_profiles == 0:
            raise ValueError("No light profile has been selected!")
        pixel_size = coolest_object.instrument.pixel_size
        if pixel_size is None:
            pixel_size = 1.
        self.pixel_area = pixel_size**2

    def surface_brightness(self, return_extent=False):
        """Returns the surface brightness as stored in the COOLEST file"""
        if self.num_profiles > 1:
            warnings.warn("When more than a single light profile has been selected, "
                          "the method `surface_brightness()` only considers the first profile")
        values = self.profile_list[0].surface_brightness(**self.param_list[0])
        if return_extent:
            extent = self.profile_list[0].get_extent()
            return values, extent
        return values

    def evaluate_surface_brightness(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        image = np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            flux_k = profile.evaluate_surface_brightness(x, y, **params)
            if profile.units == 'flux_per_ang':
                flux_k *= self.pixel_area
            image += flux_k
        return image

    @staticmethod
    def _get_api_profile(profile_in, *args):
        """
        Takes as input a light profile from the template submodule
        and instantites the corresponding profile from the API submodule
        """
        ProfileClass = getattr(light, profile_in.type)
        return ProfileClass(*args)

    @staticmethod
    def _get_point_estimates(profile_in):
        parameters = {}
        for name, param in profile_in.parameters.items():
            parameters[name] = param.point_estimate.value
        return parameters

    @staticmethod
    def _get_grid_params(profile_in, fits_dir):
        if profile_in.type == 'PixelatedRegularGrid':
            data = profile_in.parameters['pixels'].get_pixels(directory=fits_dir)
            parameters = {'pixels': data}
            fov_x = profile_in.parameters['pixels'].field_of_view_x
            fov_y = profile_in.parameters['pixels'].field_of_view_y
            npix_x = profile_in.parameters['pixels'].num_pix_x
            npix_y = profile_in.parameters['pixels'].num_pix_y
            fixed_parameters = (fov_x, fov_y, npix_x, npix_y)

        elif profile_in.type == 'IrregularGrid':
            x, y, z = profile_in.parameters['pixels'].get_xyz(directory=fits_dir)
            parameters = {'x': x, 'y': y, 'z': z}
            fov_x = profile_in.parameters['pixels'].field_of_view_x
            fov_y = profile_in.parameters['pixels'].field_of_view_y
            npix = profile_in.parameters['pixels'].num_pix
            fixed_parameters = (fov_x, fov_y, npix)
        return parameters, fixed_parameters

    @staticmethod
    def _selected(index, selection):
        if isinstance(selection, str) and selection.lower() == 'all':
            return True
        elif isinstance(selection, (list, tuple, np.ndarray)) and index in selection:
            return True
        elif isinstance(selection, (int, float)) and int(selection) == index:
            return True
        return False
