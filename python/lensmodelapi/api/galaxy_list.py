__author__ = 'aymgal'

from typing import List

from lensmodelapi.api.galaxy import Galaxy, SourceGalaxy, LensGalaxy


class GalaxyList(list):

    def __init__(self,
                 galaxies: List[Galaxy]):
        list.__init__(self, galaxies)

    def num_sources():
        count = 0
        for g in self:
            if isinstance(g, SourceGalaxy):
                count += 1
        return count

    def num_lenses():
        count = 0
        for g in self:
            if isinstance(g, LensGalaxy):
                count += 1
        return count
