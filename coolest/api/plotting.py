__author__ = 'aymgal', 'lynevdv', 'gvernard'


import os
import copy
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm
from matplotlib.colors import ListedColormap
from getdist import plots,chains,MCSamples

from coolest.api.analysis import Analysis
from coolest.api.composable_models import *
from coolest.api import util
from coolest.api import plot_util as plut

import pandas as pd


# matplotlib global settings
plt.rc('image', interpolation='none', origin='lower') # imshow settings

# logging settings
logging.getLogger().setLevel(logging.INFO)


class ModelPlotter(object):
    """Create pyplot panels from a lens model stored in the COOLEST format.

    Parameters
    ----------
    coolest_object : COOLEST
        COOLEST instance
    coolest_directory : str, optional
        Directory which contains the COOLEST template, by default None
    color_bad_values : str, optional
        Color assigned to NaN values (typically negative values in log-scale), 
        by default '#111111' (dark gray)
    """

    def __init__(self, coolest_object, coolest_directory=None, 
                 color_bad_values='#222222'):
        self.coolest = coolest_object
        self._directory = coolest_directory

        self.cmap_flux = copy.copy(plt.get_cmap('magma'))
        self.cmap_flux.set_bad(color_bad_values)

        self.cmap_mag = plt.get_cmap('viridis')
        self.cmap_conv = plt.get_cmap('cividis')
        self.cmap_res = plt.get_cmap('RdBu_r')

        #cmap_colors = self.cmap_flux(np.linspace(0, 1, 256))
        #cmap_colors[0,:] = [0.15, 0.15, 0.15, 1.0]  # Set the color of the very first value to gray
        #self.cmap_flux_mod = ListedColormap(cmap_colors)

    def plot_data_image(self, ax, norm=None, cmap=None, xylim=None,
                        neg_values_as_bad=False, add_colorbar=True):
        """plt.imshow panel with the data image"""
        if cmap is None:
            cmap = self.cmap_flux
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.plt_extent
        image = self.coolest.observation.pixels.get_pixels(directory=self._directory)
        ax, im = plut.plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap, norm=norm,
                                neg_values_as_bad=neg_values_as_bad, 
                                xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        return image

    def plot_surface_brightness(self, ax, coordinates=None,
                                extent_irreg=None, norm=None, cmap=None, 
                                xylim=None, neg_values_as_bad=True,
                                plot_points_irreg=False, add_colorbar=True,
                                kwargs_light=None,
                                plot_caustics=None, caustics_color='white', caustics_alpha=0.5,
                                coordinates_lens=None, kwargs_lens_mass=None):
        """plt.imshow panel showing the surface brightness of the (unlensed)
        lensing entity selected via kwargs_light (see ComposableLightModel docstring)"""
        if extent_irreg is not None:
            raise ValueError("`extent_irreg` is deprecated; use `xylim` instead.")
        if kwargs_light is None:
            kwargs_light = {}
        light_model = ComposableLightModel(self.coolest, self._directory, **kwargs_light)
        if plot_caustics:
            if kwargs_lens_mass is None:
                raise ValueError("`kwargs_lens_mass` must be provided to compute caustics")
            if coordinates_lens is None:
                coordinates_lens = util.get_coordinates(self.coolest).create_new_coordinates(pixel_scale_factor=0.1)
            # NOTE: here we assume that `kwargs_light` is for the source!
            mass_model = ComposableMassModel(self.coolest, self._directory, **kwargs_lens_mass)
            _, caustics = util.find_all_lens_lines(coordinates_lens, mass_model)
        if cmap is None:
            cmap = self.cmap_flux
        if coordinates is not None:
            x, y = coordinates.pixel_coordinates
            image = light_model.evaluate_surface_brightness(x, y)
            extent = coordinates.plt_extent
            ax, im = plut.plot_regular_grid(ax, image, extent=extent, cmap=cmap,
                                             neg_values_as_bad=neg_values_as_bad, 
                                             norm=norm, xylim=xylim)
        else:
            values, extent_model, coordinates = light_model.surface_brightness(return_extra=True)
            if isinstance(values, np.ndarray) and len(values.shape) == 2:
                image = values
                ax, im = plut.plot_regular_grid(ax, image, extent=extent_model, 
                                        cmap=cmap, 
                                        neg_values_as_bad=neg_values_as_bad,
                                        norm=norm, xylim=xylim)
            else:
                points = values
                if xylim is None:
                    xylim = extent_model
                ax, im = plut.plot_irregular_grid(ax, points, xylim, norm=norm, cmap=cmap, 
                                                   neg_values_as_bad=neg_values_as_bad,
                                                   plot_points=plot_points_irreg)
                image = None
        if plot_caustics:
            for caustic in caustics:
                ax.plot(caustic[0], caustic[1], lw=1, color=caustics_color, alpha=caustics_alpha)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        return image, coordinates

    def plot_model_image(self, ax,
                         norm=None, cmap=None, xylim=None, neg_values_as_bad=False,
                         kwargs_source=None, add_colorbar=True, kwargs_lens_mass=None,
                         **model_image_kwargs):
        """plt.imshow panel showing the surface brightness of the (lensed)
        selected lensing entities (see ComposableLensModel docstring)
        """
        if cmap is None:
            cmap = self.cmap_flux
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_image(**model_image_kwargs)
        extent = coordinates.plt_extent
        ax, im = plut.plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm, xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        return image

    def plot_model_residuals(self, ax, mask=None,
                             norm=None, cmap=None, xylim=None, add_chi2_label=False, chi2_fontsize=12,
                             kwargs_source=None, add_colorbar=True, kwargs_lens_mass=None,
                             **model_image_kwargs):
        """plt.imshow panel showing the normalized model residuals image"""
        if cmap is None:
            cmap = self.cmap_res
        if norm is None:
            norm = Normalize(-6, 6)
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_residuals(mask=mask, **model_image_kwargs)
        extent = coordinates.plt_extent
        ax, im = plut.plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=False, 
                                norm=norm, xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("(data $-$ model) / noise")
        if add_chi2_label is True:
            num_constraints = np.size(image) if mask is None else np.sum(mask)
            red_chi2 = np.sum(image**2) / num_constraints
            ax.text(0.05, 0.05, r'$\chi^2_\nu$='+f'{red_chi2:.2f}', color='black', alpha=1, 
                    fontsize=chi2_fontsize, va='bottom', ha='left', transform=ax.transAxes,
                    bbox={'color': 'white', 'alpha': 0.6})
        return image

    def plot_convergence(self, ax, coordinates=None,
                         norm=None, cmap=None, xylim=None, neg_values_as_bad=False,
                         add_colorbar=True, kwargs_lens_mass=None):
        """plt.imshow panel showing the 2D convergence map associated to the
        selected lensing entities (see ComposableMassModel docstring)
        """
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                         **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_conv
        if coordinates is None:
            coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.plt_extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_convergence(x, y)
        ax, im = plut.plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm, xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\kappa$")
        return image
    
    def plot_convergence_diff(
            self, ax, reference_map, relative_error=True,    
            norm=None, cmap=None, xylim=None, coordinates=None,
            add_colorbar=True, kwargs_lens_mass=None,
            plot_crit_lines=False, crit_lines_color='black', crit_lines_alpha=0.5):
        """plt.imshow panel showing the 2D convergence map associated to the
        selected lensing entities (see ComposableMassModel docstring)
        """
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                         **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_res
        if norm is None:
            norm = Normalize(-1, 1)
        if coordinates is None:
            coordinates = util.get_coordinates(self.coolest)
        if plot_crit_lines:
            critical_lines, _ = util.find_all_lens_lines(coordinates, mass_model)
        extent = coordinates.plt_extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_convergence(x, y)
        if relative_error is True:
            diff = (reference_map - image) / reference_map
        else:
            diff = reference_map - image
        ax, im = plut.plot_regular_grid(ax, diff, extent=extent, 
                                cmap=cmap, 
                                norm=norm, xylim=xylim)
        if plot_crit_lines:
            for cline in critical_lines:
                ax.plot(cline[0], cline[1], lw=1, color=crit_lines_color, alpha=crit_lines_alpha)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\kappa$")
        return image

    def plot_magnification(self, ax, 
                          norm=None, cmap=None, xylim=None,
                          add_colorbar=True, coordinates=None, kwargs_lens_mass=None):
        """plt.imshow panel showing the 2D magnification map associated to the
        selected lensing entities (see ComposableMassModel docstring)
        """
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                         **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_mag
        if norm is None:
            norm = Normalize(-10, 10)
        if coordinates is None:
            coordinates = util.get_coordinates(self.coolest)
        x, y = coordinates.pixel_coordinates
        extent = coordinates.plt_extent
        image = mass_model.evaluate_magnification(x, y)
        ax, im = plut.plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap, 
                                norm=norm, xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\mu$")
        return image

    def plot_magnification_diff(
            self, ax, reference_map, relative_error=True,
            norm=None, cmap=None, xylim=None,
            add_colorbar=True, coordinates=None, kwargs_lens_mass=None):
        """plt.imshow panel showing the (absolute or relative) 
        difference between 2D magnification maps
        """
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                        **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_res
        if norm is None:
            norm = Normalize(-1, 1)
        if coordinates is None:
            coordinates = util.get_coordinates(self.coolest)
        x, y = coordinates.pixel_coordinates
        extent = coordinates.plt_extent
        image = mass_model.evaluate_magnification(x, y)
        if relative_error is True:
            diff = (reference_map - image) / reference_map
        else:
            diff = reference_map - image
        ax, im = plut.plot_regular_grid(ax, diff, extent=extent, 
                                cmap=cmap,
                                norm=norm, xylim=xylim)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\mu$")
        return image


