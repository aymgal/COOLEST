# Some variables useful to access

from lensmodelapi.api.profiles import light
from lensmodelapi.api.profiles import mass
from lensmodelapi.api.regularizations import pixelated
from lensmodelapi.api import likelihood_list


all_supported_choices = {
    'light_profiles': light.SUPPORTED_CHOICES,
    'mass_profiles': mass.SUPPORTED_CHOICES,
    'pixel_regularizations': pixelated.SUPPORTED_CHOICES,
    'likelihoods': likelihood_list.SUPPORTED_CHOICES,
}
