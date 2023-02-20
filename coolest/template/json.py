import os
import json
import jsonpickle

from coolest.template.standard import COOLEST
from coolest.template.lazy import *
from coolest.template.classes.parameter import PointEstimate, PosteriorStatistics, Prior
from coolest.template.info import all_supported_choices as support


__all__ = ['JSONSerializer']


class JSONSerializer(object):

    def __init__(self,
                 file_path_no_ext: str, 
                 obj: object = None, 
                 indent: int = 2,
                 check_external_files: bool = True) -> None:
        """
        file_path_no_ext should be the absolute path
        """
        self.obj = obj
        if not os.path.isabs(file_path_no_ext):
            raise ValueError("Path to JSON file must be an absolute path")
        self.path = file_path_no_ext
        self._json_dir = os.path.dirname(file_path_no_ext)
        self.indent = indent
        # to distinguish files that can be converted back to the python API
        self._api_suffix = '_pyAPI'
        self._check_files = check_external_files

    def dump_simple(self, exclude_keys=None):
        if exclude_keys is None and hasattr(self.obj, 'exclude_keys'):
            exclude_keys = self.obj.exclude_keys
        json_path = self.path + '.json'
        result = jsonpickle.encode(self.obj, indent=self.indent)
        with open(json_path, 'w') as f:
            f.write(self.obj.to_JSON(indent=self.indent, exclude_keys=exclude_keys))

    def dump(self):
        json_path = self.path + self._api_suffix + '.json'
        result = jsonpickle.encode(self.obj, indent=self.indent)
        with open(json_path, 'w') as f:
            f.write(result)

    def load_simple(self, as_object=True):
        json_path = self.path + '.json'
        with open(json_path, 'r') as f:
            content = json.loads(f.read())
        if not as_object:
            return content  # dictionary
        return self._json_to_coolest(content)  # COOLEST object

    def load(self):
        json_path = self.path + self._api_suffix + '.json'
        with open(json_path, 'r') as f:
            content = jsonpickle.decode(f.read())
        return content  # COOLEST object

    def _json_to_coolest(self, json_content):
        c = json_content  # shorter

        # MODE
        mode = self._check_mode(c['mode'])

        # LENSING ENTITIES {GALAXY, EXTERNAL SHEAR}
        lensing_entities = self._setup_lensing_entities(c['lensing_entities'])

        # CSOMOLOGY
        cosmology = self._setup_cosmology(c['cosmology'])

        # COORDINATES
        coordinates_origin = self._setup_coordinates(c['coordinates_origin'])

        # OBSERVATION
        observation = self._setup_observation(c['observation'])

        # INSTRUMENT
        instrument = self._setup_instrument(c['instrument'])

        # METADATA
        metadata = self._check_metadata(c['meta'])

        # instantiate the master class
        coolest = COOLEST(mode,
                          coordinates_origin,
                          lensing_entities,
                          observation,
                          instrument,
                          cosmology=cosmology,
                          metadata=metadata)
        return coolest

    def _setup_instrument(self, instru_in):
        psf_settings = instru_in.pop('psf')
        psf = self._setup_psf(psf_settings)
        instru_out = Instrument(psf=psf, **instru_in)
        return instru_out

    def _setup_observation(self, obs_in):
        pixels_settings = obs_in.pop('pixels')
        noise_settings = obs_in.pop('noise')
        noise = self._setup_noise(noise_settings)
        obs_out = Observation(noise=noise, **obs_in)
        fits_path = pixels_settings.pop('fits_file')['path']
        if fits_path is not None and os.path.isabs(fits_path):
            raise ValueError("Observation FITS file must be a relative one, "
                             "and be placed in the same directory as the JSON file")
        obs_out.pixels.set_grid(fits_path,
                                check_fits_file=self._check_files,
                                fits_file_dir=self._json_dir,
                                **pixels_settings)
        return obs_out

    def _setup_coordinates(self, coord_orig_in):
        return CoordinatesOrigin(**coord_orig_in)

    def _setup_cosmology(self, cosmology_in):
        return Cosmology(**cosmology_in)
    
    def _setup_lensing_entities(self, entities_in):
        entities_out = []
        for entity_in in entities_in:
            entities_out.append(self._setup_lensing_entity(entity_in))
        return entities_out
    
    def _setup_lensing_entity(self, entity_in):
        if entity_in['type'] == 'galaxy':
            entity_out = Galaxy(entity_in['name'],
                                entity_in['redshift'],
                                light_model=self._setup_model(entity_in, 'light_model'),
                                mass_model=self._setup_model(entity_in, 'mass_model'))
        elif entity_in['type'] == 'external_shear':
            entity_out = ExternalShear(entity_in['name'],
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
        fits_path = values.pop('fits_file')['path']
        if fits_path is not None and os.path.isabs(fits_path):
            raise ValueError(f"FITS file for profile {profile_out.type} must be a relative one, "
                             f"and be placed in the same directory as the JSON file")
        profile_out.parameters['pixels'].set_grid(fits_path,
                                                  check_fits_file=self._check_files,
                                                  fits_file_dir=self._json_dir,
                                                  **values)
        
    def _update_std_parameter(self, profile_out, name, values):
        pt_estim = PointEstimate(**values['point_estimate'])
        post_stats = PosteriorStatistics(**values['posterior_stats'])
        prior = self._setup_prior(values['prior'])
        profile_out.parameters[name].set_point_estimate(pt_estim)
        profile_out.parameters[name].set_posterior(post_stats)
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
        # TODO: treat specifically the types that require a pixel FITS file
        return NoiseClass(**noise_in)

    def _setup_psf(self, psf_in):
        from coolest.template.classes import psf as psf_module
        psf_type = psf_in.pop('type')
        if psf_type is None:
            return PSF()
        if psf_type not in support['psf_types']:
            raise ValueError(f"PSF type must be in {support['psf_types']}")
        print(psf_type, psf_type, psf_type)
        PSFClass = getattr(psf_module, psf_type)        
        if psf_type == 'PixelatedPSF':
            pixels_settings = psf_in.pop('pixels')
            psf_out = PSFClass(**psf_in)
            fits_path = pixels_settings.pop('fits_file')['path']
            if fits_path is not None and os.path.isabs(fits_path):
                raise ValueError(f"FITS file for the pixelated PSF must be a relative one, "
                                 f"and be placed in the same directory as the JSON file")
            psf_out.pixels.set_grid(fits_path,
                check_fits_file=self._check_files,
                fits_file_dir=self._json_dir,
                **pixels_settings)
        else:
            psf_out = PSFClass(**psf_in)
        return psf_out

    def _check_mode(self, mode_in):
        mode_out = str(mode_in)
        if mode_out not in support['modes']:
            raise ValueError(f"The template mode can only be in '{SUPPORTED_MODES}'")
        return mode_out

    def _check_metadata(self, meta_in):
        meta_out = str(meta_in)  # TODO: might do more checks here
        return meta_out
