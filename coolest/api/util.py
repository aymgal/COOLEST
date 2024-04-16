__author__ = 'aymgal'


import os
import math
import numpy as np
# from astropy.coordinates import SkyCoord
from skimage import measure

from coolest.template.json import JSONSerializer


def convert_image_to_data_units(image, mag_tot, mag_zero_point=None, coolest_object=None):
    """
    Rescale an image such that it has units of electrons per second (e/s),
    given a total magnitude and a magnitude zero-point.

    After rescaling, the total magnitude of the image_rescaled should corresponds to

    `-2.5 * np.log10(image_rescaled.sum()) + mag_zero_point = mag_tot`

    where `mag_zero_point` corresponds to the magnitude of 1 e/s.
    :param image: input image, as a 2D array.
    :param mag_tot: target total magnitude, integrated over the whole image
    :param mag_zero_point: magnitude zero point of the observation (that corresponds to 1 e/s). If coolest_object is not None, mag_zero_point is ignored.
    :param coolest_object: if given, will be used to retrieve the zero-point magnitude of the observation.
    """
    if coolest_object is None and mag_zero_point is None:
        raise ValueError("Either a COOLEST object or a zero-point magnitude should be provided.")
    flux_tot = np.sum(image)
    image_unit_flux = image / flux_tot
    if coolest_object is not None:
        mag_zp = coolest.observation.mag_zero_point
    else:
        mag_zp = mag_zero_point
    delta_mag = mag_tot - mag_zp
    flux_unit_mag = 10 ** ( - delta_mag / 2.5 )
    image_rescaled = image_unit_flux * flux_unit_mag
    return image_rescaled


def get_coolest_object(file_path, verbose=False, **kwargs_serializer):
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)
    serializer = JSONSerializer(file_path, **kwargs_serializer)
    return serializer.load(verbose=verbose)


def get_coordinates(coolest_object, offset_x=0., offset_y=0.):
    from coolest.api.coordinates import Coordinates  # prevents circular import errors
    nx, ny = coolest_object.observation.pixels.shape
    pix_scl = coolest_object.instrument.pixel_size
    half_size_x, half_size_y = nx * pix_scl / 2., ny * pix_scl / 2.
    x_at_ij_0  = - half_size_x + pix_scl / 2.  # position of x=0 with respect to bottom left pixel
    y_at_ij_0 = - half_size_y + pix_scl / 2.  # position of y=0 with respect to bottom left pixel
    matrix_pix2ang = pix_scl * np.eye(2)  # transformation matrix pixel <-> angle
    return Coordinates(nx, ny, matrix_ij_to_xy=matrix_pix2ang,
                       x_at_ij_0=x_at_ij_0 + offset_x, 
                       y_at_ij_0=y_at_ij_0 + offset_y)


def get_coordinates_from_regular_grid(field_of_view_x, field_of_view_y, num_pix_x, num_pix_y):
    from coolest.api.coordinates import Coordinates  # prevents circular import errors
    pix_scl_x = np.abs(field_of_view_x[0] - field_of_view_x[1]) / num_pix_x
    pix_scl_y = np.abs(field_of_view_y[0] - field_of_view_y[1]) / num_pix_y
    matrix_pix2ang = np.array([[pix_scl_x, 0.], [0., pix_scl_y]])
    x_at_ij_0  = field_of_view_x[0] + pix_scl_x / 2.
    y_at_ij_0 = field_of_view_y[0] + pix_scl_y / 2.
    return Coordinates(
        num_pix_x, num_pix_y, matrix_ij_to_xy=matrix_pix2ang,
        x_at_ij_0=x_at_ij_0, y_at_ij_0=y_at_ij_0,
    )


def get_coordinates_set(coolest_file_list, reference=0):
    coordinates_list = []
    for coolest_file in coolest_file_list:

        # TODO: compute correct offsets when each file has
        # obs = self.coolest.observation
        # sky_coord = SkyCoord(obs.ra, obs.dec, frame='icrs')
        # ra, dec = sky_coord.to_string(style='hmsdms').split(' ')

        coordinates = get_coordinates(coolest_file)
        coordinates_list.append(coordinates)
    return coordinates_list


