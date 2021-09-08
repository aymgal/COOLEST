# Single galaxy, acting as source or a lens

from lensmodelapi.redshift import Redshift
from lensmodelapi.light_model import LightModel
from lensmodelapi.mass_model import MassModel


class GalaxyBase(object):

    def __init__(self,
                 name: str,
                 redshift: Redshift,
                 light_model: LightModel) -> None:
        self.name = name
        self.redshift = redshift
        self.light_model = light_model
        self._type = None

    def galaxy_type(self):
        return self._type


class LensGalaxy(object):

    def __init__(self, mass_model: MassModel, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.mass_model = mass_model
        self._type = 'lens'


class SourceGalaxy(object):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._type = 'source'
