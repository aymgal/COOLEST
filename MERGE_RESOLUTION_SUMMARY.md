# Merge Conflict Resolution Summary

## Overview
Successfully resolved all merge conflicts in `coolest/api/composable_models.py` while integrating:
- Upstream auto-selection functionality
- HEAD's multiplane mass plane grouping by redshift
- Separated source and lens light models for selective lensing
- Beta coefficient-based multiplane lens equation evaluation

## Changes Made

### 1. **ComposableLensModel.__init__** (Lines 495-620)
**Resolved Conflict:** Integration of HEAD's multi-source model architecture with upstream's auto-selection

**Solution:**
- Preserved `auto_selection` parameter from upstream
- Apply `auto_select_entities()` when `auto_selection=True` 
- Built source models as **list of ComposableLightModel** (HEAD feature) to support multiple source planes
- Kept `source_entity_indexes` tracking for multiplane redshift sorting
- Separated `lens_light` from source models to allow selective lensing

**Key Features:**
```python
# Auto-selection automatically detects entity types
if auto_selection is True:
    (kwargs_source, kwargs_lens_mass, kwargs_lens_light) = auto_select_entities(self.coolest)

# Multiple source support for multiplane systems
self.source = [ComposableLightModel(...) for ...]  # List, not single model
self.source_entity_indexes = [...]  # Track indices for redshift sorting

# Lens light kept separate from sources
self.lens_light = ComposableLightModel(...)
```

### 2. **Mass Plane Grouping by Redshift** (Lines 550-592)
**Implementation (HEAD's feature, preserved):**
- Collects all entities with mass models
- Groups them by redshift (tolerance: 1e-8)
- Creates separate `ComposableMassModel` per plane
- Stores as:
  - `self.lens_mass_sorted`: List of mass models sorted by redshift
  - `self.mass_redshifts_sorted`: Redshifts of each plane
  - `self.mass_entity_indexes_sorted`: Entity indices per plane

```python
# Automatic grouping by redshift (if no explicit selection provided)
idx_z = sorted([(i, entity[i].redshift) for i in mass_entity_indices], key=lambda x: x[1])
# Groups entities with nearly identical redshifts (tol=1e-8)
```

### 3. **Source Redshift Sorting** (Lines 593-609)
**Implementation (HEAD's feature, preserved):**
- Sorts source models by redshift
- Stores as:
  - `self.source_sorted`: Source models in ascending redshift order
  - `self.source_redshifts_sorted`: Source redshifts
  - `self.source_entity_indexes_sorted`: Entity indices per source

### 4. **Multiplane Lens Equation with Beta** (Lines 684-757)
**Implementation (HEAD's feature, preserved + enhanced):**

In `evaluate_lensed_surface_brightness()`:
- Handles both single-plane and multiplane systems
- Computes deflections through each mass plane
- Applies beta coefficients from `multiplane_betas` list
- Resolves betas automatically from cosmology if "auto"

```python
# For each mass plane j, compute deflection from all prior planes i
for i in range(j):
    beta = self.coolest.lensing_entities.resolve_beta(from_name, to_name, cosmology)
    ax, ay = self.lens_mass_sorted[i].evaluate_deflection(...)
    x_def_temp -= beta * ax
    y_def_temp -= beta * ay

# For each source, apply accumulated deflections from all prior planes
for si, src in enumerate(self.source_sorted):
    z_src = self.source_redshifts_sorted[si]
    prior_planes = [k for k, z in enumerate(self.mass_redshifts_sorted) if z < z_src]
    # Apply deflections from each prior plane scaled by its beta to the source
```

### 5. **Ray Shooting** (Lines 759-768)
**Resolved Conflict:** Integration of multiplane-aware ray shooting

**Solution:**
```python
if hasattr(self, 'lens_mass_sorted'):
    # Multiplane system
    if len(self.lens_mass_sorted) > 1:
        raise NotImplementedError(...)  # Use evaluate_lensed_surface_brightness
    elif len(self.lens_mass_sorted) == 1:
        return self.lens_mass_sorted[0].ray_shooting(x, y)
    else:
        return x, y  # No mass models
else:
    # Single mass model (legacy)
    return self.lens_mass.ray_shooting(x, y)
```

## Architectural Decisions

### 1. **Separate Source and Lens Light Models**
- **Rationale:** Allows users to selectively apply lensing to some light models and not others
- **Implementation:** `self.source` list keeps sources separate from `self.lens_light`
- **Benefit:** Users can render unlensed lens light while lensing source light

### 2. **Auto-Detection with Explicit Override**
- **Default behavior:** If `auto_selection=True` and entity/profile indices not specified, system automatically detects:
  - Lensed entities → sources
  - Unlensed entities → lens mass/light
  - Entities that are both → included in appropriate models
- **Override behavior:** Users can provide explicit `kwargs_selection_*` to bypass auto-detection

### 3. **Multiplane Reduces to Single-Plane**
- **Design:** If only one mass plane exists, system works as single-plane lens
- **Benefit:** Transparent handling of simple lensing problems within multiplane framework

### 4. **Beta Resolution Strategy**
- **"auto" betas:** Computed from cosmology and redshifts using `resolve_beta()`
- **Fixed betas:** Use provided float or Parameter values
- **Fallback:** Initialize empty `MultiPlaneBetaList()` if not in template

## Code Flow: Single vs. Multiplane

### Single-Plane System (Traditional)
```
ComposableLensModel(coolest_obj, auto_selection=True)
  ├─ auto_select_entities() → identifies one source, one lens
  ├─ self.lens_mass = [ComposableMassModel(...)]  # One-element list
  ├─ self.source = [ComposableLightModel(...)]    # One-element list
  ├─ self.lens_light = ComposableLightModel(...)
  └─ model_image() → evaluate_lensed_surface_brightness()
       └─ No multiplane logic triggered (len(lens_mass_sorted)==1)
```

### Multiplane System (New)
```
ComposableLensModel(coolest_obj, auto_selection=True)
  ├─ auto_select_entities() → identifies 2+ lenses at different z, source at highest z
  ├─ Groups mass models by z → self.lens_mass_sorted = [plane1, plane2, ...]
  ├─ Sorts sources by z → self.source_sorted = [src1, src2, ...]
  ├─ model_image() → evaluate_lensed_surface_brightness()
  │   ├─ For each mass plane j: compute x_def[j] from deflections with betas
  │   └─ For each source: apply deflections from all prior planes scaled by betas
  └─ Output: Multiplane-lensed image
```

## Syntax Verification
✓ No syntax errors found  
✓ All merge conflict markers removed  
✓ File compiles successfully

## Testing Recommendations

1. **Auto-selection:**
   ```python
   coolest_obj = load_coolest(...)
   lens_model = ComposableLensModel(coolest_obj, auto_selection=True)
   ```

2. **Multiplane rendering:**
   ```python
   image, coords = lens_model.model_image(supersampling=5, convolved=True)
   ```

3. **Manual selection:**
   ```python
   lens_model = ComposableLensModel(
       coolest_obj, 
       auto_selection=False,
       kwargs_selection_source={'entity_selection': [2]},
       kwargs_selection_lens_mass={'entity_selection': [[0], [1]]},  # Two planes
       kwargs_selection_lens_light={'entity_selection': [0, 1]}
   )
   ```

## Backward Compatibility
- ✓ Single-plane systems work transparently
- ✓ `lens_mass` is now a list; code accessing single plane should use `lens_mass[0]` or `lens_mass_sorted[0]`
- ✓ Auto-selection enabled by default (can disable with `auto_selection=False`)
