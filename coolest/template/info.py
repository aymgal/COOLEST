# Some variables useful to access

from coolest.template import standard
from coolest.template.classes import lensing_entity
from coolest.template.classes.profiles import light
from coolest.template.classes.profiles import mass
from coolest.template.classes import noise
from coolest.template.classes import psf
from coolest.template.classes import likelihood
from coolest.template.classes import probabilities
# from coolest.template.classes.regularizations import pixelated as pixel_regul


all_supported_choices = {
    'modes': standard.SUPPORTED_MODES,
    'lensing_entities': lensing_entity.SUPPORTED_CHOICES,
    'light_profiles': light.SUPPORTED_CHOICES,
    'mass_profiles': mass.SUPPORTED_CHOICES,
    # 'pixel_regularizations': pixel_regul.SUPPORTED_CHOICES,
    'likelihoods': likelihood.SUPPORTED_CHOICES,
    'noise_types': noise.SUPPORTED_CHOICES,
    'psf_types': psf.SUPPORTED_CHOICES,
    'prior_types': probabilities.PRIOR_SUPPORTED_CHOICES
}
