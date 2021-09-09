from lensmodelapi.lens_object import LensObject
from lensmodelapi.cosmology import Cosmology


class LensUniverse(object):

    def __init__(self,
                 lens_object: LensObject,
                 cosmology: Cosmology) -> None:
        self.lens_object = lens_object
        self.cosmology = cosmology

    def write_to_json(self, file_path):
        """functions that writes to a JSON all the hierarchical structure
        for a given Universe, down to each individual parameters"""
        pass # TODO
