__author__ = 'aymgal'

import numpy as np
from astropy.coordinates import SkyCoord

from coolest.api.composable_models import *
from coolest.api import util


class Analysis(object):
    """
    Handles computation of model-independent quantities and other analysis computations
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
                                  n_iter=5, return_accuracy=False, **kwargs_selection):
        """
        Calculates Einstein radius for a kappa grid starting from an initial guess with large step size and zeroing in from there.
        Uses the grid from the create_kappa_image which is built from the coolest file.

        :param center: (x, y)-coordinates of the center from which to calculate Einstein radius; if None, use the value from create_kappa_image
        :param initial_guess: initial guess for Einstein radius, default = 1
        :param initial_delta_pix: initial step size before shrinking in future iterations, default = 10 pixels
        :param n_iter: int; number of iterations, default = 5
        :param return_accuracy: bool; if True, return estimate of accuracy as well as R_Ein value
        """
        if kwargs_selection is None:
            kwargs_selection = {}
        mass_model = ComposableMassModel(self.coolest, self.coolest_dir, **kwargs_selection)

        # get an image of the convergence
        x, y = self.coordinates.pixel_coordinates
        kappa_image = mass_model.evaluate_convergence(x, y)

        # select a center
        if center is None:
            center_x, center_y = mass_model.estimate_center()
        else:
            center_x, center_y = center

        def loop_until_overshoot(r_Ein, delta, direction, runningtotal, total_pix):
            """
            this subfunction iteratively adjusts the mask radius by delta either inward or outward until the sign flips on mean_kappa-area
            """
            loopcount=0
            if r_Ein==np.nan: #return nan if given nan (needed when I put this in a loop below)
                return np.nan, np.nan, 0, runningtotal, total_pix
            while (runningtotal-total_pix)*direction>0:
                if loopcount > 100:
                    raise Warning('Stuck in very long (possibly infinite) loop')
                    break
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
                        print('WARNING: kappa is sub-critical, Einstein radius undefined.')
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
            r_Ein, delta, direction, runningtotal, total_pix = loop_until_overshoot(r_Ein, delta, direction, runningtotal, total_pix)
            direction=direction*-1
            delta=delta/2
        accuracy=grid_res/2 #after testing, accuracy is about grid_res/2
        if np.isnan(r_Ein):
            accuracy=np.nan

        if return_accuracy:
            return r_Ein, accuracy
        else:
            return r_Ein

    def effective_radial_slope(self, **kwargs_selection):
        if kwargs_selection is None:
            kwargs_selection = {}
        mass_model = ComposableMassModel(self.coolest, self.coolest_dir, **kwargs_selection)
        raise NotImplementedError

    def half_light_radius(self, **kwargs_selection):
        if kwargs_selection is None:
            kwargs_selection = {}
        light_model = ComposableLightModel(self.coolest, self.coolest_dir, **kwargs_selection)
        raise NotImplementedError
