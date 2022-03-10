# LensModelAPI: a standard for lens models

API for defining application-independent lens models, aiming to __generate template files__ to initalize models, and __store output results__ from _any_ lens modeling code/pipeline.

The first implementation takes the form of collection of Python classes, organised in a very general hierarchy common to most of lens model software packages. It can the be encoded as JSON or YAML human-readable files that serve as templates for initialiazing and storing modeling results.


## Adopted conventions

Within this framework, the following conventions are fixed and must be adopted when filling template files:

- **Units**:
    - Lengths, radii, angular positions, widths, heights: arcseconds
    - Position angles and orientations: degrees, by default in the interval (-90, +90]

- **Coordinate system**:
    - Standard cartesian coordinate system: RA decreasing along *x*, Dec increasing along *y*
    - The origin is a unique (absolute) sky coordinate (RA, Dec)
    - Position angles defined counter-clockwise from positive *y* axis (i.e. East-of-North). For elliptical profiles, the angle is measured based on the major-axis of the ellipse.

- **Standard quantities**:
    - effective radii (e.g. Einstein radius, half-light radius) are expressed along the intermediate axis, as the product average of semi-major and semi-minor axis, i.e. _r_ = sqrt(_ab_)

- **Other conventions**: TBD.


## Overview of the JSON template hierarchy

![API Hierarchy](images/api_stacked_hierarchy.png "API Hierarchy")
