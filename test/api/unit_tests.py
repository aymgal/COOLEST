__author__ = 'aangress'


import os
import numpy as np
import numpy.testing as npt
import pytest

from coolest.api import util
from coolest.api.composable_models import ComposableLensModel
from coolest.api.profiles import mass as mass_profiles


# Tests ------------------------------------------------------------------------------

def test_array2image_and_image2array_identity():
    arr = np.arange(16.)
    image = util.array2image(arr)
    assert image.shape == (4, 4)
    arr2 = util.image2array(image)
    npt.assert_allclose(arr, arr2)


def test_array2image_invalid_size_raises():
    with pytest.raises(ValueError):
        util.array2image(np.arange(10.))


def test_downsampling_block_mean():
    image = np.arange(16.).reshape(4, 4)
    down = util.downsampling(image, factor=2)
    assert down.shape == (2, 2)
    # block means from a 4x4 grid
    expected = np.array([[2.5, 4.5], [10.5, 12.5]])
    npt.assert_allclose(down, expected)


def test_effective_radius_for_gaussian_light():
    # 2D Gaussian with sigma=1 should have half-light radius ~= sqrt(2*ln(2))
    size = 101
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    xx, yy = np.meshgrid(x, y)
    sigma = 1.0
    light = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    r_eff, grid_res = util.effective_radius(light, xx, yy, outer_radius=5, initial_guess=1.0, n_iter=20)
    expected = np.sqrt(2.0 * np.log(2.0))
    npt.assert_allclose(r_eff, expected, rtol=0.15)
    assert grid_res > 0


def test_ellipticity_from_moments_axis_ratio():
    # Ellipse oriented with axis along x/y and known q
    size = 101
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    xx, yy = np.meshgrid(x, y)
    sigma_x = 2.0
    sigma_y = 1.0
    light = np.exp(-(xx**2 / (2 * sigma_x**2) + yy**2 / (2 * sigma_y**2)))
    phi, q = util.ellipticity_from_moments(light, pixel_size=0.1)
    assert 0 <= phi <= np.pi
    npt.assert_allclose(q, sigma_y / sigma_x, rtol=0.2)


def test_azim_averaged_two_point_correlation_consistency():
    # simple constant image should give roughly constant covariance values
    image = np.ones((8, 8))
    bins, means, sdevs, cov = util.azim_averaged_two_point_correlation(image, dpix=1.0, rmax=3.0, Nbins=3)
    assert len(bins) == 3
    assert means.shape == (3,)
    assert sdevs.shape == (3,)
    # covariance centre is maximum for constant image
    center_val = cov[cov.shape[0] // 2, cov.shape[1] // 2]
    assert np.isfinite(center_val)


@pytest.mark.parametrize("profile_cls,params", [
    (mass_profiles.PEMD, dict(theta_E=1.0, gamma=2.0, q=1.0, phi=0.0, center_x=0.0, center_y=0.0)),
    (mass_profiles.SIE, dict(theta_E=1.0, q=0.9, phi=10.0, center_x=0.0, center_y=0.0)),
    (mass_profiles.ExternalShear, dict(gamma_ext=0.05, phi_ext=20.0)),
    (mass_profiles.ConvergenceSheet, dict(kappa_s=0.1)),
])
def test_ray_shooting_different_mass_profiles(profile_cls, params):
    # verify that simple ray shooting follows beta = theta - alpha for each mass profile
    x = np.array([[0.1, 0.2], [0.0, -0.1]])
    y = np.array([[0.0, 0.1], [-0.1, 0.2]])

    profile = profile_cls()
    ax_expected, ay_expected = profile.evaluate_deflection(x, y, **params)
    x_rs_expected = x - ax_expected
    y_rs_expected = y - ay_expected

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    model = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    cmass = model.lens_mass_sorted[0]

    cmass.profile_list = [profile]
    cmass.param_list = [params]

    x_rs, y_rs = cmass.ray_shooting(x, y)

    npt.assert_allclose(x_rs, x_rs_expected, rtol=1e-8, atol=1e-10)
    npt.assert_allclose(y_rs, y_rs_expected, rtol=1e-8, atol=1e-10)


def test_get_coolest_object_reads_template():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    assert coolest_obj is not None
    assert len(coolest_obj.lensing_entities) == 2
    assert coolest_obj.observation.pixels.num_pix_x == 100


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

# Make a test that checks a specific coolest model and verifies that the model image it produces matches an expected image from a saved FITS file. This will ensure that the model image generation is consistent and correct for a known case.
def test_composable_lens_model_image_matches_expected():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)
    model = ComposableLensModel(coolest_obj, coolest_directory=current_dir)
    image, coords = model.model_image(supersampling=1, convolved=False)

    expected_image_path = os.path.join(current_dir, '_templates', 'sis_temp_expected_image.npy')
    expected_image = np.load(expected_image_path)

    npt.assert_allclose(image, expected_image, rtol=1e-5, atol=1e-8)

# Make a test that checks whether a standard model image is produced when a zero mass second lensing plane is added to an existing COOLEST setup that produces said model image.
def test_composable_lens_model_image_with_zero_mass_second_plane():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, '_templates', 'sis_temp')
    coolest_obj = util.get_coolest_object(template_path, check_external_files=False)

    # Add a second lensing plane with zero mass
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

# Make a test that checks if two different COOLEST files produce the same model image: one will have a user defined beta value and one will have a redshift values that can be used to calcualte the same beta value. This will ensure that the redshift to beta conversion is consistent and correct.
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