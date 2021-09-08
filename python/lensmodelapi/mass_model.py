from lensmodelapi import mass_profile


class MassModel(object):

    def __init__(self, 
                 profile_names: list) -> None:
        self.profiles = []
        for name in profile_names:
            if name not in mass_profile.SUPPORTED_PROFILES:
                raise ValueError("Profile '{name}' is not supported.")
            self.profiles.append(getattr(mass_profile, name))
        

# class Substructure(MassModel):

#     def __init__(self):
#         super().__init__()
