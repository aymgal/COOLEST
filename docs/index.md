# Welcome to the COOLEST documentation!

COOLEST stands for **COde-independent Organized LEns STandard** and its goal is to accelerate strong gravitational lensing research by provided a unifying standard to express lens models.

After a lens modeling analysis is published and available as a manuscript, it is often challenging to **(1) reproduce the results** with the same or another similar modeling software, or **(2) start a new analysis** directly based on published results, **(3) reliably and quantitatively compare results** from different analyses. Moreover, there is currently no practical way to share and store lens models within the lensing community.

The **COde-independent Organized LEns STandard (COOLEST)** proposes a solution to the above problems. COOLEST is a standard for **describing, storing and sharing lens models** more easily, independently of the specific modeling techniques and software packages. The main element of COOLEST is a unique JSON hierarchical template file, that stores in a human-readable way the necessary lens model data. Another key element is a suit of visualization tools that automatically produces a series of images, plots and other analysis products from a COOLEST file.

Currently, this repository hosts a Python API to *generate*, *manipulate* and *update* COOLEST files. The API structure exactly mirrors the hierarchy of the template file. Visualization and analysis classes will soon be added.

Ultimately, the goal is that modeling software packages each have an interface (a simple function) that converts code-specific model choices and parameter values to COOLEST conventions. This way, all lens modeling results---best-fit parameter values, posterior distributions---can be saved effortlessly to this standard, ready to be shared and used for further analyses.

```{toctree}
---
hidden:
caption: API Reference
maxdepth: 3
---
The COOLEST object <autoapi/coolest/template/standard/index>
Light profiles <autoapi/coolest/template/classes/profiles/light/index>
Mass profiles <autoapi/coolest/template/classes/profiles/mass/index>
Analysis & Plotting API <autoapi/coolest/api/index>
Template system <autoapi/coolest/template/index>
```