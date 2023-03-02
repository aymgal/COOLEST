import os
import time
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LogNorm, TwoSlopeNorm

from coolest.api.plotting import ModelPlotter, MultiModelPlotter
from coolest.api import util


def get_coolest_template(code_choice):
    json_files = glob.glob(os.path.join(code_choice, '*.json'))
    file_no_ext = os.path.splitext(json_files[0])[0]
    if file_no_ext[-6:] == '_pyAPI':
        file_no_ext = file_no_ext[:-6]
    return file_no_ext

vkl1 = get_coolest_template('vkl_model')
print(vkl1)
coolest_vkl1 = util.get_coolest_object(vkl1)


print(coolest_vkl1.lensing_entities)
print([entity.name for entity in coolest_vkl1.lensing_entities])


coordinates = util.get_coordinates(coolest_vkl1)
x, y = coordinates.pixel_coordinates
print("data extent:", coordinates.plt_extent)

coordinates_src = coordinates.create_new_coordinates(pixel_scale_factor=0.1,
                                                     grid_shape=(1.8, 1.8))
x_src, y_src = coordinates_src.pixel_coordinates
print("new coordinates extent:", coordinates_src.plt_extent)


#x_src, y_src = np.meshgrid(np.linspace(-1, 1, 20), np.linspace(-1, 1, 20))

# create the figure
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# initialize the plotter
plotter = ModelPlotter(coolest_vkl1, coolest_directory=os.path.dirname(vkl1))

norm = None # Normalize(-1e-4)

plotter.plot_surface_brightness(
    axes[0], title="Adaptive",
    entity_selection=[2],
    norm=norm, 
    extent=coordinates_src.extent)

plotter.plot_surface_brightness(
    axes[1], title="Adaptive (interp.)",
    entity_selection=[2],
    norm=norm,
    coordinates=coordinates_src)


#axes[1, 0].axis('off')
#axes[1, 1].axis('off')
fig.tight_layout()
plt.show()

