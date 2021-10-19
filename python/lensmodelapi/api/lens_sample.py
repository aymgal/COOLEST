__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.lens_object import LensObject


class LensSample(list):

    def __init__(self,
                 *lens_objects: Tuple[LensObject]):
        list.__init__(self, lens_objects)
        