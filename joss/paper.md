---
title: 'COOLEST: COde-independent Organized LEns STandard'
tags:
  - Python
  - astronomy
  - gravitational lensing
  - lens modeling
  - standard
authors:
  - name: Aymeric Galan
    orcid: 0000-0003-2547-9815
    affiliation: "1,2"
    corresponding: true
  - name: Lyne Van de Vyvere
    orcid: 0000-0002-0585-4203
    affiliation: 3
  - name: Matthew R. Gomer
    orcid: 0000-0001-5562-3879
    affiliation: 3
  - name: Georgios Vernardos
    orcid: 0000-0001-8554-7248
    affiliation: "1,4"
  - name: Dominique Sluse
    orcid: 0000-0001-6116-2095
    affiliation: 3
affiliations:
  - name: Institute of Physics, Laboratory of Astrophysics, École Polytechnique Fédérale de Lausanne (EPFL), Switzerland
    index: 1
  - name: Technical University of Munich, TUM School of Natural Sciences, Department of Physics, James-Franck-Strasse 1, 85748 Garching, Germany
    index: 2
  - name: STAR Institute, Quartier Agora, Allée du Six Août, 19c, 4000 Liège, Belgium
    index: 3
  - name: Department of Physics and Astronomy, Lehman College, City University of New York, 250 Bedford Park Boulevard West, Bronx, NY 10468-1589, USA
    index: 4
date: 16 Mai 2023
bibliography: paper.bib
---

# Summary

Any mass concentration in the Universe, luminous or dark, from vast galaxy clusters to stars within galaxies, can be studied through its gravitational deflection of light rays from background sources. This phenomenon, in its most impressive regime, is known as Strong Gravitational Lensing (SGL). It has several cutting-edge applications, for example: measuring the Hubble constant and shedding more light into the apparent tension between early and late Universe, detecting the presence of massive subhalos within distant galaxies that can constrain different dark matter models, and studying a galaxy’s mass partition between baryons and dark matter with direct implications on galaxy evolution.

Extracting information from SGL data requires the careful analysis of images of gravitational lenses, a process referred to as _lens modeling_, in order to generate an image of the lens based on models of mass and light distributions of the different physical objects in play (e.g., galaxies, quasars). In this paper we call a _lens model_ the full set of model components, including all mass and light models as well as the point spread function (PSF) model. Over the past twenty years, several lens modeling codes have been developed and used in published works. Unfortunately, there is currently no efficient and systematic way to access these published results and use them directly for new studies, which slows down new research and causes a waste of research time. The reason is simple: these modeling codes being based on different methods and conventions, bridging the gap between them is a challenging task.

Here we introduce COOLEST---the COde-independent Organized LEnsing STandard---to the lensing community, which allows researchers to, _independently of the original modeling code_:

