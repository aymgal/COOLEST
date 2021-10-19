__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.base import APIBaseObject
from lensmodelapi.api.lens_sample import LensSample
from lensmodelapi.api.cosmology import Cosmology


class LensUniverse(APIBaseObject):

    def __init__(self,
                 cosmology: Cosmology,
                 lens_sample: LensSample) -> None:
        self.lens_sample = lens_sample
        self.cosmology = cosmology
        super().__init__()
        