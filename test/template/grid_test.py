__author__ = 'aymgal'


import pytest
from unittest import TestCase

from coolest.template.lazy import *


class TestMissingFile(TestCase):

    def test_missing_file_regular_grid(self):
        galaxy = Galaxy('some galaxy', 1.5, light_model=LightModel('PixelatedRegularGrid'))
        with self.assertRaises(RuntimeError):
            galaxy.light_model[0].parameters['pixels'].set_grid('dum_image.fits',
                                                            check_fits_file=True)

    def test_missing_file_irregular_grid(self):
        galaxy = Galaxy('some galaxy on irregular grid', 1.2,
                          light_model=LightModel('IrregularGrid'))
        with self.assertRaises(RuntimeError):
            galaxy.light_model[0].parameters['pixels'].set_grid('dum_table.fits',
                                                            check_fits_file=True)
