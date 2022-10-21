__author__ = 'aymgal'


import numpy as np


def convert_image_to_data_units(image, pixel_size, mag_tot, mag_zero_point):
    """
    Rescale an image so that it has units of electrons per second (e/s),
    which is the default data units in COOLEST.
    :param pixel_size: pixel size (in arcsec) of the image
    :param image: input image (whatever units)
    :param mag_tot: target total magnitude, integrated over the whole image
    :param mag_zero_point: magnitude zero point of the observation (magnitude that corresponds to 1 e/s)
    """
    pixel_area = pixel_size**2
    flux_tot = np.sum(image) * pixel_area
    image_unit_flux = image / flux_tot
    delta_mag = mag_tot - mag_zero_point
    flux_unit_mag = 10 ** ( - delta_mag / 2.5 )
    return image_unit_flux * flux_unit_mag
