# LensModelAPI: a standard for lens models

API for defining application-independent lens models, aiming to __generate input files__ and __store output files__ for any lens modeling code/pipeline.

The first implementation takes the form of collection of Python classes, organised in a very general hierarchy common to every lens model paradigms. It can the be encoded in a JSON or YAML human-readable file that serves as the base for initialiazing and storing modeling results.

Current hierarchy:

![API Hierarchy](images/api_stacked_hierarchy.png "API Hierarchy")
