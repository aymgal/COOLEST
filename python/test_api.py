# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as YAML or JSON files.

from lensmodelapi.lazy import *
from lensmodelapi import info
from lensmodelapi.standard import CoolestStandard
from lensmodelapi.io import APISerializer

from pprint import pprint


############## LENS MODELING ################


# Setup cosmology
cosmology = Cosmology(H0=73.0, Om0=0.3)

# Create a couple of source galaxies at different redshifts
source_1 = Galaxy('a source galaxy', 2.0,
                  light_model=LightModel('Sersic'))

source_2 = Galaxy('another source', 1.5,
                  light_model=LightModel('PixelatedRegularGrid'))

source_3 = Galaxy('a GLEE source', 1.2,
                  light_model=LightModel('PixelatedRegularGrid'))

# Create a lens galaxy
lens_1 = Galaxy('a lens galaxy', 0.5,
                light_model=LightModel('Sersic', 'Sersic'),
                mass_model=MassModel('PEMD', 'PixelatedPotential'))

# Defines the external shear
ext_shear = ExternalShear('my lovely external shear', lens_1.redshift,
                          mass_model=MassModel('ExternalShear'))

# Put them in a list, which will also create unique IDs for each profile
entity_list = LensingEntityList(ext_shear, lens_1, source_1, source_2, source_3)

# Define regularization strategies and link them to a given profile
regularization_list = RegularizationList(('PixelStarlet', source_2.light_model[0]),
                                         ('PixelPositivity', source_2.light_model[0]), 
                                         ('PixelCurvature', source_3.light_model[0]),
                                         ('PixelBLWavelet', lens_1.mass_model[1]))

# Choose which likelihood terms you want to include
likelihood_list = LikelihoodList('imaging_data')

# Define the origin of the coordinates system
origin = CoordinatesOrigin('00h11m20.244s', '-08d45m51.48s')  # <- in degrees (2.83435, )

# # TESTS
# # - add a gaussian prior to a given parameter
# from lensmodelapi.api.probabilities import GaussianPrior
# lens_1.mass_model.profiles[0].parameters['gamma'].set_prior(GaussianPrior(mean=2.0, width=0.2))

# # - add a point estimate to a given parameter
# from lensmodelapi.api.parameter import PointEstimate
# lens_1.light_model.profiles[1].parameters['q'].set_point_estimate(PointEstimate(value=0.89))

# # - add a posterior distribution (as 0th and 1st order statistics)
# from lensmodelapi.api.probabilities import PosteriorStatistics
# source_1.light_model.profiles[0].parameters['R_sersic'].set_posterior(PosteriorStatistics(mean=0.12, median=0.15, 
#                                                                                           percentile_16th=0.03, percentile_84th=0.05))

# Define the LensModel that merges physical objects (galaxies), 
# regularization strategies and a choice of coordinate system
lens_model = LensModel('My Favorite Lens ever',
                       entity_list,
                       coordinates_origin=origin,
                       regularizations=regularization_list,
                       likelihoods=likelihood_list,
                       cosmology=cosmology)

# Assign the list of galaxies to a LensObject
# along with the coordinate system and (optinonally) the observation
# lens_object_1 = LensObject('My Favorite Lens ever', lens_model)

# lens_object_2 = LensObject('Same system in another band for instance', lens_model)

# Wrap up a list of objects (here, only one) into a LensSample object
# lens_sample = LensSample(lens_object_1)  # , lens_object_2, lens_object_3, ...
# print("FINAL OBJECT\n", lens_sample, '\n')

# Master object for the standard
master = CoolestStandard('mock', lens_model)
print("FINAL OBJECT\n", master, '\n')

# print supported profiles so far
print("Supported choices:")
pprint(info.all_supported_choices)

print("#"*30 + " serialization " + "#"*30)
# import json
# from lensmodelapi.encoders.json import JSONProfile, JSONParameter
# print(json.dumps(source_1.light_model.profiles, cls=JSONProfile, indent=4))
# print(json.dumps(lens_1.mass_model.profiles[1].parameters, cls=JSONParameter, indent=4))

# TESTS WITH YAML
sample_encoder_yaml = APISerializer('api_input_file_YAML',
                                    obj=master, indent=2)
sample_encoder_yaml.yaml_dump()
sample_encoder_yaml.dump_yaml_to_json()
# test construct class from YAML
standard_master_1 = sample_encoder_yaml.yaml_load()
print("Retrieved object is a CoolestStandard instance?", 
      isinstance(standard_master_1, CoolestStandard))
print("Meta data:", standard_master_1.meta)

# TESTS WITH JSON
sample_encoder_json = APISerializer('api_input_file_JSON', 
                                    obj=master, indent=2)
sample_encoder_json.json_dump()
sample_encoder_json.json_dump_simple()
standard_master_2 = sample_encoder_json.json_load()
print("Retrieved object is a CoolestStandard instance?", 
      isinstance(standard_master_2, CoolestStandard))
print("Meta data:", standard_master_2.meta)






############## OBSERVATIONAL DATA ################


# Provide data file
data = Data(FitsFile('test_image.fits'),
            noise_map=None,
            wht_map=None,
            arc_mask=FitsFile('arc_mask.fits'),
            likelihood_mask=None,
            time_delays=[10., 20., 40.],
            magnification_ratios=None)

# Defines the instrument
instrument = Instrument('some instrument',
                        FitsFile('test_psf.fits'),
                        pixel_size=0.08, 
                        field_of_view_ra=None,
                        field_of_view_dec=None,
                        exposure_time=1000,
                        background_rms=0.05,
                        psf_pixel_size=None)

# estimate background noise from data
instrument.set_background_rms(data.estimate_background_noise())

# check consistency between data and instrument
# data.check_consistency_with_instrument(instrument)

# or update instrument field-of-view based on data
instrument.update_fov_with_data(data)

# group as an observation
observation = Observation(data, instrument)

# save it in a JSON file
data_encoder_json = APISerializer('api_obs_file_JSON', obj=observation, indent=2)
data_encoder_json.json_dump_simple()


