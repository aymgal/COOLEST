__author__ = 'aymgal'

import os
import numpy as np
import math
import logging
from scipy import signal
import pandas as pd
from functools import partial

from coolest.api import util


# logging settings
logging.getLogger().setLevel(logging.WARNING)


class BaseComposableModel(object):
    """Given a COOLEST object, evaluates a selection of mass or light profiles.
    This class serves as parent for more specific classes and should not be 
    instantiated by the user.

    Parameters
    ----------
    model_type : str
        Either 'light_model' or 'mass_model'
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str, optional
        Directory which contains the COOLEST template, by default None
    load_posterior_samples : bool, optional
        If True, and if the COOLEST metadata provides it, the constructor will
        attempt to load the chain file containing posterior samples, in addition
        to point estimates for each profile parameters. Default is False.
    entity_selection : list, optional
        List of indices of the lensing entities to consider; If None, 
        selects the first entity which has a model of type model_type, by default None
    profile_selection : list, optional
        List of either lists of indices, or 'all', for selecting which (mass or light) profile 
        of a given lensing entity to consider. If None, selects all the 
        profiles of within the corresponding entity, by default None

    Raises
    ------
    ValueError
        No valid entity found or no profiles found.
    """
        
    _chain_key = "chain_file_name"
    _supported_eval_modes = ('point', 'posterior')

    def __init__(self, model_type, 
                 coolest_object, coolest_directory=None, 
                 load_posterior_samples=False,
                 entity_selection=None, profile_selection=None):
        if entity_selection is None:
            # finds the first entity that has a 'model_type' profile
            entity_selection = None
            for i, entity in enumerate(coolest_object.lensing_entities):
                if model_type == 'light_model' \
                    and entity.type == 'galaxy' \
                    and len(entity.light_model) > 0:
                    entity_selection = [i]
                    break
                elif model_type == 'mass_model' \
                    and len(entity.mass_model) > 0:
                    entity_selection = [i]
                    break
            if entity_selection is None:
                raise ValueError("No lensing entity with light profiles have been found")
            else:
                logging.warning(f"Found valid profile for lensing entity (index {i}) for model type '{model_type}'")
        if profile_selection is None:
            profile_selection = 'all'
        entities = coolest_object.lensing_entities
        self.directory = coolest_directory
        self._posterior_bool, self._csv_path = False, None
        if load_posterior_samples:
            metadata = coolest_object.meta
            if self._chain_key not in metadata:
                logging.warning(f"Metadata key '{self._chain_key}' is missing "
                                f"from COOLEST template, hence no posterior samples "
                                f"will be loaded.")
            else:
                self._posterior_bool = True
                self._csv_path = os.path.join(self.directory, metadata[self._chain_key])
        self.setup_profiles_and_params(model_type, entities, 
                                        entity_selection, profile_selection)
        self.num_profiles = len(self.profile_list)
        if self.num_profiles == 0:
            raise ValueError("No profile has been selected!")

    def setup_profiles_and_params(self, model_type, entities, 
                                  entity_selection, profile_selection):
        profile_list = []
        param_list, post_param_list = [], []
        info_list = []
        for i, entity in enumerate(entities):
            if self._selected(i, entity_selection):
                if model_type == 'light_model' and entity.type == 'external_shear':
                    raise ValueError(f"External shear (entity index {i}) has no light model")
                for j, profile in enumerate(getattr(entity, model_type)):
                    if self._selected(j, profile_selection):
                        if 'Grid' in profile.type:
                            if self.directory is None:
                                raise ValueError("The directory in which the COOLEST file is located "
                                                 "must be provided for loading FITS files.")
                            params, fixed_params = self._get_grid_params(profile, self.directory)
                            profile_list.append(self._get_api_profile(model_type, profile, *fixed_params))
                            post_params = None  # TODO: support samples for grid parameters
                        else:
                            params, post_params = self._get_regular_params(
                                profile, samples_file_path=self._csv_path
                            )
                            profile_list.append(self._get_api_profile(model_type, profile))
                        param_list.append(params)
                        post_param_list.append(post_params)
                        info_list.append((entity.name, entity.redshift))
        self.profile_list = profile_list
        self.param_list = param_list
        self.info_list = info_list
        if self._posterior_bool is True:
            post_param_list, post_weights = self._finalize_post_samples(post_param_list, self._csv_path)
            self.post_param_list = post_param_list
            self.post_weights = np.array(post_weights)
        else:
            self.post_param_list = None
            self.post_weights = None

    def estimate_center(self):
        # TODO: improve this (for now simply considers the first profile that has a center)
        for profile, params in zip(self.profile_list, self.param_list):
            if 'center_x' in params:
                center_x = params['center_x']
                center_y = params['center_y']
                logging.info(f"Picked center from profile '{profile.type}'")
                return center_x, center_y
        raise ValueError("Could not estimate a center from the composed model")

    @staticmethod
    def _get_api_profile(model_type, profile_in, *extra_profile_args):
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
        return ProfileClass(*extra_profile_args)

    @staticmethod
    def _get_regular_params(profile_in, samples_file_path=None):
        parameters = {}  # best-fit values
        samples = {} if samples_file_path else None  # posterior samples
        for name, param in profile_in.parameters.items():
            parameters[name] = param.point_estimate.value
            if samples is not None:
                # read just the column corresponding to the parameter ID
                column = pd.read_csv(
                    samples_file_path, 
                    usecols=[param.id], 
                    delimiter=',',
                )
                # TODO: take into account probability weights from nested sampling runs!
                samples[name] = list(column[param.id])
        return parameters, samples

    @staticmethod
    def _get_grid_params(profile_in, fits_dir):
        param_in = profile_in.parameters['pixels']
        if profile_in.type == 'PixelatedRegularGrid':
            data = param_in.get_pixels(directory=fits_dir)
            parameters = {'pixels': data}
            fov_x = param_in.field_of_view_x
            fov_y = param_in.field_of_view_y
            npix_x = param_in.num_pix_x
            npix_y = param_in.num_pix_y
            fixed_parameters = (fov_x, fov_y, npix_x, npix_y)

        elif profile_in.type == 'IrregularGrid':
            x, y, z = param_in.get_xyz(directory=fits_dir)
            parameters = {'x': x, 'y': y, 'z': z}
            fov_x = param_in.field_of_view_x
            fov_y = param_in.field_of_view_y
            npix = param_in.num_pix
            fixed_parameters = (fov_x, fov_y, npix)
        return parameters, fixed_parameters
    
    @staticmethod
    def _finalize_post_samples(param_list_of_samples, samples_file_path):
        """
        Takes as input the samples grouped at the leaves of the nested container structure,
        and returns a list of items each organized as self.param_list
        """
        num_profiles = len(param_list_of_samples)
        profile_0 = param_list_of_samples[0]
        num_samples = len(profile_0[list(profile_0.keys())[0]])
        samples_of_param_list = [
            [{} for _ in range(num_profiles)] for _ in range(num_samples)
        ]
        for i in range(num_samples):
            for k in range(num_profiles):
                for key in param_list_of_samples[k].keys():
                    samples_of_param_list[i][k][key] = param_list_of_samples[k][key][i]
        # also load and return the probability weights
        # read just the column corresponding to the parameter ID
        weights_key = 'probability_weights'
        column = pd.read_csv(
            samples_file_path, 
            usecols=[weights_key], 
            delimiter=',',
        )
        weights_list = list(column[weights_key])
        return samples_of_param_list, weights_list

    @staticmethod
    def _selected(index, selection):
        if isinstance(selection, str) and selection.lower() == 'all':
            return True
        elif isinstance(selection, (list, tuple, np.ndarray)) and index in selection:
            return True
        elif isinstance(selection, (int, float)) and int(selection) == index:
            return True
        return False

    def _check_eval_mode(self, mode):
        if mode not in self._supported_eval_modes:
            raise NotImplementedError(
                f"Only evaluation modes "
                f"{self._supported_eval_modes} are supported "
                f"(received '{mode}')."
        )


