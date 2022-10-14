__author__ = 'aymgal'

from typing import Tuple

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lens_object import LensObject


class LensSample(list, APIBaseObject):

    def __init__(self,
                 *lens_objects: Tuple[LensObject]):
        list.__init__(self, lens_objects)
        