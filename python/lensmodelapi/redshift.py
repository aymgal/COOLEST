# Single redshift plane

from lensmodelapi.base import APIBaseObject


class Redshift(APIBaseObject):

    def __init__(self, 
                 z: float) -> None:
        if z < 0:
            raise ValueError("Redshift cannot be negative.")
        self.z = z
        super().__init__()
        