class ComposableLightModel(BaseComposableModel):
    """Given a COOLEST object, evaluates a selection of entity and their light profiles.

    Parameters
    ----------
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str, optional
        Directory which contains the COOLEST template, by default None
    entity_selection : list, optional
        List of indices of the lensing entities to consider; If None, 
        selects the first entity that has a light model, by default None
    profile_selection : list, optional
        List of either lists of indices, or 'all', for selecting which light profile 
        of a given lensing entity to consider. If None, selects all the 
        profiles of within the corresponding entity, by default None

    Raises
    ------
    ValueError
        No valid entity found or no profiles found.
    """

    def __init__(self, coolest_object, coolest_directory=None, **kwargs_selection):
        super().__init__('light_model', coolest_object, 
                         coolest_directory=coolest_directory,
                         **kwargs_selection)
        pixel_size = coolest_object.instrument.pixel_size
        if pixel_size is None:
            self.pixel_area = 1.
        else:
            self.pixel_area = pixel_size**2

    def surface_brightness(self, return_extra=False):
        """Returns the surface brightness as stored in the COOLEST file"""
        if self.num_profiles > 1:
            logging.warning("When more than a single light profile has been selected, "
                            "the method `surface_brightness()` only considers the first profile")
        profile = self.profile_list[0]
        values = profile.surface_brightness(**self.param_list[0])
        if return_extra:
            extent = profile.get_extent()
            coordinates = profile.get_coordinates()
            return values, extent, coordinates
        return values

    def evaluate_surface_brightness(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        image = np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            flux_k = profile.evaluate_surface_brightness(x, y, **params)
            if profile.units == 'per_ang':
                flux_k *= self.pixel_area
            image += flux_k
        return image


class ComposableMassModel(BaseComposableModel):
    """Given a COOLEST object, evaluates a selection of entity and their mass profiles.

    Parameters
    ----------
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str, optional
        Directory which contains the COOLEST template, by default None
    entity_selection : list, optional
        List of indices of the lensing entities to consider; If None, 
        selects the first entity that has a mass model, by default None
    profile_selection : list, optional
        List of either lists of indices, or 'all', for selecting which mass profile 
        of a given lensing entity to consider. If None, selects all the 
        profiles of within the corresponding entity, by default None

    Raises
    ------
    ValueError
        No valid entity found or no profiles found.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 load_posterior_samples=False,
                 **kwargs_selection):
        super().__init__('mass_model', coolest_object, 
                         coolest_directory=coolest_directory,
                         load_posterior_samples=load_posterior_samples,
                         **kwargs_selection)

    def evaluate_potential(self, x, y, mode='point', last_n_samples=None):
        """Evaluates the lensing potential field at given coordinates"""
        self._check_eval_mode(mode)
        if mode == 'point' or self._posterior_bool is False:
            return self._eval_pot_point(x, y, self.param_list)
        elif mode == 'posterior':
            return self._eval_pot_posterior(x, y, self.post_param_list, last_n_samples)

    def _eval_pot_point(self, x, y, param_list):
        psi = np.zeros_like(x)
        for k, profile in enumerate(self.profile_list):
            psi += profile.potential(x, y, **param_list[k])
        return psi
    
    def _eval_pot_posterior(self, x, y, param_list, last_n_samples):
        # map the point function at each sample
        use_all_samples = last_n_samples is None or last_n_samples <= 0
        val_list = param_list if use_all_samples else param_list[-last_n_samples:]
        mapped = map(partial(self._eval_pot_point, x, y), val_list)
        return np.array(list(mapped))
    
    def fermat_potential(self, x, y, x_src, y_src, mode='point', last_n_samples=None):
        """Computes the Fermat potential for image (x, y) and source position (x_src, y_src)
        """
        # gravitational term
        psi = self.evaluate_potential(x, y, mode=mode, last_n_samples=last_n_samples)
        # geometric term
        geo = ((x - x_src)**2 + (y - y_src)**2) / 2.
        geo = np.broadcast_to(geo, psi.shape)  # makes sure geo has same shape as psi
        return geo - psi
    
    def evaluate_deflection(self, x, y):
        """Evaluates the lensing deflection field at given coordinates"""
        alpha_x, alpha_y = np.zeros_like(x), np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            a_x, a_y = profile.deflection(x, y, **params)
            alpha_x += a_x
            alpha_y += a_y
        return alpha_x, alpha_y

    def evaluate_convergence(self, x, y):
        """Evaluates the lensing convergence (i.e., 2D mass density) at given coordinates"""
        kappa = np.zeros_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            kappa += profile.convergence(x, y, **params)
        return kappa

    def evaluate_hessian(self, x, y):
        """Evaluates the lensing Hessian components at given coordinates"""
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
        return H_xx_sum, H_xy_sum, H_yx_sum, H_yy_sum
    
    def evaluate_jacobian(self, x, y):
        """Evaluates the lensing Jacobian (d beta / d theta)  at given coordinates"""
        H_xx, H_xy, H_yx, H_yy = self.evaluate_hessian(x, y)
        A = np.array([[1 - H_xx, -H_xy], [-H_yx, 1 - H_yy]])
        return A
    
    def evaluate_magnification(self, x, y):
        """Evaluates the lensing magnification at given coordinates"""
        H_xx, H_xy, H_yx, H_yy = self.evaluate_hessian(x, y)
        det_A = (1 - H_xx) * (1 - H_yy) - H_xy*H_yx
        mu = 1. / det_A
        return mu

    def ray_shooting(self, x, y):
        """evaluates the lens equation beta = theta - alpha(theta)"""
        alpha_x, alpha_y = self.evaluate_deflection(x, y)
        x_rs, y_rs = x - alpha_x, y - alpha_y
        return x_rs, y_rs


class ComposableLensModel(object):
    """Given a COOLEST object, evaluates a selection of entity and 
    their mass and light profiles, typically to construct an image of the lens.

    Parameters
    ----------
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str, optional
        Directory which contains the COOLEST template, by default None
    entity_selection : list, optional
        List of indices of the lensing entities to consider; If None, 
        selects the first entity that has a light/mass model, by default None
    profile_selection : list, optional
        List of either lists of indices, or 'all', for selecting which light/mass profile 
        of a given lensing entity to consider. If None, selects all the 
        profiles of within the corresponding entity, by default None

    Raises
    ------
    ValueError
        No valid entity found or no profiles found.
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 kwargs_selection_source=None, kwargs_selection_lens_mass=None):
        self.coolest = coolest_object
        self.coord_obs = util.get_coordinates(self.coolest)
        self.directory = coolest_directory
        if kwargs_selection_source is None:
            kwargs_selection_source = {}
        if kwargs_selection_lens_mass is None:
            kwargs_selection_lens_mass = {}
        self.lens_mass = ComposableMassModel(coolest_object, 
                                             coolest_directory,
                                             **kwargs_selection_lens_mass)
        self.source = ComposableLightModel(coolest_object, 
                                          coolest_directory,
                                          **kwargs_selection_source)

    def model_image(self, supersampling=5, convolved=True, super_convolution=True):
        """generates an image of the lens based on the selected model components"""
        obs = self.coolest.observation
        psf = self.coolest.instrument.psf
        if convolved is True and psf.type == 'PixelatedPSF':
            scale_factor = obs.pixels.pixel_size / psf.pixels.pixel_size
            supersampling_conv = int(round(scale_factor))
            if not math.isclose(scale_factor, supersampling_conv):
                raise ValueError(f"PSF supersampling ({scale_factor}) not close to an integer?")
            if supersampling_conv < 1:
                raise ValueError("PSF pixel size smaller than data pixel size")
        if supersampling < 1:
            raise ValueError("Supersampling must be >= 1")
        if convolved is True and supersampling_conv > supersampling:
            supersampling = supersampling_conv
            logging.warning(f"Supersampling adapted to the PSF pixel size ({supersampling})")
        coord_eval = self.coord_obs.create_new_coordinates(pixel_scale_factor=1./supersampling)
        x, y = coord_eval.pixel_coordinates
        image = self.evaluate_lensed_surface_brightness(x, y)
        if convolved is True:
            if psf.type != 'PixelatedPSF':
                raise NotImplementedError
            kernel = psf.pixels.get_pixels(directory=self.directory)
            kernel_sum = kernel.sum()
            if not math.isclose(kernel_sum, 1., abs_tol=1e-3):
                kernel /= kernel_sum
                logging.warning(f"PSF kernel is not normalized (sum={kernel_sum}), "
                                f"so it has been normalized before convolution")
            if np.isnan(image).any():
                np.nan_to_num(image, copy=False, nan=0., posinf=None, neginf=None)
                logging.warning("Found NaN values in image prior to convolution; "
                                "they have been replaced by zeros.")
            if super_convolution and supersampling_conv == supersampling:
                # first convolve then downscale
                image = signal.fftconvolve(image, kernel, mode='same')
                image = util.downsampling(image, factor=supersampling)
            else:
                # first downscale then convolve
                image = util.downsampling(image, factor=supersampling)
                image = signal.fftconvolve(image, kernel, mode='same')
        elif supersampling > 1:
            image = util.downsampling(image, factor=supersampling)
        return image, self.coord_obs

    def model_residuals(self, mask=None, **model_image_kwargs):
        """computes the normalized residuals map as (data - model) / sigma"""
        model, _ = self.model_image(**model_image_kwargs)
        data = self.coolest.observation.pixels.get_pixels(directory=self.directory)
        noise = self.coolest.observation.noise
        if noise.type != 'NoiseMap':
            raise NotImplementedError
        sigma = noise.noise_map.get_pixels(directory=self.directory)
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
        return self.lens_mass.ray_shooting(x, y)
