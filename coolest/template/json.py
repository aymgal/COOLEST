import os
import json
import jsonpickle
import math

from coolest.template.standard import COOLEST
from coolest.template.lazy import *
from coolest.template.classes.parameter import PointEstimate, PosteriorStatistics, Prior
from coolest.template.info import all_supported_choices as support


__all__ = ['JSONSerializer']


class JSONSerializer(object):
    """Object that write a COOLEST object to a JSON template file,
    or loads the content of a JSON template file in the COOLEST format.

    For reading, either a plain JSON format or the one generated via `jsonpickle` can be provided.
    For the latter, the JSON file should end with the suffix `'_pyAPI'` (before the .json extension).

    NOTE: the support for reading the template with `jsonpickle` will probably 
    be suppressed in the future. Hence we advise users to work with the 
    pure JSON template files instead.
    
    Parameters
    ----------
    file_path_no_ext : str
        Path to the JSON template, or the one to be created.
        It should NOT include the .json extension nor the optional '_pyAPI' suffix
    obj : object, optional
        Instance of the COOLEST object (from the `standard` module) 
        to be encoded, by default None
    indent : int, optional
        Number of spaces used to indent lines in the JSON file, by default 2
    check_external_files : bool, optional
        If True, will check the existence of external (e.g., FITS files) 
        specified within the JSON template, by default True

    Raises
    ------
    ValueError
        If the provided path to the JSON file is not an absolute path
    ValueError
        If the provided path contains the .json extension
    """

    # suffix to filename to distinguish files that can be read using jsonpickle
    _api_suffix = '_pyAPI'

    def __init__(self,
                 file_path_no_ext: str, 
                 obj: object = None, 
                 indent: int = 2,
                 check_external_files: bool = True) -> None:
        if not os.path.isabs(file_path_no_ext):
            raise ValueError("Path to JSON file must be an absolute path")
        if file_path_no_ext[-5:].lower() == '.json':
            raise ValueError("The provided template name should not contain the JSON extension")
        self.path = file_path_no_ext
        self._json_dir = os.path.dirname(file_path_no_ext)
        self.obj = obj
        self.indent = indent
        self._check_files = check_external_files

    def dump_simple(self, exclude_keys=None):
        """Write to disk the template file, in plain JSON format.

        Parameters
        ----------
        exclude_keys : bool, optional
            List of class attributes that should not be included 
            in the JSON file, by default None
        """
        if exclude_keys is None:
            exclude_keys = self.obj.exclude_keys
        json_path = self.path + '.json'
        with open(json_path, 'w') as f:
            f.write(self.obj.to_JSON(indent=self.indent, exclude_keys=exclude_keys))

    def dump_jsonpickle(self):
        """Write to disk the template file, using the `jsonpickle` package

        WARNING: this feature may be dropped in the future.
        """
        json_path = self.path + self._api_suffix + '.json'
        result = jsonpickle.encode(self.obj, indent=self.indent)
        with open(json_path, 'w') as f:
            f.write(result)

    def load(self, skip_jsonpickle=False, validate=True, verbose=True):
        """Read the JSON template file and build up the corresponding COOLEST object.
        It will first try to load the '_pyAPI' template if it exists using `jsonpickle`, 
        otherwise it will fall back to reading the pure json template.

        Parameters
        ----------
        skip_jsonpickle : bool, optional
            If True, will not try to read the _pyAPI template with jsonpickle first, by default False
        verbose : bool, optional
            If True, prints useful output for debugging, by default False

        Returns
        -------
        COOLEST object
            COOLEST object that corresponds to the JSON template
        """
        json_path = self.path + '.json'
        jsonpickle_path = self.path + self._api_suffix + '.json'
        if os.path.exists(jsonpickle_path) and not skip_jsonpickle:
            instance = self.load_jsonpickle(jsonpickle_path)
        else:
            if verbose:
                print(f"Template file '{jsonpickle_path}' not found, now trying to read '{json_path}'.")
            instance = self.load_simple(json_path, as_object=True, validate=validate)
        assert isinstance(instance, COOLEST)
        return instance

    def load_simple(self, json_path, as_object=True, validate=True):
        """Read the JSON template file and build up the corresponding COOLEST object. 

        Parameters
        ----------
        json_path: str
            Path to the json file to be read.
        as_object : bool, optional
            _description_, by default True

        Returns
        -------
        COOLEST object
            COOLEST object that corresponds to the JSON template
        """
        with open(json_path, 'r') as f:
            content = json.loads(f.read())
        if not as_object:
            return content  # dictionary
        return self._json_to_coolest(content, validate)  # COOLEST object

    def load_jsonpickle(self, jsonpickle_path):
        """Read the JSON template file and build up the corresponding COOLEST object
        using the `jsonpickle`.

        Parameters
        ----------
        jsonpickle_path: str
            Path to the json file to be read with `jsonpickle`.

        Returns
        -------
        COOLEST object
            COOLEST object that corresponds to the JSON template
        """
        with open(jsonpickle_path, 'r') as f:
            content = jsonpickle.decode(f.read())
        return content  # COOLEST object

    def _json_to_coolest(self, json_content, validate):
        """Creates from scratch a COOLEST instance based on the content of a JSON
        file, given as a nested dictionnary.

        Parameters
        ----------
        json_content : dict
            Content of the JSON template file

        Returns
        -------
        COOLEST object
            COOLEST object that corresponds to the JSON template
        """
        c = json_content  # shorter

        # MODE
        mode = self._check_mode(c['mode'])

        # LENSING ENTITIES {GALAXY, MASSFIELDS}
        lensing_entities = self._setup_lensing_entities(c['lensing_entities'])

        # COSMOLOGY
        cosmology = self._setup_cosmology(c.get('cosmology', None))

        # COORDINATES
        coordinates_origin = self._setup_coordinates(c['coordinates_origin'])

        # OBSERVATION
        observation = self._setup_observation(c['observation'])

        # INSTRUMENT
        instrument = self._setup_instrument(c['instrument'])

        # LIKELIHOODS
        likelihoods = self._setup_likelihoods(c.get('likelihoods', None))

        # METADATA
        metadata = self._check_metadata(c['meta'])

        # instantiate the master class
        coolest = COOLEST(mode,
                          coordinates_origin,
                          lensing_entities,
                          observation,
                          instrument,
                          cosmology=cosmology,
                          likelihoods=likelihoods,
                          metadata=metadata)

        # check consistency across the whole coolest object
        if validate:
            self._validate_global(coolest)
        return coolest

    @staticmethod
    def _validate_global(coolest):
        """Performs consistency checks regarding some key properties of the COOLEST object.
        For instance, it checks that the pixel size of both the observation and
        the instrument are consistent.
        The checks performed here are those that cannot be handled by individual 
        class constructors called during instantiation of the COOLEST object.

        Parameters
        ----------
        coolest : COOLEST object
            Instance of a COOLEST object

        Raises
        ------
        ValueError
            In case observed instrumental pixel sizes are inconsistent
        """
        # PIXEL SIZE
        instru_pix_size = coolest.instrument.pixel_size
        obs_pix_size = coolest.observation.pixels.pixel_size
        isclose_bool = math.isclose(instru_pix_size, obs_pix_size,
                                    rel_tol=1e-09, abs_tol=0.0)
        if obs_pix_size not in (0, None) and not isclose_bool:
            raise ValueError(f"Pixel size of observation ({obs_pix_size}) is inconsistent with "
                             f"the instrument pixel size ({instru_pix_size})")
        # INSTANCE METHODS
        coolest.observation.check_consistency_with_instrument(coolest.instrument)
        if coolest.likelihoods is not None:
            coolest.likelihoods.check_consistency_with_observation(coolest.observation)
        # TODO: further standardize these checks (using class methods?)

    def _setup_instrument(self, instru_in):
        psf_settings = instru_in.pop('psf')
        psf = self._setup_psf(psf_settings)
        instru_out = Instrument(psf=psf, **instru_in)
        return instru_out

    def _setup_observation(self, obs_in):
        pixels_settings = obs_in.pop('pixels')
        pixels = self._setup_grid(pixels_settings, PixelatedRegularGrid)
        noise_settings = obs_in.pop('noise')
        noise = self._setup_noise(noise_settings)
        obs_out = Observation(pixels=pixels, noise=noise, **obs_in)
        return obs_out
    
    def _setup_likelihoods(self, likelihoods_in):
        if likelihoods_in is None:
            return None
        likelihoods_out = []
        for likelihood_in in likelihoods_in:
            likelihoods_out.append(self._setup_likelihood(likelihood_in))
        return DataLikelihoodList(*likelihoods_out)
    
    def _setup_likelihood(self, likelihood_in):
        if likelihood_in['type'] == 'ImagingDataLikelihood':
            likelihood_out = ImagingDataLikelihood(
                mask=self._setup_img_ll_mask(likelihood_in['mask'])
            )
        else:
            raise ValueError(f"Supported likelihoods entities are "
                             f"{support['likelihoods']}")
        return likelihood_out
    
    def _setup_img_ll_mask(self, mask_in):
        mask_out = self._setup_grid(mask_in, PixelatedRegularGrid)
        return mask_out

    def _setup_coordinates(self, coord_orig_in):
        return CoordinatesOrigin(**coord_orig_in)

    def _setup_cosmology(self, cosmology_in):
        if cosmology_in is None:
            return None
        return Cosmology(**cosmology_in)
    
    def _setup_lensing_entities(self, entities_in):
        entities_out = []
        for entity_in in entities_in:
            entities_out.append(self._setup_lensing_entity(entity_in))
        return LensingEntityList(*entities_out)
    
    def _setup_lensing_entity(self, entity_in):
        if entity_in['type'] == 'Galaxy':
            entity_out = Galaxy(entity_in['name'],
                                entity_in['redshift'],
                                light_model=self._setup_model(entity_in, 'light_model'),
                                mass_model=self._setup_model(entity_in, 'mass_model'))
        elif entity_in['type'] == 'MassField':
            entity_out = MassField(entity_in['name'],
                                   entity_in['redshift'],
                                   mass_model=self._setup_model(entity_in, 'mass_model'))
        else:
            raise ValueError(f"Supported lensing entities are "
                             f"{support['lensing_entities']}")
        self._update_parameters(entity_in, entity_out)
        return entity_out
    
    def _setup_model(self, entity_in, model_type):
        profile_types = [profile['type'] for profile in entity_in[model_type]]
        if model_type == 'light_model':
            model_out = LightModel(*profile_types)
        elif model_type == 'mass_model':
            model_out = MassModel(*profile_types)
        else:
            raise ValueError("The `model_type` can only be 'light_model' or 'mass_model'")
        return model_out
    
    def _update_parameters(self, entity_in, entity_out):
        self._update_parameters_values(entity_in, entity_out, 'mass_model')
        self._update_parameters_values(entity_in, entity_out, 'light_model')

    def _update_parameters_values(self, entity_in, entity_out, model_type):
        if model_type not in entity_in:
            return
        for i, profile in enumerate(entity_in[model_type]):
            # get the corresponding profile object in the model being updated
            profile_out = getattr(entity_out, model_type)[i]

            for name, values in profile['parameters'].items():

                # pop the id as this was already set at instantiation
                _ = values.pop('id', None)

                # pixelated profiles, for now only one value given (point estimate)
                if 'Grid' in profile['type']:
                    self._update_grid_parameter(profile_out, name, values)

                # other (analytical) parameters
                else:
                    self._update_std_parameter(profile_out, name, values)

    def _update_grid_parameter(self, profile_out, name, values):
        if name != 'pixels':
            raise NotImplementedError("Support for grid parameters other than "
                                      "'pixels' is not implemented.")
        if 'Regular' in profile_out.type:
            pixels = self._setup_grid(values, PixelatedRegularGrid)
            profile_out.parameters['pixels'] = pixels
        elif 'Irregular' in profile_out.type:
            pixels = self._setup_grid(values, IrregularGrid)
            profile_out.parameters['pixels'] = pixels
        else:
            raise ValueError(f"Unknown grid profile ({profile_out.type})")
        
    def _update_std_parameter(self, profile_out, name, values):
        pt_estim = PointEstimate(**values['point_estimate'])
        profile_out.parameters[name].set_point_estimate(pt_estim)
        if 'posterior_stats' in values:
            post_stats = PosteriorStatistics(**values['posterior_stats'])
            profile_out.parameters[name].set_posterior(post_stats)
        if 'prior' in values:
            prior = self._setup_prior(values['prior'])
            profile_out.parameters[name].set_prior(prior)

    def _setup_prior(self, prior_in):
        from coolest.template.classes import probabilities as proba_module
        prior_type = prior_in.pop('type')
        if prior_type is None:
            return Prior()
        PriorClass = getattr(proba_module, prior_type)
        return PriorClass(**prior_in)

    def _setup_noise(self, noise_in):
        from coolest.template.classes import noise as noise_module
        noise_type = noise_in.pop('type')
        if noise_type is None:
            return Noise()
        if noise_type not in support['noise_types']:
            raise ValueError(f"Noise type must be in {support['noise_types']}")
        NoiseClass = getattr(noise_module, noise_type)
        if noise_type == 'NoiseMap':
            pixels_settings = noise_in.pop('noise_map')
            noise_map = self._setup_grid(pixels_settings, PixelatedRegularGrid)
            noise_out = NoiseClass(noise_map=noise_map, **noise_in)
        elif noise_type == 'NoiseRealization':
            pixels_settings = noise_in.pop('noise_realization')
            noise_realization = self._setup_grid(pixels_settings, PixelatedRegularGrid)
            noise_out = NoiseClass(noise_realization=noise_realization, **noise_in)
        elif noise_type == 'DrizzledNoise':
            pixels_settings = noise_in.pop('wht_map')
            wht_map = self._setup_grid(pixels_settings, PixelatedRegularGrid)
            noise_out = NoiseClass(wht_map=wht_map, **noise_in)
        else:
            noise_out = NoiseClass(**noise_in)
        return noise_out

    def _setup_psf(self, psf_in):
        from coolest.template.classes import psf as psf_module
        psf_type = psf_in.pop('type')
        if psf_type is None:
            return PSF()
        if psf_type not in support['psf_types']:
            raise ValueError(f"PSF type must be in {support['psf_types']}")
        PSFClass = getattr(psf_module, psf_type)        
        if psf_type == 'PixelatedPSF':
            pixels_settings = psf_in.pop('pixels')
            pixels = self._setup_grid(pixels_settings, PixelatedRegularGrid)
            psf_out = PSFClass(pixels=pixels, **psf_in)
        else:
            psf_out = PSFClass(**psf_in)
        return psf_out

    def _setup_grid(self, grid_in, GridClass):
        fits_path = grid_in.pop('fits_file')['path']
        if fits_path is not None and os.path.isabs(fits_path):
            raise ValueError(f"FITS file '{fits_path}' must be a relative path instead, "
                             f"and placed in the same directory as the JSON file")
        return GridClass(fits_path, 
            check_fits_file=self._check_files, 
            fits_file_dir=self._json_dir,
            **grid_in)

    def _check_mode(self, mode_in):
        mode_out = str(mode_in)
        if mode_out not in support['modes']:
            raise ValueError(f"The template mode can only be in '{SUPPORTED_MODES}'")
        return mode_out

    def _check_metadata(self, meta_in):
        meta_out = meta_in  # TODO: might do more checks here
        return meta_out
