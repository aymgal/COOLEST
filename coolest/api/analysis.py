__author__ = 'aymgal', 'mattgomer', 'gvernard'

import numpy as np
from astropy.coordinates import SkyCoord
import logging

from coolest.api.composable_models import *
from coolest.api import util

# logging settings
logging.getLogger().setLevel(logging.INFO)

__all__ = [
    'Analysis',
]

class Analysis(object):
    """Handles computation of model-independent quantities 
    and other analysis computations.
    
    NOTE: Except for methods that do have a `coordinates` keyword argument,
    the grid used to performed the computations will always be the one corresponding
    to the instrument / observation field-of-view, with resolution controlled by the
    `supersampling` keyword argument below.

    Parameters
    ----------
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str
        Directory which contains the COOLEST template and other data files
    supersampling : int, optional
        Supersampling factor (relative to the instrument pixel size)
        that defines the grid on which computations are performed, by default 1.
    """

    def __init__(self, coolest_object, coolest_directory, supersampling=1):
        self.coolest = coolest_object
        self.coolest_dir = coolest_directory
        base_coordinates = util.get_coordinates(self.coolest)
        if supersampling > 1:
            self.coordinates = base_coordinates.create_new_coordinates(pixel_scale_factor=1./supersampling)
        else:
            self.coordinates = base_coordinates

    def effective_einstein_radius(self, center=None, initial_guess=1, initial_delta_pix=10, 
                                  n_iter=5, return_accuracy=False, max_loopcount=100, 
                                  **kwargs_selection):
        """Calculates Einstein radius for a kappa grid starting from an initial guess with large step size and zeroing in from there.
        Uses the grid from the create_kappa_image which is built from the coolest file.

        Parameters
        ----------
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate Einstein radius; if None, use the value from create_kappa_image, by default None
        initial_guess : int, optional
            initial guess for Einstein radius, by default 1
        initial_delta_pix : int, optional
            initial step size before shrinking in future iterations, by default 10
        n_iter : int, optional
            number of iterations, by default 5
        return_accuracy : bool, optional
            if True, return estimate of accuracy as well as R_Ein value, by default False

        Returns
        -------
        float, or (float, float) if return_accuracy is True
            Effective Einstein radius

        Raises
        ------
        RuntimeError
            If the algorithm is running for more than 100 loops.
        """
        if kwargs_selection is None:
            kwargs_selection = {}
        mass_model = ComposableMassModel(self.coolest, self.coolest_dir, **kwargs_selection)

        # get an image of the convergence
        x, y = self.coordinates.pixel_coordinates
        kappa_image = mass_model.evaluate_convergence(x, y)

        # import matplotlib.pyplot as plt
        # plt.imshow(np.log10(kappa_image))
        # plt.show()

        # select a center
        if center is None:
            center_x, center_y = mass_model.estimate_center()
        else:
            center_x, center_y = center

        def _loop_until_overshoot(r_Ein, delta, direction, runningtotal, total_pix):
            """
            this subfunction iteratively adjusts the mask radius by delta either inward or outward until the sign flips on mean_kappa-area
            """
            loopcount=0
            if r_Ein==np.nan: #return nan if given nan (needed when I put this in a loop below)
                return np.nan, np.nan, 0, runningtotal, total_pix
            while (runningtotal-total_pix)*direction>0:
                if loopcount > max_loopcount:
                    raise RuntimeError('Stuck in very long (possibly infinite) loop')
                if direction > 0:
                    mask=only_between_r1r2(r_Ein, r_Ein+delta,r_grid)
                else:
                    mask=only_between_r1r2(r_Ein-delta, r_Ein, r_grid)
                kappa_annulus=np.sum(kappa_image[mask])
                added_pix=np.sum(mask)
                runningtotal=runningtotal+kappa_annulus*direction
                total_pix=total_pix+added_pix*direction
                r_Ein=r_Ein+delta*direction

                if r_Ein < min_guess:
                    #Either we overshot into the center region between pixels (rare), or kappa is subcritical.
                    #check starting from zero
                    mask=only_between_r1r2(0,min_guess,r_grid)
                    runningtotal=np.sum(kappa_image[mask])
                    total_pix=np.sum(mask)
                    if runningtotal-total_pix < 0:
                        logging.warning('kappa is sub-critical, Einstein radius undefined.')
                        return np.nan, np.nan, 0, runningtotal, total_pix
                loopcount+=1
            return r_Ein, delta, direction, runningtotal, total_pix

        def only_between_r1r2(r1, r2, r_grid):
            if r1 > r2:
                raise ValueError('r2 must be greater than r1')
            return (r_grid >= r1) & (r_grid < r2)

        #some initialization: if there is an even number of pixels we don't want to be stuck in the center between 4 pixels.
        grid_res=np.abs(x[0,0]-x[0,1])
        initial_delta=grid_res*initial_delta_pix #default inital step size is 10 pixels
        min_guess=grid_res*np.sqrt(2)+1e-6
        initial_guess=max(initial_guess,min_guess) #initial guess must include at least one pixel

        r_grid=np.sqrt((x-center_x)**2+(y-center_y)**2)
        mask=only_between_r1r2(0,initial_guess,r_grid)
        runningtotal=np.sum(kappa_image[mask])
        total_pix=np.sum(mask)
        if runningtotal > total_pix: #move outward
            direction=1
        elif runningtotal < total_pix: #move inward
            direction=-1
        else:
            return initial_guess
        r_Ein=initial_guess
        delta=initial_delta

        for n in range(n_iter):
            #overshoots, turn around and backtrack at higher precision
            r_Ein, delta, direction, runningtotal, total_pix = _loop_until_overshoot(r_Ein, delta, direction, runningtotal, total_pix)
            direction=direction*-1
            delta=delta/2
        accuracy=grid_res/2 #after testing, accuracy is about grid_res/2
        if np.isnan(r_Ein):
            accuracy=np.nan

        if return_accuracy:
            return r_Ein, accuracy
        else:
            return r_Ein

    def kappa_1d_profile(self, center=None, r_vec=np.linspace(0, 10, 100),**kwargs_selection):
        """Calculates 1D profile using the kappa grid.

        Parameters
        ----------
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate; if None, use the value from , by default None
        r_vec : _type_, optional
            range of radii over which to calculate the 1D profile, by default np.linspace(0, 10, 100)

        Returns
        -------
        (array, array)
            kappa values and associated radius values
        """
        if kwargs_selection is None:
            kwargs_selection = {}
        mass_model = ComposableMassModel(self.coolest, self.coolest_dir, **kwargs_selection)
        x, y = self.coordinates.pixel_coordinates
        kappa_image = mass_model.evaluate_convergence(x, y)
        if center is None:
            center_x, center_y = mass_model.estimate_center()
        else:
            center_x, center_y = center
        r_grid=np.sqrt((x-center_x)**2+(y-center_y)**2)
        kappa_profile=np.zeros_like(r_vec)
        for r_i,r in enumerate(r_vec):
            if r_i==0:
                r_min=0
            else:
                r_min=r_vec[r_i-1]
            in_radial_bin=(r_grid > r_min) & (r_grid <= r)
            kappa_profile[r_i]=np.mean(kappa_image[in_radial_bin])
        return kappa_profile, r_vec

    def effective_radial_slope(self, r_eval=None, center=None, r_vec=np.linspace(0, 10, 100),**kwargs_selection):
        """Numerically calculates slope of the kappa profile. Because this is defined on a grid, it is not as accurate or robust as an analytical calculation. 

        Parameters
        ----------
        r_eval : float, optional
            radius at which to return a single value of the slope (e.g. Einstein radius). If None (default), returns slope for all values in r_vec, by default None
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate; if None, use the value from create_kappa_image, by default None
        r_vec : array-like, optional
            range of radii over which to calculate the 1D profile, by default np.linspace(0, 10, 100)

        Returns
        -------
        float
            Effective slope
        """
        kappa_profile, r_vec =self.kappa_1d_profile(center=center, r_vec=r_vec, **kwargs_selection)
        rise=np.log10(kappa_profile[:-1])-np.log10(kappa_profile[1:])
        run=np.log10(r_vec[:-1])-np.log10(r_vec[1:])
        slope=np.append(0,rise/run)#add a zero at r=0 so that slope as same size as r_vec
        if r_eval==None:
            return slope 
        else:
            closest_r = self._find_nearest(r_vec,r_eval) #just takes closest r. Could rebuild it to interpolate.
            return slope[r_vec==closest_r]

    def effective_radius_light(self, outer_radius=10, center=None, coordinates=None,
                               initial_guess=1, initial_delta_pix=10, 
                               n_iter=10, return_model=False, return_accuracy=False,
                               circular_mask_radius=None, **kwargs_selection):
        """Computes the effective radius of the 2D surface brightness profile, 
        based on a definition similar to the half-light radius.

        Parameters
        ----------
        outer_radius : int, optional
            outer limit of integration within which half the light is calculated to estimate the effective radius, by default 10
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate Einstein radius; if None, use the value from create_kappa_image, by default None
        coordinates : Coordinates, optional
            Instance of a Coordinates object to be used for the computation.
            If None, will use an instance based on the Instrument, by default None
        initial_guess : int, optional
            Initial guess for effective radius in arcsecond, by default 1
        initial_delta_pix : int, optional
            Initial step size in pixels before shrinking in future iterations, by default 10
        n_iter : int, optional
            Number of iterations, by default 5
        circular_mask_radius : float, optional
            If not None, multiply the flux by a circular mask with radius `circular_mask_radius` 
            to force to zero any flux outside of it.
        return_model : bool, optional
            If True, also returns the surface brightness map used to comouted the radius. By default False.
        return_accuracy : bool, optional
            if True, return a rough estimate of accuracy as well, by default False

        Returns
        -------
        float
            Effective radius

        Raises
        ------
        Warning
            If integration loop exceeds outer bound before convergence.
        """
        if kwargs_selection is None:
            kwargs_selection = {}

        light_model = ComposableLightModel(self.coolest, self.coolest_dir, **kwargs_selection)

        # select a center
        if center is None:
            center_x, center_y = light_model.estimate_center()
        else:
            center_x, center_y = center

        # get an image of the convergence
        if coordinates is None:
            x, y = self.coordinates.pixel_coordinates
        else:
            x, y = coordinates.pixel_coordinates
        # make sure to evaluate the profile such that it is centered on the image
        x_ = x + center_x
        y_ = y + center_y
        light_image = light_model.evaluate_surface_brightness(x_, y_)
        light_image[np.isnan(light_image)] = 0.
        
        #if limit of integration exceeds FoV, raise warning
        if coordinates is None:
            x_FoV = self.coolest.observation.pixels.field_of_view_x
            y_FoV = self.coolest.observation.pixels.field_of_view_y
        else:
            x_FoV = (coordinates.extent[0], coordinates.extent[1])
            y_FoV = (coordinates.extent[2], coordinates.extent[3])
        out_of_FoV=False
        if outer_radius - center_x < x_FoV[0] or outer_radius + center_x > x_FoV[1]:
            out_of_FoV=True
        if outer_radius - center_y < y_FoV[0] or outer_radius + center_y > y_FoV[1]:
            out_of_FoV=True
        if out_of_FoV is True:
            logging.warning("Outer limit of integration exceeds FoV; effective radius may not be accurate.")

        if circular_mask_radius is not None:  # circular mask that fills the FoV
            mask = (np.hypot(x, y) < circular_mask_radius).astype(float)  # 0. and 1. only
            light_image *= mask
            # import matplotlib.pyplot as plt
            # plt.imshow(np.log10(light_image))
            # plt.show()
            # raise

        r_eff, accuracy = util.effective_radius(
            light_image, x, y, outer_radius=outer_radius, initial_guess=initial_guess, 
            initial_delta_pix=initial_delta_pix, n_iter=n_iter
        )

        if return_model and return_accuracy:
            return r_eff, accuracy, light_image
        elif return_model:
            return r_eff, light_image
        elif return_accuracy:
            return r_eff, accuracy
        return r_eff

    def two_point_correlation(self, Nbins=100, rmax=None, normalize=False, 
                              use_profile_coordinates=True, coordinates=None, 
                              min_flux=None, min_flux_frac=None, 
                              return_cov=False, return_map=False,
                              **kwargs_selection):
        """
        The two point correlation function can be obtained from the covariance matrix of an image and the distances between its pixels.
        By binning the covariance matrix entries in distance (or radial) bins, one can obtain the 1D correlation function.
        There are two ways to obtain the covariance matrix:
        1) it is equivalent to the inverse Fourier transform of the power spectrum, and
        2) by calculating explicitly the covariance between any two pixels
        Here we use the first way.

        Parameters
        ----------
        Nbins : int, optional
            The number of radial bins to use for converting the 2D covariance matrix into a 1D correlation function.
        rmax : float, optional
            A value for the maximum extent of the radial bins. If none is given then it is equal to half the diagonal of the provided image.
        normalize : bool, optional
            Normalize the given image by its maximum. Default is False.
        coordinates : Coordinates, optional
            Instance of a Coordinates object to be used for the computation.
            If None, will use an instance based on the Instrument, by default None
        use_profile_coordinates : bool, optional
            If True and `coordinates=None`, uses the coordinates attached to the light profile, if available. Default is True.
        min_flux : float, optional
            Minimum flux value considered in the computation of the correlation function. 
            Default is None (i.e., no thresholding).
        min_flux_frac : float, optional
            Same as min_flux, but given as a fraction of the maximum flux value.
            If `min_flux` is not None, `min_flux_frac` is ignored.
            Default is None (i.e., no thresholding).
        return_cov : bool, optional
            If True, also returns the full covariance matrix. Default is False.
        return_cov : bool, optional
            If True, also returns the full covariance matrix. Default is False. 

        Returns
        -------
        (array, array, array)
            The location, value, and uncertainty of the 1D bins of the two-point correlation function.
            The location (radius/distance) is in the same units as the coordinates.
        """
        if kwargs_selection is None:
            kwargs_selection = {}
        if coordinates is None:
            coordinates = self.coordinates

        light_model = ComposableLightModel(self.coolest, self.coolest_dir, **kwargs_selection)

        if use_profile_coordinates is True:
            light_image, _, coordinates = light_model.surface_brightness(return_extra=True)
            if coordinates is None:
                # can be known if e.g. the underlying light profile is not pixelated
                raise ValueError("Light profile does not have any coordinates grid attached to it.")
        else:
            if coordinates is None:
                coordinates = self.coordinates
            x, y = coordinates.pixel_coordinates
            light_image = light_model.evaluate_surface_brightness(x, y)
        
        light_image = np.nan_to_num(light_image, nan=0.)
        cov_mask = np.ones_like(light_image)
        if min_flux is not None:
            logging.info(f"Setting to zero any flux below {min_flux}.")
            light_image[light_image < min_flux] = 0.
            cov_mask[light_image < min_flux] = 0.
        elif min_flux_frac is not None:
            min_flux = min_flux_frac*light_image.max()
            logging.info(f"Setting to zero any flux below {min_flux}.")
            light_image[light_image < min_flux] = 0.
            cov_mask[light_image < min_flux] = 0.
        cov_mask = cov_mask.astype(bool)

        extent = coordinates.extent
        dpix = coordinates.pixel_size
        
        if rmax is None:
            rmax = np.hypot(extent[0]-extent[1],extent[2]-extent[3])/2.0

        if normalize:
            max_image = np.amax(light_image)
            light_image = np.divide(light_image,max_image)
        
        bins, means, sdevs, cov = util.azim_averaged_two_point_correlation(
            light_image, dpix, rmax, Nbins,
        )

        if return_cov and return_map:
            return bins, means, sdevs, cov, light_image
        elif return_cov:
            return bins, means, sdevs, cov
        elif return_map:
            return bins, means, sdevs, light_image
        return bins, means, sdevs
    

    def total_magnitude(self, outer_radius=10, center=None, coordinates=None,
                        no_re_eval=False, flux_factor=None, mag_zero_point=None, **kwargs_selection):
        """Computes the effective radius of the 2D surface brightness profile, 
        based on a definition similar to the half-light radius.

        Parameters
        ----------
        outer_radius : int, optional
            outer limit of integration within which half the light is calculated 
            to integrate the flux, by default 10
        no_re_eval : bool, option
            If True, do re-evaluate the light profile (only relevant for pixelated profiles). Default is False.
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate Einstein radius; if None, use the value from create_kappa_image, by default None
        coordinates : Coordinates, optional
            Instance of a Coordinates object to be used for the computation.
            If None, will use an instance based on the Instrument, by default None
        mag_zero_point : float, optional
            Magnitude zero-point corresponding to 1 electron per second. 
            Must be given when no mag_zero_point has been found in the self.coolest object.
        
        TODO: flux_factor is temporary, this will be removed in the future.

        Returns
        -------
        float
            Total magnitude from the flux integrated over the field of view.
        """
        if kwargs_selection is None:
            kwargs_selection = {}

        light_model = ComposableLightModel(self.coolest, self.coolest_dir, **kwargs_selection)

        # get an image of the convergence
        if no_re_eval:
            light_image, _, coordinates = light_model.surface_brightness(return_extra=True)
            light_image[np.isnan(light_image)] = 0.
            x, y = coordinates.pixel_coordinates
        else:
            # select a center
            if center is None:
                center_x, center_y = light_model.estimate_center()
            else:
                center_x, center_y = center
            if coordinates is None:
                x, y = self.coordinates.pixel_coordinates
            else:
                x, y = coordinates.pixel_coordinates
            # make sure to evaluate the profile such that it is centered on the image
            x_ = x + center_x
            y_ = y + center_y
            light_image = light_model.evaluate_surface_brightness(x_, y_)
            light_image[np.isnan(light_image)] = 0.

        # retrieve the zero-point from the
        if self.coolest.observation.mag_zero_point is not None:
            logging.info(f"Using magnitude zero-point from self.coolest object ({mag_zero_point}).")
            mag_zero_point = self.coolest.observation.mag_zero_point
        elif mag_zero_point is None:
            raise ValueError("No `mag_zero_point` has been found in the COOLEST object, "
                             "hence `mag_zero_point` must be provided.")
        else:
            logging.info(f"Using the magnitude zero-point ({mag_zero_point}.)")

        if outer_radius is not None:
            mask = (np.hypot(x, y) < outer_radius).astype(float)  # 0. and 1. only
            light_image *= mask

        # compute the magnitude
        flux_tot = light_image.sum()
        if flux_factor is not None:
            flux_tot *= flux_factor  # temporary feature
        mag_tot = -2.5*np.log10(flux_tot) + mag_zero_point
    
        return mag_tot

    def ellipticity_from_moments(self, center=None, coordinates=None, **kwargs_selection):
        """Estimates the axis ratio and position angle of the model map 
        based on central moments of the image.

        Parameters
        ----------
        center : (float, float), optional
            (x, y)-coordinates of the center from which to calculate Einstein radius; if None, use the value from create_kappa_image, by default None
        coordinates : Coordinates, optional
            Instance of a Coordinates object to be used for the computation.
            If None, will use an instance based on the Instrument, by default None
        
        Returns
        -------
        float
            Ellipticity measurement (axis)

        Raises
        ------
        Warning
            If integration loop exceeds outer bound before convergence.
        """
        if kwargs_selection is None:
            kwargs_selection = {}

        light_model = ComposableLightModel(self.coolest, self.coolest_dir, **kwargs_selection)

        # select a center
        if center is None:
            center_x, center_y = light_model.estimate_center()
        else:
            center_x, center_y = center

        # get an image of the convergence
        if coordinates is None:
            x, y = self.coordinates.pixel_coordinates
            pixel_size = self.coordinates.pixel_size
        else:
            x, y = coordinates.pixel_coordinates
            pixel_size = coordinates.pixel_size
            
        # make sure to evaluate the profile such that it is centered on the image
        x_ = x + center_x
        y_ = y + center_y
        light_image = light_model.evaluate_surface_brightness(x_, y_)
        light_image[np.isnan(light_image)] = 0.

        # compute the ellipticity and position angle
        phi_rad, q = util.ellipticity_from_moments(light_image, pixel_size)
        phi = phi_rad * 180./np.pi + 90. # conversion to COOLEST conventions

        return q, phi

    def lensing_information(self, a=16, b=0, 
                            noise_map=None, arc_mask=None, theta_E=None,
                            entity_idx_theta_E=0, profile_idx_theta_E=0):
        """
        Computes the 'lensing information' defined in Yi Tan et al. 2023, Equations (8) and (9).
        https://ui.adsabs.harvard.edu/abs/2023arXiv231109307T/abstract
        """
        data = self.coolest.observation.pixels.get_pixels()
        # TODO: subtract the lens light
        print("WARNING: no lens light subtracted; assuming the data contains only the arcs.")
        if noise_map is None:
            raise NotImplementedError("Getting the noise map from the COOLEST instance is yet implemented.")
        if theta_E is None:
            mass_profile = self.coolest.lensing_entities[entity_idx_theta_E].mass_model[profile_idx_theta_E]
            theta_E = mass_profile.parameters['theta_E'].point_estimate.value
        x, y = self.coordinates.pixel_coordinates
        I, theta_E, phi_ref, mask = util.lensing_information(
            data, x, y, theta_E, noise_map, a=a, b=b, arc_mask=arc_mask
        )
        return I, theta_E, phi_ref, mask
    
    @staticmethod
    def _find_nearest(array, value):
        """subfunction to find nearest closest element in array to value"""
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    