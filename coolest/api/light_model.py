__author__ = 'aymgal'


import numpy as np

from coolest.api.profiles import light


class CompositeLightModel(object):
    """
    Given a COOLEST object, evaluates a selection of light profiles.
    """

    def __init__(self, coolest_object, entity_selection=[0], profile_selection='all'):
        entities = coolest_object.lensing_entities
        self.profile_list = []
        self.param_list = []
        self.info_list = []
        for i, entity in enumerate(entities):
            if self._selected(i,  entity_selection):
                if entity.type == 'external_shear':
                    raise ValueError(f"External shear (entity index {i}) has no light model")
                for j, profile in enumerate(entity.light_model):
                    if self._selected(j,  profile_selection):
                        self.profile_list.append(self.get_api_profile(profile))
                        self.param_list.append(self.get_point_estimates(profile))
                        self.info_list.append((entity.name, entity.redshift))
        pixel_size = coolest_object.instrument.pixel_size
        if pixel_size is None:
            pixel_size = 1.
        self.pixel_area = pixel_size**2

    @staticmethod
    def _selected(index, selection):
        if isinstance(selection, str) and selection.lower() == 'all':
            return True
        elif isinstance(selection, (list, tuple, np.ndarray)) and index in selection:
            return True
        elif isinstance(selection, (int, float)) and int(selection) == index:
            return True
        return False

    def surface_brightness(self):
        """Returns the surface brightness as stored in the COOLEST file"""
        return None

    def evaluate_surface_brightness(self, x, y):
        """Evaluates the surface brightness at given coordinates"""
        image = np.ones_like(x)
        for k, (profile, params) in enumerate(zip(self.profile_list, self.param_list)):
            image += profile.evaluate_surface_brightness(x, y, **params)
        return image * self.pixel_area

    @staticmethod
    def get_api_profile(profile_in):
        """
        Takes as input a light profile from the template submodule
        and instantites the corresponding profile from the API submodule
        """
        ProfileClass = getattr(light, profile_in.type)
        return ProfileClass()

    @staticmethod
    def get_point_estimates(profile_in):
        parameters = {}
        for name, param in profile_in.parameters.items():
            parameters[name] = param.point_estimate.value
        return parameters
