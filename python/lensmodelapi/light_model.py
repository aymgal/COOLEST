# Light model, as an ensemble of light profiles

from lensmodelapi import light_profile


class LightModel(object):

    def __init__(self, 
                 profile_names: list) -> None:
        self.profiles = []
        for name in profile_names:
            if name not in light_profile.SUPPORTED_PROFILES:
                raise ValueError("Profile '{name}' is not supported.")
            self.profiles.append(getattr(light_profile, name))
