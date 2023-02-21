# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as a JSON file.

import os

from coolest.template.lazy import *
from coolest.template import info
from coolest.template.standard import COOLEST
from coolest.template.json import JSONSerializer

from pprint import pprint


############## LENS MODELING ################


# Setup cosmology
cosmology = Cosmology(H0=73.0, Om0=0.3)

# Create a couple of source galaxies at different redshifts
source_1 = Galaxy('a source galaxy', 2.0,
                  light_model=LightModel('Sersic'))

source_2 = Galaxy('another source', 1.5,
                  light_model=LightModel('PixelatedRegularGrid'))
source_2.light_model[0].parameters['pixels'].set_grid('test_image.fits',
                                                      field_of_view_x=(-3.0, 1.0),
                                                      field_of_view_y=(-2.0, 2.0))
print("pixel size:", source_2.light_model[0].parameters['pixels'].pixel_size)

source_3 = Galaxy('a VKL source', 1.2,
                  light_model=LightModel('IrregularGrid'))
source_3.light_model[0].parameters['pixels'].set_grid('test_irreg_grid.fits',
                                                      check_fits_file=True)


# Create a lens galaxy
lens_1 = Galaxy('a lens galaxy', 0.5,
                light_model=LightModel('Sersic', 'Sersic'),
                mass_model=MassModel('PEMD', 'PixelatedRegularGridPotential'))
lens_1.mass_model[1].parameters['pixels'].set_grid('test_image.fits',
                                                   field_of_view_x=(-3.0, 1.0),
                                                   field_of_view_y=(-2.0, 2.0))

# Defines the external shear
ext_shear = ExternalShear('my lovely external shear', lens_1.redshift,
                          mass_model=MassModel('ExternalShear'))

# Put them in a list, which will also create unique IDs for each profile
entity_list = LensingEntityList(ext_shear, lens_1, source_1, source_2)

# Define the origin of the coordinates system
origin = CoordinatesOrigin('00h11m20.244s', '-08d45m51.48s')

# EXAMPLE for accessing specific parameters and add priors/values/posteriors
# - add a gaussian prior to a given parameter
from coolest.template.classes.probabilities import GaussianPrior
lens_1.mass_model[0].parameters['gamma'].set_prior(GaussianPrior(mean=2.0, width=0.2))

# - add a point estimate to a given parameter
from coolest.template.classes.parameter import PointEstimate
ext_shear.mass_model[0].parameters['gamma_ext'].set_point_estimate(0.07)
lens_1.light_model[1].parameters['q'].set_point_estimate(PointEstimate(value=0.89))

# - add a posterior distribution (as 0th and 1st order statistics)
from coolest.template.classes.probabilities import PosteriorStatistics
source_1.light_model[0].parameters['theta_eff'].set_posterior(PosteriorStatistics(mean=0.11, median=0.15, 
                                                                                 percentile_16th=0.03, percentile_84th=0.05))

# Provide data file
obs_pixels = PixelatedRegularGrid('test_image.fits')  # if None, COOLEST mode will be automatically set to 'mock'

# Select the type of noise
# noise = InstrumentalNoise()
# noise = UniformGaussianNoise(std_dev=0.004)
noise = NoiseMap(noise_map=PixelatedRegularGrid('test_image.fits'))


observation = Observation(pixels=obs_pixels, noise=noise)

# Defines the instrument
psf = PixelatedPSF(pixels=PixelatedRegularGrid('test_psf.fits'), description="a PSF kernel")
#psf = GaussianPSF(0.2)

instrument = Instrument('some instrument',
                        readout_noise=4,
                        pixel_size=0.08, 
                        band='F160W',
                        psf=psf)

# Master object for the standard
master = COOLEST('MOCK',
                 origin,
                 entity_list,
                 observation, 
                 instrument, 
                 cosmology)
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
template_abs_path = os.path.join(os.getcwd(), 'coolest_template')
encoder_json = JSONSerializer(template_abs_path, 
                              obj=master, indent=2,
                              check_external_files=False)
encoder_json.dump()
encoder_json.dump_simple()
master_2 = encoder_json.load()
print("Retrieved object is a COOLEST instance?", 
      isinstance(master_2, COOLEST))
print("Meta data:", master_2.meta)

# test reading the JSON file that does not contain jsonpickle tags
master_3 = encoder_json.load_simple()
print("Retrieved object is a COOLEST instance?", 
      isinstance(master_3, COOLEST))
print("Meta data:", master_3.meta)

