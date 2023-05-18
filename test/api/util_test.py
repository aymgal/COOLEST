__author__ = 'aymgal'


import pytest
import numpy as np
import numpy.testing as npt

from coolest.api import util


@pytest.mark.parametrize("field_of_view_x", [[0., 2.], [-1., 1.], [-2., 0.]])
@pytest.mark.parametrize("field_of_view_y", [[0., 2.], [-1., 1.], [-2., 0.]])
@pytest.mark.parametrize("num_pix_x", [10, 11])
@pytest.mark.parametrize("num_pix_y", [10, 11])
def test_get_coordinates_from_regular_grid(field_of_view_x, field_of_view_y, num_pix_x, num_pix_y):
    # tests that the coordinates object has the same center and FoV as the original settings
    coordinates = util.get_coordinates_from_regular_grid(field_of_view_x, field_of_view_y, num_pix_x, num_pix_y)
    assert coordinates.num_points == num_pix_x*num_pix_y
    plt_extent = coordinates.plt_extent
    retrieved_field_of_view_x = [plt_extent[0], plt_extent[1]]
    npt.assert_allclose(retrieved_field_of_view_x, field_of_view_x, atol=1e-8)
    retrieved_field_of_view_y = [plt_extent[2], plt_extent[3]]
    npt.assert_allclose(retrieved_field_of_view_y, field_of_view_y, atol=1e-8)
    npt.assert_allclose(coordinates.center, (np.mean(field_of_view_x), np.mean(field_of_view_y)), atol=1e-8)
