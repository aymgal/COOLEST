__author__ = 'aymgal'


from astropy.coordinates import SkyCoord

from coolest.template.json import JSONSerializer
from coolest.api.coordinates import Coordinates


class Analysis(object):
    """
    Handles computation of model-independent quantities and other analysis computations
    """

    def __init__(self, coolest_file_path, **kwargs_json):
        serializer = JSONSerializer(coolest_file_path, **kwargs_json)
        try:
            self.coolest = serializer.load()
        except Exception as e:
            print(e)
            self.coolest = serializer.load_simple()

    def effective_einstein_radius(self):
        pass

    def effective_radial_slope(self):
        pass

    def half_light_radius(self):
        pass
