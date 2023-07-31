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
                 color_bad_values='#111111'):
        self.coolest = coolest_object
        self._directory = coolest_directory

        self.cmap_flux = copy.copy(plt.get_cmap('magma'))
        self.cmap_flux.set_bad(color_bad_values)

        self.cmap_mag = plt.get_cmap('twilight_shifted')
        self.cmap_conv = plt.get_cmap('cividis')
        self.cmap_res = plt.get_cmap('RdBu_r')

        #cmap_colors = self.cmap_flux(np.linspace(0, 1, 256))
        #cmap_colors[0,:] = [0.15, 0.15, 0.15, 1.0]  # Set the color of the very first value to gray
        #self.cmap_flux_mod = ListedColormap(cmap_colors)

    def plot_data_image(self, ax, title=None, norm=None, cmap=None, 
                        neg_values_as_bad=False, add_colorbar=True):
        """plt.imshow panel with the data image"""
        if cmap is None:
            cmap = self.cmap_flux
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.plt_extent
        image = self.coolest.observation.pixels.get_pixels(directory=self._directory)
        ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        if title is not None:
            ax.set_title(title)
        return image

    def plot_surface_brightness(self, ax, title=None, coordinates=None, 
                                extent=None, norm=None, cmap=None, neg_values_as_bad=True,
                                plot_points_irreg=False, add_colorbar=True, kwargs_light=None):
        """plt.imshow panel showing the surface brightness of the (unlensed)
        lensing entity selected via kwargs_light (see ComposableLightModel docstring)"""
        if kwargs_light is None:
            kwargs_light = {}
        light_model = ComposableLightModel(self.coolest, self._directory, **kwargs_light)
        if cmap is None:
            cmap = self.cmap_flux
        if coordinates is not None:
            x, y = coordinates.pixel_coordinates
            image = light_model.evaluate_surface_brightness(x, y)
            extent = coordinates.plt_extent
            ax, im = self._plot_regular_grid(ax, image, extent=extent, cmap=cmap,
                                             neg_values_as_bad=neg_values_as_bad, 
                                             norm=norm)
        else:
            values, extent_model, coordinates = light_model.surface_brightness(return_extra=True)
            if extent is None:
                extent = extent_model
            if isinstance(values, np.ndarray) and len(values.shape) == 2:
                image = values
                ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                        cmap=cmap, 
                                        neg_values_as_bad=neg_values_as_bad,
                                        norm=norm)
            else:
                points = values
                ax, im = self._plot_irregular_grid(ax, points, extent, norm=norm, cmap=cmap, 
                                                   neg_values_as_bad=neg_values_as_bad,
                                                   plot_points=plot_points_irreg)
                image = None
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        if title is not None:
            ax.set_title(title)
        return image, coordinates

    def plot_model_image(self, ax, supersampling=5, convolved=False, title=None,
                         norm=None, cmap=None, neg_values_as_bad=False,
                         kwargs_source=None, add_colorbar=True, kwargs_lens_mass=None):
        """plt.imshow panel showing the surface brightness of the (lensed)
        selected lensing entities (see ComposableLensModel docstring)
        """
        if cmap is None:
            cmap = self.cmap_flux
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_image(supersampling=supersampling, 
                                                    convolved=convolved)
        extent = coordinates.plt_extent
        ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("flux")
        if title is not None:
            ax.set_title(title)
        return image

    def plot_model_residuals(self, ax, supersampling=5, mask=None, title=None,
                             norm=None, cmap=None, add_chi2_label=False, chi2_fontsize=12,
                             kwargs_source=None, add_colorbar=True, kwargs_lens_mass=None):
        """plt.imshow panel showing the normalized model residuals image"""
        if cmap is None:
            cmap = self.cmap_res
        if norm is None:
            norm = Normalize(-6, 6)
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_residuals(supersampling=supersampling, 
                                                        mask=mask)
        extent = coordinates.plt_extent
        ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=False, 
                                norm=norm)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label("(data $-$ model) / noise")
        if add_chi2_label is True:
            num_constraints = np.size(image) if mask is None else np.sum(mask)
            red_chi2 = np.sum(image**2) / num_constraints
            ax.text(0.05, 0.05, r'$\chi^2_\nu$='+f'{red_chi2:.2f}', color='black', alpha=1, 
                    fontsize=chi2_fontsize, va='bottom', ha='left', transform=ax.transAxes,
                    bbox={'color': 'white', 'alpha': 0.6})
        if title is not None:
            ax.set_title(title)
        return image

    def plot_convergence(self, ax, title=None,
                         norm=None, cmap=None, neg_values_as_bad=False,
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
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.plt_extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_convergence(x, y)
        ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\kappa$")
        if title is not None:
            ax.set_title(title)
        return image

    def plot_magnification(self, ax, title=None,
                          norm=None, cmap=None, neg_values_as_bad=False,
                          add_colorbar=True, kwargs_lens_mass=None):
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
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.plt_extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_magnification(x, y)
        ax, im = self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if add_colorbar:
            cb = plut.nice_colorbar(im, ax=ax, max_nbins=4)
            cb.set_label(r"$\mu$")
        if title is not None:
            ax.set_title(title)
        return image
        
    @staticmethod
    def _plot_regular_grid(ax, image_, neg_values_as_bad=True, **imshow_kwargs):
        if neg_values_as_bad:
            image = np.copy(image_)
            image[image < 0] = np.nan
        else:
            image = image_
        if neg_values_as_bad:
            image[image < 0] = np.nan
        im = ax.imshow(image, **imshow_kwargs)
        im.set_rasterized(True)
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))
        return ax, im

    @staticmethod
    def _plot_irregular_grid(ax, points, extent, neg_values_as_bad=True,
                             norm=None, cmap=None, plot_points=False):
        x, y, z = points
        im = plut.plot_voronoi(ax, x, y, z, neg_values_as_bad=neg_values_as_bad, 
                              norm=norm, cmap=cmap, zorder=1)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.set_aspect('equal', 'box')
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))
        if plot_points:
            ax.scatter(x, y, s=5, c='white', marker='.', alpha=0.4, zorder=2)
        return ax, im


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

    def plot_surface_brightness(self, axes, global_title="surf. brightness", titles=None, **kwargs):
        return self._plot_light_multi('plot_surface_brightness', global_title, axes, titles=titles, **kwargs)

    def plot_data_image(self, axes, global_title="data", titles=None, **kwargs):
        return self._plot_data_multi(global_title, axes, titles=titles, **kwargs)

    def plot_model_image(self, axes, global_title="model", titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_model_image', global_title, axes, titles=titles, **kwargs)

    def plot_model_residuals(self, axes, global_title="residuals", titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_model_residuals', global_title, axes, titles=titles, **kwargs)

    def plot_convergence(self, axes, global_title="convergence", titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_convergence', global_title, axes, titles=titles, **kwargs)

    def plot_magnification(self, axes, titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_magnification', "magnification", axes, titles=titles, **kwargs)

    def _plot_light_multi(self, method_name, global_title, axes, titles=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [global_title]
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_light' in kwargs:
                kwargs_['kwargs_light'] = {k: v[i] for k, v in kwargs['kwargs_light'].items()}
            image = getattr(plotter, method_name)(ax, title=titles[i], **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_mass_multi(self, method_name, global_title, axes, titles=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [global_title]
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_lens_mass' in kwargs:
                kwargs_['kwargs_lens_mass'] = {k: v[i] for k, v in kwargs['kwargs_lens_mass'].items()}
            image = getattr(plotter, method_name)(ax, title=titles[i], **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_lens_model_multi(self, method_name, global_title, axes, titles=None, kwargs_select=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [global_title]
        kwargs_ = copy.deepcopy(kwargs)
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            if 'kwargs_source' in kwargs:
                kwargs_['kwargs_source'] = {k: v[i] for k, v in kwargs['kwargs_source'].items()}
            if 'kwargs_lens_mass' in kwargs:
                kwargs_['kwargs_lens_mass'] = {k: v[i] for k, v in kwargs['kwargs_lens_mass'].items()}
            image = getattr(plotter, method_name)(ax, title=titles[i], **kwargs_)
            image_list.append(image)
        return image_list

    def _plot_data_multi(self, global_title, axes, titles=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [global_title]
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            if ax is None:
                continue
            image = getattr(plotter, 'plot_data_image')(ax, title=titles[i], **kwargs)
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





def plot_corner(parameter_id_list,chain_objs,chain_dirs,chain_names=None,point_estimate_objs=None,point_estimate_dirs=None,point_estimate_names=None,colors=None,labels=None,mc_samples_kwargs=None):
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
    
    # Get the chain file headers from the first object in the list
    chain_file = os.path.join(chain_dirs[0],chain_objs[0].meta["chain_file_name"])
    

    # Set the chain names
    if chain_names is None:
        chain_names = ["chain "+str(i) for i in range(0,len(chain_objs))]
    

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
    for i in range(0,len(chain_objs)):
        chain_file = os.path.join(chain_dirs[i],chain_objs[i].meta["chain_file_name"]) # Here get the chain file path for each coolest object

        # Each chain file can have a different number of free parameters
        f = open(chain_file)
        header = f.readline()
        f.close()
        chain_file_headers = header.split(',')
        chain_file_headers.pop() # Remove the last column name that is the probability weights
        chain_file_headers_set = set(chain_file_headers)
        
        # Check that the given parameters are a subset of those in the chain file
        assert parameter_id_set.issubset(chain_file_headers_set), "Not all given parameters are free parameters for model %d (not in the chain file: %s)!" % (i,chain_file)

        # Set the labels for the parameters in the chain file
        par_labels = []
        if labels is None:
            for par_id in chain_file_headers:
                if par_id in parameter_id_list:
                    param = coolest_obj.lensing_entities.get_parameter_from_id(par_id)
                    par_labels.append(param.latex_str.strip('$'))
                else:
                    par_labels.append(par_id)
        else:
            label_keys = list(labels.keys())
            for par_id in chain_file_headers:
                if par_id in label_keys:
                    par_labels.append(labels[par_id])
                else:
                    param = coolest_obj.lensing_entities.get_parameter_from_id(par_id)
                    if param:
                        par_labels.append(param.latex_str.strip('$'))
                    else:
                        par_labels.append(par_id)
                    
        # Read parameter values and probability weights
        samples = np.loadtxt(chain_file,skiprows=1,delimiter=',')
        sample_par_values = samples[:,:-1]
        
        # Clean-up the probability weights
        mypost = samples[:,-1]
        min_non_zero = np.min(mypost[np.nonzero(mypost)])
        sample_prob_weight = np.where(mypost<min_non_zero,min_non_zero,mypost)
        #sample_prob_weight = mypost

        # Create MCSamples object
        mysample = MCSamples(samples=sample_par_values,names=chain_file_headers,labels=par_labels,settings=mc_samples_kwargs)
        mysample.reweightAddingLogLikes(-np.log(sample_prob_weight))
        mcsamples.append(mysample)


        
    # Make the plot
    image = plots.getSubplotPlotter(subplot_size=1)    
    image.triangle_plot(mcsamples,params=parameter_id_list,legend_labels=chain_names,filled=True,colors=colors)

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

                
    return image