- store lens models in a JSON format that is lightweight and easy to read and manipulate;
- group together all necessary data, model and inference files (such as images and arrays in standard [FITS](https://heasarc.gsfc.nasa.gov/docs/heasarc/fits.html) and [`pickle`](https://docs.python.org/3/library/pickle.html) formats);
- compute a set of key lensing quantities, such as the effective Einstein radius and mass density slope;
- compare models by generating standardized figures using a Python API.

Any lens modeling code can adhere to this standard via a small interface that converts code-dependent quantities to the COOLEST conventions. The documentation and all Python routines incorporated in the API serve to keep development time to a minimum for code developers. Figure \autoref{fig:example_plotting_api} below gives a concrete example of panels generated with the plotting API, alongside quantities computed with the analysis API.

![Figure generated from the output of 3 different lens modeling codes after converting it to the COOLEST standard and using the accompanying plotting API. In this example, each code models the source in fundamentally different ways: analytically with shapelets (model 1), using wavelets on a regular grid (model 2) and using the semi-linear inversion technique on an adaptive grid (model 3). The top left panel shows the (simulated) observation, while the bottom left panel shows model residuals (residuals from other models are indistinguishable). Remaining columns, from left to right, contain for each code the image of the model (top row) and the image of the reconstructed source (bottom row). \label{fig:example_plotting_api}](coolest_plot_example.png)

# Statement of need

In SGL studies, the lens modeling step is often the most time-consuming. The complexity of a lens model primarily depends on the resolution of the observed lens images and its signal-to-noise (S/N). While low-resolution and noisy images can be modeled with simply parametrized functions ($\sim 10^1$ parameters), high-resolution and deep images require much more complexity ($\sim 10^2$ to $10^4$ parameters) and many optimization steps before successfully modeling the observation. Moreover, different scientific goals do not warrant the same modeling effort, which naturally influences model complexity. Other types of observation (e.g., in radio wavelengths) are not directly obtained as images and thus require extra lens modeling steps.

Such a variety of data sets and scientific objectives have led to the development of different lens modeling codes. These codes may be written in different programming languages and generally based on fundamentally different assumptions, some are not open-source, and some may not be well-documented. Consequently, when a new SGL study gets published, it is very challenging and time-consuming (sometimes impossible) to use these new results in any subsequent analysis, should it be with the same code or with a different one that is better suited to the new objective. Moreover, comparing lens models with previously published ones is as challenging, exactly for the same reasons. In the past, only a few studies have tried to compare a selection of output quantities from different lens modeling analyses: in the context of lensing by galaxy clusters [@refsdal2016; @Meneghetti2017], or for time-delay cosmography with lensed quasars [@tdlmc2021; @tdcosmo2022]. However, until now, there has been no standard way to describe, store and share lens modeling products.

This is the motivation behind COOLEST: because lens modeling products follow the same theoretical foundations, we could built a standard based on precise conventions so that lens models can be described _independently of the original modeling code_. Important lens modeling products typically include the lens mass distribution, the unconvolved surface brightness of both the lens and the (unlensed) source galaxies, as well as a model of the point spread function of the instrument. COOLEST offers a simple and human-readable way to describe a lens model, summarized in a single JSON template file, and optionally links to external files (typically in the standard astronomical [FITS](https://heasarc.gsfc.nasa.gov/docs/heasarc/fits.html) format for images and tables, or in the [`pickle`](https://docs.python.org/3/library/pickle.html) format for high-dimensional arrays), all stored within a single directory. At the core of the template is a list of _lensing entities_, a new concept which allows researchers to describe the gravitational lens directly in terms of physical objects (e.g., galaxies or quasars), which is more intuitive than the abstract description used within modeling codes. It also enables a novel way to cross-reference physical objects among different analyses, including non-lensing analyses such as those focusing on galaxy evolution.

In summary, COOLEST aims at bridging the existing gap between independent SGL analyses and science goals, by providing a standardized way of describing and sharing lens models, within and outside the lensing community.

# Other applications

While originally focused on the description of systems in which an individual galaxy is acting as the lens (galaxy-galaxy strong lenses), COOLEST is also suitable when a cluster of galaxies is lensing several background objects (cluster-scale strong lenses). The similar formalism between these two SGL regimes (e.g., the description of deflectors mass profiles at different redshifts) means that the template file system can be directly used to store individual components of a given cluster lens model. Although new mass profiles might need to be implemented in the Python API, the standard presented here is general enough to encompass a wide range of complexity in lensing configurations, from individual galaxies to galaxy clusters.

The concise and lightweight storage provided by COOLEST is also particularly appropriate for handling the remarkable increase in the number of known gravitational lenses. Upcoming large scale surveys will discover many thousands of such systems, which will rapidly trigger many new lens modeling analyses. Large databases are being built to record all known and future gravitational lenses (e.g., [SLED](https://sled.astro.unige.ch/)). The standard we propose, powered by its lightweight storage system, is suitable for storing existing lens models (with proper publication references, if any) directly within the database, alongside the lens information. Moreover, we anticipate that the analysis and plotting API we provide will be useful to generate on-the-fly products that researchers can easily retrieve online from the database servers.

# Content of the standard

COOLEST is composed of three distinct building blocks:

- __Conventions__: a set of fixed conventions, such as the coordinate systems, units and profile definitions, which are implicitly assumed when manipulating lens models stored in the template file;
- __Template file system__: a Python interface to create, store and manipulate COOLEST template and external files;
- __Analysis & plotting API__: a Python interface to compute key lensing quantities and generate different plots.

The template file stores most of the necessary data, including observational and instrumental properties, and particular model choices that describe the gravitational lens. It stores individual model parameter values (as point estimates), as well as a description of their prior distribution (if any) and first-order statistics of their posterior distributions (e.g., from MCMC chains). An example of such a [template file](https://github.com/aymgal/COOLEST/blob/main/examples), and how to generate and fill one programmatically, is provided on our GitHub repository.

Depending on the application, observational data, model images and PSF kernels can be linked to the template file via dedicated fields, and placed within the same directory. Additionally, the `'meta'` field of the template is also used to refer to inference data such as MCMC chains, stored in separate files.

All details regarding the conventions and Python interfaces are given on the COOLEST [documentation website](https://coolest.readthedocs.io). We warmly encourage the lensing community to adhere to the proposed standard, provide feedback and contribute to its development.

# Related software

Lens modeling and simulation codes that already have an interface with COOLEST:

- `Herculens` [@herculens2022]
- `VKL` [@vkl2022]
- `MOLET` [@molet2022]
- `Lenstronomy` [@lenstronomy2021]

Examples of other lens modeling codes:

- `giga-lens` [@gigalens2022]
- `PyAutoLens` [@pyautolens2021]
- `GLaD` [@glad2020]
- `GLASS ` [@glass2020]
- `GLEE` [@glee2010]
- `glafic` [@glafic201O]
- `lenstool ` [@lenstool2007]

# Acknowledgements

The authors thank Frédéric Courbin and Austin Peel for useful discussion. This work is supported by the Swiss National Science Foundation (SNSF). This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation program (grant agreement No 787886).

# References
