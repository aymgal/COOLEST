# What is a "lensing entity" in COOLEST?

## General description of a strong lensing system

In most lensing analyses, one refers to the notion of lensing planes to group physical objects -- such as galaxies, quasars or supernovae -- that belong to the same redshifts. Although from an implementation and mathematical point of view the notion of lensing plane is more convenient, grouping the physical objects into such planes is not necessarily unique (e.g., depending on redshift measurements available). Therefore, different analyses can have different arrangements of planes which prevent a straightforward comparison between them and hinders the goal of having a unified standard.

## From lensing planes to physical objects

After a lens model has been obtained, one can go back to the description of the mass and light distributions of the underlying physical components of the lensing system (e.g., the main lens galaxy, one of its satellites, the source object, etc.). This explicit description is more intuitive for both lensing and non-lensing experts, and makes it straightforward to cross-match properties of these objects with other measurements from non-lensing analyses. This will become primordial in the near future with the large increase of complementary datasets available.

Nevertheless, not all components of a lens model refer to a well-defined physical object. The most common example is the "external shear", which accounts for the mass of several (possibly unknown) physical objects surrounding the main lens. As it is unrealistic to decompose an external shear into its underlying components, one needs to store it as is. We describe below how both physical objects and abstract massive components are stored within a COOLEST template file.

## Lensing entities in COOLEST

COOLEST is based on the concept of **lensing entity**, which is split in two categories: physical objects such as galaxies, and approximations of several underlying massive objects. A lensing entity is named, has a redshift, and can be any of the following types:

- [**`Galaxy`**](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/galaxy/index.html#coolest.template.classes.galaxy.Galaxy): describes a galaxy with a mass model and light model, each of this model being composed of a list of profiles. If a galaxy is only lensed, it does not need a mass model; conversely if the light distribution of a galaxy is ignored, it can be empty.

- [**`MassField`**](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/mass_field/index.html#coolest.template.classes.mass_field.MassField): describes a generic field of massive objects, for instance an external shear field.

Within the Python API, each lensing entity is an instance of the [`LensingEntity`](https://coolest.readthedocs.io/en/latest/autoapi/coolest/template/classes/lensing_entity/index.html#coolest.template.classes.lensing_entity.LensingEntity) object (see the API documentation for the full list of attributes, which reflects the structure of the template file).

Note that a lensing entity can still, if necessary, be composed of several physical objects; in this case, the `"name"` of the field may be used to specify it appropriately (e.g., "main lens and its satellite"). Moreover, unknown redshifts can be replaced by hypothetical values that only provides the ordering of the entities along the redshift axis.
