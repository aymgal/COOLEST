# COOLEST: COde-independent Organized LEns STandard

![License](https://img.shields.io/github/license/aymgal/COOLEST)
![PyPi python support](https://img.shields.io/badge/Python-3.7-blue)
[![Coverage Status](https://coveralls.io/repos/github/aymgal/COOLEST/badge.svg)](https://coveralls.io/github/aymgal/COOLEST)


## A standard for gravitational lens modeling

After a lens modeling analysis is published and available as a manuscript, it is often challenging to **(1) reproduce the results** with the same or another similar modeling software, or **(2) start a new analysis** directly based on published results, **(3) reliably and quantitatively compare results** from different analyses. Moreover, there is currently no practical way to share and store lens models within the community.

The **COde-independent Organized LEns STandard (COOLEST)** proposes a solution to the above problems. COOLEST is a standard for **describing, storing and sharing lens models** more easily, independently of the specific modeling techniques and software packages. The main element of COOLEST is a unique JSON hierarchical template file, that stores in a human-readable way the necessary lens model data. Another key element is a suit of visualization tools that automatically produces a series of images, plots and other analysis products from a COOLEST file.

Currently, this repository hosts a Python API to __generate__, __manipulate__ and __update__ COOLEST files. The API structure exactly mirrors the hierarchy of the template file. Visualization and analysis classes will soon be added.

Ultimately, the goal is that modeling software packages each have an interface (a simple function) that converts code-specific model choices and parameter values to COOLEST conventions. This way, all lens modeling results---best-fit parameter values, posterior distributions---can be saved effortlessly to this standard, ready to be shared and used for further analyses.



## Adopted conventions

COOLEST defines a set of fixed conventions to define coordinate systems, model parameters such as ellipticities, and how data files are stored/linked to the template. Here is a subset of those conventions:

- **Units**:
    - Lengths, radii, angular positions, widths, heights are expressed in arcseconds
    - Position angles and orientations of elliptical profiles are defined in the interval (-90, +90] degrees

- **Coordinate system**:
    - Standard cartesian coordinate system: RA decreasing along *x*, Dec increasing along *y*
    - The origin is a unique (absolute) sky coordinate (RA, Dec)
    - Position angles defined counter-clockwise from positive *y* axis (i.e. East-of-North). For elliptical profiles, the angle is measured based on the major-axis of the ellipse.

- **Standard quantities**:
    - effective radii (e.g. Einstein radius, half-light radius) are expressed along the intermediate axis, as the product average of semi-major and semi-minor axis, i.e. _r_ = sqrt(_ab_)

_**The full list of conventions will soon be uploaded on this repository.**_


## Overview of the JSON template hierarchy

![API Hierarchy](images/api_stacked_hierarchy.png "API Hierarchy")
