__author__ = 'aymgal'


import pytest
import numpy as np
import numpy.testing as npt

from coolest.api import util


@pytest.mark.parametrize("field_of_view_x", [[0., 2.], [-1., 1.]])
@pytest.mark.parametrize("field_of_view_y", [[0., 2.], [-1., 1.]])
@pytest.mark.parametrize("num_pix_x", [2., 3., 10, 11.])
@pytest.mark.parametrize("num_pix_y", [2., 3., 10, 11.])
def test_get_coordinates_from_regular_grid(field_of_view_x, field_of_view_y, num_pix_x, num_pix_y):
    coordinates = util.get_coordinates_from_regular_grid(field_of_view_x, field_of_view_y, num_pix_x, num_pix_y)
    plt_extent = coordinates.plt_extent
    retrieved_field_of_view_x = [plt_extent[0], plt_extent[1]]
    npt.assert_allclose(retrieved_field_of_view_x, field_of_view_x)
