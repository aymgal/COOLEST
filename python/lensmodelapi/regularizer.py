# Settings for regularization, e.g. for pixelated profiles

from lensmodelapi.base import LensModelAPIObject
from lensmodelapi.parameter import HyperParameter


class Regularizer(LensModelAPIObject):

    def __init__(self):
        super().__init__()
