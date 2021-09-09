# Test script that creates a whole LensUniverse model
# emulating a series of inputs from e.g. a user interface,
# and finally write it on disk as a JSON file.


# Provide data files
from lensmodelapi.data import Data

data = Data('path/to/data/image.fits',
            'path/to/data/psf.fits',
            0.08, psf_pixel_size=0.08)
print("DATA\n", data.__dict__, '\n')

# Setup cosmology 
from lensmodelapi.cosmology import Cosmology

cosmology = Cosmology(H0=73.0, Om0=0.3)
print("COSMOLOGY\n", cosmology.__dict__, '\n')

# Create a couple of source galaxies
from lensmodelapi.redshift import Redshift
from lensmodelapi.model import LightModel
from lensmodelapi.galaxy import SourceGalaxy

source_1 = SourceGalaxy('a source galaxy', 
                              Redshift(2.0),
                              LightModel(['SersicElliptical']))
print("SOURCE 1\n", source_1.light_model.__dict__, '\n')

source_2 = SourceGalaxy('another source', 
                               Redshift(1.5),
                               LightModel(['PixelatedRegularGrid']))
print("SOURCE 2\n", source_2.light_model.__dict__, '\n')

# Create a lens galaxy
from lensmodelapi.model import MassModel
from lensmodelapi.galaxy import LensGalaxy

lens_1 = LensGalaxy('a lens galaxy',
                    Redshift(0.5),
                    LightModel(['SersicElliptical', 'SersicElliptical']),
                    MassModel(['PEMD', 'ExternalShearEllipticity']))
print("LENS 1\n", lens_1.mass_model.__dict__)
print("a single parameter\n", lens_1.light_model.profiles[0].parameters[-1].__dict__, '\n')

# Assign all galaxies to LensObject, along with the data and a coordinate system
from lensmodelapi.galaxy_list import GalaxyList
from lensmodelapi.lens_object import LensObject
galaxies = GalaxyList([lens_1, source_1, source_2])
lens_object = LensObject(galaxies, data=data)
print("OBJECT\n", lens_object.__dict__, '\n')

# Wrap up the object and cosmology into a LensUniverse master object
from lensmodelapi.lens_universe import LensUniverse
lens_universe = LensUniverse(lens_object, cosmology)
print("UNIVERSE\n", lens_universe.__dict__, '\n')
