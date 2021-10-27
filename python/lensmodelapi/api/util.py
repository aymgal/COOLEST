__author__ = 'aymgal'

# Utility functions to use throughout the API

def profile_to_id(model_type, profile_name, profile_idx, galaxy_idx):
    return f'galaxy-{galaxy_idx}_{model_type}-model_{profile_name}-{profile_idx}'

def id_to_profile(id_str):
    galaxy_str, model_str, profile_str = id_str.split('_')
    galaxy_idx = int(galaxy_str.split('-')[1])
    profile_name, profile_idx = profile_str.split('-')
    profile_idx = int(profile_idx)
    model_type = model_str.split('-')[0]
    return model_type, profile_name, profile_idx, galaxy_idx

def regul_to_id(regul_name, regul_idx):
    return f'regularization-model_{regul_name}-{regul_idx}'

def id_to_regul(id_str):
    regul_str, model_str = id_str.split('_')
    regul_name, regul_idx = model_str.split('-')
    regul_idx = int(regul_idx)
    return regul_name, regul_idx
    