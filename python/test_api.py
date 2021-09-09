# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as a JSON file.

from lensmodelapi.observation import FitsFile, Observation
from lensmodelapi.coordinates import Coordinates
from lensmodelapi.cosmology import Cosmology
from lensmodelapi.redshift import Redshift
from lensmodelapi.galaxy import SourceGalaxy, LensGalaxy
from lensmodelapi.model import LightModel, MassModel
from lensmodelapi.lens_object import LensObject
from lensmodelapi.lens_universe import LensUniverse
from lensmodelapi import info


# Provide data files
image = FitsFile('test_image.fits',
                 pixel_size=0.08)
psf = FitsFile('test_psf.fits',
               pixel_size=0.08)
observation = Observation(image, psf, update_with_fits=True)
print("OBSERVATION\n", observation.__dict__)
print("image array shape\n", observation.image.array_shape, '\n')

coordinates = Coordinates(ra_orientation='left', 
                          dec_orientation='top',
                          origin='center')
coordinates.update_with_observation(observation)

# Setup cosmology 
cosmology = Cosmology(H0=73.0, Om0=0.3)
print("COSMOLOGY\n", cosmology.__dict__, '\n')

# Create a couple of source galaxies at different redshifts
source_1 = SourceGalaxy('a source galaxy', 
                        Redshift(2.0),
                        LightModel(['SersicElliptical']))
print("SOURCE 1\n", source_1.light_model.__dict__, '\n')

source_2 = SourceGalaxy('another source', 
                        Redshift(1.5),
                        LightModel(['PixelatedRegularGrid']))
print("SOURCE 2\n", source_2.light_model.__dict__, '\n')

# Create a lens galaxy
lens_1 = LensGalaxy('a lens galaxy',
                    Redshift(0.5),
                    LightModel(['SersicElliptical', 'SersicElliptical']),
                    MassModel(['PEMD', 'ExternalShearEllipticity']))
print("LENS 1\n", lens_1.mass_model.__dict__)
print("a single parameter\n", lens_1.light_model.profiles[0].parameters[-1].__dict__, '\n')

# Assign the list of galaxies to a LensObject
# along with the coordinate system and (optinonally) the observation
lens_object = LensObject([lens_1, source_1, source_2], 
                         coordinates, 
                         observation=observation)
print("OBJECT\n", lens_object.__dict__, '\n')

# Wrap up the object and cosmology into a LensUniverse master object
lens_universe = LensUniverse(lens_object, cosmology)
print("UNIVERSE\n", lens_universe.__dict__, '\n')

# print supported profiles so far
print(info.supported_mass_profiles, info.supported_light_profiles)
