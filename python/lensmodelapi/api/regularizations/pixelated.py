__author__ = 'aymgal'

from lensmodelapi.api.regularization import Regularization
from lensmodelapi.api.parameter_list import ParameterList
from lensmodelapi.api.parameter import HyperParameter
from lensmodelapi.api.parameter import DefinitionRange


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
    'PixelPositivity',
    'PixelDefault',
]
SUPPORTED_CHOICES = __all__


class PixelEntropy(Regularization):

    def __init__(self, **kwargs):
        description = "Entropy regularization"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for entropy regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm e}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelRidge(Regularization):

    def __init__(self, **kwargs):
        description = "Ridge regularization (L2 norm)"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for Ridge norm regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm ridge}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelLasso(Regularization):

    def __init__(self, **kwargs):
        description = "Lasso regularization (L1 norm)"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for Lasso norm regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm lasso}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelGradient(Regularization):

    def __init__(self, **kwargs):
        description = "Gradient regularization (first spatial derivative)"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for gradient regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm grad}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelCurvature(Regularization):

    def __init__(self, **kwargs):
        description = "Curvature regularization (second spatial derivative)"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for curvature regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm curv}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelExponentialKernel(Regularization):

    def __init__(self, **kwargs):
        description = "Exponential kernel regularization"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for exponential kernel regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm exp}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelGaussianKernel(Regularization):

    def __init__(self, **kwargs):
        description = "Gaussian kernel regularization"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter for gaussian kernel regularization",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm gauss}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelStarlet(Regularization):

    def __init__(self, **kwargs):
        description = "Starlets regularization"
        parameters = ParameterList(
            HyperParameter('lambda_hf',
                           "Lagrange parameter for first starlet scale (high frequencies)",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm s, hf}$"),
            HyperParameter('lambda',
                           "Lagrange parameter from second to last starlet scales (excluding coarse scale)",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm s}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelBLWavelet(Regularization):

    def __init__(self, **kwargs):
        description = "Battle-Lemarie wavelet regularization"
        parameters = ParameterList(
            HyperParameter('lambda_hf',
                           "Lagrange parameter for first Battle-Lemarie scale (high frequencies)",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm BL, hf}$"),
        )
        super().__init__(description, parameters, **kwargs)

class PixelPositivity(Regularization):

    def __init__(self, **kwargs):
        description = "Non-negativity constraint on pixel values"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda_{\rm pos}$"),
        )
        super().__init__(description, parameters, **kwargs)


class PixelDefault(Regularization):

    def __init__(self, **kwargs):
        description = "Default regularization strategy, set by the specific modelling code"
        parameters = ParameterList(
            HyperParameter('lambda',
                           "Lagrange parameter",
                           DefinitionRange(min_value=0.0),
                           latex_name=r"$\lambda$"),
        )
        super().__init__(description, parameters, **kwargs)
