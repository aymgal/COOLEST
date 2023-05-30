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

``` {admonition} Availability
Implemented in both `coolest.template` and `coolest.api`.
```

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

``` {admonition} Availability
Implemented in `coolest.template`.
```

The convergence of a SPEMD profile is the following :
$$
  \kappa_{\rm SPEMD}(x,y) = \frac{3-\gamma}{2} \left(\frac{b}{\sqrt{qx^2+y^2/q + s^2}} \right)^{\gamma -1}
$$

with $\gamma$ the logarithmic power-law slope (when $\gamma=2$, the profile is isothermal), $q$ the axis ratio, $s$ the core-radius. For rather small scale radii, that is $s<0.1~b$, $\theta_E \simeq  b - s^{3-\gamma} q^{(\gamma-1)/2}$ where $\theta_E$ is as define in our conventions.

### Generic power-law profile

_Implemented in `coolest.template` and `coolest.api`._

The PEMD profile is characterized by the same equation with $s=0$; in this case, $b$ is thus equal to the Einstein radius as define in our conventions.

### Cored isothermal power-law

``` {admonition} Availability
Implemented in `coolest.template`.
```

The Non-singular Isothermal Ellipsoid (NIE) is the special case of a SPEMD, with isothermal slope $\gamma=2$. The convergence is thus
$$
    \kappa_{\rm NIE}(x,y) = \frac12 \frac{b}{\sqrt{qx^2 + y^2/q + s^2}} \ ,
$$
where the Einstein radius is equal to $b$ for no core ($s=0$). For a small cored radius $s<0.1$, the approximation formula given for SPEMD should hold.


## Dark matter profiles

### Navarro-Frenk-White

``` {admonition} Availability
Implemented in `coolest.template`.
```

The **Navarro, Frenk, and White** NFW profile is defined using 3D characteristic density $\rho_c$, and 3D scale radius $r_s$ as
$$
  \rho(r) = \frac{\rho_c}{(r/r_s)(1+r/r_s)^2} \ .
$$

Projection into 2D and addition of ellipticity is defined by \cite{Golse2002}.

## Baryonic matter profiles

``` {admonition} Availability
Implemented in `coolest.template`.
```

Following [Dutton et al. 2011](https://ui.adsabs.harvard.edu/abs/2011MNRAS.417.1621D/exportcitation), the chameleon profile is defined as the difference between two NIE profiles with different core radii $s_{\rm c}$ and $s_{\rm t}$. The former defines an overall core radius, and latter defines a truncation radius (hence $s_{\rm t} > s_{\rm c}$). The two NIE components have the same normalization $b$ to ensure the
total mass is finite. The convergence of the chameleon profile is thus
$$
\begin{align}
  \nonumber
  \kappa_{\rm chm}(x, y) &\equiv \kappa_{\rm NIE, c}(x, y) - \kappa_{\rm NIE, t}(x, y) \\
  \nonumber
  &= \frac{b}{2} \left[ \frac{1}{\sqrt{qx^2 + y^2/q + s_{\rm c}^2}} - \frac{1}{\sqrt{qx^2 + y^2/q + s_{\rm t}^2}} \right] \ .
\end{align}
$$
The lens potential and deflection angles are similarly defined, as the difference of the potentials and deflections of two NIEs.

## Massive fields

### External shear

``` {admonition} Availability
Implemented in both `coolest.template` and `coolest.api`.
```

The lens potential due to shear only with respect to the origin and for an angle $\phi$ measured counter-clockwise from the positive x-axis, is given by:
$$
  \psi(\boldsymbol{r}) \equiv \psi(r,\phi) = \frac{r^2}{2} \, \gamma_{\rm ext} \, \cos\left[ 2 (\phi - \phi_{\rm ext}) \right],
$$
or equivalently:
$$  
  \psi(x,y) = \frac12 \, \gamma_1 \, (x^2 - y^2) + \gamma_2 \, x \, y,
$$
where in the last equation we set:
$$
  \gamma_1 = \gamma_{\rm ext} \, \cos (2 \phi_{\rm ext}) \quad \mathrm{and} \quad \gamma_2 = \gamma_{\rm ext} \, \sin (2 \phi_{\rm ext}).
$$
The angle and magnitude of the shear are related to its $\gamma_1$ and $\gamma_2$ components through:
$$
  \gamma_{\rm ext} = \sqrt{\gamma_1^2 + \gamma_2^2} \quad \mathrm{and} \quad \phi_{\rm ext} = \frac12 \tan^{-1} \left( \frac{\gamma_2}{\gamma_1} \right).
$$

### Flexion shift

``` {admonition} Availability
Soon implemented in `coolest.template`.
```
