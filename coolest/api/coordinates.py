__author__ = 'aymgal', 'sibirrer'  # partly based on lenstronomy and herculens routines


import numpy as np
import copy

from coolest.api import util


class Coordinates(object):
    """Object that holds the grid of pixel coordinates and provides
    conversions between coordinates in pixel units ('i', 'j') 
    and physical ('x', 'y', in arcseconds) units.

    Parameters
    ----------
    nx : int
        Number of pixels along the x axis
    ny : int
        Number of pixels along the y axis
    matrix_ij_to_xy : 2x2 ndarray
        Matrix such that when multiplied to vector of coordinates in pixel
        units, it returns the vector in physical units.
        Note that it should be diagonal according to COOLEST conventions.
    x_at_ij_0 : physical
        x-coordinate of the pixel with index (0, 0)
    y_at_ij_0 : _type_
        y-coordinate of the pixel with index (0, 0)
    """

    def __init__(self, nx, ny, matrix_ij_to_xy, x_at_ij_0, y_at_ij_0):
        self._matrix_pix2ang = matrix_ij_to_xy
        self._matrix_ang2pix = np.linalg.inv(self._matrix_pix2ang)
        self._ra_at_xy_0 = x_at_ij_0
        self._dec_at_xy_0 = y_at_ij_0
        self._x_at_radec_0, self._y_at_radec_0 \
            = self.map_coord(-self._ra_at_xy_0, -self._dec_at_xy_0, 
                             0, 0, self._matrix_ang2pix)
        self._nx = nx
        self._ny = ny
        self._x_grid, self._y_grid = self.coordinate_grid_2d(nx, ny)
        self._model_grids = {}

    @property
    def pixel_area(self):
        return np.abs(np.linalg.det(self._matrix_pix2ang))

    @property
    def pixel_size(self):
        return np.sqrt(self.pixel_area)

    @property
    def num_points(self):
        return self._nx * self._ny

    @property
    def pixel_coordinates(self):
        return self._x_grid, self._y_grid

    @property
    def pixel_axes(self):
        return self._x_grid[0, :], self._y_grid[:, 0]

    @property
    def extent(self):
        """set of extreme coordinates points"""
        return [self._x_grid[0, 0], self._x_grid[-1, -1], self._y_grid[0, 0], self._y_grid[-1, -1]]

    @property
    def plt_extent(self):
        """set of coordinates of the borders of the grid (useful for matplotlib functions)"""
        extent = copy.copy(self.extent)
        # WARNING: the following assumes NO ROTATION (i.e. coordinates axes aligned with x/y axes)
        half_pix = self.pixel_size / 2.
        pix_scl_x = self._matrix_pix2ang[0, 0]
        pix_scl_y = self._matrix_pix2ang[1, 1]
        if self.x_is_inverted:
            extent[0] += pix_scl_x / 2.
            extent[1] -= pix_scl_x / 2.
        else:
            extent[0] -= pix_scl_x / 2.
            extent[1] += pix_scl_x / 2.
        if self.y_is_inverted:
            extent[2] += pix_scl_y / 2.
            extent[3] -= pix_scl_y / 2.
        else:
            extent[2] -= pix_scl_y / 2.
            extent[3] += pix_scl_y / 2.
        return extent

    @property
    def shape(self):
        return self._nx * self.pixel_size, self._ny * self.pixel_size

    @property
    def center(self):
        return np.mean(self._x_grid), np.mean(self._y_grid)

    @property
    def x_is_inverted(self):
        return self._matrix_pix2ang[0, 0] < 0

    @property
    def y_is_inverted(self):
        return self._matrix_pix2ang[1, 1] < 0

    @staticmethod
    def map_coord(ra, dec, x_0, y_0, M):
        x, y = np.array(M).dot(np.array([ra, dec]))
        return x + x_0, y + y_0

    def radec_to_pixel(self, ra, dec):
        return self.map_coord(ra, dec, self._x_at_radec_0, self._y_at_radec_0, self._matrix_ang2pix)

    def pixel_to_radec(self, x, y):
        return self.map_coord(x, y, self._ra_at_xy_0, self._dec_at_xy_0, self._matrix_pix2ang)

    @staticmethod
    def grid_from_coordinate_transform(nx, ny, Mpix2coord, x_at_ij_0, y_at_ij_0):
        a = np.arange(nx)
        b = np.arange(ny)
        matrix = np.dstack(np.meshgrid(a, b)).reshape(-1, 2)
        x_grid = matrix[:, 0]
        y_grid = matrix[:, 1]
        ra_grid = x_grid * Mpix2coord[0, 0] + y_grid * Mpix2coord[0, 1] + x_at_ij_0
        dec_grid = x_grid * Mpix2coord[1, 0] + y_grid * Mpix2coord[1, 1] + y_at_ij_0
        return ra_grid, dec_grid

    def coordinate_grid_1d(self, nx, ny):
        ra_coords, dec_coords = self.grid_from_coordinate_transform(nx, ny, self._matrix_pix2ang, self._ra_at_xy_0, self._dec_at_xy_0)
        return ra_coords, dec_coords

    def coordinate_grid_2d(self, nx, ny):
        ra_coords, dec_coords = self.coordinate_grid_1d(nx, ny)
        ra_coords = util.array2image(ra_coords, nx, ny)
        dec_coords = util.array2image(dec_coords, nx, ny)
        return ra_coords, dec_coords

    def create_new_coordinates(self, pixel_scale_factor=None, 
                               grid_center=None, grid_shape=None):
        """Based on the current coordinates, creates a sub-coordinates system
        potentially shifted, with a different pixel size and field-of-view.

        Parameters
        ----------
        pixel_scale_factor : float, optional
            Ratio between the new pixel size and the original pixel size, by default None
        grid_center : (float, float), optional
            x and y center coordinates of the new coordinates grid, by default None
        grid_shape : (float, float), optional
            Width and height (in arcsec) of the new coordinates grid, by default None

        Returns
        -------
        Coordinates
            New instance of a Coordinates object
        """
        unchanged_count = 0
        if grid_center is None or grid_center == self.center:
            grid_center_ = self.center
            unchanged_count += 1
        else:
            grid_center_ = grid_center
        if grid_shape is None or grid_shape == self.shape:
            grid_shape_ = self.shape
            unchanged_count += 1
        else:
            grid_shape_ = grid_shape
        if pixel_scale_factor is None or pixel_scale_factor == 1:
            pixel_scale_factor_ = 1
            unchanged_count += 1
        else:
            pixel_scale_factor_ = pixel_scale_factor

        # in case it's the same region as the base coordinate grid
        if unchanged_count == 3:
            return copy.deepcopy(self)

        pixel_size = self.pixel_size * float(pixel_scale_factor_)
        center_x, center_y = grid_center_
        width, height = grid_shape_
        nx = round(width / pixel_size)
        ny = round(height / pixel_size)

        matrix_pix2ang = self._matrix_pix2ang / self.pixel_size * pixel_size

        cx, cy = nx / 2., ny / 2.
        cra, cdec = matrix_pix2ang.dot(np.array([cx, cy]))
        x_at_ij_0, y_at_ij_0 = - cra + center_x + pixel_size/2., - cdec + center_y + pixel_size/2.

        return Coordinates(nx, ny, matrix_pix2ang, x_at_ij_0, y_at_ij_0)
