# COOLEST API: `coolest.api` submodule

## Analysis with `coolest.api.analysis`

Based on a `coolest` object, the `Analysis` class handles computation of model-independent quantities, including the Einstein radius, mass density slope, effective radius, axis ratio from central moments, etc. 

## Models: `coolest.api.composable_model`

Based on a `coolest` object, a "composable model" selects the required light and mass model components, and performs lens model computations, including convolution by the PSF, ray-tracing and supersampling. 

## Plotting: `coolest.api.plotting`

The plotting routines, separated into different classes, allow the user to visualize the lens models, optionally evaluating the model components on different types of grid (`ModelPlotter`, `MultiModelPlotter`), or generate posterior distributions plots (`ParametersPlotter`).
