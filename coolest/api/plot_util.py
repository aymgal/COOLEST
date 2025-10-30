__author__ = 'aymgal', 'Giorgos Vernardos'


import numpy as np
import warnings
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from coolest.api.composable_models import ComposableLensModel
import os
import tarfile
import tempfile
import zipfile
import io
from coolest.api import util
from coolest.api.analysis import Analysis


def plot_voronoi(ax, x, y, z, neg_values_as_bad=False, 
                 norm=None, cmap=None, zmin=None, zmax=None, 
                 edgecolor=None, zorder=1):

    if cmap is None:
        cmap = plt.get_cmap('inferno')
    if norm is None:
        if zmin is None:
            zmin = np.min(z)
        if zmax is None:
            zmax = np.max(z)
        norm = Normalize(zmin, zmax)

    # get voronoi regions
    voronoi_points = np.column_stack((x,y))
    vor = Voronoi(voronoi_points)
    new_regions, vertices = voronoi_finite_polygons_2d(vor)
    
    # get cell colors
    m = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

    # plot voronoi points
    #point_colors = [ m.to_rgba(v) for v in z ]
    #ax.scatter(voronoi_points[:,0],voronoi_points[:,1],c=point_colors)

    # plot voronoi cells
    for i, region in enumerate(new_regions):
        polygon = vertices[region]
        z_i = z[i]
        if neg_values_as_bad is True and z_i < 0.:
            cell_color = m.to_rgba(np.nan)
        else:
            cell_color = m.to_rgba(z_i)
        ax.fill(*zip(*polygon), facecolor=cell_color, edgecolor=edgecolor, zorder=zorder)
    return m


def voronoi_finite_polygons_2d(vor,radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    This function is taken from: https://gist.github.com/pv/8036995

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())
        
    return new_regions, np.asarray(new_vertices)


def std_colorbar(mappable, label=None, fontsize=12, label_kwargs={}, **colorbar_kwargs):
    cb = plt.colorbar(mappable, **colorbar_kwargs)
    if label is not None:
        colorbar_kwargs.pop('label', None)
        cb.set_label(label, fontsize=fontsize, **label_kwargs)
    return cb

def std_colorbar_residuals(mappable, res_map, vmin, vmax, label=None, fontsize=12, 
                           label_kwargs={}, **colorbar_kwargs):
    if res_map.min() < vmin and res_map.max() > vmax:
        cb_extend = 'both'
    elif res_map.min() < vmin:
        cb_extend = 'min'
    elif res_map.max() > vmax:
        cb_extend = 'max'
    else:
        cb_extend = 'neither'
    colorbar_kwargs.update({'extend': cb_extend})
    return std_colorbar(mappable, label=label, fontsize=fontsize, 
                        label_kwargs=label_kwargs, **colorbar_kwargs)

def nice_colorbar(mappable, ax=None, position='right', pad=0.1, size='5%', label=None, fontsize=12, 
                  invisible=False, 
                  #max_nbins=None,
                  divider_kwargs={}, colorbar_kwargs={}, label_kwargs={}):
    divider_kwargs.update({'position': position, 'pad': pad, 'size': size})
    if ax is None:
        ax = mappable.axes
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(**divider_kwargs)
    if invisible:
        cax.axis('off')
        return None
    cb = plt.colorbar(
        mappable, cax=cax, 
        **colorbar_kwargs
    )
    if label is not None:
        colorbar_kwargs.pop('label', None)
        cb.set_label(label, fontsize=fontsize, **label_kwargs)
    if position == 'top':
        cax.xaxis.set_ticks_position('top')
    # if max_nbins is not None: # TODO: this leads to strange results
    #     # cb.locator = ticker.LogLocator(subs=range(10))
    #     # cb.update_ticks()
    return cb

