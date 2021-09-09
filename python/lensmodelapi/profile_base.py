# Base class for any profile (mass or light)

from lensmodelapi.parameter import ParameterList


class Profile(object):

    def __init__(self,
                 name: str, 
                 description: str, 
                 parameters: ParameterList) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters
        self._type = None
        self._id = None

    def set_id(self, unique_id: str) -> None:
        self._id = unique_id
        

class ProfileList(list):

    def __init__(self, 
                 profile_module,
                 profile_names: list[str], 
                 *args, **kwargs):
        for name in profile_names:
            if name not in profile_module.SUPPORTED_PROFILES:
                raise ValueError("Profile '{name}' is not supported.")
            self.append(getattr(profile_module, name))
        list.__init__(self, *args, **kwargs)
