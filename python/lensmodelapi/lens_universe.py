__author__ = 'aymgal'

from typing import List

from lensmodelapi.base import APIBaseObject
from lensmodelapi.lens_object import LensObject
from lensmodelapi.lens_sample import LensSample
from lensmodelapi.cosmology import Cosmology


class LensUniverse(APIBaseObject):

    def __init__(self,
                 lens_objects: List[LensObject],
                 cosmology: Cosmology) -> None:
        self.lens_sample = LensSample(lens_objects)
        self.cosmology = cosmology
        super().__init__()
        