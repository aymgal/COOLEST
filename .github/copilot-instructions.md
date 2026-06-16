# CoPilot / AI agent instructions for COOLEST

Short, action-oriented guidance to be immediately productive in this repository.

1) Big picture
- COOLEST defines a JSON-based template standard (conventions in `docs/conventions.md`) and provides two main Python APIs:
  - `coolest.template` — helpers to create, load and validate template JSONs and linked files (FITS, PSFs).
  - `coolest.api` — analysis, composable model classes and plotting utilities used to compute lensing quantities and render model images.

2) Key modules & classes to inspect first
- `coolest.api.analysis.Analysis` — high-level analysis helpers (Einstein radius, kappa profiles, effective radius).
- `coolest.api.composable_models` — core composition logic:
  - `BaseComposableModel`, `ComposableLightModel`, `ComposableMassModel`, `ComposableLensModel`.
  - Important behaviors: evaluation modes (`mode='point'|'posterior'`), support for pixelated/irregular grids, PSF convolution and downsampling.
- `coolest/api/profiles/*` — concrete `light` and `mass` profile implementations used by the composable models.
- `coolest/template` and `coolest/template/classes` — canonical JSON fields and classes used to populate the API objects.

3) Project-specific conventions and patterns
- Template metadata: keys in the COOLEST JSON are relied upon (example: metadata key `chain_file_name` is used to load posterior samples). See `BaseComposableModel._chain_key`.
- CSV posterior expectations: when `load_posterior_samples=True` the code reads a CSV column for each parameter by `param.id` and expects a `probability_weights` column for weights.
- Grid profiles: `PixelatedRegularGrid` and `IrregularGrid` load pixel arrays or x/y/z arrays from FITS via the template `parameters` objects — the repository requires providing the template directory (`coolest_directory`) when using grids.
- Coordinates: many APIs call `util.get_coordinates(coolest)` and use a `Coordinates.create_new_coordinates(pixel_scale_factor=...)` helper — adjust supersampling via that call when testing or rendering.
- Convolution & supersampling: `ComposableLensModel.model_image()` will adapt `supersampling` to the PSF pixel size and either convolve-then-downsample or downsample-then-convolve according to `super_convolution`.

4) Typical developer workflows (commands)
- Install dev version with dependencies:
  - `python -m venv .venv && .venv\Scripts\activate` (Windows)
  - `pip install -e .` or `pip install -e .[opt]` to include optional deps.
- Run unit tests: `pytest test` (project README) or run specific notebooks in `docs/notebooks` for examples.
- Quick checks: `python -c "import coolest; print(coolest.__version__)"` and small interactive checks using `Analysis` / `ComposableLensModel`.

5) Important files and entry points to reference in PRs
- `README.md` (root) — installation and high-level overview.
- `docs/conventions.md` — canonical definitions for coordinates, units and profile naming.
- `coolest/template` — how template objects are structured; required when handling file-backed grids/PSFs.
- `coolest/api/composable_models.py` — composition and evaluation logic; many callers rely on the exact CSV and FITS-loading behavior here.
- `setup.py`, `pyproject.toml`, `requirements*.txt` — packaging & dependency lists.

6) External dependencies to be aware of
- numpy, scipy, pandas, astropy — heavy numeric and I/O use.
- matplotlib used in example notebooks and plotting utilities (optional for core API tests).

7) Debugging tips and pitfalls
- Logging: modules set default logging levels (api sets WARNING/INFO). Override via standard `logging` configuration to see more detail.
- Missing directory for FITS-backed profiles: many grid/PSF profile methods raise when `coolest_directory` is not provided — pass it during tests.
- Posterior samples: CSV columns are read by `param.id` — mismatched ids or missing `probability_weights` will raise or produce empty posterior arrays.
- Numerical issues: code often uses NaN sanitization (e.g., `np.nan_to_num`) before convolution — watch for unexpected NaNs when constructing templates.

8) Examples (quick copy-paste)
- Instantiate analysis and compute Einstein radius:
  - `from coolest.api.analysis import Analysis`
  - `a = Analysis(coolest_obj, ".")`
  - `a.effective_einstein_radius()`
- Render a model image:
  - `from coolest.api.composable_models import ComposableLensModel`
  - `lm = ComposableLensModel(coolest_obj, ".")`
  - `img, coords = lm.model_image(supersampling=5)`

9) What NOT to assume
- DO NOT assume posterior CSVs exist for every template — the code checks `meta` keys.
- DO NOT assume pixelated profiles will work without providing a directory containing FITS files.

If anything here is unclear or you want more examples (unit-test snippets or common PR checklists), tell me which area to expand. 
