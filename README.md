# LensModelAPI: a standard for lens models

API for defining application-independent lens models, aiming to __generate template files__ to initalize models, and __store output results__ from _any_ lens modeling code/pipeline.

The first implementation takes the form of collection of Python classes, organised in a very general hierarchy common to most of lens model software packages. It can the be encoded as JSON or YAML human-readable files that serve as templates for initialiazing and storing modeling results.


## Adopted conventions

Within this framework, the following conventions are fixed and must be adopted when filling template files:
- **coordinates origin**: center of the imaging data cutout
- **coordinates orientation**: RA increasing along x direction, Dec increasing along y direction
- **position**: East-of-North
- **external shear**: strength and position angle
- **radii**: intermediate-axis (applies to e.g. Einstein radii, half-ligh radii, etc.)


## Current hierarchy

![API Hierarchy](images/api_stacked_hierarchy.png "API Hierarchy")
