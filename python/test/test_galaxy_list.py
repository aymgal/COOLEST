__author__ = 'aymgal'

from lensmodelapi.api.galaxy_list import GalaxyList


model_type_in = 'light'
profile_name_in = 'SersicElliptical'
profile_idx_in = 0
galaxy_idx_in = 1
test_id = GalaxyList.profile_to_id(model_type_in, profile_name_in, profile_idx_in, galaxy_idx_in)
# print(test_id)

model_type_out, profile_name_out, profile_idx_out, galaxy_idx_out \
    = GalaxyList.id_to_profile(test_id)

assert model_type_in == model_type_out
assert profile_name_in == profile_name_out
assert galaxy_idx_in == galaxy_idx_out
assert profile_idx_in == profile_idx_out
