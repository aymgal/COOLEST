import setuptools
import os

name = 'coolest'

release_info = {}
infopath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                           name, '__init__.py'))
with open(infopath) as open_file:
    exec(open_file.read(), release_info)

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

# Use the README as long description but remove the second version 
# of the logo (readable only by GitHub's dark mode interface)
long_description = readme.replace('<img src="https://raw.githubusercontent.com/aymgal/COOLEST/main/images/full_logo_dark_bg.png#gh-dark-mode-only" width="600" alt="COOLEST logo" />', '')

# Python version
python_requires = '>=3.8'

# Required packages
install_requires = [
    'numpy>=1.20.0',
    'scipy>=1.6.3',
    'jsonpickle>=2.0.0',
    'astropy>=4.2.0',
]

# Optional packages
install_optional = [
    'matplotlib>=3.7.0',    # for plotting
    'lenstronomy>=1.11.7',  # for shapelets light profiles
    'ipython',              # for running example notebooks
    'ipykernel',            # notebooks in custom environment
    'getdist>=1.3.2',       # for making corner plots
]

version = release_info['__version__']

setuptools.setup(
    name=name,
    author=release_info['__author__'],
    author_email=release_info['__email__'],
    version=version,
    url=release_info['__url__'],
    download_url=f"https://github.com/aymgal/coolest/archive/refs/tags/v{version}.tar.gz",
    packages=setuptools.find_packages(),
    license=release_info['__license__'],
    description=release_info['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["coolest", "lensing", "gravitation", "astrophysics"],

    python_requires=python_requires,
    install_requires=install_requires,

    extras_require={
        "opt": install_optional,  # installable via `pip install coolest[opt]`
    },

    setup_requires=['pytest-runner',],
    tests_require=['pytest', 'pytest-cov', 'pytest-pep8'],
)
