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

# Provide data file
image_file = PixelFitsFile('test_image.fits', pixel_size=0.08)  # if None, COOLEST mode will be automatically set to 'mock'

# Select the type of noise
#from lensmodelapi.api.noise import InstrumentalNoise
#noise = InstrumentalNoise()
from lensmodelapi.api.noise import UniformGaussianNoise
noise = UniformGaussianNoise(std_dev=0.004)

observation = Observation(image=image_file,
                          noise=noise,
                          time_delays=[10., 20., 40.],
                          magnification_ratios=None)

# Defines the instrument
psf_file = PSF(PixelFitsFile('test_psf.fits', pixel_size=0.08))
instrument = Instrument('some instrument',
                        pixel_size=0.08, 
                        band='F160W',
                        psf=psf_file)

# Master object for the standard
master = CoolestStandard(origin,
                         entity_list,
                         observation, 
                         instrument, 
                         cosmology,
                         regularizations=regularization_list,
                         likelihoods=likelihood_list)
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


