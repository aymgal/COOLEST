__author__ = 'aymgal'


from lensmodelapi.lens_object import LensObject
from lensmodelapi.cosmology import Cosmology


class LensUniverse(object):

    def __init__(self,
                 lens_object: LensObject,
                 cosmology: Cosmology) -> None:
        self.lens_object = lens_object
        self.cosmology = cosmology
