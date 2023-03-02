__author__ = 'aymgal'


from astropy.coordinates import SkyCoord

from coolest.template.json import JSONSerializer


class Analysis(object):
    """
    Handles computation of model-independent quantities and other analysis computations
    """

    def __init__(self, coolest_object, **kwargs_json):
        self.coolest = coolest_object

    def effective_einstein_radius(self):
        pass

    def effective_radial_slope(self):
        pass

    def half_light_radius(self):
        pass
