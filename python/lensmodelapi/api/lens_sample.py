__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.lens_object import LensObject


class LensSample(list):

    def __init__(self,
                 lens_objects: List[LensObject]):
        list.__init__(self, lens_objects)
        