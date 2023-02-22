__author__ = 'Giorgos Vernardos'

from coolest.template.lazy import *
from coolest.template.standard import COOLEST
from coolest.template.classes.grid import IrregularGrid
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import sys













# The following part of the code is a dummy plotting program
############################################################

# import matplotlib
import matplotlib.pyplot as plt
import matplotlib

# create an object of type IrregularGrid
source_4 = Galaxy('a VKL source', 1.2, light_model=LightModel('IrregularGrid'))
#source_4.light_model[0].pixels.field_of_view_x = (-10,10)
#source_4.light_model[0].pixels.field_of_view_y = (-10,10)
#source_4.light_model[0].pixels.set_fits('/home/giorgos/myCodes/COOLEST/mytests/dum_table.fits')
source_4.light_model[0].pixels.set_fits('/home/giorgos/myCodes/verykool/my_VKL_source.fits')


# create axes for one or more plots
fig,ax = plt.subplots(figsize=(15,6))

# This is the key command:
# Pass an axis object and an IrregularGrid object to the plotting function
ax = plot_voronoi(ax,source_4.light_model[0].pixels)

# save the figure
plt.savefig('test_plot.pdf')
