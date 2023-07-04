# The different template modes

The key `"mode"` indicates the purpose of the COOLEST template: 1) storing a previously optimized lens model (default), 2) using as input to generate new mock imaging data, or 3) generate a template filled with additional information and fields. The mode does not change the structure of the file, but only filters out which keys are present in it.

The three supported modes are as follows:

- `"MAP"` (default): the template stores a lens model that was optimized on some data, and typically contain maximum _a posteriori_ (MAP) parameter values, posterior statistics and optionally prior distribution and parameters that have fixed during modeling. The `"instrument"` and `"observation"` keys should be consistent with the data that was modeled.

- `"MOCK"`: the template stores all necessary information regarding the simulation of a mock lens. The template can then be used an input file to a simulator that shares an interface with COOLEST. The `"instrument"` and `"observation"` keys define the observational properties of the mock (field of view, noise, etc.).

- `"DOC"`: the template contains a lot of additional fields that give. This mode does not have explicit purpose other than given more details about the different fields of a COOLEST template (depending on the amount of information, it may become rather cluttered). Typically, the additional fields not present in the other two modes are parameters units, definition intervals, LaTeX strings, etc.

``` {admonition} Note
Only the modes `"MAP"` and `"MOCK"` find obvious applications in a strong lensing analysis. `"DOC"` is mostly meant for development purposes.
```

This example notebook shows how to generate templates files. The resulting files can be retrieved in the different modes: [`"MAP"`](../notebooks/template_dir/coolest_template.json), [`"MOCK"`](../notebooks/template_dir/coolest_template_mock.json), [`"DOC"`](../notebooks/template_dir/coolest_template_doc.json).
