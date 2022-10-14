# COOLEST API: `coolest.api` submodule


## Analysis: `coolest.api.analysis`

- load the content of a COOLEST file
- perform computations of model-independent quantities:
    - effective Einstein radius
    - effective mass density slope
    - effective (half-light) radius


## Plotting: `coolest.api.plotting`

- instantiate an `Analysis` object from a COOLEST file
- defines general settings for all plots (colors, cmaps, etc...)
- could have child classes
    - Obervationlotter(Plotter)
    - LightPlotter(Plotter)
        - LensLightPlotter(LightPlotter)
        - SourcePlotter(LightPlotter)
    - MassPlotter(Plotter)
