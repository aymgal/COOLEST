---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Supported mass profiles

The equations for elliptical profiles provided in the following are valid for coordinates $(x,y)$ centered on the origin and with the major axis of the ellipsoid along the $x$ axis which corresponds to a position angle $\phi=-90^\circ$ following COOLEST conventions.

_**TODO**: add references to publications_

## Total mass profiles

### Power-law profiles

#### Singular isothermal ellipsoid (SIE)

The SIE lens potential is given by
$$
  \psi_{\rm SIE}(x,y) = \frac{\theta_{\rm E} \sqrt{q}~x}{\sqrt{1-q^2}} {\rm arctan} \left( \frac{\sqrt{1-q^2}~x}{\sqrt{q^2x^2+y^2}} \right) + \frac{\theta_{\rm E} \sqrt{q} ~y}{\sqrt{1-q^2}} {\rm arctanh} \left( \frac{\sqrt{1-q^2}~y}{\sqrt{q^2x^2+y^2}} \right) \ ,
$$
with $\theta_{\rm E}$ being the Einstein radius (as the product average of the minor and major axis of the ellipse at mean enclose convergence is 1), and $q$ being the axis ratio.

The SIE convergence has the following analytical formula
$$
  \kappa_{\rm SIE}(x,y) = \frac{\theta_{\rm E}}{2\sqrt{qx^2+y^2/q}} \ ,
$$

In COOLEST, the singular isothermal sphere (SIS) can be expressed as a SIE with fixed axis ratio $q=0$ (the value position angle is irrelevant in this case).

#### Softened power-law elliptical mass distribution (SPEMD)

The convergence of a SPEMD profile is the following :
$$
  \kappa_{\rm SPEMD}(x,y) = \frac{3-\gamma}{2} \left(\frac{b}{\sqrt{qx^2+y^2/q + s^2}} \right)^{\gamma -1}
$$

with $\gamma$ the logarithmic power-law slope (when $\gamma=2$, the profile is isothermal), $q$ the axis ratio, $s$ the core-radius. For rather small scale radii, that is $s<0.1~b$, $\theta_E \simeq  b - s^{3-\gamma} q^{(\gamma-1)/2}$ where $\theta_E$ is as define in our conventions.

The PEMD profile is characterized by the same equation with $s=0$; in this case, $b$ is thus equal to the Einstein radius as define in our conventions. 

## Baryon + dark matter profiles

NFW, Chameleon, etc...

## Massive fields

- External shear

- Flexion shift