def array2image(array, nx=0, ny=0):
    """Convert a 1d array into a 2d array.

    Note: this only works when length of array is a perfect square, or else if
    nx and ny are provided

    :param array: image values
    :type array: array of size n**2
    :returns:  2d array
    :raises: AttributeError, KeyError
    """
    if nx == 0 or ny == 0:
        # Avoid turning n into a JAX-traced object with jax.numpy.sqrt
        n = int(np.sqrt(len(array)))
        if n**2 != len(array):
            err_msg = f"Input array size {len(array)} is not a perfect square."
            raise ValueError(err_msg)
        nx, ny = n, n
    image = array.reshape(int(nx), int(ny))
    return image


def image2array(image):
    """Convert a 2d array into a 1d array.

    :param array: image values
    :type array: array of size (n,n)
    :returns:  1d array
    :raises: AttributeError, KeyError
    """
    # nx, ny = image.shape  # find the size of the array
    # imgh = np.reshape(image, nx * ny)  # change the shape to be 1d
    # return imgh
    return image.ravel()


def downsampling(image, factor=1):
    if factor < 1:
        raise ValueError(f"Downscaling factor must be > 1")
    if factor == 1:
        return image
    f = int(factor)
    nx, ny = np.shape(image)
    if int(nx/f) == nx/f and int(ny/f) == ny/f:
        down = image.reshape([int(nx/f), f, int(ny/f), f]).mean(3).mean(1)
        return down
    else:
        raise ValueError(f"Downscaling factor {factor} is not possible with shape ({nx}, {ny})")


def effective_radius(light_map, x, y, outer_radius=10, initial_guess=1, initial_delta_pix=10, n_iter=10):
    """Computes the effective radius of the 2D surface brightness profile, 
    based on a definition similar to the half-light radius.
    NOTE: This functions assumes that the profile is centered on the grid.

    Parameters
    ----------
    light_map : ndarray
        2D array of the light model
    x : ndarray
        x-coordinates associated to the light model
    y : ndarray
        y-coordinates associated to the light model
    outer_radius : int, optional
        outer limit of integration within which half the light is calculated to estimate the effective radius, by default 10
    initial_guess : int, optional
        Initial guess for effective radius in arcsecond, by default 1
    initial_delta_pix : int, optional
        Initial step size in pixels before shrinking in future iterations, by default 10
    n_iter : int, optional
        Number of iterations, by default 5

    Returns
    -------
    (float, float)
        Effective radius and spacing of the coordinates grid (approximate accuracy)

    Raises
    ------
    RuntimeError
        If integration loop exceeds outer bound before convergence.
    """
    #initialize
    grid_res=np.abs(x[0,0]-x[0,1])
    initial_delta=grid_res*initial_delta_pix #default inital step size is 10 pixels
    r_grid=np.hypot(x, y)
    total_light=np.sum(light_map[r_grid<outer_radius])
    cumulative_light=np.sum(light_map[r_grid<initial_guess])
    if cumulative_light < total_light/2: #move outward
        direction=1
    elif cumulative_light > total_light/2: #move inward
        direction=-1
    else:
        return initial_guess
    r_eff=initial_guess
    delta=initial_delta
    loopcount=0

    for n in range(n_iter): #overshoots, turn around and backtrack at higher precision
        while (total_light/2.-cumulative_light)*direction>0: 
            if loopcount > 100:
                raise RuntimeError('Stuck in very long (possibly infinite) loop')
            r_eff=r_eff+delta*direction
            cumulative_light=np.sum(light_map[r_grid<r_eff])
            loopcount+=1
        direction=direction*-1
        delta=delta/2.

    return r_eff, grid_res
            

