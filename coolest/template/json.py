import os
import json
import jsonpickle

from coolest.template.standard import COOLEST, SUPPORTED_MODES
from coolest.template.lazy import *
from coolest.template.classes.parameter import PointEstimate, PosteriorStatistics, Prior
from coolest.template.info import all_supported_choices


__all__ = ['JSONSerializer']


class JSONSerializer(object):

    def __init__(self,
                 file_path_no_ext: str, 
                 obj: object = None, 
                 indent: int = 2,
                 check_external_files: bool = True) -> None:
        self.obj = obj
        self.path = file_path_no_ext
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
        return self.json_to_coolest(content)  # COOLEST object

    def load(self):
        json_path = self.path + self._api_suffix + '.json'
        with open(json_path, 'r') as f:
            content = jsonpickle.decode(f.read())
        return content  # COOLEST object

    def json_to_coolest(self, json_content):
        c = json_content  # shorter

        # MODE
        if c['mode'] not in SUPPORTED_MODES:
            raise ValueError(f"The template mode can only be in '{SUPPORTED_MODES}'")

        # LENSING ENTITIES {GALAXY, EXTERNAL SHEAR}
        lensing_entities = self.setup_lensing_entities(c['lensing_entities'])

        # CSOMOLOGY
        cosmology = self.setup_cosmology(c['cosmology'])

        # COORDINATES
        coordinates_origin = self.setup_coordinates(c['coordinates_origin'])

        coolest = COOLEST(c['mode'],
                          coordinates_origin,
                          lensing_entities,
                          c['observation'],
                          c['instrument'],
                          cosmology=cosmology,
                          metadata=c['meta'])
        return coolest

    def setup_coordinates(self, coord_orig_in):
        return CoordinatesOrigin(**coord_orig_in)

    def setup_cosmology(self, cosmology_in):
        return Cosmology(**cosmology_in)
    
    def setup_lensing_entities(self, entities_in):
        entities_out = []
        for entity_in in entities_in:
            entities_out.append(self.setup_lensing_entity(entity_in))
        return entities_out
    
    def setup_lensing_entity(self, entity_in):
        if entity_in['type'] == 'galaxy':
            entity_out = Galaxy(entity_in['name'],
                                entity_in['redshift'],
                                light_model=self.setup_model(entity_in, 'light_model'),
                                mass_model=self.setup_model(entity_in, 'mass_model'))
        elif entity_in['type'] == 'external_shear':
            entity_out = ExternalShear(entity_in['name'],
                                       entity_in['redshift'],
                                       mass_model=self.setup_model(entity_in, 'mass_model'))
        else:
            raise ValueError(f"Supported lensing entities are "
                             f"{all_supported_choices['lensing_entities']}")
        self.update_parameters(entity_in, entity_out)
        return entity_out
    
    def setup_model(self, entity_in, model_type):
        profile_types = [profile['type'] for profile in entity_in[model_type]]
        if model_type == 'light_model':
            model_out = LightModel(*profile_types)
        elif model_type == 'mass_model':
            model_out = MassModel(*profile_types)
        else:
            raise ValueError("The `model_type` can only be 'light_model' or 'mass_model'")
        return model_out
    
    def update_parameters(self, entity_in, entity_out):
        self.update_parameters_values(entity_in, entity_out, 'mass_model')
        self.update_parameters_values(entity_in, entity_out, 'light_model')

    def update_parameters_values(self, entity_in, entity_out, model_type):
        if model_type not in entity_in:
            return
        for i, profile in enumerate(entity_in[model_type]):
            # get the corresponding profile object in the model being updated
            profile_out = getattr(entity_out, model_type)[i]

            for name, values in profile['parameters'].items():

                # pixelated profiles, for now only one value given (point estimate)
                if 'Grid' in profile['type']:
                    self.update_grid_parameter(profile_out, name, values)

                # other (analytical) parameters
                else:
                    self.update_std_parameter(profile_out, name, values)

    def update_grid_parameter(self, profile_out, name, values):
        assert name == 'pixels', "Support for grid parameters other than 'pixels' is not implemented."
        fits_path = values.pop('fits_file')['path']
        profile_out.parameters['pixels'].set_grid(fits_path, **values,
                                                  check_fits_file=self._check_files)
        
    def update_std_parameter(self, profile_out, name, values):
        pt_estim = PointEstimate(**values['point_estimate'])
        post_stats = PosteriorStatistics(**values['posterior_stats'])
        prior = Prior(ptype=values['prior']['type'])
        profile_out.parameters[name].set_point_estimate(pt_estim)
        profile_out.parameters[name].set_posterior(post_stats)
        profile_out.parameters[name].set_prior(prior)
