# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as YAML or JSON files.

from coolest.template.lazy import *
from coolest.template import info
from coolest.template.standard import COOLEST
from coolest.template.io import APISerializer

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
                mass_model=MassModel('PEMD', 'PixelatedRegularGridPotential'))

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

# EXAMPLE for accessing specific parameters and add priors/values/posteriors
# - add a gaussian prior to a given parameter
from coolest.template.api.probabilities import GaussianPrior
lens_1.mass_model[0].parameters['gamma'].set_prior(GaussianPrior(mean=2.0, width=0.2))

# - add a point estimate to a given parameter
from coolest.template.api.parameter import PointEstimate
lens_1.light_model[1].parameters['q'].set_point_estimate(PointEstimate(value=0.89))

# - add a posterior distribution (as 0th and 1st order statistics)
from coolest.template.api.probabilities import PosteriorStatistics
source_1.light_model[0].parameters['R_sersic'].set_posterior(PosteriorStatistics(mean=0.12, median=0.15, 
                                                                                 percentile_16th=0.03, percentile_84th=0.05))

# Provide data file
obs_pixels = PixelatedRegularGrid('test_image.fits')  # if None, COOLEST mode will be automatically set to 'mock'

# Select the type of noise
from coolest.template.api.noise import InstrumentalNoise, UniformGaussianNoise
#noise = InstrumentalNoise()
noise = UniformGaussianNoise(std_dev=0.004)

observation = Observation(pixels=obs_pixels, noise=noise)

# Defines the instrument
from coolest.template.api.psf import PixelatedPSF, GaussianPSF
psf = PixelatedPSF(PixelatedRegularGrid('test_psf.fits'))
#psf = GaussianPSF(0.2)

instrument = Instrument('some instrument',
                        pixel_size=0.08, 
                        band='F160W',
                        psf=psf)

# Master object for the standard
master = COOLEST('MOCK',
                         origin,
                         entity_list,
                         observation, 
                         instrument, 
                         cosmology,
                         likelihoods=likelihood_list)
print("FINAL OBJECT\n", master, '\n')

# print supported profiles so far
print("Supported choices:")
pprint(info.all_supported_choices)

print("#"*30 + " serialization " + "#"*30)
# import json
# from coolest.template.encoders.json import JSONProfile, JSONParameter
# print(json.dumps(source_1.light_model.profiles, cls=JSONProfile, indent=4))
# print(json.dumps(lens_1.mass_model.profiles[1].parameters, cls=JSONParameter, indent=4))

# export as JSON file
sample_encoder_json = APISerializer('coolest_template', 
                                    obj=master, indent=2)
sample_encoder_json.json_dump()
sample_encoder_json.json_dump_simple()
standard_master_2 = sample_encoder_json.json_load()
print("Retrieved object is a COOLEST instance?", 
      isinstance(standard_master_2, COOLEST))
print("Meta data:", standard_master_2.meta)


