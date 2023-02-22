__author__ = 'aymgal', 'lynevdv'


import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm

from coolest.api.analysis import Analysis
from coolest.api.light_model import CompositeLightModel
from coolest.api.util import read_json_param
from coolest.api import plot_util as plut

# matplotlib global settings
plt.rc('image', interpolation='none', origin='lower') # imshow settings


class ModelPlotter(object):
    """
    Creates pyplot panels from a lens model stored in the COOLEST format
    """

    def __init__(self, coolest_object, coolest_directory=None):
        self.coolest = coolest_object
        self.analysis = Analysis(self.coolest)
        cmap_flux = copy.copy(plt.get_cmap('magma'))
        cmap_flux.set_bad('black')
        self.cmap_flux = cmap_flux
        self._directory = coolest_directory

    def plot_surface_brightness(self, ax, title=None, coordinates=None, 
                                extent=None, norm=None, cmap=None,
                                **kwargs_selection):
        light_model = CompositeLightModel(self.coolest, self._directory, **kwargs_selection)
        if cmap is None:
            cmap = self.cmap_flux
        if coordinates is not None:
            x, y = coordinates.pixel_coordinates
            image = light_model.evaluate_surface_brightness(x, y)
            extent = coordinates.extent
            self._plot_regular_grid(ax, image, extent=extent, 
                                    cmap=self.cmap_flux, 
                                    norm=norm)
        else:
            values, extent_model = light_model.surface_brightness(return_extent=True)
            if extent is None:
                extent = extent_model
            if isinstance(values, np.ndarray) and len(values.shape) == 2:
                image = values
                self._plot_regular_grid(ax, image, extent=extent, 
                                        cmap=self.cmap_flux, 
                                        norm=norm)
            else:
                points = values
                self._plot_irregular_grid(ax, points, extent, norm=norm, 
                                          cmap=self.cmap_flux)
                image = None
        if title is not None:
            ax.set_title(title)
        return image
        
    @staticmethod
    def _plot_regular_grid(ax, image, **imshow_kwargs):
        im = ax.imshow(image, **imshow_kwargs)
        plut.nice_colorbar(im)
        return ax

    @staticmethod
    def _plot_irregular_grid(ax, points, extent, norm=None, cmap=None):
        x, y, z = points
        ax = plut.plot_voronoi(ax, x, y, z, norm=norm, cmap=cmap)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.set_aspect('equal', 'box')
        #plt.colorbar()
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

    def plot_surface_brightness(self, axes, titles=None, 
                                coordinates=None, norm=None, cmap=None,
                                **kwargs_selection_list):
        if kwargs_selection_list is None:
            kwargs_selection_list = self.num_models * [{}]
        if titles is None:
            titles = self.num_models * [None]
        assert len(axes) == self.num_models, "Inconsistent number of subplot axes"
        image_list = []
        for i, (ax, plotter) in enumerate(zip(axes, self.plotter_list)):
            kw_select = {key: val[i] for key, val in kwargs_selection_list.items()}
            image = plotter.plot_surface_brightness(ax, coordinates=coordinates, 
                                                    title=titles[i],
                                                    norm=norm, cmap=cmap, **kw_select)
            image_list.append(image)
        return image_list




class Comparison_analytical(object):
    """
    Handles plot of analytical models in a comparative way
    """
    def __init__(self,coolest_file_list, nickname_file_list, posterior_bool_list):
        self.file_names = nickname_file_list
        self.posterior_bool_list = posterior_bool_list
        self.param_lens, self.param_source = read_json_param(coolest_file_list,self.file_names, lens_light=False)

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