def ellipticity_from_moments(light_map, pixel_size):
    # compute central momoments
    try:
        # scikit-image version 0.19.3 and older
        mu = measure.moments_central(light_map, order=2, spacing=(pixel_size, pixel_size))
    except IndexError:
        # scikit-image version 0.20.0 and beyond
        mu = measure.moments_central(light_map, order=2, spacing=pixel_size)

    # use the moments to estimate orientation and ellipticity (https://en.wikipedia.org/wiki/Image_moment)
    mu_20_ = mu[2, 0] / mu[0, 0]
    mu_02_ = mu[0, 2] / mu[0, 0]
    mu_11_ = mu[1, 1] / mu[0, 0]
    lambda_1 = (mu_20_ + mu_02_) / 2. + np.sqrt(4*mu_11_**2 + (mu_20_ - mu_02_)**2) / 2.
    lambda_2 = (mu_20_ + mu_02_) / 2. - np.sqrt(4*mu_11_**2 + (mu_20_ - mu_02_)**2) / 2.
    q = np.sqrt(lambda_2 / lambda_1)  # b/a, axis ratio
    phi = np.arctan(2. * mu_11_ / (mu_20_ - mu_02_)) / 2.  # position angle
    if mu_02_ > mu_20_:
        phi += np.pi / 2.  # makes it consistent angles conventions in COOLEST
    return phi, q


def azim_averaged_two_point_correlation(light_image, dpix, rmax, Nbins):
    """
    The two point correlation function can be obtained from the covariance matrix of an image and the distances between its pixels.
    By binning the covariance matrix entries in distance (or radial) bins, one can obtain the 1D correlation function.
    There are two ways to obtain the covariance matrix:
    1) it is equivalent to the inverse Fourier transform of the power spectrum, and
    2) by calculating explicitly the covariance between any two pixels
    Here we use the first way.

    Parameters
    ----------
    light_image : 2D ndarray
        Pixels of the image to analyse.
    dpix : float
        Pixel size
    Nbins : int, optional
        The number of radial bins to use for converting the 2D covariance matrix into a 1D correlation function.
    rmax : float, optional
        A value for the maximum extent of the radial bins. If none is given then it is equal to half the diagonal of the provided image. 

    Returns
    -------
    (array, array, array, array)
        The location, value, uncertainty and covariance matrix 
        The covariance matrix here is the inverse of fourier transform of power spectrum)
    """
    # Fourier transform image
    fouriertf = np.fft.fft2(light_image, norm='ortho')
    # Power spectrum (the square of the signal)
    absval2 = fouriertf.real**2 + fouriertf.imag**2
    # Covariance matrix (the inverse fourier transform of the power spectrum)
    complex_cov = np.fft.fftshift(np.fft.ifft2(absval2, norm='ortho'))
    cov = complex_cov.real
    
    # Bin the 2D covariance matrix into radial bins
    rmin = 0.0
    dr = (rmax-rmin)/Nbins
    bins = np.arange(rmin,rmax,dr)
    vals = [[] for _ in range(len(bins))]
    # Ni = Nj = the total number of pixels in the image
    Ni = cov.shape[1]
    Nj = cov.shape[0]
    for i in range(0,Ni):
        for j in range(0,Nj):
            r = np.hypot((j-Nj/2.0)*dpix,(i-Ni/2.0)*dpix)
            if r < rmax and i != j:
                index = int(np.floor(r/dr))
                vals[index].append(cov[i][j])
                
    means = np.zeros(len(bins))                    
    sdevs = np.zeros(len(bins))
    for i in range(0,len(bins)):
        if len(vals[i]) > 0:
            means[i] = np.mean(vals[i])
            sdevs[i] = np.std(vals[i])

    return bins, means, sdevs, cov
    