class MultiModelPlotter(object):
    """Wrapper around a set of ModelPlotter instances to produce panels that
    consistently compare different models, evaluated on the same
    coordinates systems.

    Parameters
    ----------
    coolest_objects : list
        List of COOLEST instances
    coolest_directories : list, optional
        List of directories corresponding to each COOLEST instance, by default None
    kwargs_plotter : dict, optional
        Additional keyword arguments passed to ModelPlotter
    """

    def __init__(self, coolest_objects, coolest_directories=None, **kwargs_plotter):
        self.num_models = len(coolest_objects)
        if coolest_directories is None:
            coolest_directories = self.num_models * [None]
        self.plotter_list = []
        for coolest, c_dir in zip(coolest_objects, coolest_directories):
            self.plotter_list.append(ModelPlotter(coolest, coolest_directory=c_dir,
                                                  **kwargs_plotter))

    def plot_surface_brightness(self, axes, **kwargs):
        return self._plot_light_multi('plot_surface_brightness',axes, **kwargs)

    def plot_data_image(self, axes, **kwargs):
        return self._plot_data_multi(axes, **kwargs)

    def plot_model_image(self, axes, **kwargs):
        return self._plot_lens_model_multi('plot_model_image', axes, **kwargs)

    def plot_model_residuals(self, axes, **kwargs):
        return self._plot_lens_model_multi('plot_model_residuals', axes, **kwargs)

    def plot_convergence(self, axes, **kwargs):
        return self._plot_lens_model_multi('plot_convergence', axes, **kwargs)

    def plot_magnification(self, axes, **kwargs):
        return self._plot_lens_model_multi('plot_magnification', axes, **kwargs)

    def plot_convergence_diff(self, axes, *args, **kwargs):
        return self._plot_lens_model_multi('plot_convergence_diff', axes, *args, **kwargs)

    def plot_magnification_diff(self, axes, *args, **kwargs):
        return self._plot_lens_model_multi('plot_magnification_diff', axes, *args, **kwargs)

    def _plot_light_multi(self, method_name, axes, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_light' in kwargs:
                kwargs_['kwargs_light'] = {k: v[i] for k, v in kwargs['kwargs_light'].items()}
            if 'kwargs_lens_mass' in kwargs:  # used for over-plotting caustics
                kwargs_['kwargs_lens_mass'] = {k: v[i] for k, v in kwargs['kwargs_lens_mass'].items()}
            image = getattr(plotter, method_name)(ax, **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_mass_multi(self, method_name, axes, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_lens_mass' in kwargs:
                kwargs_['kwargs_lens_mass'] = {k: v[i] for k, v in kwargs['kwargs_lens_mass'].items()}
            image = getattr(plotter, method_name)(ax, **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_lens_model_multi(self, method_name, axes, *args, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_source' in kwargs:
                kwargs_['kwargs_source'] = {k: v[i] for k, v in kwargs['kwargs_source'].items()}
            if 'kwargs_lens_mass' in kwargs:
                kwargs_['kwargs_lens_mass'] = {k: v[i] for k, v in kwargs['kwargs_lens_mass'].items()}
            image = getattr(plotter, method_name)(ax, *args, **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_data_multi(self, axes, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            image = getattr(plotter, 'plot_data_image')(ax, **kwargs)
            image_list.append(image)
        return image_list


class Comparison_analytical(object):
    """Handles plot of analytical models in a comparative way

    Parameters
    ----------
    coolest_file_list : list
        List of paths to COOLEST templates
    nickname_file_list : list
        List of shorter names related to each COOLEST model
    posterior_bool_list : list
        List of bool to toggle errorbars on point-estimate values
    """

    def __init__(self,coolest_file_list, nickname_file_list, posterior_bool_list):
        self.file_names = nickname_file_list
        self.posterior_bool_list = posterior_bool_list
        self.param_lens, self.param_source = util.read_json_param(coolest_file_list,
                                                                  self.file_names, 
                                                                  lens_light=False)

    def plotting_routine(self,param_dict,idx_file=0):
        """
        plot the parameters

        INPUT
        -----
        param_dict: dict, organized dictonnary with all parameters results of the different files
        idx_file: int, chooses the file on which the choice of plotted parameters will be made
        (not very clear: basically in file 0 you may have a sersic fit and in file 1 sersic+shapelets. If you choose
         idx_file=0, you will plot the sersic results of both file. If you choose idx_file=1, you will plot all the
         sersic and shapelets parameters when available)
        """

        #find the numer of parameters to plot and define a nice looking figure
        number_param = len(param_dict[self.file_names[idx_file]])
        unused_figs = []
        if number_param <= 4:
            print('so few parameters not implemented yet')
        else:
            if number_param % 4 == 0:
                num_lines = int(number_param / 4.)
            else:
                num_lines = int(number_param / 4.) + 1

                for idx in range(3):
                    if (number_param + idx) % 4 != 0:
                        unused_figs.append(-idx - 1)
                    else:
                        break

        f, ax = plt.subplots(num_lines, 4, figsize=(4 * 3.5, 2.5 * num_lines))
        markers = ['*', '.', 's', '^','<','>','v','p','P','X','D','1','2','3','4','+']
        #may find a better way to define markers but right now, it is sufficient

        for j, file_name in enumerate(self.file_names):
            i = 0
            result = param_dict[file_name]
            for key in result.keys():
                idx_line = int(i / 4.)
                idx_col = i % 4
                p = result[key]
                m = markers[j]
                if self.posterior_bool_list[j]:
                    # UNCOMMENT IF NO ERROR BARS AVAILABLE ON SHEAR
                    #             if (j== 1) and (key=='SHEAR_0_gamma_ext' or key == 'SHEAR_0_phi_ext'):
                    #                 ax[idx_line,idx_col].plot(j,p['point_estimate'],marker=m,ls='',label=file_name)
                    #                 i+=1
                    #                 continue

                    #trick to plot correct error bars if close to the +180/-180 edge
                    if (key == 'SHEAR_0_phi_ext' or key == 'PEMD_0_phi'):
                        if p['percentile_16th'] > p['median']:
                            p['percentile_16th'] -= 180.
                        if p['percentile_84th'] < p['median']:
                            p['percentile_84th'] += 180.
                    ax[idx_line, idx_col].errorbar(j, p['median'], [[p['median'] - p['percentile_16th']],
                                                                    [p['percentile_84th'] - p['median']]],
                                                   marker=m, ls='', label=file_name)
                else:
                    ax[idx_line, idx_col].plot(j, p['point_estimate'], marker=m, ls='', label=file_name)

                if j == 0:
                    ax[idx_line, idx_col].get_xaxis().set_visible(False)
                    ax[idx_line, idx_col].set_ylabel(p['latex_str'], fontsize=12)
                    ax[idx_line, idx_col].tick_params(axis='y', labelsize=12)
                i += 1

        ax[0, 0].legend()
        for idx in unused_figs:
            ax[-1, idx].axis('off')
        plt.tight_layout()
        plt.show()
        return f,ax
    
    def plot_source(self,idx_file=0):
        f,ax = self.plotting_routine(self.param_source,idx_file)
        return f,ax
    
    def plot_lens(self,idx_file=0):
        f,ax = self.plotting_routine(self.param_lens,idx_file)
        return f,ax





def plot_corner(parameter_id_list, 
                chain_objs, chain_dirs, chain_names=None, 
                point_estimate_objs=None, point_estimate_dirs=None, point_estimate_names=None, 
                colors=None, labels=None, subplot_size=1, mc_samples_kwargs=None, 
                filled_contours=True, angles_range=None, shift_sample_list=None):
    """
    Adding this as just a function for the moment.
    Takes a list of COOLEST files as input, which must have a chain file associated to them, and returns a corner plot.

    Parameters
    ----------
    parameter_id_list : array
        A list of parameter unique ids obtained from lensing entities. Their order determines the order of the plot panels.
    chain_objs : array
        A list of coolest objects that have a chain file associated to them.
    chain_dirs : array
        A list of paths matching the coolest files in 'chain_objs'.
    chain_names : array, optional
        A list of labels for the coolest models in the 'chain_objs' list. Must have the same order as 'chain_objs'.
    point_estimate_objs : array, optional
        A list of coolest objects that will be used as point estimates.
    point_estimate_dirs : array
        A list of paths matching the coolest files in 'point_estimate_objs'.
    point_estimate_names : array, optional
        A list of labels for the models in the 'point_estimate_objs' list. Must have the same order as 'point_estimate_objs'.
    labels : dict, optional
        A dictionary matching the parameter_id_list entries to some human-readable labels.

    Returns
    -------
    An image
    """

    chains.print_load_details = False # Just to silence messages
    parameter_id_set = set(parameter_id_list)
    Npars = len(parameter_id_list)
    Nobjs = len(chain_objs)
    
    # Set the chain names
    if chain_names is None:
        chain_names = ["chain "+str(i) for i in range(Nobjs)]
    
    if shift_sample_list is None:
        shift_sample_list = [None]*Nobjs
    
    # Get the values of the point_estimates
    point_estimates = []
    if point_estimate_objs is not None:
        for coolest_obj in point_estimate_objs:
            values = []
            for par in parameter_id_list:
                param = coolest_obj.lensing_entities.get_parameter_from_id(par)
                val = param.point_estimate.value
                if val is None:
                    values.append(None)
                else:
                    values.append(val)
            point_estimates.append(values)


            
    mcsamples = []
    for i in range(Nobjs):
        chain_file = os.path.join(chain_dirs[i],chain_objs[i].meta["chain_file_name"]) # Here get the chain file path for each coolest object

        # Each chain file can have a different number of free parameters
        f = open(chain_file)
        header = f.readline()
        f.close()

        if ';' in header:
            raise ValueError("Columns must be coma-separated (no semi-colon) in chain file.")

        chain_file_headers = header.split(',')
        num_cols = len(chain_file_headers)
        chain_file_headers.pop() # Remove the last column name that is the probability weights
        chain_file_headers_set = set(chain_file_headers)
        
        # Check that the given parameters are a subset of those in the chain file
        assert parameter_id_set.issubset(chain_file_headers_set), "Not all given parameters are free parameters for model %d (not in the chain file: %s)!" % (i,chain_file)

        # Set the labels for the parameters in the chain file
        par_labels = []
        if labels is None:
            labels = {}
        for par_id in parameter_id_list:
            if labels.get(par_id, None) is None:
                param = coolest_obj.lensing_entities.get_parameter_from_id(par_id)
                par_labels.append(param.latex_str.strip('$'))
            else:
                par_labels.append(labels[par_id])
                    
        # Read parameter values and probability weights
        column_indices = [chain_file_headers.index(par_id) for par_id in parameter_id_list]
        columns_to_read = sorted(column_indices) + [num_cols-1]  # add last one for probability weights
        samples = pd.read_csv(chain_file, usecols=columns_to_read, delimiter=',')
    
        # Re-order columnds to match parameter_id_list and par_labels
        sample_par_values = np.array(samples[parameter_id_list])

        # If needed, shift samples by a constant
        if shift_sample_list[i] is not None:
            for param_id, value in shift_sample_list[i].items():
                sample_par_values[:, parameter_id_list.index(param_id)] += value
                print(f"INFO: posterior for parameter '{param_id}' from model '{chain_names[i]}' "
                      f"has been shifted by {value}.")

        # Clean-up the probability weights
        mypost = np.array(samples['probability_weights'])
        min_non_zero = np.min(mypost[np.nonzero(mypost)])
        sample_prob_weight = np.where(mypost<min_non_zero,min_non_zero,mypost)
        #sample_prob_weight = mypost

        # Create MCSamples object
        mysample = MCSamples(samples=sample_par_values,names=parameter_id_list,labels=par_labels,settings=mc_samples_kwargs)
        mysample.reweightAddingLogLikes(-np.log(sample_prob_weight))
        mcsamples.append(mysample)


        
    # Make the plot
    image = plots.getSubplotPlotter(subplot_size=subplot_size)    
    image.triangle_plot(mcsamples,
                        params=parameter_id_list,
                        legend_labels=chain_names,
                        filled=filled_contours,
                        colors=colors,
                        line_args=[{'ls':'-', 'lw': 2, 'color': c} for c in colors], 
                        contour_colors=colors)


    my_linestyles = ['solid','dotted','dashed','dashdot']
    my_markers    = ['s','^','o','star']

    for k in range(0,len(point_estimates)):
        # Add vertical and horizontal lines
        for i in range(0,Npars):
            val = point_estimates[k][i]
            if val is not None:
                for ax in image.subplots[i:,i]:
                    ax.axvline(val,color='black',ls=my_linestyles[k],alpha=1.0,lw=1)
                for ax in image.subplots[i,:i]:
                    ax.axhline(val,color='black',ls=my_linestyles[k],alpha=1.0,lw=1)

        # Add points
        for i in range(0,Npars):
            val_x = point_estimates[k][i]
            for j in range(i+1,Npars):
                val_y = point_estimates[k][j]
                if val_x is not None and val_y is not None:
                    image.subplots[j,i].scatter(val_x,val_y,s=10,facecolors='black',color='black',marker=my_markers[k])
                else:
                    pass    


    # Set default ranges for angles
    if angles_range is None:
        angles_range = (-90, 90)
    for i in range(0,len(parameter_id_list)):
        dum = parameter_id_list[i].split('-')
        name = dum[-1]
        if name in ['phi','phi_ext']:
            xlim = image.subplots[i,i].get_xlim()
            #print(xlim)
        
            if xlim[0] < -90:
                for ax in image.subplots[i:,i]:
                    ax.set_xlim(left=angles_range[0])
                for ax in image.subplots[i,:i]:
                    ax.set_ylim(bottom=angles_range[0])
            if xlim[1] > 90:
                for ax in image.subplots[i:,i]:
                    ax.set_xlim(right=angles_range[1])
                for ax in image.subplots[i,:i]:
                    ax.set_ylim(top=angles_range[1])

            
    return image