def nice_colorbar_residuals(mappable, res_map, vmin, vmax, ax=None, position='right', pad=0.1, size='5%', 
                            invisible=False, label=None, fontsize=12,
                            divider_kwargs={}, colorbar_kwargs={}, label_kwargs={}):
    if res_map.min() < vmin and res_map.max() > vmax:
        cb_extend = 'both'
    elif res_map.min() < vmin:
        cb_extend = 'min'
    elif res_map.max() > vmax:
        cb_extend = 'max'
    else:
        cb_extend = 'neither'
    colorbar_kwargs.update({'extend': cb_extend})
    return nice_colorbar(mappable, ax=ax, position=position, pad=pad, size=size, label=label, fontsize=fontsize,
                  invisible=invisible, colorbar_kwargs=colorbar_kwargs, label_kwargs=label_kwargs,
                  divider_kwargs=divider_kwargs)

def cax_colorbar(fig, cax, norm=None, cmap=None, mappable=None, label=None, fontsize=12, orientation='horizontal', label_kwargs={}):
    if mappable is None:
        mappable = ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(mappable=mappable, orientation=orientation, cax=cax)
    if label is not None:
        cb.set_label(label, fontsize=fontsize, **label_kwargs)

def scale_bar(ax, size, unit_suffix='"', loc='lower left', color='#FFFFFFBB', fontsize=12):
    if size == int(size):
        label = f"{int(size)}"
    else:
        label = f"{size:.1f}"
    label += unit_suffix
    artist = AnchoredSizeBar(
        ax.transData,
        size, label,
        loc=loc, label_top=True,
        pad=0.8, sep=5, 
        color=color, fontproperties=dict(size=fontsize),
        frameon=False, size_vertical=0,
    )
    ax.add_artist(artist)
    return artist

def plot_regular_grid(ax, title, image_, neg_values_as_bad=False, xylim=None, **imshow_kwargs):
    if neg_values_as_bad:
        image = np.copy(image_)
        image[image < 0] = np.nan
    else:
        image = image_
    im = ax.imshow(image, **imshow_kwargs)
    im.set_rasterized(True)
    set_xy_limits(ax, xylim)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    ax.set_title(title)
    return ax, im

def plot_irregular_grid(ax, title, points, xylim, neg_values_as_bad=False,
                            norm=None, cmap=None, plot_points=False):
    x, y, z = points
    im = plot_voronoi(ax, x, y, z, neg_values_as_bad=neg_values_as_bad, 
                      norm=norm, cmap=cmap, zorder=1)
    ax.set_aspect('equal', 'box')
    set_xy_limits(ax, xylim)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    if plot_points:
        ax.scatter(x, y, s=5, c='white', marker='.', alpha=0.4, zorder=2)
    ax.set_title(title)
    return ax, im

def set_xy_limits(ax, xylim):
    if xylim is None: return  # do nothing
    if isinstance(xylim, (int, float)):
        xylim_ = [-xylim, xylim, -xylim, xylim]
    elif isinstance(xylim, (list, tuple)) and len(xylim) == 2:
        xylim_ = [xylim[0], xylim[1], xylim[0], xylim[1]]
    elif not isinstance(xylim, (list, tuple)) and len(xylim) != 4:
        raise ValueError("`xylim` argument should be a single number, a 2-tuple or a 4-tuple.")
    else:
        xylim_ = xylim
    ax.set_xlim(xylim_[0], xylim_[1])
    ax.set_ylim(xylim_[2], xylim_[3])

def panel_label(ax, text, color, fontsize, alpha=0.8, loc='upper left'):
    if loc == 'upper left':
        x, y, ha, va = 0.03, 0.97, 'left', 'top'
    elif loc == 'lower left':
        x, y, ha, va = 0.03, 0.03, 'left', 'bottom'
    elif loc == 'upper right':
        x, y, ha, va = 0.97, 0.97, 'right', 'top'
    elif loc == 'lower right':
        x, y, ha, va = 0.97, 0.03, 'right', 'bottom'
    ax.text(x, y, text, color=color, fontsize=fontsize, alpha=alpha, 
            ha=ha, va=va, transform=ax.transAxes)

