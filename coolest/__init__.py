"""

This file initializes the coolest module
and provides some basic information about the package.

"""

# Set the package release version
version_info = (0, 0, 1)
__version__ = '.'.join(str(c) for c in version_info)

# Set the package details
__author__ = 'COOLEST developers'
__email__ = 'aymeric.galan@gmail.com'
__year__ = '2021-2023'
__credits__ = 'COOLEST developers'
__url__ = 'https://github.com/aymgal/COOLEST'
__description__ = 'Standard for Strong Gravitational Lens Modeling'

# Default package properties
__license__ = 'MIT'
__about__ = ('{} Author: {}, Email: {}, Year: {}, {}'
             ''.format(__name__, __author__, __email__, __year__,
                       __description__))

