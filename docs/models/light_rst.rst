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

# Supported light profiles

The equations for elliptical profiles provided in the following are valid for coordinates $(x,y)$ centered on the origin and with the major axis of the ellipsoid along the $x$ axis which corresponds to a position angle $\phi=-90^\circ$ following COOLEST conventions.

_**TODO**: add references to publications_

## Analytical light profiles

### Sérsic profile

``` {admonition} Availability
Implemented in both `coolest.template` and `coolest.api`.
```

The brightness profile of the **elliptical Sérsic profile** is given by:
$$
  I(x,y) \equiv I_{\rm eff} \exp \left\{ -b_n \left[ \left(\frac{\sqrt{qx^2 + y^2/q}}{\theta_{\rm eff}}\right)^{1/n} - 1\right] \right\},
$$
where $b_n$ is calculated by \cite{Capaccioli1989} as:
$$
  b_n = 1.9992n - 0.3271.
$$
The halt-light radius, $\theta_{\rm eff}$, is where the brightness of a circular profile is equal to $I_{\rm eff}$.
Similarly for the elliptical case, where the brightness is equal to $I_{\rm eff}$ on the ellipse whose major axis (located on the x-axis) is equal to $\theta_{\rm eff}$.

If the total magnitude, $M_{\rm tot}$, of such a source is given for an instrument with known zero-point, $ZP$, then: 
$$
  I_{\rm eff} = \frac{b_{\rm n}^{2n}\,10^{-0.4(M_{\rm tot} - ZP)}}{2\pi\, \theta_{\rm eff}^2 \, n \, e^{b_{\rm n}} \, \Gamma(2 n )\, q},
$$
where $\Gamma$ is the gamma function.

## Pixelated profiles

### Regular grid of pixels

``` {admonition} Availability
Implemented in both `coolest.template` and `coolest.api`.
```

__TODO__

### Irregular grid of pixels

``` {admonition} Availability
Implemented in both `coolest.template` and `coolest.api`.
```

__TODO__
