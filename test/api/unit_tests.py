__author__ = 'aangress'


import os
import numpy as np
import numpy.testing as npt
import pytest

from coolest.api import util
from coolest.api.composable_models import ComposableLensModel
from coolest.api.profiles import mass as mass_profiles

# All tests can be run from terminal using "pytest unit_tests.py"
# Tests ------------------------------------------------------------------------------

# Various generic mass profiles if wanted/needed for tests
'''
@pytest.mark.parametrize("profile_cls,params", [
    (mass_profiles.PEMD, dict(theta_E=1.0, gamma=2.0, q=1.0, phi=0.0, center_x=0.0, center_y=0.0)),
    (mass_profiles.SIE, dict(theta_E=1.0, q=0.9, phi=10.0, center_x=0.0, center_y=0.0)),
    (mass_profiles.ExternalShear, dict(gamma_ext=0.05, phi_ext=20.0)),
    (mass_profiles.ConvergenceSheet, dict(kappa_s=0.1)),
])
'''
# Tests to see if COOLEST properly reads in a template file
def test_get_coolest_object_reads_template():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    assert coolest_obj is not None
    assert len(coolest_obj.lensing_entities) == 2
    assert coolest_obj.observation.pixels.num_pix_x == 100

# Tests to see if COOLEST properly generates a model image from a template file.
# Checks to see if image shape/pixel values are expected/reasonable values (finite, 100 x 100)
def test_composable_lens_model_image_from_coolest_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    model = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    image, coords = model.model_image(supersampling=1, convolved=False)
    assert image.shape == (100, 100)
    assert np.isfinite(image).all()
    assert image.mean() > 0
    assert coords.num_points == 100 * 100

# Checks a specific coolest model and verifies that
# the model image it produces matches an expected image from a saved FITS file. 
# This will ensure that the model image generation is correct for a known case
def test_composable_lens_model_image_matches_expected():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    model = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    image, coords = model.model_image(supersampling=1, convolved=False)

    expected_image_path = os.path.join(current_dir, '_templates', 'sis_temp_expected_image.npy')
    expected_image = np.load(expected_image_path)

    npt.assert_allclose(image, expected_image, rtol=1e-5, atol=1e-8)

# Checks that adding a zero-mass second lens plane does not affect
# resulting model image
def test_composable_lens_model_image_with_zero_mass_second_plane():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)

    # Add a second lens plane with zero mass
    from coolest.template.lazy import Galaxy, MassModel, LensingEntityList
    zero_mass_lens = Galaxy('zero mass lens', 0.5, lensed=False,
                            mass_model = MassModel('PEMD'))
    zero_mass_lens.mass_model[0].parameters['theta_E'].set_point_estimate(0.0)
    zero_mass_lens.mass_model[0].parameters['gamma'].set_point_estimate(2.0)
    zero_mass_lens.mass_model[0].parameters['q'].set_point_estimate(1.0)
    zero_mass_lens.mass_model[0].parameters['phi'].set_point_estimate(0.0)
    zero_mass_lens.mass_model[0].parameters['center_x'].set_point_estimate(0.0)
    zero_mass_lens.mass_model[0].parameters['center_y'].set_point_estimate(0.0)

    coolest_obj.lensing_entities.append(zero_mass_lens)

    model = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    image_with_zero_mass = model.model_image(supersampling=1, convolved=False)[0]

    # Get the original image without the zero mass plane
    coolest_obj.lensing_entities.pop()  # Remove the zero mass lens
    model_original = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    original_image = model_original.model_image(supersampling=1, convolved=False)[0]

    npt.assert_allclose(image_with_zero_mass, original_image, rtol=1e-5, atol=1e-8)

# Checks that the model image matches an expected image for a double lens system
def test_composable_lens_model_image_matches_expected_double_lens():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp_double')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)

    from coolest.api.plotting import ModelPlotter
    import matplotlib.pyplot as plt
    splotter = ModelPlotter(coolest_obj, coolest_directory=template_path)
    plt.figure()
    ax = plt.gca()
    image = splotter.plot_model_image(
        title ='Model image', ax = ax, convolved = False, auto_selection = True
        )
    expected_image_path = os.path.join(current_dir, '_templates', 'sis_temp_double_expected_image.npy')
    expected_image = np.load(expected_image_path)
    print(image[50,50], expected_image[50,50])
    npt.assert_allclose(image, expected_image, rtol=1e-5, atol=1e-8)

# Make a test that checks if two different COOLEST files produce the same model image:
# one will have a user defined beta value
# one will have a redshift values that can be used to calculate the same beta value
# This will ensure that the redshift to beta conversion is consistent and correct.
def test_composable_lens_model_image_with_redshift_vs_beta():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path_beta = os.path.join(current_dir, '_templates', 'sis_temp_double')
    coolest_obj_beta = util.get_coolest_object(template_path_beta, check_external_files=False)
    model_beta = ComposableLensModel(coolest_obj_beta, coolest_directory=current_dir)
    image_beta, coords_beta = model_beta.model_image(supersampling=1, convolved=False)

    template_path_redshift = os.path.join(current_dir, '_templates', 'sis_temp_double_with_beta')
    coolest_obj_redshift = util.get_coolest_object(template_path_redshift, check_external_files=False)
    model_redshift = ComposableLensModel(coolest_obj_redshift, coolest_directory=current_dir)
    image_redshift, coords_redshift = model_redshift.model_image(supersampling=1, convolved=False)

    npt.assert_allclose(image_beta, image_redshift, rtol=1e-5, atol=1e-8)