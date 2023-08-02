# Definitions of mass and light profiles

In order to bring together different modeling codes and ensure models are consistent with others, a necessary part of COOLEST is the definition of a set of mass and light profile parametrizations.

``` {admonition} Note
In the current python interface of the standard, mass and light profiles are implemented in two separate subpackages: `coolest.template` and `coolest.api`. This allows to separate the template file system from the plotting & analysis API. The availability of these implementations are specified for each profile in the documentation pages below.
```

The different profiles are split into two broad categories:

- [mass profiles](https://coolest.readthedocs.io/en/latest/models/mass.html) to describe lens potentials, surface mass densities and other lensing-related quantities;
- [light profiles](https://coolest.readthedocs.io/en/latest/models/mass.html) to describe surface brightness distributions, including extended (galaxies) or point-like (stars, quasars) objects.

```{toctree}
---
hidden:
caption: Supported profiles
maxdepth: 1
---
Mass profiles <mass>
Light profiles <light>
```