def lensing_information(data_lens_sub, x, y, theta_E, noise_map, center_x_lens=0, center_y_lens=0,
                        a=16, b=0, arc_mask=None):
    """
    Computes the 'lensing information' defined in Tan et al. 2023, Equations (8) and (9).
    https://ui.adsabs.harvard.edu/abs/2023arXiv231109307T/abstract

    Parameters
    ----------
    data_lens_sub : np.ndarray
        Imaging data as a 2D array. It is assumed to contain no lens light.
    x : np.ndarray
        2D array of x coordinates, in arcsec.
    y : np.ndarray
        2D array of y coordinates, in arcsec.
    theta_E : float
        Einstein radius in arcsec, by default None
    noise_map : np.ndarray
        2D array with 1-sigma noise level per pixel (same units as `data_lens_sub`), by default None
    center_x_lens : int, optional
        x coordinates of the center of the lens, by default 0
    center_y_lens : int, optional
        y coordinates of the center of the lens, by default 0
    a : int, optional
        Exponent in Eq. (9) from Yi Tan et al. 2023, by default 16
    b : int, optional
        Exponent in Eq. (9) from Yi Tan et al. 2023, by default 0
    arc_mask : np.ndarray, optional
        Binary 2D array with 1s where there is are lensed arcs, by default None

    Returns
    -------
    4-tuple
        Lensing information I, Einstein radius, reference azimuthal angle, total mask used for computing I
    """
    if arc_mask is None:
        arc_mask = np.ones_like(data_lens_sub)
    # estimate background noise from one corner of the noise map
    sigma_bkg = np.mean(noise_map[:10, :10])
    # build a mask to only consider pixels at least 3 times the background noise level
    snr_mask = np.where(data_lens_sub > 3.*sigma_bkg, 1., 0.)
    # combine user mask and SNR mask
    arc_mask_tot = snr_mask * arc_mask
    # shift coordinates so that lens is at (0, 0)
    theta_x, theta_y = x - center_x_lens, y - center_y_lens
    # compute polar coordinates centered on the lens
    theta_r = np.hypot(theta_x, theta_y)
    phi = np.arctan2(theta_y, theta_x)
    # find index of the brightest pixel (within the arc mask)
    max_idx = np.where(data_lens_sub == (data_lens_sub*arc_mask_tot).max())
    # get azimuthal angle corresponding to the brightest pixel
    phi_ref = float(np.arctan2(theta_y[max_idx], theta_x[max_idx]))
    # compute the weights following Eq. (9) from Yi Tan et al. 2023
    weights = ( 1. + np.abs(theta_r - theta_E) / theta_E * (1 + np.abs(phi - phi_ref) / phi_ref)**b )**a
    # compute the weighted sum
    numerator = np.sum(arc_mask_tot*weights*data_lens_sub)
    denominator = np.sqrt(np.sum(arc_mask_tot*noise_map**2))
    lens_I = numerator / denominator
    return lens_I, theta_E, phi_ref, arc_mask_tot


def split_lens_source_params(coolest_list, name_list, lens_light=False):
    """
    Read several json files already containing a model with the results of this model fitting

    INPUT
    -----
    file_list: list, list of path or names of the file to read
    name_list: list, list of shorter names to distinguish the files
    lens_light: bool, if True, computes the lens light kwargs as well (not yet implemented)

    OUTPUT
    ------
     param_all_lens, param_all_source: organized dictionaries readable by plotting function
    """

    param_all_lens = {}
    param_all_source = {}
    for idx_file, file_name in enumerate(name_list):

        print(file_name)
        coolest_obj = coolest_list[idx_file]

        if coolest_obj.mode == 'MAP':
            print('LENS COOLEST : ', coolest_obj.mode)
        else:
            print('LENS COOLEST IS NOT MAP, BUT IS ', coolest_obj.mode)

        lensing_entities_list = coolest_obj.lensing_entities

        param_lens = {}
        param_source = {}

        if lensing_entities_list is not None:

            creation_lens_source_light = True

            idx_lens = 0
            idx_lens_light = 0
            idx_source = 0
            idx_ps = 0

            min_red = 0
            max_red = 5
            creation_red_list = True
            red_list = []
            MultiPlane = False
            for lensing_entity in lensing_entities_list:
                red_list.append(lensing_entity.redshift)
            min_red = np.min(red_list)
            max_red = np.max(red_list)

            for lensing_entity in lensing_entities_list:
                if lensing_entity.type == "Galaxy":
                    galac = lensing_entity

                    if galac.redshift > min_red:
                        # SOURCE OF LIGHT
                        light_list = galac.light_model
                        for light in light_list:

                            if light.type == 'Sersic':
                                read_sersic(light, param_source)
                                idx_source += 1
                            else:
                                print('Light Type ', light.type, ' not yet implemented.')

                    if galac.redshift < max_red:
                        # LENSING GALAXY
                        if galac.redshift > min_red:
                            MultiPlane = True
                            print('Multiplane lensing to consider.')
                        mass_list = galac.mass_model
                        for mass in mass_list:

                            if mass.type == 'PEMD':
                                read_pemd(mass, param_lens)
                                idx_lens += 1
                            elif mass.type == 'SIE':
                                read_sie(mass, param_lens)
                                idx_lens += 1
                            else:
                                print('Mass Type ', mass.type, ' not yet implemented.')

                    if (galac.redshift <= min_red) and (galac.redshift >= max_red):
                        print('REDSHIFT ', galac.redshift, ' is not in the range ]', min_red, ',', max_red, '[')

                elif lensing_entity.type == "MassField":
                    shear_list = lensing_entity.mass_model
                    for shear_idx in shear_list:

                        if shear_idx.type == 'ExternalShear':
                            read_shear(shear_idx, param_lens)
                            idx_lens += 1
                        else:
                            print("type of Shear ", shear_idx.type, " not implemented")
                else:
                    print("Lensing entity of type ", lensing_enity.type, " is unknown.")

        param_all_lens[name_list[idx_file]] = param_lens
        param_all_source[name_list[idx_file]] = param_source

    return param_all_lens, param_all_source


