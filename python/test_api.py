# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as YAML or JSON files.

from lensmodelapi.api.observation import FitsFile, Data, Instrument
from lensmodelapi.api.coordinates import Coordinates
from lensmodelapi.api.cosmology import Cosmology
from lensmodelapi.api.galaxy import SourceGalaxy, LensGalaxy
from lensmodelapi.api.galaxy_list import GalaxyList
from lensmodelapi.api.mass_light_model import MassModel, LightModel
from lensmodelapi.api.regularization_list import RegularizationList
from lensmodelapi.api.likelihood_list import LikelihoodList
from lensmodelapi.api.lens_model import LensModel
from lensmodelapi.api.lens_object import LensObject
from lensmodelapi.api.lens_universe import LensUniverse
from lensmodelapi import info
from lensmodelapi.encoder import HierarchyEncoder

from pprint import pprint

# Provide data file
data = Data(FitsFile('test_image.fits'),
            noise_map=None,
            wht_map=None)

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

# check consistency
# data.check_consistency_with_instrument(instrument)

# or update instrument field-of-view based on data
instrument.update_fov_with_data(data)

# Setup coordinate systems that defines e.g. centers of model profiles
coordinates = Coordinates(orientation_ra='left', 
                          orientation_dec='top',
                          origin='center')

# Setup cosmology
cosmology = Cosmology(H0=73.0, Om0=0.3)

# Create a couple of source galaxies at different redshifts
source_1 = SourceGalaxy('a source galaxy', 2.0,
                        LightModel(['SersicElliptical']))

source_2 = SourceGalaxy('another source', 1.5,
                        LightModel(['PixelatedRegularGrid']))

source_3 = SourceGalaxy('a GLEE source', 1.2,
                        LightModel(['PixelatedRegularGrid']))

# Create a lens galaxy
lens_1 = LensGalaxy('a lens galaxy', 0.5,
                    LightModel(['SersicElliptical', 'SersicElliptical']),
                    MassModel(['PEMD', 'ExternalShearEllipticity']))

# Order in a list, which will also create unique IDs for each profile
galaxy_list = GalaxyList([lens_1, source_1, source_2, source_3])

# Define regularization strategies and link them to a given profile
regularization_list = RegularizationList([('PixelStarlet', source_2.light_model.profiles[0]), 
                                          ('PixelBLWavelet', source_2.light_model.profiles[0]),
                                          ('PixelCurvature', source_3.light_model.profiles[0])])

# Choose which likelihood terms you want to include
likelihood_list = LikelihoodList(['imaging_data'])

# Define the LensModel that merges physical objects (galaxies), 
# regularization strategies and a choice of coordinate system
lens_model = LensModel(galaxy_list,
                       regularization_list,
                       likelihood_list,
                       coordinates)

# Assign the list of galaxies to a LensObject
# along with the coordinate system and (optinonally) the observation
name = 'My Favorite Lens ever'
lens_object = LensObject(name,
                         instrument,
                         lens_model,
                         data=data)

# Wrap up a list of objects (here, only one) and a cosmology into a LensUniverse master object
lens_universe = LensUniverse([lens_object], cosmology)
print("FINAL LENS UNIVERSE OBJECT\n", lens_universe.__dict__, '\n')

# print supported profiles so far
print("Supported choices:")
pprint(info.all_supported_choices)

print("#"*30 + " serialization " + "#"*30)
# import json
# from lensmodelapi.encoders.json import JSONProfile, JSONParameter
# print(json.dumps(source_1.light_model.profiles, cls=JSONProfile, indent=4))
# print(json.dumps(lens_1.mass_model.profiles[1].parameters, cls=JSONParameter, indent=4))

encoder = HierarchyEncoder(lens_universe, 'test_api', indent=2)
encoder.yaml_dump()
encoder.yaml_to_json()

# test construct class from YAML
lens_universe_2 = encoder.yaml_load_universe()
print("Retrieved object is a LensUniverse instance?", 
      isinstance(lens_universe_2, LensUniverse))

pprint(lens_universe_2.lens_sample[0].name)
