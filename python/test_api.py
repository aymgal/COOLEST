# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as YAML or JSON files.

from lensmodelapi.lazy import *
from lensmodelapi import info
from lensmodelapi.io import APISerializer

from pprint import pprint

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

# Put them in a list, which will also create unique IDs for each profile
galaxy_list = GalaxyList(lens_1, source_1, source_2, source_3)

# Defines the external shear
ext_shear = ExternalShear('my lovely external shear', lens_1.redshift,
                          mass_model=MassModel('ExternalShearEllipticity'))

# Define regularization strategies and link them to a given profile
regularization_list = RegularizationList(('PixelStarlet', source_2.light_model.profiles[0]),
                                         ('PixelPositivity', source_2.light_model.profiles[0]), 
                                         ('PixelCurvature', source_3.light_model.profiles[0]),
                                         ('PixelBLWavelet', lens_1.mass_model.profiles[1]))

# Choose which likelihood terms you want to include
likelihood_list = LikelihoodList('imaging_data')

# TESTS
# - add a gaussian prior to a given parameter
from lensmodelapi.api.probabilities import GaussianPrior
lens_1.mass_model.profiles[0].parameters['gamma'].set_prior(GaussianPrior(mean=2.0, width=0.2))

# - add a point estimate to a given parameter
from lensmodelapi.api.parameter import PointEstimate
lens_1.light_model.profiles[1].parameters['e1'].set_point_estimate(PointEstimate(value=0.34))

# - add a posterior distribution (as 0th and 1st order statistics)
from lensmodelapi.api.probabilities import PosteriorStatistics
source_1.light_model.profiles[0].parameters['R_sersic'].set_posterior(PosteriorStatistics(mean=0.12, median=0.15, 
                                                                                          percentile_16th=0.03, percentile_84th=0.05))

# Define the LensModel that merges physical objects (galaxies), 
# regularization strategies and a choice of coordinate system
lens_model = LensModel(galaxy_list,
                       external_shear=ext_shear,
                       regularizations=regularization_list,
                       likelihoods=likelihood_list)

# Assign the list of galaxies to a LensObject
# along with the coordinate system and (optinonally) the observation
lens_object_1 = LensObject('My Favorite Lens ever',
                           instrument,
                           lens_model,
                           data=data)

# lens_object_2 = LensObject('Same system in another band',
#                            instrument,
#                            lens_model,
#                            data=data_2)

# can do another LensObject just the same... and build a LensSample
lens_sample = LensSample(lens_object_1)  # , lens_object_2, lens_object_3, ...

# Wrap up a list of objects (here, only one) and a cosmology into a LensUniverse master object
lens_universe = LensUniverse(cosmology, lens_sample)
print("FINAL LENS UNIVERSE OBJECT\n", lens_universe.__dict__, '\n')

# print supported profiles so far
print("Supported choices:")
pprint(info.all_supported_choices)

print("#"*30 + " serialization " + "#"*30)
# import json
# from lensmodelapi.encoders.json import JSONProfile, JSONParameter
# print(json.dumps(source_1.light_model.profiles, cls=JSONProfile, indent=4))
# print(json.dumps(lens_1.mass_model.profiles[1].parameters, cls=JSONParameter, indent=4))

# TESTS WITH YAML
encoder_yaml = APISerializer('api_input_file_YAML', obj=lens_universe, indent=2)
encoder_yaml.yaml_dump()
encoder_yaml.dump_yaml_to_json()
# test construct class from YAML
lens_universe_2 = encoder_yaml.yaml_load()
print("Retrieved object is a LensUniverse instance?", 
      isinstance(lens_universe_2, LensUniverse))
print("First lens in the sample:", lens_universe_2.lens_sample[0].name)

# TESTS WITH JSON
encoder_json = APISerializer('api_input_file_JSON', obj=lens_universe, indent=2)
encoder_json.json_dump()
encoder_json.json_dump_simple()
lens_universe_3 = encoder_json.json_load()
print("Retrieved object is a LensUniverse instance?", 
      isinstance(lens_universe_3, LensUniverse))
print("First lens in the sample:", lens_universe_3.lens_sample[0].name)