def normalize_across_images(plotter_list, data_model_specifier, kwargs_source = None, kwargs_lens_mass = None,
                            supersampling=5, convolved=True, super_convolution=True):
    """Calculate the vmin and vmax to normalize the colormap across multiple coolest objects

    Parameters
    ----------
    plotter_list: list
        List of ModelPlotter objects. May be acquired from MultiModelPlotter object
    data_model_specifier: list
        List of 0s and 1s; 0 = data, 1 = model. Specifies which set of pixel values should be used
        when finding global minima and maxima -- data or model
    kwargs_source: dict
        Dictionary with "entity_selection" key, same as used in MultiModelPlotters.
        "Entity_selection" contains list of lists. Selects source entities.
        Insert dummy None values into dictionary for data.
    kwargs_lens_mass: dict
        Dictionary with "entity_selection" key, same as used in MultiModelPlotters.
        "Entity_selection" contains list of lists. Selects lens mass entities.
        Insert dummy None values into dictionary for data.
    supersampling: int
        Model image generation param
    convolved: bool
        Model image generation param
    super_convolution: bool
        Model image generation param
    
    
    Returns
    -------
    vmin: float
        global min value across all coolest objects in plotter_list for the specified data/models
    vmax: float
        global max value across all coolest objects in plotter_list for the specified data/models    
    """
    
    mins = []
    maxes = []
    ks_arr = kwargs_source['entity_selection']
    km_arr = kwargs_lens_mass['entity_selection']
    for plotter, d_or_f, ks, km in zip(plotter_list, data_model_specifier, ks_arr, km_arr):
        # Check if we are finding extrema for data or model
        if d_or_f == 0:
            image = plotter.coolest.observation.pixels.get_pixels(directory=plotter._directory)
        elif d_or_f == 1:
            lens_model = ComposableLensModel(plotter.coolest, plotter._directory,
                                         kwargs_selection_source=dict(entity_selection=ks),
                                         kwargs_selection_lens_mass=dict(entity_selection=km))
            image, _ = lens_model.model_image(supersampling, convolved, super_convolution)
        # Find min and max and append
        mins.append(np.min(image))
        maxes.append(np.max(image))
    vmin = min(mins)
    vmax = max(maxes)
    return vmin, vmax

    
