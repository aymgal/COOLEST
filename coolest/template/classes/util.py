__author__ = 'aymgal'

# Utility functions to use throughout the API

def galaxy_profile_to_id(model_type, profile_name, profile_idx, entity_idx):
    return f'{entity_idx}-galaxy-{model_type}-{profile_idx}-{profile_name}'

def mass_field_profile_to_id(profile_name, profile_idx, entity_idx):
    return f'{entity_idx}-massfield-mass-{profile_idx}-{profile_name}'

def parameter_to_id(param_name, parent_profile_id):
    return f'{parent_profile_id}-{param_name}'

def unpack_profile_id(id_str):
    entity_idx, _, model_type, profile_idx, profile_name = id_str.split('-')
    return int(entity_idx), str(model_type), int(profile_idx), str(profile_name)

def unpack_parameter_id(id_str):
    entity_idx, _, model_type, profile_idx, profile_name, param_name = id_str.split('-')
    return int(entity_idx), str(model_type), int(profile_idx), str(profile_name), str(param_name)
