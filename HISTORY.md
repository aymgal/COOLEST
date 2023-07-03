# CHANGELOG

## 04/10/22

- The `ExternalShear` object has been replaced ba a more general `MassField` object. This is for supporting higher-order lensing fields such as flexion in the future. The two supported types of `LensingEntity` are thus `Galaxy` and `MassField`.

- The type of lensing entity now reflects their class name. For instance, before it was `'galaxy'`, now it is `'Galaxy'`.

- The single parameter of the `GaussianPSF` has changed from the standard deviation `std_dev` to the more widely used full width at half maximum `fwhm`.


## 14/10/22

### Major changes:

- the path to submodules changed: `coolest.template.api` is now `coolest.template.classes`. This is because the API will now be formally containing analysis tools (in the future coolest.api submodule)
- a single PixelatedRegularGrid class is now used for the observation image data, pixelated PSF, and pixelated light and mass profiles

### Minor changes:

- reorganized the repository structure, `coolest` is now at the root
- the example of template generation is now in the `examples` directory
- a 'DOC' mode has been added to the root COOLEST class (for usage with the documentation website, see separate repository)


## 02/06/22

### Major changes

These affect the template structure:

- hierachy levels 'lens_sample', 'lens_object' and 'lens_model' jave been removed; 'lensing_entities' is the relevant field now for model choices.
- the 'origin' is at the root level

### Standard changes:

- the PSF can now be either a GaussianPSF, or a PixelatedPSF
- the noise can now be one of the following choices: UniformGaussianNoise, NoiseMap, NoiseRealization, InstrumentalNoise, DrizzledNoise
- the FitsFile object is now more explicit, renamed PixelFitsFile and containing number of pixels and pixel size

### Minor changes:

- renaming of classes
- COOLEST standard now supports two distinct modes: 'MAP' to store model results, and 'MOCK' for simulating an observation


##  31/05/22

### Major changes
Theese affect the template structure:

- new field: 'lensing_entity'

    - a list of either 'galaxy'-type objects or 'external_shear'-type objects
    - each have a redshift, a name, etc... but 'external_shear' items can not have light profiles
    
- 'light_model' and 'mass_model' are now themselves list of profiles: there is no sub-field 'profiles' anymore
- 'lens_object' and 'lens_sample' have been removed. It means that ONE coolest template is related ONE lens system
- 'cosmology' is now outside of 'lens_model'

### Standard changes

- new field: 'instrument'

    - with optional 'image' fits file; if not provided, the 'mode' should be 'mock' (automatic via the API)
    - with 'noise' sub-fields, optionally with a 'noise_map', option for including Poisson noise or not

- new field: 'observation'

    - with 'psf' sub-fields, as a fits file for the psf kernel and potentially different pixel size
    
### Minor changes:

- new field: 'meta'

    - for more flexbility for storing metadata, e.g. the name and version of the modeling code used to update/read the file
    - for now it contains one sub-field: the 'mode' is set 'mock' if the coolest file is used for mocking, or 'model' if used to store modeling results

- new field: 'standard'
    - defines more explicitely the standard system: 'coolest'

- many descriptive fields have been removed by default, as set in the CoolestStandard module (python class attributes were not removed though)
