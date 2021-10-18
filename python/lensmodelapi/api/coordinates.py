__author__ = 'aymgal'

from lensmodelapi.api.base import APIBaseObject


class Coordinates(APIBaseObject):

    _orientations_ra = ['left', 'right']
    _orientations_dec = ['top', 'bottom']
    _origins = ['center', 'bottom_left']

    def __init__(self, 
                 orientation_ra: str = 'left', 
                 orientation_dec: str = 'top',
                 origin: str = 'center',
                 ) -> None:
        if orientation_ra not in self._orientations_ra:
            raise ValueError(f"RA orientation can only be in {self._orientations_ra}.")
        self.orientation_ra = orientation_ra
        if orientation_dec not in self._orientations_dec:
            raise ValueError(f"Dec orientation can only be in {self._orientations_dec}.")
        self.orientation_dec = orientation_dec
        if origin not in self._origins:
            raise ValueError(f"Dec orientation can only be in {self._origins}.")
        self.origin = origin
        super().__init__()
