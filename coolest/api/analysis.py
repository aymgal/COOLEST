__author__ = 'XXX'


from coolest.template.json import JSONSerializer


class Analysis(object):
    """
    Handles computation of model-independent quantities and other analysis computations
    """

    def __init__(self, coolest_file_path):
        self.coolest_data = JSONSerializer(coolest_file_path).load()

    def effective_einstein_radius(self):
        pass

    def effective_radial_slope(self):
        pass

    def half_light_radius(self):
        pass
