__author__ = 'aymgal'


import pytest
import os
import numpy as np
import numpy.testing as npt

from coolest.api.analysis import Analysis
from coolest.api import util


def _get_analysis_instance(supersampling):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    coolest_path = os.path.join(current_dir, '_templates', 'pemd_sersic')
    coolest_object = util.get_coolest_object(coolest_path, check_external_files=False)
    return Analysis(coolest_object, os.path.dirname(os.path.abspath(coolest_path)),
                    supersampling=supersampling)

@pytest.mark.parametrize("supersampling", [1, 5, 10])
@pytest.mark.parametrize("axis_ratio", [1.0, 0.9, 0.8])
@pytest.mark.parametrize("radius", [0.8, 1.1, 1.4])
def test_effective_einstein_radius(supersampling, axis_ratio, radius):
    analysis = _get_analysis_instance(supersampling)
    coolest = analysis.coolest
    # alter some parameter values for the test
    coolest.lensing_entities[0].mass_model[0].parameters['q'].set_point_estimate(axis_ratio)
    coolest.lensing_entities[0].mass_model[0].parameters['theta_E'].set_point_estimate(radius)
    # theoretical value
    theta_E_th = coolest.lensing_entities[0].mass_model[0].parameters['theta_E'].point_estimate.value
    # computed value
    theta_E_eff = analysis.effective_einstein_radius(entity_selection=[0], 
                                                     profile_selection='all')
    npt.assert_allclose(theta_E_th, theta_E_eff, rtol=4e-2)

@pytest.mark.parametrize("supersampling", [1, 5, 10])
@pytest.mark.parametrize("axis_ratio", [1.0, 0.9, 0.8])
@pytest.mark.parametrize("slope", [-0.8, -1.0, -1.2])
def test_effective_radial_slope(supersampling, axis_ratio, slope):
    analysis = _get_analysis_instance(supersampling)
    coolest = analysis.coolest
    # alter some parameter values for the test
    coolest.lensing_entities[0].mass_model[0].parameters['q'].set_point_estimate(axis_ratio)
    coolest.lensing_entities[0].mass_model[0].parameters['gamma'].set_point_estimate(-slope+1.)
    # theoretical value
    theta_E = coolest.lensing_entities[0].mass_model[0].parameters['theta_E'].point_estimate.value
    gamma = coolest.lensing_entities[0].mass_model[0].parameters['gamma'].point_estimate.value
    slope_th = - gamma + 1.
    slope_eff = analysis.effective_radial_slope(r_eval=theta_E, 
                                                entity_selection=[0], 
                                                profile_selection='all')
    npt.assert_allclose(slope_th, slope_eff, rtol=5e-2)

@pytest.mark.parametrize("supersampling", [1, 5, 10])
@pytest.mark.parametrize("axis_ratio", [1.0, 0.8, 0.6])
@pytest.mark.parametrize("radius", [0.2, 0.5, 1.2])
def test_effective_radius_light(supersampling, axis_ratio, radius):
    analysis = _get_analysis_instance(supersampling)
    coolest = analysis.coolest
    # alter some parameter values for the test
    coolest.lensing_entities[1].light_model[0].parameters['q'].set_point_estimate(axis_ratio)
    coolest.lensing_entities[1].light_model[0].parameters['theta_eff'].set_point_estimate(radius)
    # prepare a field-of-view that is large enough for accurate light integration
    coord_large = analysis.coordinates.create_new_coordinates(grid_shape=(20, 20))  # 20x20 arcsec
    # theoretical value
    theta_eff_th = coolest.lensing_entities[1].light_model[0].parameters['theta_eff'].point_estimate.value
    # computed value
    theta_eff = analysis.effective_radius_light(coordinates=coord_large, n_iter=10,
                                                entity_selection=[1], 
                                                profile_selection='all')
    npt.assert_allclose(theta_eff_th, theta_eff, rtol=4e-2)
