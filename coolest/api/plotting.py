__author__ = 'aymgal', 'lynevdv'


import copy
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm
from matplotlib.colors import ListedColormap

from coolest.api.analysis import Analysis
from coolest.api.composable_models import *
from coolest.api import util
from coolest.api import plot_util as plut

# matplotlib global settings
plt.rc('image', interpolation='none', origin='lower') # imshow settings

# logging settings
logging.getLogger().setLevel(logging.INFO)


class ModelPlotter(object):
    """
    Creates pyplot panels from a lens model stored in the COOLEST format
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

    def plot_surface_brightness(self, ax, title=None, coordinates=None, 
                                extent=None, norm=None, cmap=None, neg_values_as_bad=True,
                                plot_points_irreg=False, kwargs_light=None):
        if kwargs_light is None:
            kwargs_light = {}
        light_model = ComposableLightModel(self.coolest, self._directory, **kwargs_light)
        if cmap is None:
            cmap = self.cmap_flux
        if coordinates is not None:
            x, y = coordinates.pixel_coordinates
            image = light_model.evaluate_surface_brightness(x, y)
            extent = coordinates.extent
            self._plot_regular_grid(ax, image, extent=extent, 
                                    cmap=cmap,
                                    neg_values_as_bad=neg_values_as_bad, 
                                    norm=norm)
        else:
            values, extent_model, coordinates = light_model.surface_brightness(return_extra=True)
            if extent is None:
                extent = extent_model
            if isinstance(values, np.ndarray) and len(values.shape) == 2:
                image = values
                self._plot_regular_grid(ax, image, extent=extent, 
                                        cmap=cmap, 
                                        neg_values_as_bad=neg_values_as_bad,
                                        norm=norm)
            else:
                points = values
                self._plot_irregular_grid(ax, points, extent, norm=norm, 
                                          cmap=cmap, 
                                          neg_values_as_bad=neg_values_as_bad,
                                          plot_points=plot_points_irreg)
                image = None
        if title is not None:
            ax.set_title(title)
        return image, coordinates

    def plot_model_image(self, ax, supersampling=5, convolved=False, title=None,
                         norm=None, cmap=None, neg_values_as_bad=False,
                         kwargs_source=None, kwargs_lens_mass=None):
        if cmap is None:
            cmap = self.cmap_flux
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_image(supersampling=supersampling, 
                                                    convolved=convolved)
        extent = coordinates.extent
        self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if title is not None:
            ax.set_title(title)
        return image

    def plot_model_residuals(self, ax, supersampling=5, mask=None, title=None,
                             norm=None, cmap=None, 
                             kwargs_source=None, kwargs_lens_mass=None):
        if cmap is None:
            cmap = self.cmap_res
        if norm is None:
            norm = Normalize(-6, 6)
        lens_model = ComposableLensModel(self.coolest, self._directory,
                                         kwargs_selection_source=kwargs_source,
                                         kwargs_selection_lens_mass=kwargs_lens_mass)
        image, coordinates = lens_model.model_residuals(supersampling=supersampling, 
                                                        mask=mask)
        extent = coordinates.extent
        self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=False, 
                                norm=norm)
        if title is not None:
            ax.set_title(title)
        return image

    def plot_convergence(self, ax, title=None,
                         norm=None, cmap=None, neg_values_as_bad=False,
                         kwargs_lens_mass=None):
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                         **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_conv
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_convergence(x, y)
        self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
        if title is not None:
            ax.set_title(title)
        return image

    def plot_magnification(self, ax, title=None,
                          norm=None, cmap=None, neg_values_as_bad=False,
                          kwargs_lens_mass=None):
        if kwargs_lens_mass is None:
            kwargs_lens_mass = {}
        mass_model = ComposableMassModel(self.coolest, self._directory,
                                         **kwargs_lens_mass)
        if cmap is None:
            cmap = self.cmap_mag
        if norm is None:
            norm = Normalize(-10, 10)
        coordinates = util.get_coordinates(self.coolest)
        extent = coordinates.extent
        x, y = coordinates.pixel_coordinates
        image = mass_model.evaluate_magnification(x, y)
        self._plot_regular_grid(ax, image, extent=extent, 
                                cmap=cmap,
                                neg_values_as_bad=neg_values_as_bad, 
                                norm=norm)
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
        plut.nice_colorbar(im)
        return ax

    @staticmethod
    def _plot_irregular_grid(ax, points, extent, neg_values_as_bad=True,
                             norm=None, cmap=None, plot_points=False):
        x, y, z = points
        m = plut.plot_voronoi(ax, x, y, z, neg_values_as_bad=neg_values_as_bad, 
                              norm=norm, cmap=cmap, zorder=1)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.set_aspect('equal', 'box')
        plut.nice_colorbar(m, ax=ax)
        if plot_points:
            ax.scatter(x, y, s=5, c='white', marker='.', alpha=0.4, zorder=2)
        return ax


class MultiModelPlotter(object):
    """
    Creates pyplot panels from several lens model
    """

    def __init__(self, coolest_objects, coolest_directories=None):
        self.num_models = len(coolest_objects)
        if coolest_directories is None:
            coolest_directories = self.num_models * [None]
        self.plotter_list = []
        for coolest, c_dir in zip(coolest_objects, coolest_directories):
            self.plotter_list.append(ModelPlotter(coolest, coolest_directory=c_dir))

    def plot_surface_brightness(self, axes, titles=None, **kwargs):
        return self._plot_light_multi('plot_surface_brightness', "surf. brightness", axes, titles=titles, **kwargs)

    def plot_model_image(self, axes, titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_model_image', "model", axes, titles=titles, **kwargs)

    def plot_model_residuals(self, axes, titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_model_residuals', "residuals", axes, titles=titles, **kwargs)

    def plot_convergence(self, axes, titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_convergence', "convergence", axes, titles=titles, **kwargs)

    def plot_magnification(self, axes, titles=None, **kwargs):
        return self._plot_lens_model_multi('plot_magnification', "magnification", axes, titles=titles, **kwargs)

    def _plot_light_multi(self, method_name, default_title, axes, titles=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [default_title]
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

    def _plot_mass_multi(self, method_name, default_title, axes, titles=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [default_title]
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

    def _plot_lens_model_multi(self, method_name, default_title, axes, titles=None, kwargs_select=None, **kwargs):
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        if titles is None:
            titles = self.num_models * [default_title]
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


class Comparison_analytical(object):
    """
    Handles plot of analytical models in a comparative way
    """
    def __init__(self,coolest_file_list, nickname_file_list, posterior_bool_list):
        self.file_names = nickname_file_list
        self.posterior_bool_list = posterior_bool_list
        self.param_lens, self.param_source = util.read_json_param(coolest_file_list,self.file_names, lens_light=False)

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
