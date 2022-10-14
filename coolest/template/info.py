# Some variables useful to access

from coolest.template.classes.profiles import light
from coolest.template.classes.profiles import mass
from coolest.template.classes import noise
from coolest.template.classes import psf
from coolest.template.classes.regularizations import pixelated as pixel_regul
from coolest.template.classes import likelihood_list


all_supported_choices = {
    'light_profiles': light.SUPPORTED_CHOICES,
    'mass_profiles': mass.SUPPORTED_CHOICES,
    'pixel_regularizations': pixel_regul.SUPPORTED_CHOICES,
    'likelihoods': likelihood_list.SUPPORTED_CHOICES,
    'noise': noise.SUPPORTED_CHOICES,
    'psf': psf.SUPPORTED_CHOICES,
}
