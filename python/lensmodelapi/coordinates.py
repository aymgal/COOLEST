__author__ = 'aymgal'

from lensmodelapi.observation import Observation


class Coordinates(object):

    # TODO: support for general pixel shape (using pixel to angle matrix)

    def __init__(self, 
                 ra_orientation: str = 'left', 
                 dec_orientation: str = 'top',
                 origin: str = 'center',
                 pixel_size: float = None,        # can be inferred from a Data object
                 ra_field_of_view: float = None,  # can be inferred from a Data object
                 dec_field_of_view: float = None, # can be inferred from a Data object
                 ) -> None:
        if ra_orientation not in ['left', 'top']:
            raise ValueError("RA orientation can either be 'left' or 'right'.")
        self.ra_orientation = ra_orientation
        if dec_orientation not in ['top', 'bottom']:
            raise ValueError("Dec orientation can either be 'left' or 'right'.")
        self.dec_orientation = dec_orientation
        self.pixel_size = pixel_size
        self.ra_field_of_view = ra_field_of_view
        self.dec_field_of_view = dec_field_of_view

    def update_with_observation(self, observation: Observation) -> None:
        self.pixel_size = observation.image.pixel_size
        self.ra_field_of_view  = observation.image.array_shape[0] * self.pixel_size
        self.dec_field_of_view = observation.image.array_shape[1] * self.pixel_size
