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

### Singular isothermal power-law

_Implemented in_
- [x] `coolest.template`
- [x] `coolest.api`

The **singular power-law ellipsoid** (SIE) lens potential is given by
$$
  \psi_{\rm SIE}(x,y) = \frac{\theta_{\rm E} \sqrt{q}~x}{\sqrt{1-q^2}} {\rm arctan} \left( \frac{\sqrt{1-q^2}~x}{\sqrt{q^2x^2+y^2}} \right) + \frac{\theta_{\rm E} \sqrt{q} ~y}{\sqrt{1-q^2}} {\rm arctanh} \left( \frac{\sqrt{1-q^2}~y}{\sqrt{q^2x^2+y^2}} \right) \ ,
$$
with $\theta_{\rm E}$ being the Einstein radius (as the product average of the minor and major axis of the ellipse at mean enclose convergence is 1), and $q$ being the axis ratio.

The SIE convergence has the following analytical formula
$$
  \kappa_{\rm SIE}(x,y) = \frac{\theta_{\rm E}}{2\sqrt{qx^2+y^2/q}} \ ,
$$

In COOLEST, the **singular isothermal sphere** (SIS) can be expressed as a SIE with fixed axis ratio $q=1$ (the position angle value is irrelevant in this case). In this case, the potential and convergence are simply
$$
  \psi_{\rm SIS} (x,y)= \theta_E  \sqrt{x^2+y^2} \ , \\
  \kappa_{\rm SIS}(x,y)=\frac{\theta_E }{2\sqrt{x^2+y^2}} \ .
$$

### Cored generic power-law

The convergence of a SPEMD profile is the following :
$$
  \kappa_{\rm SPEMD}(x,y) = \frac{3-\gamma}{2} \left(\frac{b}{\sqrt{qx^2+y^2/q + s^2}} \right)^{\gamma -1}
$$

with $\gamma$ the logarithmic power-law slope (when $\gamma=2$, the profile is isothermal), $q$ the axis ratio, $s$ the core-radius. For rather small scale radii, that is $s<0.1~b$, $\theta_E \simeq  b - s^{3-\gamma} q^{(\gamma-1)/2}$ where $\theta_E$ is as define in our conventions.

### Generic power-law profile

_Available in_
- [x] `coolest.template`
- [x] `coolest.api`

The PEMD profile is characterized by the same equation with $s=0$; in this case, $b$ is thus equal to the Einstein radius as define in our conventions.

### Cored isothermal power-law

_Available in_
- [x] `coolest.template`
- [ ] `coolest.api`

The Non-singular Isothermal Ellipsoid (NIE) is the special case of a SPEMD, with isothermal slope $\gamma=2$. The convergence is thus
$$
    \kappa_{\rm NIE}(x,y) = \frac12 \frac{b}{\sqrt{qx^2 + y^2/q + s^2}} \ ,
$$
where the Einstein radius is equal to $b$ for no core ($s=0$). For a small cored radius $s<0.1$, the approximation formula given for SPEMD should hold.


## Dark matter profiles

### Navarro-Frenk-White

The **Navarro, Frenk, and White** NFW profile is defined using 3D characteristic density $\rho_c$, and 3D scale radius $r_s$ as
$$
  \rho(r) = \frac{\rho_c}{(r/r_s)(1+r/r_s)^2} \ .
$$

Projection into 2D and addition of ellipticity is defined by \cite{Golse2002}.

## Baryonic matter profiles

NFW, Chameleon, etc...

## Massive fields

- External shear

- Flexion shift
