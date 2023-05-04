__author__ = 'aymgal'

# Utility functions to use throughout the API

def galaxy_profile_to_id(model_type, profile_name, profile_idx, galaxy_idx):
    return f'galaxy_{galaxy_idx}-{model_type}_model-{profile_name}_{profile_idx}'

def mass_field_profile_to_id(profile_name, profile_idx, field_idx):
    return f'massfield_model_{field_idx}-{profile_name}_{profile_idx}'

def galaxy_id_to_profile(id_str):
    galaxy_str, model_str, profile_str = id_str.split('-')
    galaxy_idx = int(galaxy_str.split('_')[1])
    profile_name, profile_idx = profile_str.split('_')
    profile_idx = int(profile_idx)
    model_type = model_str.split('_')[0]
    return model_type, profile_name, profile_idx, galaxy_idx

def regul_to_id(regul_name, regul_idx):
    return f'regularization_model-{regul_name}_{regul_idx}'

def id_to_regul(id_str):
    regul_str, model_str = id_str.split('-')
    regul_name, regul_idx = model_str.split('_')
    regul_idx = int(regul_idx)
    return regul_name, regul_idx
    
def class_name_to_type(name):
    import re
    return re.sub('(?<!^)(?=[A-Z])', '_', name).lower()
