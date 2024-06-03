__author__ = 'aymgal'

from coolest.template.classes.base import APIBaseObject
from coolest.template.classes.grid import PixelatedRegularGrid


__all__ = [
    'ImagingDataLikelihood',
]

SUPPORTED_CHOICES = [
    'ImagingDataLikelihood', 

    # TODO: implement the following classes:
    # 'TimeDelayLikelihood',
    # 'MagnificationRatioLikelihood',
    # 'ImagePlanePositionLikelihood',
    # 'SourcePlanePositionLikelihood',
]


class Likelihood(APIBaseObject):
    """Abstract likelihood object.

    Parameters
    ----------
    name : str
        Name of the entity (e.g., the name of the galaxy)
    redshift : float
        Redshift of the entity, if known / assumed
    mass_model : MassModel, optional
        Mass model (i.e., a set of mass profiles), by default None

    Raises
    ------
    ValueError
        If the provided redshift is negative.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.type = self.__class__.__name__  # name of the children class
        super().__init__()


class ImagingDataLikelihood(Likelihood):
    """Imaging data likelihood, which typically holds the type of
    likelihood (e.g., Gaussian) and information about masked pixels.

    Parameters
    ----------
    mask : PixelatedRegularGrid, optional
        Binary mask with 0 for masked areas and 1 for areas included
        in the likelihood computation, by default None
    """

    def __init__(self, 
                 mask: PixelatedRegularGrid = None,
                ) -> None:
        self.mask = mask

    def check_consistency_with_observation(self, observation):
        """Checks that the data image is consistent with instrument properties"""
        width  = abs(self.pixels.field_of_view_x[1] - self.pixels.field_of_view_x[0])
        height = abs(self.pixels.field_of_view_y[1] - self.pixels.field_of_view_y[0])
        num_pix_ra = int(width / observation.pixels.pixel_size)
        error_message_ra = f"Field-of-view along RA is inconsistent (data: {num_pix_ra}, likelihood mask: {self.mask.num_pix_x})."
        assert self.pixels.num_pix_x  == num_pix_ra, error_message_ra
        num_pix_dec = int(height / observation.pixels.pixel_size)
        error_message_dec = f"Field-of-view along Dec is inconsistent (data: {num_pix_dec}, likelihood mask: {self.mask.num_pix_y})."
        assert self.pixels.num_pix_y  == num_pix_dec, error_message_dec
        # TODO: check pixel size value?
