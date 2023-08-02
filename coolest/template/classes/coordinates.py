__author__ = 'aymgal'


from astropy.coordinates import SkyCoord

from coolest.template.classes.base import APIBaseObject


class CoordinatesOrigin(APIBaseObject):
    """Defines the origin of the coordinate system, given in RA-Dec.
    That origin is then assumed to lie at the center of a data pixel.

    Parameters
    ----------
    ra : str, optional
        Right ascension (hms format), by default '0h0m0.0s'
    dec : str, optional
        Declination (dms format), by default '0d0m0.0s'
    """

    def __init__(self, 
                 ra: str = '0h0m0.0s',
                 dec: str = '0d0m0.0s') -> None:
        self.ra, self.dec = self._check_sky_coord(ra, dec)
        super().__init__()

    def _check_sky_coord(self, origin_ra, origin_dec):
        # creates astropy object to check everything is good
        sky_coord = SkyCoord(origin_ra, origin_dec, frame='icrs')
        return sky_coord.to_string(style='hmsdms').split(' ')


# class Coordinates(APIBaseObject):

#     _orientations_ra = ['left', 'right']
#     _orientations_dec = ['top', 'bottom']
#     _origins = ['center', 'bottom-left']
#     _angles = ['east-to-north', 'west-to-north', 'east-to-south', 'west-to-south']
#     _coord_in_pixel = ['center', 'bottom-left']

#     def __init__(self, 
#                  orientation_ra: str = 'left', 
#                  orientation_dec: str = 'top',
#                  origin_position: str = 'center',
#                  angles_orientation: str = 'east-to-north',
#                  coordinate_in_pixel: str = 'center',
#                  ) -> None:
#         if orientation_ra not in self._orientations_ra:
#             raise ValueError(f"RA orientation can only be in {self._orientations_ra}.")
#         self.orientation_ra = orientation_ra
#         if orientation_dec not in self._orientations_dec:
#             raise ValueError(f"Dec orientation can only be in {self._orientations_dec}.")
#         self.orientation_dec = orientation_dec
#         if origin_position not in self._origins:
#             raise ValueError(f"Position of the origin can only be in {self._origins}.")
#         self.origin_position = origin_position
#         if angles_orientation not in self._angles:
#             raise ValueError(f"Angle orientation can only be in {self._angles}.")
#         self.angles_orientation = angles_orientation
#         if coordinate_in_pixel not in self._coord_in_pixel:
#             raise ValueError(f"Coordinate position inside a given pixel "
#                              "can only be in {self._coord_in_pixel}.")
#         self.coordinate_in_pixel = coordinate_in_pixel
#         super().__init__()

#     def update_with_instrument(self, instrument):
#         pixel_size = instrument.pixel_size
#         sign_ra  = (self.orientation_ra == 'left')
#         sign_dec = (self.orientation_dec == 'top')
#         self.pix2angle_matrix = [
#             [sign_ra * pixel_size, 0],
#             [0, sign_dec * pixel_size],
#         ]
#         if self.origin_position == 'center':
#             half_fov_ra = instrument.field_of_view_ra / 2.
#             half_fov_dec = instrument.field_of_view_ra / 2.
#             self.ra_at_xy_0 = - half_fov_ra + pixel_size / 2.
#             self.dec_at_xy_0 = - half_fov_dec + pixel_size / 2.
#         else:
#             self.ra_at_xy_0 = 0.
#             self.dec_at_xy_0 = 0.
