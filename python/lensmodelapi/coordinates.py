__author__ = 'aymgal'

from lensmodelapi.base import APIBaseObject


class Coordinates(APIBaseObject):

    _ra_orientations = ['left', 'right']
    _dec_orientations = ['top', 'bottom']
    _origins = ['center', 'bottom_left']

    def __init__(self, 
                 ra_orientation: str = 'left', 
                 dec_orientation: str = 'top',
                 origin: str = 'center',
                 ) -> None:
        if ra_orientation not in self._ra_orientations:
            raise ValueError(f"RA orientation can only be in {self._ra_orientations}.")
        self.ra_orientation = ra_orientation
        if dec_orientation not in self._dec_orientations:
            raise ValueError(f"Dec orientation can only be in {self._dec_orientations}.")
        self.dec_orientation = dec_orientation
        if origin not in self._origins:
            raise ValueError(f"Dec orientation can only be in {self._origins}.")
        self.origin = origin
        super().__init__()
