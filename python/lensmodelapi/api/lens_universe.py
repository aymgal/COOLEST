__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lens_object import LensObject
from lensmodelapi.api.lens_sample import LensSample
from lensmodelapi.api.cosmology import Cosmology


class LensUniverse(APIBaseObject):

    def __init__(self,
                 lens_objects: List[LensObject],
                 cosmology: Cosmology) -> None:
        self.lens_sample = LensSample(lens_objects)
        self.cosmology = cosmology
        super().__init__()
        