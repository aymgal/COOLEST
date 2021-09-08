# Single mass profile

from lensmodelapi.parameter import NonLinearParameter


__all__ = ['SIE', 'ExternalShearEllipticity', 'ExternalShearAngleStrength']
SUPPORTED_PROFILES = __all__


class _MassProfileBase(object):

    def __init__(self, 
                 name: str, 
                 description: str, 
                 parameters: str):
        self.name = name
        self.description = description
        self.parameters = parameters
        

class SIE(_MassProfileBase):
    
    def __init__(self):
        name = 'SIE'
        description = "Singular isothermal sphere"
        parameters = [
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               min_value=0.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ]
        super(name, description, parameters)


class PEMD(_MassProfileBase):
    
    def __init__(self):
        name = 'PEMD'
        description = "Powerlaw elliptical mass distribution"
        parameters = [
            NonLinearParameter('gamma',
                               "Mass density slope at Einstein radius",
                               min_value=1.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('theta_E',
                               "Einstein radius",
                               min_value=0.0,
                               latex_name=r"$\theta_{\rm E}$"),
            NonLinearParameter('e1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_1$"),
            NonLinearParameter('e2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$e_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               latex_name=r"$y_0$")
        ]
        super(name, description, parameters)


class ExternalShearEllipticity(_MassProfileBase):
    
    def __init__(self):
        name = 'ext_shear_gamma1gamma2'
        description = "External shear defined with ellipticity"
        parameters = [
            NonLinearParameter('gamma1',
                               "Complex ellipticity component 1",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('gamma2',
                               "Complex ellipticity component 2",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        ]
        super(name, description, parameters)


class ExternalShearAngleStrength(_MassProfileBase):
    
    def __init__(self):
        name = 'ext_shear_gamma_psi'
        description = "External shear defined with ellipticity"
        parameters = [
            NonLinearParameter('gamma',
                               "Strength of external shear",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_1$"),
            NonLinearParameter('phi',
                               "Orientation of external shear",
                               min_value=-1.0,
                               max_value=1.0,
                               latex_name=r"$\gamma_2$"),
            NonLinearParameter('center_x',
                               "Profile center along x coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$x_0$"),
            NonLinearParameter('center_y',
                               "Profile center along y coordinates",
                               fixed=True,
                               default_value=0.0,
                               latex_name=r"$y_0$")
        ]
        super(name, description, parameters)
