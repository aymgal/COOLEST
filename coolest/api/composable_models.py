__author__ = 'aymgal'


import numpy as np
import warnings
from scipy import signal

from coolest.api import util


class BaseComposableModel(object):
    """
    Given a COOLEST object, evaluates a selection of mass or light profiles.
    """

    def __init__(self, model_type, coolest_object, coolest_directory=None, 
                 entity_selection=[0], profile_selection='all'):
        entities = coolest_object.lensing_entities
        self.profile_list, self.param_list, self.info_list \
            = self.select_profiles(model_type, entities, 
                                   entity_selection, profile_selection,
                                   coolest_directory)
        self.num_profiles = len(self.profile_list)
        if self.num_profiles == 0:
            raise ValueError("No profile has been selected!")

    def select_profiles(self, model_type, entities, 
                        entity_selection, profile_selection, 
                        coolest_directory):
        profile_list = []
        param_list = []
        info_list = []
        for i, entity in enumerate(entities):
            if self._selected(i, entity_selection):
                if model_type == 'light_model' and entity.type == 'external_shear':
                    raise ValueError(f"External shear (entity index {i}) has no light model")
                for j, profile in enumerate(getattr(entity, model_type)):
                    if self._selected(j, profile_selection):
                        if 'Grid' in profile.type:
                            if coolest_directory is None:
                                raise ValueError("The directory in which the COOLEST file is located "
                                                 "must be provided for loading FITS files")
                            params, fixed = self._get_grid_params(profile, coolest_directory)
                            profile_list.append(self._get_api_profile(model_type, profile, *fixed))
                            param_list.append(params)
                        else:
                            profile_list.append(self._get_api_profile(model_type, profile))
                            param_list.append(self._get_point_estimates(profile))
                        info_list.append((entity.name, entity.redshift))
        return profile_list, param_list, info_list

    @staticmethod
    def _get_api_profile(model_type, profile_in, *args):
        """
        Takes as input a light profile from the template submodule
        and instantites the corresponding profile from the API submodule
        """
        if model_type == 'light_model':
            from coolest.api.profiles import light
            ProfileClass = getattr(light, profile_in.type)
        elif model_type == 'mass_model':
            from coolest.api.profiles import mass
            ProfileClass = getattr(mass, profile_in.type)
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


class ComposableLightModel(BaseComposableModel):
    """
    Given a COOLEST object, evaluates a selection of light profiles.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 entity_selection=[0], profile_selection='all'):
        entities = coolest_object.lensing_entities
        super().__init__('light_model', coolest_object, 
                         coolest_directory=coolest_directory,
                         entity_selection=entity_selection,
                         profile_selection=profile_selection)
        pixel_size = coolest_object.instrument.pixel_size
        if pixel_size is None:
            self.pixel_area = 1.
        else:
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


class ComposableMassModel(BaseComposableModel):
    """
    Given a COOLEST object, evaluates a selection of light profiles.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 entity_selection=[0], profile_selection='all'):
        entities = coolest_object.lensing_entities
        super().__init__('mass_model', coolest_object, 
                         coolest_directory=coolest_directory,
                         entity_selection=entity_selection,
                         profile_selection=profile_selection)

    def evaluate_deflection(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        alpha_x, alpha_y = np.zeros_like(x), np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            a_x, a_y = profile.deflection(x, y, **params)
            alpha_x += a_x
            alpha_y += a_y
        return alpha_x, alpha_y

    def evaluate_convergence(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        psi = np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            psi += profile.convergence(x, y, **params)
        return psi

    def evaluate_magnification(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        H_xx_sum = np.zeros_like(x)
        H_xy_sum = np.zeros_like(x)
        H_yx_sum = np.zeros_like(x)
        H_yy_sum = np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            H_xx, H_xy, H_yx, H_yy = profile.hessian(x, y, **params)
            H_xx_sum += H_xx
            H_xy_sum += H_xy
            H_yx_sum += H_yx
            H_yy_sum += H_yy
        det_A = (1 - H_xx_sum) * (1 - H_yy_sum) - H_xy_sum*H_yx_sum
        mu = 1. / det_A
        return mu


class ComposableLensModel(object):
    """
    Given a COOLEST object, evaluates a selection of light profiles.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 kwargs_selection_source=None, kwargs_selection_lens_mass=None):
        self.coolest = coolest_object
        self.coord_obs = util.get_coordinates(self.coolest)
        self.lens_mass = ComposableMassModel(coolest_object, 
                                             coolest_directory,
                                             **kwargs_selection_lens_mass)
        self.source = ComposableLightModel(coolest_object, 
                                          coolest_directory,
                                          **kwargs_selection_source)

    def model_image(self, supersampling=5, convolved=True):
        obs = self.coolest.observation
        psf = self.coolest.instrument.psf
        if convolved is True and psf.type == 'PixelatedPSF':
            scale_factor = obs.pixels.pixel_size / psf.pixels.pixel_size
            supersampling_conv = int(round(scale_factor))
            print("supersampling_conv:", supersampling_conv, obs.pixels.pixel_size / psf.pixels.pixel_size)
            if supersampling_conv < 1:
                raise ValueError("PSF pixel size smaller than data pixel size")
        if supersampling < 1:
            raise ValueError("Supersampling must be >= 1")
        if convolved is True and supersampling_conv > supersampling:
            supersampling = supersampling_conv
            logging.warning("Supersampling factor adapted to the PSF pixel size")
        coord_eval = self.coord_obs.create_new_coordinates(pixel_scale_factor=1./supersampling)
        x, y = coord_eval.pixel_coordinates
        image = self.evaluate_lensed_surface_brightness(x, y)
        if convolved is True:
            if psf.type != 'PixelatedPSF':
                raise NotImplementedError
            kernel = psf.pixels.get_pixels()
            assert kernel.sum() == 1.
            if supersampling_conv == supersampling:
                # first convolve...
                image = signal.fftconvolve(image, kernel, mode='same')
                # ...then dowsnscale 
                image = util.downsampling(image, factor=supersampling)
            elif supersampling_conv == 1:
                # first dowsnscale...
                image = util.downsampling(image, factor=supersampling)
                # ...then convolve
                image = signal.fftconvolve(image, kernel, mode='same')
        elif supersampling > 1:
            image = util.downsampling(image, factor=supersampling)
        return image, self.coord_obs

    def model_residuals(self, supersampling=5, mask=None):
        model, _ = self.model_image(supersampling=supersampling, 
                                    convolved=True)
        data = self.coolest.observation.pixels.get_pixels()
        noise = self.coolest.observation.noise
        if noise.type != 'NoiseMap':
            raise NotImplementedError
        sigma = noise.noise_map.get_pixels()
        if mask is None:
            mask = np.ones_like(model)
        return ((data - model) / sigma) * mask, self.coord_obs

    def evaluate_lensed_surface_brightness(self, x, y):
        """Evaluates the surface brightness of a lensed source at given coordinates"""
        # ray-shooting
        x_rs, y_rs = self.ray_shooting(x, y)
        # evaluates at ray-shooted coordinates
        lensed_image = self.source.evaluate_surface_brightness(x_rs, y_rs)
        return lensed_image

    def ray_shooting(self, x, y):
        """evaluates the lens equation beta = theta - alpha(theta)"""
        alpha_x, alpha_y = self.lens_mass.evaluate_deflection(x, y)
        x_rs, y_rs = x - alpha_x, y - alpha_y
        return x_rs, y_rs
