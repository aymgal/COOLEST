# Some variables useful to access

from coolest.template.api.profiles import light
from coolest.template.api.profiles import mass
from coolest.template.api import noise
from coolest.template.api import psf
from coolest.template.api.regularizations import pixelated
from coolest.template.api import likelihood_list


all_supported_choices = {
    'light_profiles': light.SUPPORTED_CHOICES,
    'mass_profiles': mass.SUPPORTED_CHOICES,
    'pixel_regularizations': pixelated.SUPPORTED_CHOICES,
    'likelihoods': likelihood_list.SUPPORTED_CHOICES,
    'noise': noise.SUPPORTED_CHOICES,
    'psf': psf.SUPPORTED_CHOICES,
}
