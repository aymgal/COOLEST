__author__ = 'aymgal'

from lensmodelapi.regularization import Regularization
from lensmodelapi.parameter_list import ParameterList
from lensmodelapi.parameter import HyperParameter

__all__ = [
    'PixelEntropy',
    'PixelRidge',
    'PixelLasso',
    'PixelGradient',
    'PixelCurvature',
    'PixelExponentialKernel',
    'PixelGaussianKernel',
    'PixelStarlet',
    'PixelBLWavelet',
]
SUPPORTED_PROFILES = __all__


class PixelEntropy(Regularization):

    def __init__(self):
        description = "Entropy regularization"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for entropy regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm e}$"),
        ])
        super().__init__(description, parameters)


class PixelRidge(Regularization):

    def __init__(self):
        description = "Ridge regularization (L2 norm)"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for Ridge norm regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm ridge}$"),
        ])
        super().__init__(description, parameters)


class PixelLasso(Regularization):

    def __init__(self):
        description = "Lasso regularization (L1 norm)"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for Lasso norm regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm lasso}$"),
        ])
        super().__init__(description, parameters)


class PixelGradient(Regularization):

    def __init__(self):
        description = "Gradient regularization (first spatial derivative)"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for gradient regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm grad}$"),
        ])
        super().__init__(description, parameters)


class PixelCurvature(Regularization):

    def __init__(self):
        description = "Curvature regularization (second spatial derivative)"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for curvature regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm curv}$"),
        ])
        super().__init__(description, parameters)


class PixelExponentialKernel(Regularization):

    def __init__(self):
        description = "Exponential kernel regularization"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for exponential kernel regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm exp}$"),
        ])
        super().__init__(description, parameters)


class PixelGaussianKernel(Regularization):

    def __init__(self):
        description = "Gaussian kernel regularization"
        parameters = ParameterList([
            HyperParameter('lambda',
                           "Lagrange parameter for gaussian kernel regularization",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm gauss}$"),
        ])
        super().__init__(description, parameters)


class PixelStarlet(Regularization):

    def __init__(self):
        description = "Starlets regularization"
        parameters = ParameterList([
            HyperParameter('lambda_hf',
                           "Lagrange parameter for first starlet scale (high frequencies)",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm s, hf}$"),
            HyperParameter('lambda',
                           "Lagrange parameter from second to last starlet scales (excluding coarse scale)",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm s}$"),
        ])
        super().__init__(description, parameters)


class PixelBLWavelet(Regularization):

    def __init__(self):
        description = "Battle-Lemarie wavelet regularization"
        parameters = ParameterList([
            HyperParameter('lambda_hf',
                           "Lagrange parameter for first Battle-Lemarie scale (high frequencies)",
                           min_value=0.0,
                           latex_name=r"$\lambda_{\rm BL, hf}$"),
        ])
        super().__init__(description, parameters)
