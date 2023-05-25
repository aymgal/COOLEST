# What is a "lensing entity" in COOLEST?

## How to describe a lensing system

In the goal of describing lens models as intuitively as possible, the different components in the COOLEST template closely follow the physical objects that they describes. In particular, the template explcitely describes indivual galaxies (or quasars), as opposed to the more abstract "lensing planes". While the latter is usually a more practical description of the model within modeling codes, the former is more intuitive and closer to the end goal, which is understanding the mass and light distribution of galaxies. 

However, not all components of a lens model straightforwardly refer to a physical object. The most common example is the "external shear", which is a profile accounting for the mass of several (unknown) physical objects surrounding the main lens. As it would be nearly impossible to decompose the external shear into its individual true sub-components, one needs to store as is.

## The COOLEST choice

In COOLEST, we introduce the concept of **lensing entity**, which can broadly be split into two categories: physical objects such as galaxies, and other components that are more abstract approximations of physical objects. In a COOLEST template, the list of lensing entitities is stored under the `'lensing_entities'` key. Within the Python API, each lensing entity is an instance of the [`LensingEntity`](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/lensing_entity/index.html#coolest.template.classes.lensing_entity.LensingEntity) object.

Currently, a lensing entity can be any of the following types:

- [**`Galaxy`**](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/galaxy/index.html#coolest.template.classes.galaxy.Galaxy): describes a galaxy with a mass model and light model, each of this model being composed of a list of profiles. If a galaxy is only lensed, it does not need a mass model; conversely if the light distribution of a galaxy is ignored, it can be empty.

- [**`MassField`**](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/mass_field/index.html#coolest.template.classes.mass_field.MassField): describes a generic field of massive objects, for instance an external shear field.

In the template, the `'type'` key should thus be one of the above types.
