---
title: 'COOLEST: COde-independent Organized LEns STandard'
tags:
  - Python
  - astronomy
  - strong lensing
  - lens modeling
authors:
  - name: Aymeric Galan
    orcid: 0000-0003-2547-9815
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Author with no affiliation
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 3
affiliations:
  - name: Technical University of Munich, TUM School of Natural Sciences, Department of Physics, James-Franck-Strasse 1, 85748 Garching, Germany
    index: 1
  - name: Institution Name, Country
    index: 2
  - name: Independent Researcher, Country
    index: 3
date: 21 April 2023
bibliography: paper.bib
---

# Summary

The current cosmological model $\Lambda$CDM is more and more challenged by a number of observations of the Universe. In particular, observations seem to favor different properties of dark matter and dark energy than previously thought. Strong gravitational lensing (SGL) is one of the best observational tools to address these challenges, because it reveals the distribution of any type of matter and can be used to constrain the properties of dark energy.

Extracting information from SGL data requires the careful analysis of images of gravitational lenses, a process referred to as _lens modeling_. Over the past twenty years, several lens modeling codes have been developed and used in published works. Unfortunately, there is currently no efficient and systematic way to access these published results and use them directly for new studies, which slows down new research and causes a waste of research time. The reason is simple: these modeling codes being based on different assumptions and conventions, bridging the gap between them is a challenging task.

Here we introduce COOLEST---the COde-independent Organized LEnsing STandard---to the lensing community, which allows researchers to, _independently of the original modeling code_:

- store lens models in a JSON format that is easy to read and manipulate, and lightweight;
- group together all necessary data, model and inference files (as images and array in FITS and pickled formats);
- compute a set of key lensing quantities in a model-independent way;
- generate publication-ready figures via an Python API to compare models side-to-side.

Any lens modeling code can adhere to this standard via a small interface that converts code-dependent quantities to the COOLEST conventions. The documentation and all Python routines incorporated in the API are meant to keep development time to a minimum for code developers.

![Figure generated with the Plotting API of COOLEST, comparing lens models obtained with three different modeling codes (numbered 1 to 3). Top row, from left to right: simulated observation of a strongly lensed source, best-fit models produced by two different codes (using different field of views), model residuals from model 1. Bottom row: source models 1 and 2 evaluated at the same sky coordinates, source model 2 on its original (regular) pixelated grid, and source model 3 on its original (irregular) pixelated grid. \label{fig:example_plotting_api}](coolest_plot_example.png)


# Statement of need

In SGL studies, the lens modeling step is often the most time-consuming. The complexity of a lens model primarily depends on the resolution of the observed lens images and its signal-to-noise (S/N). While low-resolution and noisy images can be modeled with simply parametrized functions ($\sim 10^1$ parameters), high-resolution and deep images require much more complexity ($\sim 10^2$ to $10^4$ parameters) and many optimization steps before successfully modeling the observation. Moreover, different scientific goals do not warrant the same modeling effort, which naturally influences model complexity. Other types of observation (e.g., in radio wavelengths) are not directly obtained as images and thus require extra lens modeling steps.

Such a large variety of data sets and scientific objectives have led to the development of different lens modeling codes. These codes may be written in different programming languages and generally based on fundamentally different assumptions, some are not open-source, and some may not be well-documented. Consequently, when a new SGL study gets published, it is very challenging and time-consuming (sometimes impossible) to use these new results to start a new lens modeling analysis, should it be with the same code or with a different code that is better suited to the new objective. Moreover, comparing lens models with previously published models is as challenging, exactly for the same reasons. So far, there is no standard way to describe, store and share lens modeling products to accelerate SGL research.

This is the motivation behind COOLEST: because lens modeling products follow the same theoretical foundations, we could built a standard based on precise conventions so that lens models can be described _independently of the original modeling code_. Important lens modeling products typically include the lens mass distribution, the unconvolved surface brightness of both the lens and the (unlensed) source galaxies, as well as a model of the point spread function of the instrument. COOLEST offers a simple and human-readable way to describe a lens model, summarized in a single JSON template file, and optionally links to external files (with .fits and .pkl extenstions), all stored within a single directory. At the core of the template is a list of _lensing entities_, which allow to describe the gravitational lens directly in terms of physical objects (i.e., galaxies or quasars), alongside more abstract lensing components called _mass fields_ (i.e., external shear or flexion shift fields). Since the content of the template follows a set well-defined conventions, it can be compared effortlessly with other models that are compliant with COOLEST. Additionally, since physical objects like galaxies are directly encoded in the template, it enables straightforward access to relevant quantities that are useful for non-lensing studies, such as those focusing on galaxy evolution.

Such a concise storage provides a practical way to share a given lens model and refer to it for later analyses. In addition to the advantages mentioned above, this standard is particularly appropriate in the context of the remarkable increase of the number of known gravitational lenses. Upcoming large scale surveys will discover many thousands of such systems, which will rapidly trigger many new lens modeling analyses. Large databases are beeing built to record all known and future gravitational lenses [__ref to SLED?__]. The standard we propose, powered by its lightweight storage system, is the ideal tool for storing existing lens models (with proper publication references, if any) alongside the lens information, directly within the database. Moreover, we anticipate that the analysis and plotting API we provide will be useful to generate on-the-fly products that researchers can easily retrieve online from the database servers.

# Content of the standard

COOLEST is composed of three distinct building blocks:

- __Conventions__: a set of fixed definitions adopted by the standard, such as the coordinate systems and units, which are implicitely assumed when manipulating the store lens model;
- __Template system__ (`coolest.template`): a Python interface to create, store and manipulate COOLEST template and external files;
- __Analysis & plotting API__ (`coolest.api`): a Python interface to compute key lensing quantities and generate different plots.

The template file stores most of the data and lens model information, including observational and instrumental properties, and particular model choices that describe the gravitational lens. It stores indivual model parameter values (as point estimates), as well as a description of their prior distribution (if any) and first-order statistics of their posterior distributions (e.g., from MCMC chains). An example of such a [template file](https://github.com/aymgal/COOLEST/blob/main/examples/coolest_template.json), and how to generate and fill one, is provided on our GitHub repository.

The parent directory of that template, depending on the application, can also contain observational data, model images and PSF models. Additionally, the `'meta'` field of the template is also used to refer to inference data such as MCMC chains, stored in separate files.

All details regarding the conventions and Python interfaces are given on the COOLEST [documentation website](https://coolest.readthedocs.io).

<!-- # Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text. -->

<!-- # Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% } -->


# Related software

The following lens modeling codes already have at least a minimal interface with COOLEST:

- `Lenstronomy` `[@lenstronomy2018; @lenstronomy2021]`
- `Herculens` `[@herculens2021]`
- `VKL` `[@vkl2022]`

Other lens modeling codes:

- `GLEE` `[@glee2010; @glee2012]`
- `PyAutoLens` `[@pyautolens2015; @pyautolens2018; @pyautolens2021]`
- `giga-lens` `[@gigalens2022]`

Lens model databases:

- ???


# Acknowledgements

The authors thank XXX for useful discussion. This work is supported by the Swiss National Science Foundation (SNSF, Post.Doc Mobility grant XXX). XXXXXX

# References

XXX.
