__author__ = 'Giorgos Vernardos'

from coolest.template.lazy import *
from coolest.template.standard import COOLEST
from coolest.template.classes.grid import IrregularGrid
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

def plot_voronoi(ax,irr_grid):
    # ax: is an instance of matplotlib axes
    # irr_grid: is an instance of IrregularGrid

    x,y,z = irr_grid.get_xyz()

    # get voronoi regions
    voronoi_points = np.column_stack((x,y))
    vor = Voronoi(voronoi_points)
    new_regions, vertices = voronoi_finite_polygons_2d(vor)
    
    # get cell colors
    norm = matplotlib.colors.Normalize(vmin=0,vmax=7)
    cmap = matplotlib.cm.inferno_r
    m = matplotlib.cm.ScalarMappable(norm=norm,cmap=cmap)

    # plot voronoi points
    #point_colors = [ m.to_rgba(v) for v in z ]
    #ax.scatter(voronoi_points[:,0],voronoi_points[:,1],c=point_colors)

    # plot voronoi cells
    for i,region in enumerate(new_regions):
        polygon = vertices[region]
        cell_color = m.to_rgba(z[i])
        ax.fill(*zip(*polygon),alpha=1.0,facecolor=cell_color,edgecolor='white')

    ax.set_xlim(irr_grid.field_of_view_x)
    ax.set_ylim(irr_grid.field_of_view_y)
    ax.set_aspect('equal')

    return ax



# This function is taken from: https://gist.github.com/pv/8036995
def voronoi_finite_polygons_2d(vor,radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

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











# The following part of the code is a dummy plotting program
############################################################

# import matplotlib
import matplotlib.pyplot as plt
import matplotlib

# create an object of type IrregularGrid
source_4 = Galaxy('a VKL source', 1.2, light_model=LightModel('IrregularGrid'))
#source_4.light_model[0].pixels.field_of_view_x = (-10,10)
#source_4.light_model[0].pixels.field_of_view_y = (-10,10)
source_4.light_model[0].pixels.set_fits('/home/giorgos/myCodes/COOLEST/mytests/dum_table.fits')

# create axes for one or more plots
fig,ax = plt.subplots(figsize=(15,6))

# This is the key command:
# Pass an axis object and an IrregularGrid object to the plotting function
ax = plot_voronoi(ax,source_4.light_model[0].pixels)

# save the figure
plt.savefig('test_plot.pdf')
