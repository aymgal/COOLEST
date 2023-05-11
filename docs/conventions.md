# COOLEST conventions

The standard relies on a set of fixed conventions, that are implicitly assumed by all lens models stored in the COOLEST format.

## Units

- Width, height, angular positions and length (e.g. radii) are all given in **arcseconds**.
- Position angles and orientations are given in **degrees**, by default in the interval $(-90^\circ, +90^\circ]$. This typically holds true for profiles with $180^\circ$-symmetry such as elliptical profiles and external shear. Otherwise, it is explicitly mentioned in the profile definition.
- data and model images (e.g., including pixelated light profiles) are assumed to be given in **electrons per second**. If these units are evidently not suitable to the type of data (e.g., radio wavelenghts), the alternative units must be specified in the `'meta'` section of the template.


## Coordinates system

- The origin of the coordinate system in which all quantities are defined is fixed by a **single absolute J2000 coordinate**, given in `0h:0m:0.0s` (right ascension) and `0d:0m:0.0s` (declination) format. Any dependence on a specific field-of-view should be subtracted out.
- Quantities are expressed in a **cartesian coordinate system** $(x, y)$, the $x$ axis positively increasing to the right, the $y$ axis positively increasing upwards. Since coordinates are then always aligned with the image axes, this is a more intuitive description compared to (RA, Dec).
- Position angles and orientations (usually denoted $\phi$) are measured counter-clockwise from the positive $y$ axis. Thus it is similar to the frequently used "East-of-North" convention.

[label](../schemes/conventions_coordinates.pdf)

## Notations

- Cartesian coordinates are given $(x,y)$, polar coordinates are $(r,\phi)$. If required, the radial vector (in polar coordinates) is $\boldsymbol{r}$.
- Parameters and quantities representing radii are given in angular units (i.e. arcsec) and thus it is better suited to note them "$\theta$" (instead of "$r$"). This includes the Einstein radius ($\theta_{\rm E}$) and the effective radius ($\theta_{\rm eff}$), for instance. However, fpr some profiles are systematically defined with "$r$" in the literature (e.g., NFW), the common notations are followed.
- the lens potential is $\psi$, the deflection angle is $\alpha$, and the convergence is $\kappa$.


## Ellipticity parametrization

XX
