__author__ == 'aymgal'


import numpy as np


def convert_image_to_data_units(image, mag_tot, mag_zero_point):
    """
    Rescale an image so that it has units of electrons per second (e/s),
    which is the default data units in COOLEST.
    :param image: input image (whatever units)
    :param mag_tot: target total magnitude, integrated over the whole image
    :param mag_zero_point: magnitude zero point of the observation (magnitude that corresponds to 1 e/s)
    """
    flux_tot = np.sum(image)
    image_unit_flux = image / flux_tot
    flux_unit_mag = 10 ** ( - (mag_tot - mag_zero_point) / 2.5)
    return image_unit_flux * flux_unit_mag
