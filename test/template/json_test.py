__author__ = 'aymgal'


import pytest

from coolest.template.lazy import *
from coolest.template.standard import COOLEST
from coolest.template.json import JSONSerializer


class TestJSONSerialization(object):

    def setup(self):
        self.template_name = 'test'
        self.check_files = False

    def test_dump_and_read_pure_json(self):

        # Setup cosmology
        cosmology = Cosmology(H0=73.0, Om0=0.3)

        # Create a couple of source galaxies at different redshifts
        source_1 = Galaxy('a source galaxy', 2.0,
                          light_model=LightModel('Sersic'))

        source_2 = Galaxy('another source', 1.5,
                          light_model=LightModel('PixelatedRegularGrid'))
        source_2.light_model[0].parameters['pixels'].set_grid('test_image_1.fits',
                                                              field_of_view_x=(-3.0, 1.0),
                                                              field_of_view_y=(-2.0, 2.0),
                                                              check_fits_file=self.check_files)

        source_3 = Galaxy('a VKL source', 1.2,
                          light_model=LightModel('IrregularGrid'))
        source_3.light_model[0].parameters['pixels'].set_grid('dum_table.fits',
                                                              check_fits_file=self.check_files)


        # Create a lens galaxy
        lens_1 = Galaxy('a lens galaxy', 0.5,
                        light_model=LightModel('Sersic', 'Sersic'),
                        mass_model=MassModel('PEMD', 'PixelatedRegularGridPotential'))
        lens_1.mass_model[1].parameters['pixels'].set_grid('test_image_2.fits',
                                                              field_of_view_x=(-3.0, 1.0),
                                                              field_of_view_y=(-2.0, 2.0),
                                                              check_fits_file=self.check_files)

        # Defines the external shear
        ext_shear = ExternalShear('my lovely external shear', lens_1.redshift,
                                  mass_model=MassModel('ExternalShear'))

        # Put them in a list, which will also create unique IDs for each profile
        entity_list = LensingEntityList(ext_shear, lens_1, source_1, source_2, source_3)

        # Define the origin of the coordinates system
        origin = CoordinatesOrigin('00h11m20.244s', '-08d45m51.48s')  # <- in degrees (2.83435, )

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
        from coolest.template.classes.noise import InstrumentalNoise, UniformGaussianNoise
        noise = InstrumentalNoise()
        # noise = UniformGaussianNoise(std_dev=0.004)

        observation = Observation(pixels=obs_pixels, noise=noise)

        # Defines the instrument
        from coolest.template.classes.psf import PixelatedPSF, GaussianPSF
        psf = PixelatedPSF(PixelatedRegularGrid('test_psf.fits'))
        #psf = GaussianPSF(0.2)

        instrument = Instrument('some instrument',
                                readout_noise=4,
                                pixel_size=0.08, 
                                band='F160W',
                                psf=psf)

        # Master object for the standard
        coolest = COOLEST('MOCK',
                          origin,
                          entity_list,
                          observation, 
                          instrument, 
                          cosmology)
        
        # export as JSON file
        serializer = JSONSerializer(self.template_name, obj=coolest,
                                    check_external_files=self.check_files)
        serializer.dump()
        serializer.dump_simple()
        coolest_2 = serializer.load()
        assert isinstance(coolest_2, COOLEST)

        # test reading the JSON file that does not contain jsonpickle tags
        # and btw we also instantiate another JSONSerializer as a test
        serializer_2 = JSONSerializer(self.template_name, obj=None,
                                      check_external_files=self.check_files)
        coolest_3 = serializer_2.load_simple()
        assert isinstance(coolest_3, COOLEST)

        # test that the content of the new json file is *exactly* the same as the original one
        json_orig = serializer.load_simple(as_object=False)
        json_new  = serializer_2.load_simple(as_object=False)

        assert json_orig == json_new