def dmr_corner(tar_path, output_dir = None):
    """Given .tar.gz COOLEST file, plots and optionally saves DMR and corner plots for COOLEST file. Returns dictionary of important extracted information.

    Parameters
    ----------
    tar_path : string
        Path to .tar.gz COOLEST file
    output_dir : string, optional
        Path to automatically save DMR and corner plot to if specified, by default None
    
    Returns
    -------
    results: dictionary
        Contains useful information about the COOLEST objects
    """
    from coolest.api.plotting import ModelPlotter, ParametersPlotter  # placed here to avoid circular import
    
    results = {}
    with tempfile.TemporaryDirectory() as tmpdir:
            
        if tar_path[-7:] == '.tar.gz':
            # Extract tar.gz archive
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        elif tar_path[-4:] == '.zip':
            # Extract zip archive
            with zipfile.ZipFile(tar_path, 'r') as zipf:
                zipf.extractall(tmpdir)
        else:
            raise ValueError("Target path must point to a .tar.gz or .zip archive.")

        # Get path to the extracted JSON file
        extracted_items = os.listdir(tmpdir)
        if '__MACOSX' in extracted_items:
            extracted_items.remove('__MACOSX')  # remove macOS artifact folder if present
        extracted_path = os.path.join(tmpdir, extracted_items[0])
        if os.path.isdir(extracted_path):
            extracted_files = os.listdir(extracted_path)
        else:
            extracted_files = extracted_items
            extracted_path = tmpdir  # fallback
        
        json_files = [f for f in extracted_files if f.endswith(".json")]
        if not json_files:
            raise ValueError("No .json file found in archive.")
        elif len(json_files) > 1:
            raise ValueError("Multiple .json files found in archive.")
        
        json_path = os.path.join(extracted_path, json_files[0])
        target_path = os.path.splitext(json_path)[0]

        # Load COOLEST object
        coolest_1 = util.get_coolest_object(target_path, verbose=False)

        # Run analysis
        analysis = Analysis(coolest_1, target_path, supersampling=5)

        coord_orig = util.get_coordinates(coolest_1)
        coord_src = coord_orig.create_new_coordinates(pixel_scale_factor=0.1, grid_shape=(1.42, 1.42))

        # Extract values
        r_eff_source = analysis.effective_radius_light(center=(0,0), coordinates=coord_src, outer_radius=1., entity_selection=[2])
        einstein_radius = analysis.effective_einstein_radius(entity_selection=[0,1])

        results['r_eff_source'] = r_eff_source
        results['einstein_radius'] = einstein_radius
        results['lensing_entities'] = [type(le).__name__ for le in coolest_1.lensing_entities]
        results['source_light_model'] = [type(m).__name__ for m in coolest_1.lensing_entities[2].light_model]

        ### DMR Plot
        norm = Normalize(-0.005, 0.05)
        fig, axes = plt.subplots(2, 2, constrained_layout=True)
        splotter = ModelPlotter(coolest_1, coolest_directory=os.path.dirname(target_path))

        splotter.plot_data_image(axes[0, 0], norm=norm)
        axes[0, 0].set_title("Observed Data")

        splotter.plot_model_image(
            axes[0, 1],
            supersampling=5, convolved=True,
            kwargs_source=dict(entity_selection=[2]),
            kwargs_lens_mass=dict(entity_selection=[0, 1]),
            norm=norm
        )
        axes[0, 1].text(0.05, 0.05, f"$\\theta_{{\\rm E}}$ = {einstein_radius:.2f}\"", color='white', fontsize=12,
                        transform=axes[0, 1].transAxes)
        axes[0, 1].set_title("Image Model")

        splotter.plot_model_residuals(axes[1, 0], supersampling=5, add_chi2_label=True, chi2_fontsize=12,
                                      kwargs_source=dict(entity_selection=[2]),
                                      kwargs_lens_mass=dict(entity_selection=[0, 1]))
        axes[1, 0].set_title("Normalized Residuals")

        splotter.plot_surface_brightness(axes[1, 1], kwargs_light=dict(entity_selection=[2]),
                                         norm=norm, coordinates=coord_src)
        axes[1, 1].text(0.05, 0.05, f"$\\theta_{{\\rm eff}}$ = {r_eff_source:.2f}\"", color='white', fontsize=12,
                        transform=axes[1, 1].transAxes)
        axes[1, 1].set_title("Surface Brightness")

        for ax in axes[1]:
            ax.set_xlabel(r"$x$ (arcsec)")
            ax.set_ylabel(r"$y$ (arcsec)")
            
        if output_dir is not None:
            dmr_plot_path = os.path.join(output_dir, "dmr_plot.png")
            plt.savefig(dmr_plot_path, format='png', bbox_inches='tight')
            results['dmr_plot'] = dmr_plot_path
        plt.show()
        plt.close()

        

        
        ### Corner Plot
        truth = coolest_1
        # Only creates corner plot if sampling method was used to create lens model
        # Otherwise, no chains available for corner plot!
        if 'chain_file_name' in truth.meta.keys():
            free_pars = truth.lensing_entities.get_parameter_ids()[:-2]
            reorder = [2, 3, 4, 5, 6, 0, 1]
            pars = [free_pars[i] for i in reorder]
            results['free_parameters'] = pars
    
            param_plotter = ParametersPlotter(
                pars, [truth],
                coolest_directories=[os.path.dirname(target_path)],
                coolest_names=["Smooth source"],
                ref_coolest_objects=[truth],
                colors=['#7FB6F5', '#E03424'],
            )
    
            settings = {
                "ignore_rows": 0.0,
                "fine_bins_2D": 800,
                "smooth_scale_2D": 0.5,
                "mult_bias_correction_order": 5
            }
            param_plotter.init_getdist(settings_mcsamples=settings)
            param_plotter.plot_triangle_getdist(filled_contours=True, subplot_size=3)
            if output_dir is not None:
                corner_plot_path = os.path.join(output_dir, "corner_plot.png")
                plt.savefig(corner_plot_path, format='png', bbox_inches='tight')
                results['corner_plot'] = corner_plot_path
            plt.close()
    
            
        
    return results