def read_shear(mass, param={}, prefix='SHEAR_0_'):
    """
    Reads the parameters of a coolest.template.classes.profiles.mass.ExternalShear object

    INPUT
    -----
    mass : coolest.template.classes.profiles.mass.ExternalShear object
    param : dict, already existing dictionnary with ordered parameters readable by plotting function
    prefix : str, prefix to use in saving parameters names

    OUTPUT
    ------
    param : updated param
    """

    for mass_name, mass_param in mass.parameters.items():
        p = getattr(mass_param.point_estimate, 'value')
        p_84 = getattr(mass_param.posterior_stats, 'percentile_84th')
        p_16 = getattr(mass_param.posterior_stats, 'percentile_16th')
        p_med = getattr(mass_param.posterior_stats, 'median')
        p_mean = getattr(mass_param.posterior_stats, 'mean')
        latex_name = getattr(mass_param, 'latex_str')
        if mass_name == 'gamma_ext':
            param[prefix + 'gamma_ext'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                           'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'phi_ext':
            param[prefix + 'phi_ext'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                         'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        else:
            print(shear_name, " not known")
    print('\t Shear correctly added')

    return param


def read_pemd(mass, param={}, prefix='PEMD_0_'):
    """
    Reads the parameters of a coolest.template.classes.profiles.mass.PEMD object

    INPUT
    -----
    mass : coolest.template.classes.profiles.mass.PEMD object
    param : dict, already existing dictionnary with ordered parameters readable by plotting function
    prefix : str, prefix to use in saving parameters names

    OUTPUT
    ------
    param : updated param
    """

    for mass_name, mass_param in mass.parameters.items():
        p = getattr(mass_param.point_estimate, 'value')
        p_84 = getattr(mass_param.posterior_stats, 'percentile_84th')
        p_16 = getattr(mass_param.posterior_stats, 'percentile_16th')
        p_med = getattr(mass_param.posterior_stats, 'median')
        p_mean = getattr(mass_param.posterior_stats, 'mean')
        latex_name = getattr(mass_param, 'latex_str')
        if mass_name == 'theta_E':
            param[prefix + 'theta_E'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                         'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'q':
            param[prefix + 'q'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                   'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'phi':
            param[prefix + 'phi'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                     'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'center_x':
            param[prefix + 'cx'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'center_y':
            param[prefix + 'cy'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'gamma':
            param[prefix + 'gamma'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                       'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        else:
            print(mass_name, " not known")

    print('\t PEMD correctly added')

    return param


def read_sie(mass, param={}, prefix='SIE_0_'):
    """
    Reads the parameters of a coolest.template.classes.profiles.mass.SIE object

    INPUT
    -----
    mass : coolest.template.classes.profiles.mass.SIE object
    param : dict, already existing dictionnary with ordered parameters readable by plotting function
    prefix : str, prefix to use in saving parameters names

    OUTPUT
    ------
    param : updated param
    """

    for mass_name, mass_param in mass.parameters.items():
        p = getattr(mass_param.point_estimate, 'value')
        p_84 = getattr(mass_param.posterior_stats, 'percentile_84th')
        p_16 = getattr(mass_param.posterior_stats, 'percentile_16th')
        p_med = getattr(mass_param.posterior_stats, 'median')
        p_mean = getattr(mass_param.posterior_stats, 'mean')
        latex_name = getattr(mass_param, 'latex_str')
        if mass_name == 'theta_E':
            param[prefix + 'theta_E'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                         'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'q':
            param[prefix + 'q'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                   'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'phi':
            param[prefix + 'phi'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                     'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'center_x':
            param[prefix + 'cx'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif mass_name == 'center_y':
            param[prefix + 'cy'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        else:
            print(mass_name, " not known")

    print('\t SIE correctly added')

    return param


def read_sersic(light, param={}, prefix='Sersic_0_'):
    """
    Reads the parameters of a coolest.template.classes.profiles.light.Sersic object

    INPUT
    -----
    mass : coolest.template.classes.profiles.light.Sersic object
    param : dict, already existing dictionnary with ordered parameters readable by plotting function
    prefix : str, prefix to use in saving parameters names

    OUTPUT
    ------
    param : updated param
    """

    for light_name, light_param in light.parameters.items():
        p = getattr(light_param.point_estimate, 'value')
        p_84 = getattr(light_param.posterior_stats, 'percentile_84th')
        p_16 = getattr(light_param.posterior_stats, 'percentile_16th')
        p_med = getattr(light_param.posterior_stats, 'median')
        p_mean = getattr(light_param.posterior_stats, 'mean')
        latex_name = getattr(light_param, 'latex_str')
        if light_name == 'I_eff':
            param[prefix + 'A'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                   'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'n':
            param[prefix + 'n_sersic'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                          'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'theta_eff':
            param[prefix + 'R_sersic'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                          'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'q':
            param[prefix + 'q'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                   'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'phi':
            param[prefix + 'phi'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                     'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'center_x':
            param[prefix + 'cx'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        elif light_name == 'center_y':
            param[prefix + 'cy'] = {'point_estimate': p, 'percentile_84th': p_84, 'percentile_16th': p_16,
                                    'median': p_med, 'mean': p_mean, 'latex_str': latex_name}
        else:
            print(light_name, " not known")

    print('\t Sersic correctly added')

    return param


def find_critical_lines(coordinates, mag_map):
    # invert and find contours corresponding to infinite magnification (i.e., changing sign)
    inv_mag = 1. / np.array(mag_map)
    contours = measure.find_contours(inv_mag, 0.)
    # convert to model coordinates
    lines = []
    for contour in contours:
        curve_x, curve_y = coordinates.pixel_to_radec(contour[:, 1], contour[:, 0])
        lines.append((np.array(curve_x), np.array(curve_y)))
    return lines


def find_caustics(crit_lines, composable_lens):
    """`composable_lens` can be an instance of `ComposableLens` or `ComposableMass`"""
    lines = []
    for cline in crit_lines:
        cl_src_x, cl_src_y = composable_lens.ray_shooting(cline[0], cline[1])
        lines.append((np.array(cl_src_x), np.array(cl_src_y)))
    return lines


def find_all_lens_lines(coordinates, composable_lens):
    """`composable_lens` can be an instance of `ComposableLens` or `ComposableMass`"""
    from coolest.api.composable_models import ComposableLensModel, ComposableMassModel  # avoiding circular imports 
    if isinstance(composable_lens, ComposableLensModel):
        mag_fn = composable_lens.lens_mass.evaluate_magnification
    elif isinstance(composable_lens, ComposableMassModel):
        mag_fn = composable_lens.evaluate_magnification
    else:
        raise ValueError("`composable_lens` must be a ComposableLensModel or a ComposableMassModel.")
    mag_map = mag_fn(*coordinates.pixel_coordinates)
    crit_lines = find_critical_lines(coordinates, mag_map)
    caustics = find_caustics(crit_lines, composable_lens)
    return crit_lines, caustics
    

def resample_multivariate_normal(samples, num_samples=5_000, **kwargs_cov):
    """Resample following multi-variate normal distribution"""
    mean = np.mean(samples, axis=0)
    cov = np.cov(samples.T, **kwargs_cov)
    num_params = samples.shape[1]
    resampled = np.random.multivariate_normal(
        mean=mean, cov=cov, size=(int(num_samples/num_params), num_params)).reshape((-1, num_params))
    return resampled
